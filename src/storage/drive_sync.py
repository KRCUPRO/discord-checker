# src/storage/drive_sync.py
"""
Google Drive Continuous Synchronization Manager
===============================================
Google Colab 환경에서 런타임 종료 및 재접속 시 데이터 유실을 0%로 방지하고,
과거 검사 이력을 자동 복원하여 중복 조회를 건너뛰며,
신규 닉네임 발견 시 구글 드라이브로 즉시 실시간 동기화합니다.
"""

import asyncio
import os
import shutil
import sqlite3
import threading
import time
from pathlib import Path
from typing import Optional

class GoogleDriveSyncManager:
    def __init__(
        self,
        drive_dir: Optional[str] = None,
        local_data_dir: Optional[str] = "data",
        local_available_file: str = "available.txt",
        local_db_file: str = "data/d4uc_results.db",
        sync_interval_seconds: float = 30.0
    ):
        self.drive_dir = Path(drive_dir) if drive_dir else None
        self.local_data_dir = Path(local_data_dir)
        self.local_available_file = Path(local_available_file)
        self.local_db_file = Path(local_db_file)
        self.sync_interval = sync_interval_seconds

        self.is_enabled = bool(self.drive_dir and self.drive_dir.exists())
        self._is_running = False
        self._sync_task: Optional[asyncio.Task] = None
        self._lock = threading.RLock()
        self.last_sync_time: float = 0.0
        self.last_sync_status: str = "비활성" if not self.is_enabled else "대기 중"

    def restore_from_drive(self) -> int:
        """
        코랩 기동 시 구글 드라이브에 저장된 과거 DB 및 텍스트 이력을 로컬로 복원
        """
        if not self.is_enabled or not self.drive_dir:
            return 0

        restored_count = 0
        with self._lock:
            try:
                # 1. SQLite DB 복원
                drive_db = self.drive_dir / "d4uc_results.db"
                if drive_db.is_file():
                    self.local_db_file.parent.mkdir(parents=True, exist_ok=True)
                    # 드라이브 파일이 존재하고 로컬 파일이 없거나 크기가 작을 때 복원
                    if not self.local_db_file.exists() or drive_db.stat().st_size > self.local_db_file.stat().st_size:
                        shutil.copy2(str(drive_db), str(self.local_db_file))
                        restored_count += 1

                # 2. available.txt 복원 및 병합
                drive_avail = self.drive_dir / "available.txt"
                if drive_avail.is_file():
                    existing_names = set()
                    if self.local_available_file.exists():
                        with open(self.local_available_file, "r", encoding="utf-8") as f:
                            existing_names = {line.strip() for line in f if line.strip()}

                    with open(drive_avail, "r", encoding="utf-8") as f:
                        drive_names = [line.strip() for line in f if line.strip()]

                    new_names = [n for n in drive_names if n not in existing_names]
                    if new_names:
                        with open(self.local_available_file, "a", encoding="utf-8") as f:
                            for name in new_names:
                                f.write(f"{name}\n")
                        restored_count += len(new_names)

                self.last_sync_status = "복원 완료"
            except Exception as e:
                self.last_sync_status = f"복원 오류: {e}"

        return restored_count

    def sync_available_immediately(self, username: str):
        """
        '된거' (AVAILABLE) 발견 즉시 구글 드라이브 available.txt에 직접 추가 (0초 딜레이)
        """
        if not self.is_enabled or not self.drive_dir:
            return

        with self._lock:
            try:
                drive_avail = self.drive_dir / "available.txt"
                with open(drive_avail, "a", encoding="utf-8") as f:
                    f.write(f"{username}\n")
                    f.flush()
                    os.fsync(f.fileno())
            except Exception:
                pass

    def sync_to_drive(self, force_checkpoint: bool = False):
        """
        로컬 DB 및 결과 파일들을 Google Drive로 안전 복사
        """
        if not self.is_enabled or not self.drive_dir:
            return

        with self._lock:
            try:
                self.drive_dir.mkdir(parents=True, exist_ok=True)

                # 1. SQLite WAL 체크포인트 (디스크에 최신 커밋 반영)
                if force_checkpoint and self.local_db_file.is_file():
                    try:
                        conn = sqlite3.connect(str(self.local_db_file))
                        conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
                        conn.close()
                    except Exception:
                        pass

                # 2. DB 파일 복사
                if self.local_db_file.is_file():
                    dest_db = self.drive_dir / "d4uc_results.db"
                    shutil.copy2(str(self.local_db_file), str(dest_db))

                # 3. available.txt 복사
                if self.local_available_file.is_file():
                    dest_avail = self.drive_dir / "available.txt"
                    shutil.copy2(str(self.local_available_file), str(dest_avail))

                self.last_sync_time = time.time()
                self.last_sync_status = f"동기화 완료 ({time.strftime('%H:%M:%S')})"
            except Exception as e:
                self.last_sync_status = f"동기화 실패 ({e})"

    async def _periodic_sync_loop(self):
        while self._is_running:
            await asyncio.sleep(self.sync_interval)
            if self._is_running:
                self.sync_to_drive(force_checkpoint=True)

    def start_background_sync(self):
        """비동기 이벤트 루프 내에서 주기적 동기화 백그라운드 태스크 시작"""
        if not self.is_enabled:
            return
        self._is_running = True
        self._sync_task = asyncio.create_task(self._periodic_sync_loop())

    async def stop(self):
        """세션 종료 시 최종 동기화 보증 후 태스크 종료"""
        self._is_running = False
        if self._sync_task and not self._sync_task.done():
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                pass
        self.sync_to_drive(force_checkpoint=True)
