# src/storage/db.py
import json
import sqlite3
import asyncio
import time
import threading
import random
from pathlib import Path
from typing import Set, List, Optional, Tuple
from datetime import datetime
from src.network.client import CheckResult, CheckStatus
from src.utils.paths import resolve_output_path

_FILE_LOCKS = {}
_GLOBAL_LOCK = threading.Lock()

def _get_file_lock(path: Path) -> threading.Lock:
    p_str = str(path.resolve())
    with _GLOBAL_LOCK:
        if p_str not in _FILE_LOCKS:
            _FILE_LOCKS[p_str] = threading.Lock()
        return _FILE_LOCKS[p_str]

def safe_append_text(file_path: Path, content: str, retries: int = 20) -> bool:
    """다중 스레드/프로세스 환경에서 동일 파일 append 시 충돌([WinError 32]) 방지 지수 백오프 재시도"""
    lock = _get_file_lock(file_path)
    with lock:
        for attempt in range(retries):
            try:
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(content)
                    f.flush()
                return True
            except (PermissionError, OSError):
                time.sleep(0.02 * (attempt + 1) + random.uniform(0.005, 0.02))
        return False

def safe_append_csv(file_path: Path, header: str, row: str, retries: int = 20) -> bool:
    """다중 스레드/프로세스 CSV 파일 안전 동시 추가"""
    lock = _get_file_lock(file_path)
    with lock:
        for attempt in range(retries):
            try:
                exists_and_nonempty = file_path.exists() and file_path.stat().st_size > 0
                with open(file_path, "a", encoding="utf-8", newline="") as f:
                    if not exists_and_nonempty:
                        f.write(header)
                    f.write(row)
                    f.flush()
                return True
            except (PermissionError, OSError):
                time.sleep(0.02 * (attempt + 1) + random.uniform(0.005, 0.02))
        return False

class StorageManager:
    """
    고성능 비동기 SQLite WAL 및 TXT/CSV/JSON 실시간 멀티포맷 자동 저장소
    - SQLite WAL 모드 + 30초 락 타임아웃으로 다중 프로세스 충돌 0% 보장
    - 다중 인스턴스 간 1.5초 주기 실시간 델타 동기화 (타 창 검사 닉네임 자동 스킵 + 타 창 발견 닉네임 자동 반영)
    - 사용 가능 닉네임 발견 즉시 available_usernames.txt, csv, json에 안전 재시도 flush 자동 저장
    """
    def __init__(
        self,
        db_path: str = "data/d4uc_results.db",
        save_legacy: bool = True,
        available_file: str = "available.txt",
        taken_file: str = "taken.txt"
    ):
        self.db_path = resolve_output_path(db_path)
        self.save_legacy = save_legacy
        self.available_file = resolve_output_path(available_file)
        self.available_detailed_file = resolve_output_path("available_usernames.txt")
        self.available_csv_file = resolve_output_path("available_usernames.csv")
        self.available_json_file = resolve_output_path("available_usernames.json")
        self.results_dir = resolve_output_path("results")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.taken_file = resolve_output_path(taken_file)
        self.history_file = resolve_output_path("checked_history.txt")

        self.saved_available_count: int = 0
        self.tried_usernames: Set[str] = set()
        self._write_queue: asyncio.Queue[CheckResult] = asyncio.Queue()
        self._is_running = True
        self._db_task: Optional[asyncio.Task] = None
        self._sync_task: Optional[asyncio.Task] = None

        self._init_db()
        self.load_history()
        self._last_synced_rowid: int = self.get_max_rowid()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checked_usernames (
                username TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                pattern_type TEXT,
                length INTEGER,
                latency_ms REAL,
                proxy_used TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_checked_status ON checked_usernames(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_checked_at ON checked_usernames(checked_at);")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                key TEXT PRIMARY KEY,
                value INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def get_max_rowid(self) -> int:
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            cursor.execute("SELECT IFNULL(MAX(rowid), 0) FROM checked_usernames")
            max_id = cursor.fetchone()[0]
            conn.close()
            return int(max_id or 0)
        except Exception:
            return 0

    def fetch_new_checked_since(self, last_rowid: int) -> Tuple[List[str], int]:
        """다른 프로세스가 새로 검사한 닉네임 목록을 SQLite에서 델타 조회 (다중 창 중복 스킵용)"""
        new_names = []
        new_max_id = last_rowid
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT rowid, username FROM checked_usernames WHERE rowid > ? ORDER BY rowid ASC LIMIT 1000",
                (last_rowid,)
            )
            rows = cursor.fetchall()
            for r in rows:
                rid, uname = r[0], r[1]
                if uname:
                    new_names.append(uname.strip().lower())
                if rid > new_max_id:
                    new_max_id = rid
            conn.close()
        except Exception:
            pass
        return new_names, new_max_id

    def fetch_new_available_since(self, last_rowid: int) -> Tuple[List[dict], int]:
        """다른 프로세스가 새로 발견한 사용 가능 닉네임 목록을 SQLite에서 델타 조회 (다중 창 LIVE 테이블 동기화용)"""
        new_records = []
        new_max_id = last_rowid
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rowid, checked_at, username, pattern_type, latency_ms, proxy_used
                FROM checked_usernames
                WHERE status = 'available' AND rowid > ?
                ORDER BY rowid ASC LIMIT 500
            """, (last_rowid,))
            rows = cursor.fetchall()
            for r in rows:
                rid = r[0]
                new_records.append({
                    "rowid": rid,
                    "time": str(r[1]),
                    "username": str(r[2]),
                    "pattern": str(r[3] or "unknown"),
                    "latency": f"{float(r[4] or 0):.1f}ms",
                    "server": str(r[5] or "Direct"),
                    "length": len(str(r[2]))
                })
                if rid > new_max_id:
                    new_max_id = rid
            conn.close()
        except Exception:
            pass
        return new_records, new_max_id

    def load_history(self):
        # 1. Load from SQLite DB
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM checked_usernames")
            for row in cursor.fetchall():
                if row[0]:
                    self.tried_usernames.add(row[0].strip().lower())
            conn.close()
        except Exception:
            pass

        # 2. Load from all text files (available, taken, history)
        scan_files = [
            self.available_file,
            self.available_detailed_file,
            self.taken_file,
            self.history_file
        ]
        for fpath in scan_files:
            if fpath.exists():
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        for line in f:
                            s = line.strip()
                            if not s:
                                continue
                            if "] " in s:
                                name_part = s.split("] ")[1].split()[0]
                                self.tried_usernames.add(name_part.strip().lower())
                            elif "|" in s:
                                name_part = s.split("|")[0].strip()
                                self.tried_usernames.add(name_part.lower())
                            else:
                                self.tried_usernames.add(s.lower())
                except Exception:
                    pass

        # 3. Calculate initial saved count
        if self.available_file.exists():
            try:
                with open(self.available_file, "r", encoding="utf-8") as f:
                    self.saved_available_count = len([line for line in f if line.strip()])
            except Exception:
                pass

    def get_history_count(self) -> int:
        return len(self.tried_usernames)

    def get_saved_count(self) -> int:
        return self.saved_available_count

    def get_discovered_available_records(self) -> List[dict]:
        """과거 발견된 사용 가능 닉네임 전체 내역 로드"""
        records = []
        # 1. Load from available_usernames.csv
        if self.available_csv_file.exists() and self.available_csv_file.stat().st_size > 0:
            try:
                with open(self.available_csv_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if len(lines) > 1:
                        for line in lines[1:]:
                            parts = [p.strip().strip('"') for p in line.strip().split(",")]
                            if len(parts) >= 6:
                                records.append({
                                    "time": parts[0],
                                    "username": parts[1],
                                    "pattern": parts[3],
                                    "latency": f"{float(parts[4]):.1f}ms" if parts[4] else "0.0ms",
                                    "server": parts[5]
                                })
            except Exception:
                pass

        # 2. Fallback to SQLite DB
        if not records and Path(self.db_path).exists():
            try:
                conn = sqlite3.connect(self.db_path, timeout=30.0)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT checked_at, username, pattern_type, latency_ms, proxy_used
                    FROM checked_usernames
                    WHERE status = 'available'
                    ORDER BY checked_at DESC
                """)
                for row in cursor.fetchall():
                    records.append({
                        "time": str(row[0]),
                        "username": str(row[1]),
                        "pattern": str(row[2] or "unknown"),
                        "latency": f"{float(row[3] or 0):.1f}ms",
                        "server": str(row[4] or "Direct")
                    })
                conn.close()
            except Exception:
                pass

        # 3. Fallback to available_usernames.txt
        if not records and self.available_detailed_file.exists():
            try:
                with open(self.available_detailed_file, "r", encoding="utf-8") as f:
                    for line in f:
                        s = line.strip()
                        if not s or not s.startswith("["):
                            continue
                        try:
                            ts_part = s[1:20]
                            rest = s[22:]
                            after_len = rest.split("] ")[1] if "] " in rest else rest
                            segments = [p.strip() for p in after_len.split("|")]
                            uname = segments[0]
                            patt = segments[1] if len(segments) > 1 else "restored"
                            lat = segments[2] if len(segments) > 2 else "0.0ms"
                            srv = segments[3] if len(segments) > 3 else "Direct"
                            records.append({
                                "time": ts_part,
                                "username": uname,
                                "pattern": patt,
                                "latency": lat,
                                "server": srv
                            })
                        except Exception:
                            pass
            except Exception:
                pass

        # 4. Fallback to available.txt
        if not records and self.available_file.exists():
            try:
                with open(self.available_file, "r", encoding="utf-8") as f:
                    for line in f:
                        s = line.strip()
                        if not s:
                            continue
                        if s.startswith("[") and "] " in s:
                            ts_part = s.split("] ")[0].replace("[", "").strip()
                            uname = s.split("] ")[1].strip()
                        else:
                            ts_part = "Saved"
                            uname = s.strip()
                        records.append({
                            "time": ts_part,
                            "username": uname,
                            "pattern": "restored",
                            "latency": "0.0ms",
                            "server": "Saved"
                        })
            except Exception:
                pass

        return records

    @staticmethod
    def parse_imported_usernames(filepath: str | Path) -> List[str]:
        """외부 파일(.txt, .csv, .json) 파싱"""
        path = Path(filepath)
        if not path.exists():
            return []

        ext = path.suffix.lower()
        usernames = []

        if ext == ".json":
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, str):
                                usernames.append(item.strip().lower())
                            elif isinstance(item, dict) and "username" in item:
                                usernames.append(str(item["username"]).strip().lower())
                    elif isinstance(data, dict):
                        for k, v in data.items():
                            if isinstance(v, list):
                                for u in v:
                                    if isinstance(u, str):
                                        usernames.append(u.strip().lower())
            except Exception:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        for line in f:
                            s = line.strip()
                            if s:
                                item = json.loads(s)
                                if isinstance(item, dict) and "username" in item:
                                    usernames.append(str(item["username"]).strip().lower())
                except Exception:
                    pass

        elif ext == ".csv":
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if lines:
                        first_line = lines[0].lower()
                        col_idx = 0
                        if "username" in first_line:
                            headers = [h.strip().strip('"') for h in first_line.split(",")]
                            for idx, h in enumerate(headers):
                                if "username" in h:
                                    col_idx = idx
                                    break
                            data_lines = lines[1:]
                        else:
                            data_lines = lines

                        for line in data_lines:
                            parts = [p.strip().strip('"') for p in line.strip().split(",")]
                            if len(parts) > col_idx and parts[col_idx]:
                                usernames.append(parts[col_idx].lower())
            except Exception:
                pass

        else: # .txt
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        s = line.strip()
                        if not s:
                            continue
                        if "] " in s:
                            name_part = s.split("] ")[1].split()[0]
                            usernames.append(name_part.strip().lower())
                        elif "|" in s:
                            name_part = s.split("|")[0].strip()
                            usernames.append(name_part.lower())
                        else:
                            usernames.append(s.split()[0].lower())
            except Exception:
                pass

        # Deduplicate preserving order
        seen = set()
        deduped = []
        for u in usernames:
            if u not in seen:
                seen.add(u)
                deduped.append(u)
        return deduped

    load_usernames_from_file = parse_imported_usernames

    def update_recheck_status(self, username: str, new_status: CheckStatus, latency_ms: float = 0.0, proxy_used: str = ""):
        """재확인(Re-check) 결과에 따라 DB 및 파일 상태를 갱신"""
        u = username.strip().lower()
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE checked_usernames
                SET status = ?, latency_ms = ?, proxy_used = ?, checked_at = datetime('now')
                WHERE LOWER(username) = ?
            """, (new_status.value, latency_ms, proxy_used, u))
            conn.commit()
            conn.close()
        except Exception:
            pass

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if new_status == CheckStatus.TAKEN:
            safe_append_text(self.taken_file, f"[{ts}] {u} (Recheck: TAKEN)\n")

    def is_tried(self, username: str) -> bool:
        return username.lower() in self.tried_usernames

    def mark_tried(self, username: str):
        self.tried_usernames.add(username.lower())

    def unmark_tried(self, username: str):
        """네트워크/프록시 실패 시 해당 후보를 캐시에서 해제하여 즉시 재검사 가능하도록 복구"""
        self.tried_usernames.discard(username.lower())

    async def enqueue_result(self, result: CheckResult):
        self.mark_tried(result.username)
        await self._write_queue.put(result)

    async def start_worker(self):
        self._db_task = asyncio.create_task(self._process_queue())
        self._sync_task = asyncio.create_task(self._sync_external_loop())

    async def _sync_external_loop(self):
        """다중 인스턴스 환경에서 타 창이 검사한 닉네임을 1.5초마다 인메모리 tried_usernames에 실시간 반영"""
        while self._is_running:
            try:
                await asyncio.sleep(1.5)
                new_names, next_rowid = self.fetch_new_checked_since(self._last_synced_rowid)
                if new_names:
                    self.tried_usernames.update(new_names)
                    self._last_synced_rowid = next_rowid
            except asyncio.CancelledError:
                break
            except Exception:
                pass

    async def _process_queue(self):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()

        while self._is_running or not self._write_queue.empty():
            try:
                result: CheckResult = await asyncio.wait_for(self._write_queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue

            try:
                # 1. Insert into SQLite
                cursor.execute("""
                    INSERT OR REPLACE INTO checked_usernames 
                    (username, status, pattern_type, length, latency_ms, proxy_used, checked_at)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    result.username,
                    result.status.value,
                    result.pattern_type,
                    len(result.username),
                    result.latency_ms,
                    result.proxy_used
                ))
                conn.commit()

                # 2. Real-Time Multi-Format Auto-Save with safe cross-process retries (.txt, .csv, .json)
                if self.save_legacy:
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if result.status == CheckStatus.AVAILABLE:
                        self.saved_available_count += 1
                        detailed_entry = f"[{ts}] [{len(result.username)}자] {result.username} | {result.pattern_type} | {result.latency_ms:.1f}ms | {result.proxy_used or 'Direct'}\n"
                        csv_header = "Timestamp,Username,Length,Pattern,Latency_ms,Proxy_Server\n"
                        csv_row = f'"{ts}","{result.username}",{len(result.username)},"{result.pattern_type}",{result.latency_ms:.1f},"{result.proxy_used or "Direct"}"\n'
                        json_record = {
                            "timestamp": ts,
                            "username": result.username,
                            "length": len(result.username),
                            "pattern": result.pattern_type,
                            "latency_ms": round(result.latency_ms, 1),
                            "proxy": result.proxy_used or "Direct"
                        }

                        # 2.1 Append to available.txt
                        safe_append_text(self.available_file, f"[{ts}] {result.username}\n")

                        # 2.2 Append to available_usernames.txt
                        safe_append_text(self.available_detailed_file, detailed_entry)

                        # 2.3 Append to available_usernames.csv
                        safe_append_csv(self.available_csv_file, csv_header, csv_row)

                        # 2.4 Append to available_usernames.json (JSON Lines)
                        safe_append_text(self.available_json_file, json.dumps(json_record, ensure_ascii=False) + "\n")

                        # 2.5 Mirrored backup in results/ folder
                        res_txt = self.results_dir / "available_usernames.txt"
                        res_csv = self.results_dir / "available_usernames.csv"
                        res_json = self.results_dir / "available_usernames.json"
                        safe_append_text(res_txt, detailed_entry)
                        safe_append_csv(res_csv, csv_header, csv_row)
                        safe_append_text(res_json, json.dumps(json_record, ensure_ascii=False) + "\n")

                    elif result.status == CheckStatus.TAKEN:
                        safe_append_text(self.taken_file, f"[{ts}] {result.username}\n")

                    # Save all checked names to history file
                    safe_append_text(self.history_file, f"[{ts}] {result.username} ({result.status.value})\n")

            except Exception:
                pass
            finally:
                self._write_queue.task_done()

        conn.close()

    async def close(self):
        self._is_running = False
        if self._sync_task:
            self._sync_task.cancel()
        if self._db_task:
            try:
                await self._write_queue.join()
                await self._db_task
            except asyncio.CancelledError:
                pass
