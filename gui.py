# gui.py
import argparse
import asyncio
import collections
import csv
import fnmatch
import json
import os
import random
import sys
import threading
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from src.config import AppConfig
from src.network.client import DiscordApiClient, CheckStatus, CheckResult
from src.network.exceptions import RateLimitedException, WafBlockedException, ProxyFailedException
from src.proxy.manager import UnifiedProxyManager
from src.generator import (
    create_generator,
    MaskPatternGenerator,
    NumericGenerator,
    DictionaryGenerator,
    PatternGenerator,
    PermutationGenerator,
    RandomGenerator,
    HybridGenerator,
    CombinatorialGenerator
)
from src.generator.permutation_gen import SHARD_PRESETS, FIRST_CHARACTERS
from src.storage.db import StorageManager
from src.notify.webhook import DiscordWebhookNotifier
from src.ui.dashboard import DashboardMetrics
from src.ui.i18n import I18nManager
from src.ui.tooltip import CTkToolTip, create_help_badge
from src.utils.paths import get_app_dir, resolve_output_path
from curl_cffi.requests import AsyncSession

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class GuiOrchestrator:
    def __init__(
        self,
        config: AppConfig,
        on_result_cb=None,
        on_log_cb=None,
        on_status_cb=None,
        recheck_list: Optional[List[str]] = None,
        on_recheck_result_cb=None
    ):
        self.config = config
        self.on_result_cb = on_result_cb
        self.on_log_cb = on_log_cb
        self.on_status_cb = on_status_cb
        self.recheck_list = recheck_list or []
        self._recheck_lock = threading.RLock()
        self._recheck_idx = 0
        self.is_recheck_mode = bool(self.config.target.get("mode") == "recheck" and self.recheck_list)
        self.on_recheck_result_cb = on_recheck_result_cb

        self.metrics = DashboardMetrics()
        self.proxy_manager = UnifiedProxyManager(config.proxy)
        self.generator = create_generator(config.target)
        self.storage = StorageManager(
            db_path=config.storage.get("db_path", "data/d4uc_results.db"),
            save_legacy=config.storage.get("save_legacy_txt", True),
            available_file=config.storage.get("available_file", "available.txt"),
            taken_file=config.storage.get("taken_file", "taken.txt")
        )
        self.client = DiscordApiClient(
            impersonate=config.network.get("impersonate", "chrome131"),
            timeout=float(config.network.get("timeout_seconds", 4.0))
        )
        self.webhook = DiscordWebhookNotifier(
            webhook_url=config.webhook.get("url", ""),
            enabled=config.webhook.get("enabled", False),
            mention=config.webhook.get("mention", "@here")
        )
        self.concurrency = int(config.network.get("concurrency", 5))
        self.is_running = False
        self.start_time: Optional[float] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._worker_tasks: List[asyncio.Task] = []
        self._last_milestone = 0
        self._retry_queue: collections.deque = collections.deque()
        self._retry_lock = threading.Lock()

    def log(self, text: str, level: str = "INFO", worker_id: Optional[int] = None):
        if self.on_log_cb:
            ts = datetime.now().strftime("%H:%M:%S")
            self.on_log_cb(f"[{ts}] [{level}] {text}", level, worker_id)

    def hot_swap_generator(self, target_config: dict):
        """실행 중 탐색 모드/길이/패턴 조건 즉시 무중단 핫스왑(Hot-Swap) 교체"""
        self.config.target = target_config
        self.generator = create_generator(target_config)
        mode_str = target_config.get("mode", "hybrid").upper()
        len_val = target_config.get("length", 4)
        patt_str = self.generator.get_pattern_type()
        self.log(
            f"🔄 [핫스왑] 탐색 설정 즉시 반영 완료: 모드={mode_str}, 길이={len_val}자, 패턴={patt_str}",
            "SYSTEM"
        )

    def set_concurrency(self, new_count: int):
        """실행 중 동시 비동기 워커 수 무중단 동적 스케일링 (Hot-Scale)"""
        new_count = max(1, min(50, int(new_count)))
        old_count = self.concurrency
        if old_count == new_count:
            return
        self.concurrency = new_count
        self.config.network["concurrency"] = new_count

        if self.is_running and self._loop and self._loop.is_running():
            if new_count > old_count:
                for wid in range(old_count + 1, new_count + 1):
                    def _spawn_worker(w_id=wid):
                        t = asyncio.create_task(self.worker_loop(w_id))
                        self._worker_tasks.append(t)
                    self._loop.call_soon_threadsafe(_spawn_worker)
                self.log(
                    f"⚡ [동적 스케일링] 동시 비동기 워커 확장: {old_count}개 ➔ {new_count}개 (워커 {old_count+1}~{new_count} 순차 가동)",
                    "SYSTEM"
                )
            elif new_count < old_count:
                self.log(
                    f"⚡ [동적 스케일링] 동시 비동기 워커 축소: {old_count}개 ➔ {new_count}개 (워커 {new_count+1} 이상 안전 퇴장)",
                    "SYSTEM"
                )

    async def worker_loop(self, worker_id: int):
        # Staggered ramp-up to prevent burst TLS handshakes
        await asyncio.sleep(min(0.06 * (worker_id - 1), 1.2))

        session = AsyncSession()
        try:
            while self.is_running:
                # Dynamic scale down check
                if worker_id > self.concurrency:
                    break

                # 1. Candidate acquisition: Re-check Mode vs Generation Mode
                if self.is_recheck_mode:
                    with self._recheck_lock:
                        if self._recheck_idx >= len(self.recheck_list):
                            # Re-check queue exhausted
                            break
                        username = self.recheck_list[self._recheck_idx]
                        self._recheck_idx += 1
                else:
                    # Check retry queue first (re-queued candidates from network/proxy glitches)
                    username = None
                    with self._retry_lock:
                        if self._retry_queue:
                            username = self._retry_queue.popleft()

                    if not username:
                        # Unique candidate acquisition with skip-already-checked check
                        skip_already = self.config.target.get("skip_already_checked", True)
                        for _ in range(150):
                            cand = self.generator.next_username()
                            if not cand:
                                break
                            if skip_already and self.storage.is_tried(cand):
                                self.metrics.skipped_count += 1
                                continue
                            # Reserve immediately in memory so concurrent workers won't pick the same candidate
                            self.storage.mark_tried(cand)
                            username = cand
                            break

                    if not username:
                        await asyncio.sleep(0.1)
                        continue

                # 2. Proxy Lease with Zero Host Leak Hard-Gate
                is_proxy_required = (self.config.proxy.get("mode", "direct").lower() != "direct")
                proxy_ep = None

                if is_proxy_required:
                    # Retry leasing proxy until available, ensuring 0.00% direct requests leak out
                    for _ in range(20):
                        if not self.is_running:
                            break
                        if self.proxy_manager.is_rotating(worker_id=worker_id):
                            await asyncio.to_thread(self.proxy_manager.wait_until_ready, worker_id, 6.0)
                        proxy_ep = await asyncio.to_thread(self.proxy_manager.lease_proxy, worker_id)
                        if proxy_ep and proxy_ep.url:
                            break
                        await asyncio.sleep(0.2)

                    if not self.is_running:
                        break

                    if not proxy_ep or not proxy_ep.url:
                        self.log(
                            f"[워커 {worker_id}] ⏳ 프록시 터널 대기 중... (Zero-Leak 정책으로 Direct 호스트 통신 원천 차단)",
                            "PROXY",
                            worker_id=worker_id
                        )
                        await asyncio.sleep(0.5)
                        continue
                else:
                    proxy_ep = await asyncio.to_thread(self.proxy_manager.lease_proxy, worker_id)

                proxy_url = proxy_ep.url if proxy_ep else None
                prov_short = proxy_ep.provider_name.split()[0] if proxy_ep else ("Direct" if not is_proxy_required else "Proxy")
                prov_name = proxy_ep.provider_name if proxy_ep else ("Direct" if not is_proxy_required else "Proxy-Tunnel")

                # 3. Perform asynchronous check
                try:
                    pattern_name = "recheck" if self.is_recheck_mode else self.generator.get_pattern_type()
                    result = await self.client.check(
                        session=session,
                        username=username,
                        proxy=proxy_url,
                        pattern_type=pattern_name,
                        require_proxy=is_proxy_required
                    )
                    # Bind human-readable server/country string to result.proxy_used for reporting & UI
                    result.proxy_used = prov_name

                    self.proxy_manager.release_proxy(proxy_ep, success=True, rate_limited=False)
                    self.metrics.total_checked += 1

                    if result.status == CheckStatus.AVAILABLE:
                        self.metrics.available_count += 1
                        ts_str = datetime.now().strftime("%H:%M:%S")
                        prov_name = proxy_ep.provider_name if proxy_ep else "Direct"
                        self.metrics.recent_available.append(
                            (ts_str, result.username, result.pattern_type, result.latency_ms)
                        )
                        if self.is_recheck_mode:
                            self.log(
                                f"[워커 {worker_id}] ✅ [재확인 유효] '{result.username}' 여전히 사용 가능! ({result.latency_ms:.1f}ms, {prov_name})",
                                "SUCCESS",
                                worker_id=worker_id
                            )
                            if self.on_recheck_result_cb:
                                self.on_recheck_result_cb(result.username, True, f"{result.latency_ms:.1f}ms", prov_name)
                        else:
                            self.log(
                                f"[워커 {worker_id}] 🎉 사용 가능 닉네임 발견! '{result.username}' ({result.pattern_type}, {result.latency_ms:.1f}ms, {prov_name})",
                                "SUCCESS",
                                worker_id=worker_id
                            )
                            self.log(
                                f"💾 [자동 저장] '{result.username}' -> available_usernames.txt, csv, json 및 results/ 폴더에 즉시 보존 완료!",
                                "STORAGE"
                            )
                            if self.on_result_cb:
                                self.on_result_cb(ts_str, result.username, result.pattern_type, f"{result.latency_ms:.1f}ms", prov_name)
                            await self.webhook.notify_available(session, result)

                    elif result.status == CheckStatus.TAKEN:
                        self.metrics.taken_count += 1
                        prov_name = proxy_ep.provider_name if proxy_ep else "Direct"
                        if self.is_recheck_mode:
                            self.storage.update_recheck_status(result.username, CheckStatus.TAKEN, result.latency_ms, prov_name)
                            self.log(
                                f"[워커 {worker_id}] ❌ [재확인 TAKEN] '{username}' -> 다른 사용자가 이미 등록함 (사용 중 감지)!",
                                "WARN",
                                worker_id=worker_id
                            )
                            if self.on_recheck_result_cb:
                                self.on_recheck_result_cb(result.username, False, f"{result.latency_ms:.1f}ms", prov_name)
                        else:
                            self.log(
                                f"[워커 {worker_id}] ❌ '{username}' ({len(username)}자) -> 사용 중 (TAKEN) [{result.latency_ms:.1f}ms | {prov_short}]",
                                "WORKER",
                                worker_id=worker_id
                            )
                    else:
                        self.metrics.error_count += 1
                        self.log(
                            f"[워커 {worker_id}] ⚠️ '{username}' ({len(username)}자) -> 상태 불명 ({result.latency_ms:.1f}ms)",
                            "WORKER",
                            worker_id=worker_id
                        )

                    if not self.is_recheck_mode:
                        await self.storage.enqueue_result(result)

                    # Milestone telemetry logging (every 50 checks)
                    if self.metrics.total_checked - self._last_milestone >= 50:
                        self._last_milestone = self.metrics.total_checked
                        self.log(
                            f"🔍 누적 검사 현황: 총 {self.metrics.total_checked:,}개 완료 | 속도: {self.metrics.rps:.1f} req/s | 사용 가능: {self.metrics.available_count}개 | 건너뜀: {self.metrics.skipped_count:,}개",
                            "PROGRESS"
                        )

                except RateLimitedException as rle:
                    self.metrics.rate_limited_count += 1
                    # 1. Zero-loss retry preservation: re-queue candidate
                    if not self.is_recheck_mode and username:
                        self.storage.unmark_tried(username)
                        with self._retry_lock:
                            self._retry_queue.appendleft(username)

                    # 2. Dynamic 429 cooldown & cluster rotation
                    retry_secs = getattr(rle, "retry_after", 300.0) or 300.0
                    cooldown_val = min(max(retry_secs, 120.0), 600.0)
                    rotated_cluster = await asyncio.to_thread(self.proxy_manager.rotate_surfshark, worker_id, cooldown_val)

                    # 3. Clean corrupted/stale libcurl session handles
                    try:
                        await session.close()
                    except Exception:
                        pass
                    session = AsyncSession()

                    if rotated_cluster:
                        self.log(
                            f"🔄 [프록시 페널티 큐 회전] [워커 {worker_id}] 429 감지 -> 기존 국가 쿨다운 큐 이동 후 신선한 국가 배정 완료: [{rotated_cluster.country} - {rotated_cluster.city}] ('{username}' 재검사 큐 보존)",
                            "PROXY",
                            worker_id=worker_id
                        )
                    self.log(
                        f"[워커 {worker_id}] ⚠️ 429 레이트리밋 감지 ('{username}') -> 새 IP 순환 대기 ({min(retry_secs, 2.5):.1f}s)",
                        "RATELIMIT",
                        worker_id=worker_id
                    )
                    await asyncio.sleep(min(retry_secs, 2.5))

                except (WafBlockedException, ProxyFailedException) as we:
                    self.metrics.error_count += 1
                    self.proxy_manager.release_proxy(proxy_ep, success=False, rate_limited=False)
                    # 1. Zero-loss retry preservation: re-queue candidate
                    if not self.is_recheck_mode and username:
                        self.storage.unmark_tried(username)
                        with self._retry_lock:
                            self._retry_queue.appendleft(username)

                    # 2. Auto-Healing: rotate to a fresh healthy cluster immediately and restart tunnel
                    rotated_cluster = await asyncio.to_thread(self.proxy_manager.rotate_surfshark, worker_id, 300.0)

                    # 3. Wipe stale/poisoned TCP sockets from libcurl session pool
                    try:
                        await session.close()
                    except Exception:
                        pass
                    session = AsyncSession()

                    rot_desc = f" -> [{rotated_cluster.country} - {rotated_cluster.city}] 즉시 자동 회전" if rotated_cluster else ""
                    self.log(
                        f"[워커 {worker_id}] 🛡️ [프록시 자동 치유] 장애 감지({str(we)[:60]}){rot_desc} ('{username}' 재검사 큐 보존 완료)",
                        "PROXY",
                        worker_id=worker_id
                    )
                    await asyncio.sleep(0.5)

                except Exception as e:
                    self.metrics.error_count += 1
                    if not self.is_recheck_mode and username:
                        self.storage.unmark_tried(username)
                        with self._retry_lock:
                            self._retry_queue.appendleft(username)
                    self.log(f"[워커 {worker_id}] ❌ 워커 예외: {type(e).__name__} ({str(e)[:80]})", "ERROR", worker_id=worker_id)
                    await asyncio.sleep(0.4)

                # Intelligent anti-burst pacing: prevents premature Discord 429 bans per IP
                is_surfshark = (self.config.proxy.get("mode", "direct").lower() == "surfshark")
                if is_surfshark:
                    if self.concurrency >= 20:
                        base_pacing = 0.15
                        jitter = random.uniform(0.05, 0.15)
                    elif self.concurrency >= 10:
                        base_pacing = 0.25
                        jitter = random.uniform(0.05, 0.2)
                    else:
                        base_pacing = max(0.35, 2.0 / max(1, self.concurrency))
                        jitter = random.uniform(0.1, 0.25)
                else:
                    if self.concurrency >= 30:
                        base_pacing = 0.04
                        jitter = random.uniform(0.01, 0.04)
                    elif self.concurrency >= 10:
                        base_pacing = 0.08
                        jitter = random.uniform(0.02, 0.06)
                    else:
                        base_pacing = max(0.12, 1.5 / max(1, self.concurrency))
                        jitter = random.uniform(0.03, 0.08)
                await asyncio.sleep(base_pacing + jitter)
        finally:
            try:
                await session.close()
            except Exception:
                pass

    async def _run_async(self):
        self.is_running = True
        self.start_time = time.time()
        
        mode_name = self.config.target.get("mode", "hybrid")
        len_val = self.config.target.get("length", 4)
        p_mode = self.config.proxy.get("mode", "surfshark")

        self.log(f"🚀 [1단계] D4UC 비동기 엔진 가동 시작 (탐색 모드: {mode_name.upper()}, 길이: {len_val}자, 동시성: {self.concurrency}워커)", "START")
        
        await self.storage.start_worker()
        cached_count = self.storage.get_history_count()
        self.log(f"💾 [2단계] SQLite WAL 데이터베이스 및 TXT 저장소 초기화 완료 (과거 검사 닉네임 {cached_count:,}개 캐시 로드 -> 중복 검사 0% 건너뛰기 활성)", "STORAGE")

        # 3단계: 프록시 사전 실사 검증 & 1:1 워커 터널 풀 가동 (Zero Host Leak Invariant)
        if p_mode == "surfshark":
            self.log(f"🛡️ [3단계] Surfshark 1:1 워커 전용 다중 국가 터널 풀 연동 및 실사 검증 개시...", "NETWORK")
            surfshark_prov = self.proxy_manager.get_surfshark_provider()
            if not surfshark_prov:
                self.log("❌ [PROXY-GATE] Surfshark 프로바이더를 초기화할 수 없습니다.", "ERROR")
                self.is_running = False
                return

            self.log(f"🛡️ [PROXY-GATE] {self.concurrency}개 워커의 독립 국가 터널을 동시 기동 및 사전 실사 검증 중...", "NETWORK")
            tunnels_ok = await asyncio.to_thread(surfshark_prov.ensure_workers_running, self.concurrency)
            if not tunnels_ok:
                self.log("❌ [PROXY-GATE] 다중 국가 터널 실행 실패! 호스트 실제 IP 보호를 위해 검사를 전면 중단합니다.", "ERROR")
                self.is_running = False
                return

            summary = surfshark_prov.get_workers_summary(self.concurrency)
            for wid, c_info in summary:
                self.log(f"🛡️ [PROXY-GATE] 워커 {wid} ➔ 전용 국가 터널 배정 완료: {c_info}", "NETWORK")

            self.log(f"🛡️ [PROXY-GATE] ✅ 전체 {self.concurrency}개 워커 1:1 독립 국가 터널 완전 안정화 확인 (호스트 IP 노출 위험 0%). 검사를 가동합니다.", "NETWORK")
        else:
            self.log(f"🌐 [3단계] 프록시 인프라 설정 완료: {p_mode.upper()}", "NETWORK")

        self.log(f"🔒 [4단계] Chrome131 TLS JA3/JA4 스텔스 지문 위장 세션 준비 완료", "TLS")

        self._worker_tasks = [
            asyncio.create_task(self.worker_loop(i + 1))
            for i in range(self.concurrency)
        ]
        self.log(f"⚡ [5단계] {self.concurrency}개 비동기 스텔스 워커 투입 완료. 실시간 검사를 개시합니다.", "RUNNING")

        while self.is_running:
            await asyncio.sleep(0.2)

        self.log("⏹️ 사용자 요청으로 검사 작업을 중지합니다. 잔여 작업을 안전하게 정리 중...", "STOP")
        for t in self._worker_tasks:
            t.cancel()
        await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        await self.storage.close()
        self.proxy_manager.close()
        self.log(f"✅ 검사 작업이 안전하게 종료되었습니다. (누적 검사: {self.metrics.total_checked:,}개, 발견: {self.metrics.available_count}개)", "COMPLETED")

    def start_thread(self):
        def runner():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._run_async())

        t = threading.Thread(target=runner, daemon=True)
        t.start()

    def stop(self):
        self.is_running = False
        self.proxy_manager.close()

    def get_elapsed_str(self) -> str:
        if not self.start_time:
            return "00:00:00"
        el = int(time.time() - self.start_time)
        hrs = el // 3600
        mins = (el % 3600) // 60
        secs = el % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"


class DiscordCheckerGui(ctk.CTk):
    def __init__(self, default_lang: str = "ko"):
        super().__init__()

        I18nManager.set_language(default_lang)
        self.current_lang = default_lang

        self.title("Discord Username Checker V2 - Bug Bounty & Stealth Edition")
        self.geometry("1180x820")
        self.minsize(1040, 720)

        self.config = AppConfig.load()
        self.orchestrator: Optional[GuiOrchestrator] = None
        self._is_log_collapsed = False
        self._raw_logs: List[Tuple[str, str, Optional[int]]] = []
        self._pending_logs: List[str] = []
        self._log_flush_scheduled: bool = False
        self.discovered_items: List[Dict[str, Any]] = []

        self._build_ui()
        self._load_ui_from_config()
        self._restore_discovered_table()
        self._start_telemetry_loop()
        self._refresh_language()

    def _build_ui(self):
        # Grid: Column 0 (Sidebar, fixed width 360), Column 1 (Content, expandable)
        self.grid_columnconfigure(0, weight=0, minsize=360)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= LEFT SIDEBAR =================
        self.sidebar = ctk.CTkFrame(self, width=360, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_propagate(False)

        # Title & Subtitle
        self.app_title = ctk.CTkLabel(
            self.sidebar,
            text=I18nManager.t("app_title"),
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.app_title.pack(padx=20, pady=(20, 2), anchor="w")

        self.app_subtitle = ctk.CTkLabel(
            self.sidebar,
            text=I18nManager.t("app_subtitle"),
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.app_subtitle.pack(padx=20, pady=(0, 12), anchor="w")

        # Scrollable controls
        self.controls_scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.controls_scroll.pack(fill="both", expand=True, padx=6, pady=0)
        try:
            self.controls_scroll._parent_canvas.unbind_all("<Shift-MouseWheel>")
        except Exception:
            pass

        # 1. Target Mode
        mode_header = ctk.CTkFrame(self.controls_scroll, fg_color="transparent")
        mode_header.pack(fill="x", padx=6, pady=(6, 2))
        self.lbl_mode = ctk.CTkLabel(mode_header, text=I18nManager.t("target_mode"), font=ctk.CTkFont(weight="bold"))
        self.lbl_mode.pack(side="left")
        create_help_badge(mode_header, lambda: I18nManager.t("target_mode_tooltip")).pack(side="right")
        CTkToolTip(self.lbl_mode, lambda: I18nManager.t("target_mode_tooltip"))

        self.mode_menu = ctk.CTkOptionMenu(
            self.controls_scroll,
            values=[
                "Hybrid (사전+패턴+숫자+마스크)",
                "Combinatorial (비번형 영숫자 0~z 조합)",
                "Custom Mask (커스텀 패턴)",
                "Re-check (기존 닉네임 재확인)",
                "Dictionary (사전/음절)",
                "Pattern (대칭/반복)",
                "Numeric (0~9 숫자닉)",
                "Permutation (전수순열)",
                "Random (무작위)"
            ],
            command=self._on_mode_changed
        )
        self.mode_menu.pack(fill="x", padx=6, pady=(0, 8))

        # 2. Length
        len_header = ctk.CTkFrame(self.controls_scroll, fg_color="transparent")
        len_header.pack(fill="x", padx=6, pady=(4, 2))
        self.lbl_length = ctk.CTkLabel(len_header, text=I18nManager.t("length_title"), font=ctk.CTkFont(weight="bold"))
        self.lbl_length.pack(side="left")
        create_help_badge(len_header, lambda: I18nManager.t("length_tooltip")).pack(side="right")
        CTkToolTip(self.lbl_length, lambda: I18nManager.t("length_tooltip"))

        self.length_menu = ctk.CTkSegmentedButton(
            self.controls_scroll,
            values=["3", "4", "5", "6"],
            command=self._on_length_changed
        )
        self.length_menu.set("4")
        self.length_menu.pack(fill="x", padx=6, pady=(0, 8))

        # 2.5. Dynamic Mode Settings & Preview Container
        self.custom_box = ctk.CTkFrame(self.controls_scroll, fg_color="#181820", corner_radius=8)
        self.custom_box.pack(fill="x", padx=6, pady=(4, 8))

        custom_box_header = ctk.CTkFrame(self.custom_box, fg_color="transparent")
        custom_box_header.pack(fill="x", padx=8, pady=(6, 2))
        self.lbl_custom_title = ctk.CTkLabel(
            custom_box_header,
            text=I18nManager.t("mode_title_hybrid"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00c8ff"
        )
        self.lbl_custom_title.pack(side="left")

        self.btn_reset_pattern = ctk.CTkButton(
            custom_box_header,
            text=I18nManager.t("btn_custom_reset"),
            width=46,
            height=20,
            font=ctk.CTkFont(size=10),
            fg_color="#2b2b36",
            hover_color="#3a3a4a",
            command=self._on_reset_custom_pattern
        )
        # Hidden by default, shown only in custom mode
        CTkToolTip(self.btn_reset_pattern, lambda: I18nManager.t("btn_custom_reset_tooltip"))

        self.lbl_custom_badge = ctk.CTkLabel(
            custom_box_header,
            text=I18nManager.t("mode_badge_hybrid"),
            font=ctk.CTkFont(size=10),
            text_color="#00c8ff"
        )
        self.lbl_custom_badge.pack(side="right")

        # Dynamic Mode Description Label
        self.lbl_mode_desc = ctk.CTkLabel(
            self.custom_box,
            text=I18nManager.t("mode_desc_hybrid"),
            font=ctk.CTkFont(size=10),
            text_color="#aaaaaa",
            wraplength=220,
            justify="left"
        )
        self.lbl_mode_desc.pack(fill="x", padx=8, pady=(2, 4))

        # Custom Pattern Controls Frame (Only visible when Custom Mask mode is active)
        self.custom_controls_frame = ctk.CTkFrame(self.custom_box, fg_color="transparent")

        # Prefix
        prefix_header = ctk.CTkFrame(self.custom_controls_frame, fg_color="transparent")
        prefix_header.pack(fill="x", padx=8, pady=(2, 0))
        self.lbl_prefix = ctk.CTkLabel(prefix_header, text=I18nManager.t("prefix_label"), font=ctk.CTkFont(size=11))
        self.lbl_prefix.pack(side="left")
        create_help_badge(prefix_header, lambda: I18nManager.t("prefix_tooltip")).pack(side="right")
        self.prefix_entry = ctk.CTkEntry(self.custom_controls_frame, placeholder_text=I18nManager.t("prefix_placeholder"), height=26, font=ctk.CTkFont(size=11))
        self.prefix_entry.pack(fill="x", padx=8, pady=(0, 4))
        self.prefix_entry.bind("<KeyRelease>", self._on_custom_pattern_input_changed)
        CTkToolTip(self.prefix_entry, lambda: I18nManager.t("prefix_tooltip"))

        # Suffix
        suffix_header = ctk.CTkFrame(self.custom_controls_frame, fg_color="transparent")
        suffix_header.pack(fill="x", padx=8, pady=(2, 0))
        self.lbl_suffix = ctk.CTkLabel(suffix_header, text=I18nManager.t("suffix_label"), font=ctk.CTkFont(size=11))
        self.lbl_suffix.pack(side="left")
        create_help_badge(suffix_header, lambda: I18nManager.t("suffix_tooltip")).pack(side="right")
        self.suffix_entry = ctk.CTkEntry(self.custom_controls_frame, placeholder_text=I18nManager.t("suffix_placeholder"), height=26, font=ctk.CTkFont(size=11))
        self.suffix_entry.pack(fill="x", padx=8, pady=(0, 4))
        self.suffix_entry.bind("<KeyRelease>", self._on_custom_pattern_input_changed)
        CTkToolTip(self.suffix_entry, lambda: I18nManager.t("suffix_tooltip"))

        # Middle Dot Option
        dot_header = ctk.CTkFrame(self.custom_controls_frame, fg_color="transparent")
        dot_header.pack(fill="x", padx=8, pady=(2, 0))
        self.lbl_middle_dot = ctk.CTkLabel(dot_header, text=I18nManager.t("middle_dot_label"), font=ctk.CTkFont(size=11))
        self.lbl_middle_dot.pack(side="left")
        create_help_badge(dot_header, lambda: I18nManager.t("middle_dot_tooltip")).pack(side="right")
        self.middle_dot_menu = ctk.CTkOptionMenu(
            self.custom_controls_frame,
            values=[
                I18nManager.t("middle_dot_none"),
                I18nManager.t("middle_dot_opt"),
                I18nManager.t("middle_dot_req")
            ],
            height=26,
            font=ctk.CTkFont(size=11),
            command=self._on_middle_dot_changed
        )
        self.middle_dot_menu.set(I18nManager.t("middle_dot_none"))
        self.middle_dot_menu.pack(fill="x", padx=8, pady=(0, 4))
        CTkToolTip(self.middle_dot_menu, lambda: I18nManager.t("middle_dot_tooltip"))

        # Direct Mask Pattern
        mask_header = ctk.CTkFrame(self.custom_controls_frame, fg_color="transparent")
        mask_header.pack(fill="x", padx=8, pady=(2, 0))
        self.lbl_mask = ctk.CTkLabel(mask_header, text=I18nManager.t("custom_mask_label"), font=ctk.CTkFont(size=11))
        self.lbl_mask.pack(side="left")
        create_help_badge(mask_header, lambda: I18nManager.t("custom_mask_tooltip")).pack(side="right")
        self.mask_entry = ctk.CTkEntry(self.custom_controls_frame, placeholder_text=I18nManager.t("custom_mask_placeholder"), height=26, font=ctk.CTkFont(size=11))
        self.mask_entry.pack(fill="x", padx=8, pady=(0, 6))
        self.mask_entry.bind("<KeyRelease>", self._on_custom_pattern_input_changed)
        CTkToolTip(self.mask_entry, lambda: I18nManager.t("custom_mask_tooltip"))

        # Re-check Controls Frame (Only visible when Re-check mode is active)
        self.recheck_controls_frame = ctk.CTkFrame(self.custom_box, fg_color="transparent")

        recheck_header = ctk.CTkFrame(self.recheck_controls_frame, fg_color="transparent")
        recheck_header.pack(fill="x", padx=8, pady=(2, 0))
        self.lbl_recheck_range = ctk.CTkLabel(
            recheck_header,
            text=I18nManager.t("recheck_range_label"),
            font=ctk.CTkFont(size=11)
        )
        self.lbl_recheck_range.pack(side="left")
        create_help_badge(
            recheck_header,
            lambda: "과거에 검사했던 닉네임 기록(SQLite DB)에서 다시 확인해볼 범위를 선택합니다." if self.current_lang == "ko" else "Select the range of previously checked usernames from the database to re-verify."
        ).pack(side="right")
        CTkToolTip(
            self.lbl_recheck_range,
            lambda: "과거에 검사했던 닉네임 기록(SQLite DB)에서 다시 확인해볼 범위를 선택합니다." if self.current_lang == "ko" else "Select the range of previously checked usernames from the database to re-verify."
        )

        self.recheck_range_menu = ctk.CTkOptionMenu(
            self.recheck_controls_frame,
            values=[
                I18nManager.t("recheck_range_all"),
                I18nManager.t("recheck_range_1_50"),
                I18nManager.t("recheck_range_51_100"),
                I18nManager.t("recheck_range_101_200"),
                I18nManager.t("recheck_range_custom")
            ],
            height=26,
            font=ctk.CTkFont(size=11),
            command=self._on_recheck_range_changed
        )
        self.recheck_range_menu.set(I18nManager.t("recheck_range_all"))
        self.recheck_range_menu.pack(fill="x", padx=8, pady=(0, 4))

        self.lbl_recheck_count = ctk.CTkLabel(
            self.recheck_controls_frame,
            text="재확인 대상: 0개 대기 중" if self.current_lang == "ko" else "Re-check: 0 loaded",
            font=ctk.CTkFont(size=11),
            text_color="#00c8ff"
        )
        self.lbl_recheck_count.pack(anchor="w", padx=8, pady=(0, 4))

        self.btn_recheck_import_sub = ctk.CTkButton(
            self.recheck_controls_frame,
            text=I18nManager.t("btn_load_history"),
            height=24,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#2b2b36",
            hover_color="#3a3a4a",
            command=self._import_history_file
        )
        self.btn_recheck_import_sub.pack(fill="x", padx=8, pady=(0, 6))

        # Combinatorial Controls Frame (Only visible when Combinatorial mode is active)
        self.comb_controls_frame = ctk.CTkFrame(self.custom_box, fg_color="transparent")

        dir_header = ctk.CTkFrame(self.comb_controls_frame, fg_color="transparent")
        dir_header.pack(fill="x", padx=8, pady=(2, 0))
        self.lbl_comb_direction = ctk.CTkLabel(
            dir_header,
            text=I18nManager.t("comb_direction_label"),
            font=ctk.CTkFont(size=11)
        )
        self.lbl_comb_direction.pack(side="left")
        create_help_badge(dir_header, lambda: I18nManager.t("comb_direction_tooltip")).pack(side="right")

        self.comb_direction_menu = ctk.CTkOptionMenu(
            self.comb_controls_frame,
            values=[
                I18nManager.t("comb_direction_asc"),
                I18nManager.t("comb_direction_desc")
            ],
            height=26,
            font=ctk.CTkFont(size=11),
            command=self._on_comb_param_changed
        )
        self.comb_direction_menu.set(I18nManager.t("comb_direction_asc"))
        self.comb_direction_menu.pack(fill="x", padx=8, pady=(0, 4))
        CTkToolTip(self.comb_direction_menu, lambda: I18nManager.t("comb_direction_tooltip"))

        charset_header = ctk.CTkFrame(self.comb_controls_frame, fg_color="transparent")
        charset_header.pack(fill="x", padx=8, pady=(2, 0))
        self.lbl_comb_charset = ctk.CTkLabel(
            charset_header,
            text=I18nManager.t("comb_charset_label"),
            font=ctk.CTkFont(size=11)
        )
        self.lbl_comb_charset.pack(side="left")
        create_help_badge(charset_header, lambda: I18nManager.t("comb_charset_tooltip")).pack(side="right")

        self.comb_charset_menu = ctk.CTkOptionMenu(
            self.comb_controls_frame,
            values=[
                I18nManager.t("comb_charset_num_first"),
                I18nManager.t("comb_charset_alpha_first")
            ],
            height=26,
            font=ctk.CTkFont(size=11),
            command=self._on_comb_param_changed
        )
        self.comb_charset_menu.set(I18nManager.t("comb_charset_num_first"))
        self.comb_charset_menu.pack(fill="x", padx=8, pady=(0, 6))
        CTkToolTip(self.comb_charset_menu, lambda: I18nManager.t("comb_charset_tooltip"))

        # Permutation Controls Frame (Work Sharding across multiple windows)
        self.perm_controls_frame = ctk.CTkFrame(self.custom_box, fg_color="transparent")

        shard_header = ctk.CTkFrame(self.perm_controls_frame, fg_color="transparent")
        shard_header.pack(fill="x", padx=8, pady=(2, 0))

        self.lbl_perm_shard = ctk.CTkLabel(
            shard_header,
            text=I18nManager.t("perm_shard_title"),
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.lbl_perm_shard.pack(side="left")
        create_help_badge(shard_header, lambda: I18nManager.t("perm_shard_tooltip")).pack(side="right")
        CTkToolTip(self.lbl_perm_shard, lambda: I18nManager.t("perm_shard_tooltip"))

        perm_shard_options = [v["label"] for v in SHARD_PRESETS.values()] + [
            I18nManager.t("perm_custom_range_title")
        ]
        self.perm_shard_menu = ctk.CTkOptionMenu(
            self.perm_controls_frame,
            values=perm_shard_options,
            height=26,
            font=ctk.CTkFont(size=11),
            command=self._on_perm_param_changed
        )
        self.perm_shard_menu.set(perm_shard_options[0])
        self.perm_shard_menu.pack(fill="x", padx=8, pady=(0, 4))
        CTkToolTip(self.perm_shard_menu, lambda: I18nManager.t("perm_shard_tooltip"))

        # Sub-frame for Custom Range (start char ~ end char)
        self.perm_custom_range_frame = ctk.CTkFrame(self.perm_controls_frame, fg_color="transparent")
        range_row = ctk.CTkFrame(self.perm_custom_range_frame, fg_color="transparent")
        range_row.pack(fill="x", padx=8, pady=(0, 4))

        chars_37 = list(FIRST_CHARACTERS)

        self.lbl_perm_range_title = ctk.CTkLabel(
            range_row,
            text=I18nManager.t("perm_custom_range_title") + ":",
            font=ctk.CTkFont(size=11),
            text_color="#aaaaaa"
        )
        self.lbl_perm_range_title.pack(side="left", padx=(0, 4))

        self.perm_start_menu = ctk.CTkOptionMenu(
            range_row,
            values=chars_37,
            width=55,
            height=24,
            font=ctk.CTkFont(size=10),
            command=self._on_perm_param_changed
        )
        self.perm_start_menu.set("a")
        self.perm_start_menu.pack(side="left", padx=(0, 4))
        CTkToolTip(self.perm_start_menu, lambda: I18nManager.t("perm_start_char_tooltip"))

        tilde_lbl = ctk.CTkLabel(range_row, text="~", font=ctk.CTkFont(size=11))
        tilde_lbl.pack(side="left", padx=(0, 4))

        self.perm_end_menu = ctk.CTkOptionMenu(
            range_row,
            values=chars_37,
            width=55,
            height=24,
            font=ctk.CTkFont(size=10),
            command=self._on_perm_param_changed
        )
        self.perm_end_menu.set("m")
        self.perm_end_menu.pack(side="left", padx=(0, 4))
        CTkToolTip(self.perm_end_menu, lambda: I18nManager.t("perm_end_char_tooltip"))
        create_help_badge(range_row, lambda: I18nManager.t("perm_custom_range_tooltip")).pack(side="right")

        # Real-time Live Generation Preview Box
        self.preview_frame = ctk.CTkFrame(self.custom_box, fg_color="#121218", corner_radius=6)
        self.preview_frame.pack(fill="x", padx=8, pady=(4, 8))
        self.lbl_preview_title = ctk.CTkLabel(
            self.preview_frame,
            text=I18nManager.t("preview_title"),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#00c8ff"
        )
        self.lbl_preview_title.pack(anchor="w", padx=6, pady=(4, 0))
        self.lbl_preview_text = ctk.CTkLabel(
            self.preview_frame,
            text=I18nManager.t("custom_preview_idle"),
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#888888",
            wraplength=210,
            justify="left"
        )
        self.lbl_preview_text.pack(anchor="w", padx=6, pady=(0, 6))

        # 3. Proxy Mode
        proxy_header = ctk.CTkFrame(self.controls_scroll, fg_color="transparent")
        proxy_header.pack(fill="x", padx=6, pady=(4, 2))
        self.lbl_proxy = ctk.CTkLabel(proxy_header, text=I18nManager.t("proxy_title"), font=ctk.CTkFont(weight="bold"))
        self.lbl_proxy.pack(side="left")
        create_help_badge(proxy_header, lambda: I18nManager.t("proxy_tooltip")).pack(side="right")
        CTkToolTip(self.lbl_proxy, lambda: I18nManager.t("proxy_tooltip"))

        self.proxy_menu = ctk.CTkOptionMenu(
            self.controls_scroll,
            values=["Surfshark (격리 프록시)", "File Pool (proxies.txt)", "ThorData", "Direct (단일 IP)"]
        )
        self.proxy_menu.set("Surfshark (격리 프록시)")
        self.proxy_menu.pack(fill="x", padx=6, pady=(0, 8))

        # 4. Preferred Country
        country_header = ctk.CTkFrame(self.controls_scroll, fg_color="transparent")
        country_header.pack(fill="x", padx=6, pady=(4, 2))
        self.lbl_country = ctk.CTkLabel(country_header, text=I18nManager.t("country_title"), font=ctk.CTkFont(weight="bold"))
        self.lbl_country.pack(side="left")
        create_help_badge(country_header, lambda: I18nManager.t("country_tooltip")).pack(side="right")
        CTkToolTip(self.lbl_country, lambda: I18nManager.t("country_tooltip"))

        self.country_menu = ctk.CTkOptionMenu(
            self.controls_scroll,
            values=["전세계 142개 전체", "한국 + 일본 + 싱가포르", "한국 (KR)", "일본 (JP)", "미국 (US)", "유럽 (독일/영국)"]
        )
        self.country_menu.set("전세계 142개 전체")
        self.country_menu.pack(fill="x", padx=6, pady=(0, 8))

        # 5. Concurrency
        conc_header = ctk.CTkFrame(self.controls_scroll, fg_color="transparent")
        conc_header.pack(fill="x", padx=6, pady=(4, 2))
        self.lbl_concurrency = ctk.CTkLabel(conc_header, text=I18nManager.t("concurrency_title"), font=ctk.CTkFont(weight="bold"))
        self.lbl_concurrency.pack(side="left")
        create_help_badge(conc_header, lambda: I18nManager.t("concurrency_tooltip")).pack(side="right")
        CTkToolTip(self.lbl_concurrency, lambda: I18nManager.t("concurrency_tooltip"))

        self.concurrency_slider = ctk.CTkSlider(self.controls_scroll, from_=1, to=50, number_of_steps=49)
        self.concurrency_slider.set(5)
        self.concurrency_slider.pack(fill="x", padx=6, pady=(0, 2))
        self.concurrency_label = ctk.CTkLabel(self.controls_scroll, text="🟢 5 Workers (안정)", text_color="#00ff7f")
        self.concurrency_label.pack(anchor="e", padx=6, pady=(0, 8))
        self.concurrency_slider.configure(command=self._on_concurrency_changed)

        # 6. Skip Already Checked Checkbox
        self.chk_skip_already = ctk.CTkCheckBox(
            self.controls_scroll,
            text=I18nManager.t("chk_skip_already"),
            font=ctk.CTkFont(size=11),
            checkbox_width=16,
            checkbox_height=16
        )
        self.chk_skip_already.select()
        self.chk_skip_already.pack(fill="x", padx=6, pady=(4, 6))
        CTkToolTip(self.chk_skip_already, lambda: I18nManager.t("chk_skip_already_tooltip"))

        # 7. Discord Webhook
        hook_header = ctk.CTkFrame(self.controls_scroll, fg_color="transparent")
        hook_header.pack(fill="x", padx=6, pady=(4, 2))
        self.lbl_webhook = ctk.CTkLabel(hook_header, text=I18nManager.t("webhook_title"), font=ctk.CTkFont(weight="bold"))
        self.lbl_webhook.pack(side="left")
        create_help_badge(hook_header, lambda: I18nManager.t("webhook_tooltip")).pack(side="right")
        CTkToolTip(self.lbl_webhook, lambda: I18nManager.t("webhook_tooltip"))

        self.webhook_entry = ctk.CTkEntry(self.controls_scroll, placeholder_text=I18nManager.t("webhook_placeholder"))
        if self.config.webhook.get("url"):
            self.webhook_entry.insert(0, self.config.webhook.get("url"))
        self.webhook_entry.pack(fill="x", padx=6, pady=(0, 15))

        # Start / Stop Button
        self.btn_toggle = ctk.CTkButton(
            self.sidebar,
            text=I18nManager.t("btn_start"),
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#00aa55",
            hover_color="#008844",
            command=self._on_toggle_run
        )
        self.btn_toggle.pack(fill="x", padx=12, pady=(8, 12))
        CTkToolTip(self.btn_toggle, lambda: I18nManager.t("btn_toggle_tooltip"))

        # ================= RIGHT CONTENT =================
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
        self.content.grid_rowconfigure(2, weight=3) # Discovered table
        self.content.grid_rowconfigure(4, weight=2) # Log console
        self.content.grid_columnconfigure(0, weight=1)

        # Row 0: Header Area (Top Bar + Collapsible Onboarding/Quick Guide Banner)
        self.header_area = ctk.CTkFrame(self.content, fg_color="transparent")
        self.header_area.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.top_bar = ctk.CTkFrame(self.header_area, fg_color="#1e1e24", height=45)
        self.top_bar.pack(fill="x", pady=(0, 4))

        self.status_badge = ctk.CTkLabel(
            self.top_bar,
            text=I18nManager.t("status_idle"),
            text_color="#888888",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.status_badge.pack(side="left", padx=(12, 4), pady=8)

        # Compact Proxy Badge (Positioned on the left next to status to prevent right-button clipping)
        self.node_badge = ctk.CTkLabel(
            self.top_bar,
            text=I18nManager.t("proxy_badge"),
            text_color="#00c8ff",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.node_badge.pack(side="left", padx=(4, 12), pady=8)

        # Language Switcher Button
        self.btn_lang = ctk.CTkButton(
            self.top_bar,
            text=I18nManager.t("lang_switch"),
            width=120,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#2b2b36",
            hover_color="#3a3a4a",
            command=self._toggle_language
        )
        self.btn_lang.pack(side="right", padx=(4, 10), pady=8)

        # Help & Guide Button
        self.btn_help = ctk.CTkButton(
            self.top_bar,
            text=I18nManager.t("help_btn"),
            width=115,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#0066cc",
            hover_color="#0055aa",
            command=self._open_help_modal
        )
        self.btn_help.pack(side="right", padx=4, pady=8)

        # Settings Modal Button
        self.btn_settings = ctk.CTkButton(
            self.top_bar,
            text=I18nManager.t("btn_settings"),
            width=140,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#3a3a4a",
            hover_color="#4a4a5c",
            command=self._open_settings_modal
        )
        self.btn_settings.pack(side="right", padx=4, pady=8)
        CTkToolTip(self.btn_settings, lambda: I18nManager.t("btn_settings_tooltip"))

        # Collapsible Quick Guide Banner (On-screen purpose & 3-step usage)
        self.guide_banner = ctk.CTkFrame(self.header_area, fg_color="#181822", corner_radius=6, border_width=1, border_color="#2b2b3a")
        self.guide_banner.pack(fill="x", pady=(0, 2))

        guide_top_row = ctk.CTkFrame(self.guide_banner, fg_color="transparent")
        guide_top_row.pack(fill="x", padx=10, pady=(6, 4))

        self.lbl_guide_title = ctk.CTkLabel(
            guide_top_row,
            text=I18nManager.t("guide_banner_title"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00c8ff"
        )
        self.lbl_guide_title.pack(side="left")

        self.btn_toggle_guide = ctk.CTkButton(
            guide_top_row,
            text=I18nManager.t("guide_banner_hide"),
            width=65,
            height=22,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#2b2b38",
            hover_color="#3a3a4c",
            command=self._toggle_guide_banner
        )
        self.btn_toggle_guide.pack(side="right")

        self.guide_body = ctk.CTkFrame(self.guide_banner, fg_color="transparent")
        self.guide_body.pack(fill="x", padx=12, pady=(0, 8))

        self.lbl_guide_text = ctk.CTkLabel(
            self.guide_body,
            text=I18nManager.t("guide_banner_content"),
            font=ctk.CTkFont(size=11),
            text_color="#cccccc",
            justify="left",
            wraplength=760
        )
        self.lbl_guide_text.pack(anchor="w")

        # Row 1: KPI Cards Frame (6 Cards: Total, RPS, Available, Taken, 429, Skipped)
        self.kpi_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.kpi_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for col in range(6):
            self.kpi_frame.grid_columnconfigure(col, weight=1)

        self.card_total_title, self.card_total = self._create_kpi_card(self.kpi_frame, 0, "kpi_total", "0", "#ffffff")
        self.card_rps_title, self.card_rps = self._create_kpi_card(self.kpi_frame, 1, "kpi_rps", "0.0 req/s", "#ffcc00")
        self.card_avail_title, self.card_avail = self._create_kpi_card(self.kpi_frame, 2, "kpi_avail", "0", "#00ff7f")
        self.card_taken_title, self.card_taken = self._create_kpi_card(self.kpi_frame, 3, "kpi_taken", "0", "#aaaaaa")
        self.card_429_title, self.card_429 = self._create_kpi_card(self.kpi_frame, 4, "kpi_429", "0", "#ff66cc")
        self.card_skip_title, self.card_skip = self._create_kpi_card(self.kpi_frame, 5, "kpi_skipped", "0", "#00c8ff")

        # Row 2: Discovered Usernames (Treeview table)
        self.table_frame = ctk.CTkFrame(self.content, fg_color="#18181c")
        self.table_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 8))

        table_header = ctk.CTkFrame(self.table_frame, fg_color="transparent", height=35)
        table_header.pack(fill="x", padx=10, pady=(8, 4))
        
        self.lbl_table_title = ctk.CTkLabel(
            table_header,
            text=I18nManager.t("table_title"),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00ff7f"
        )
        self.lbl_table_title.pack(side="left")

        # Initial count of auto-saved available usernames
        init_saved_count = 0
        avail_path = resolve_output_path("available.txt")
        if avail_path.exists():
            try:
                with open(avail_path, "r", encoding="utf-8") as f:
                    init_saved_count = len([line for line in f if line.strip()])
            except Exception:
                pass

        # Real-time Auto-save Indicator
        self.lbl_autosave_indicator = ctk.CTkLabel(
            table_header,
            text=I18nManager.t("auto_save_indicator", count=init_saved_count),
            font=ctk.CTkFont(size=11),
            text_color="#00c8ff"
        )
        self.lbl_autosave_indicator.pack(side="left", padx=(10, 6))

        # Open Results Folder Button
        self.btn_open_folder = ctk.CTkButton(
            table_header,
            text=I18nManager.t("btn_open_folder"),
            width=115,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#2b2b36",
            hover_color="#3a3a4a",
            command=self._open_results_folder
        )
        self.btn_open_folder.pack(side="left", padx=4)
        CTkToolTip(self.btn_open_folder, lambda: I18nManager.t("btn_open_folder_tooltip"))

        # Import History Button
        self.btn_load_history = ctk.CTkButton(
            table_header,
            text=I18nManager.t("btn_load_history"),
            width=145,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#2b2b36",
            hover_color="#3a3a4a",
            command=self._import_history_file
        )
        self.btn_load_history.pack(side="left", padx=4)
        CTkToolTip(self.btn_load_history, lambda: I18nManager.t("btn_load_history_tooltip"))

        # Open Registration Button
        self.btn_open_reg = ctk.CTkButton(
            table_header,
            text=I18nManager.t("btn_open_reg"),
            width=125,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#5865F2",
            hover_color="#4752C4",
            command=lambda: webbrowser.open("https://discord.com/register")
        )
        self.btn_open_reg.pack(side="right")
        CTkToolTip(self.btn_open_reg, lambda: I18nManager.t("btn_open_reg_tooltip"))

        # Export Available Usernames Button
        self.btn_export = ctk.CTkButton(
            table_header,
            text=I18nManager.t("btn_export_avail"),
            width=125,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#2b2b36",
            hover_color="#3a3a4a",
            command=self._export_discovered_usernames
        )
        self.btn_export.pack(side="right", padx=(0, 6))
        CTkToolTip(self.btn_export, lambda: I18nManager.t("btn_export_tooltip"))

        # Row 2.5: Real-Time Search & Multi-Filter Toolbar
        self.search_filter_bar = ctk.CTkFrame(self.table_frame, fg_color="#18181f", corner_radius=6)
        self.search_filter_bar.pack(fill="x", padx=8, pady=(0, 6))

        # 1. Search Query Entry
        self.search_entry = ctk.CTkEntry(
            self.search_filter_bar,
            placeholder_text=I18nManager.t("search_placeholder"),
            height=28,
            font=ctk.CTkFont(size=11)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=4)
        self.search_entry.bind("<KeyRelease>", self._on_search_query_changed)
        CTkToolTip(self.search_entry, lambda: I18nManager.t("search_tooltip"))

        # 2. Clear Search Button [✕]
        self.btn_clear_search = ctk.CTkButton(
            self.search_filter_bar,
            text="✕",
            width=26,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#2b2b36",
            hover_color="#3a3a4a",
            command=self._clear_search_entry
        )
        self.btn_clear_search.pack(side="left", padx=(0, 6), pady=4)
        CTkToolTip(self.btn_clear_search, lambda: I18nManager.t("btn_clear_search_tooltip"))

        # 3. Filter Length Menu
        self.filter_len_menu = ctk.CTkOptionMenu(
            self.search_filter_bar,
            values=[
                I18nManager.t("filter_len_all"),
                I18nManager.t("filter_len_3"),
                I18nManager.t("filter_len_4"),
                I18nManager.t("filter_len_5"),
                I18nManager.t("filter_len_6p")
            ],
            width=95,
            height=26,
            font=ctk.CTkFont(size=11),
            command=self._on_filter_changed
        )
        self.filter_len_menu.set(I18nManager.t("filter_len_all"))
        self.filter_len_menu.pack(side="left", padx=(0, 4), pady=4)
        CTkToolTip(self.filter_len_menu, lambda: I18nManager.t("filter_len_tooltip"))

        # 4. Filter Pattern/Type Menu
        self.filter_type_menu = ctk.CTkOptionMenu(
            self.search_filter_bar,
            values=[
                I18nManager.t("filter_type_all"),
                I18nManager.t("filter_type_dict"),
                I18nManager.t("filter_type_patt"),
                I18nManager.t("filter_type_num"),
                I18nManager.t("filter_type_dot"),
                I18nManager.t("filter_type_comb"),
                I18nManager.t("filter_type_custom")
            ],
            width=115,
            height=26,
            font=ctk.CTkFont(size=11),
            command=self._on_filter_changed
        )
        self.filter_type_menu.set(I18nManager.t("filter_type_all"))
        self.filter_type_menu.pack(side="left", padx=(0, 4), pady=4)
        CTkToolTip(self.filter_type_menu, lambda: I18nManager.t("filter_type_tooltip"))

        # 5. Filter Sort Menu
        self.filter_sort_menu = ctk.CTkOptionMenu(
            self.search_filter_bar,
            values=[
                I18nManager.t("filter_sort_latest"),
                I18nManager.t("filter_sort_alpha_asc"),
                I18nManager.t("filter_sort_alpha_desc"),
                I18nManager.t("filter_sort_latency_fast")
            ],
            width=110,
            height=26,
            font=ctk.CTkFont(size=11),
            command=self._on_filter_changed
        )
        self.filter_sort_menu.set(I18nManager.t("filter_sort_latest"))
        self.filter_sort_menu.pack(side="left", padx=(0, 6), pady=4)
        CTkToolTip(self.filter_sort_menu, lambda: I18nManager.t("filter_sort_tooltip"))

        # 6. Reset Filters Button [🔄]
        self.btn_reset_filters = ctk.CTkButton(
            self.search_filter_bar,
            text="🔄",
            width=28,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="#2b2b36",
            hover_color="#3a3a4a",
            command=self._reset_all_filters
        )
        self.btn_reset_filters.pack(side="left", padx=(0, 6), pady=4)
        CTkToolTip(self.btn_reset_filters, lambda: I18nManager.t("btn_reset_filters_tooltip"))

        # 7. Live Filtered / Total Count Badge
        self.lbl_table_filter_count = ctk.CTkLabel(
            self.search_filter_bar,
            text="0 / 0개",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00ff7f"
        )
        self.lbl_table_filter_count.pack(side="right", padx=(4, 8), pady=4)

        # Custom ttk style for Dark Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#202026",
            foreground="#ffffff",
            fieldbackground="#202026",
            rowheight=26,
            font=("Segoe UI", 10)
        )
        style.configure("Treeview.Heading", background="#2a2a34", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#0078d4")])

        cols = ("time", "username", "pattern", "latency", "server")
        table_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=0)
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_columnconfigure(1, weight=0)

        self.tree = ttk.Treeview(table_container, columns=cols, show="headings", height=5)
        self.tree.column("time", width=85, anchor="center")
        self.tree.column("username", width=140, anchor="center")
        self.tree.column("pattern", width=140, anchor="center")
        self.tree.column("latency", width=95, anchor="center")
        self.tree.column("server", width=260, anchor="w")

        self.tree_yscroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree_xscroll = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.tree_yscroll.set, xscrollcommand=self.tree_xscroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_yscroll.grid(row=0, column=1, sticky="ns", padx=(2, 0))
        self.tree_xscroll.grid(row=1, column=0, sticky="ew", pady=(2, 0))

        # Right-click context menu on treeview
        self.tree_menu = tk.Menu(self, tearoff=0, bg="#2b2b36", fg="#ffffff", activebackground="#0078d4", activeforeground="#ffffff")
        self.tree_menu.add_command(label=I18nManager.t("ctx_recheck_selected"), command=self._recheck_selected_username)
        self.tree_menu.add_command(label=I18nManager.t("ctx_recheck_all"), command=self._recheck_all_usernames)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label=I18nManager.t("ctx_copy_username"), command=self._copy_selected_username)
        self.tree_menu.add_command(label=I18nManager.t("ctx_copy_all"), command=self._copy_all_discovered)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label=I18nManager.t("ctx_export_file"), command=self._export_discovered_usernames)
        self.tree_menu.add_command(label=I18nManager.t("ctx_open_discord"), command=lambda: webbrowser.open("https://discord.com/register"))
        self.tree.bind("<Button-3>", self._show_tree_context_menu)

        # Row 3: Progress Bar & Dynamic Status Bar
        self.status_bar_frame = ctk.CTkFrame(self.content, fg_color="#1b1b20", height=48)
        self.status_bar_frame.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        self.status_bar_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(self.status_bar_frame, height=6, progress_color="#00c8ff", mode="indeterminate")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=12, pady=(6, 4))

        self.lbl_status_text = ctk.CTkLabel(
            self.status_bar_frame,
            text=I18nManager.t("status_bar_idle"),
            font=ctk.CTkFont(size=11),
            text_color="#bbbbbb"
        )
        self.lbl_status_text.pack(padx=12, pady=(0, 6), anchor="w")

        # Row 4: Event Log Console (Collapsible with Clear & Save & Multi-Filters)
        self.log_frame = ctk.CTkFrame(self.content, fg_color="#18181c")
        self.log_frame.grid(row=4, column=0, sticky="nsew", pady=0)

        # Log Header Row 1: Title + Action buttons (Clear, Save, Collapse)
        self.log_header = ctk.CTkFrame(self.log_frame, fg_color="transparent", height=32)
        self.log_header.pack(fill="x", padx=10, pady=(6, 2))

        self.lbl_log_title = ctk.CTkLabel(
            self.log_header,
            text=I18nManager.t("log_title"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        self.lbl_log_title.pack(side="left")

        # Collapse / Expand Button
        self.btn_toggle_log = ctk.CTkButton(
            self.log_header,
            text=I18nManager.t("btn_collapse_log"),
            width=110,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="#2b2b34",
            hover_color="#3a3a46",
            command=self._toggle_log_collapse
        )
        self.btn_toggle_log.pack(side="right", padx=(4, 0))
        CTkToolTip(self.btn_toggle_log, lambda: I18nManager.t("btn_toggle_log_tooltip"))

        # Save Log Button
        self.btn_save_log = ctk.CTkButton(
            self.log_header,
            text=I18nManager.t("btn_save_log"),
            width=110,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="#2b2b34",
            hover_color="#3a3a46",
            command=self._save_logs_to_file
        )
        self.btn_save_log.pack(side="right", padx=4)
        CTkToolTip(self.btn_save_log, lambda: I18nManager.t("btn_save_log_tooltip"))

        # Clear Log Button
        self.btn_clear_log = ctk.CTkButton(
            self.log_header,
            text=I18nManager.t("btn_clear_log"),
            width=90,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="#2b2b34",
            hover_color="#3a3a46",
            command=self._clear_logs
        )
        self.btn_clear_log.pack(side="right", padx=4)
        CTkToolTip(self.btn_clear_log, lambda: I18nManager.t("btn_clear_log_tooltip"))

        # Log Header Row 2: Structured Filter Toolbar
        self.filter_bar = ctk.CTkFrame(self.log_frame, fg_color="#131316", height=28)
        self.filter_bar.pack(fill="x", padx=8, pady=(0, 4))

        self.chk_worker = ctk.CTkCheckBox(
            self.filter_bar,
            text=I18nManager.t("log_filter_worker"),
            font=ctk.CTkFont(size=11),
            checkbox_width=16,
            checkbox_height=16,
            command=self._apply_log_filters
        )
        self.chk_worker.select()
        self.chk_worker.pack(side="left", padx=(8, 8), pady=3)
        CTkToolTip(self.chk_worker, lambda: I18nManager.t("log_filter_worker_tooltip"))

        self.chk_success = ctk.CTkCheckBox(
            self.filter_bar,
            text=I18nManager.t("log_filter_success"),
            font=ctk.CTkFont(size=11),
            checkbox_width=16,
            checkbox_height=16,
            command=self._apply_log_filters
        )
        self.chk_success.select()
        self.chk_success.pack(side="left", padx=8, pady=3)
        CTkToolTip(self.chk_success, lambda: I18nManager.t("log_filter_success_tooltip"))

        self.chk_proxy = ctk.CTkCheckBox(
            self.filter_bar,
            text=I18nManager.t("log_filter_proxy"),
            font=ctk.CTkFont(size=11),
            checkbox_width=16,
            checkbox_height=16,
            command=self._apply_log_filters
        )
        self.chk_proxy.select()
        self.chk_proxy.pack(side="left", padx=8, pady=3)
        CTkToolTip(self.chk_proxy, lambda: I18nManager.t("log_filter_proxy_tooltip"))

        self.chk_system = ctk.CTkCheckBox(
            self.filter_bar,
            text=I18nManager.t("log_filter_system"),
            font=ctk.CTkFont(size=11),
            checkbox_width=16,
            checkbox_height=16,
            command=self._apply_log_filters
        )
        self.chk_system.select()
        self.chk_system.pack(side="left", padx=8, pady=3)
        CTkToolTip(self.chk_system, lambda: I18nManager.t("log_filter_system_tooltip"))

        self.lbl_worker_select = ctk.CTkLabel(
            self.filter_bar,
            text=I18nManager.t("log_worker_select"),
            font=ctk.CTkFont(size=11),
            text_color="#999999"
        )
        self.lbl_worker_select.pack(side="left", padx=(12, 4), pady=3)

        self.worker_filter_menu = ctk.CTkOptionMenu(
            self.filter_bar,
            values=["전체 워커", "워커 1", "워커 2", "워커 3", "워커 4", "워커 5"],
            width=105,
            height=22,
            font=ctk.CTkFont(size=11),
            command=lambda _: self._apply_log_filters()
        )
        self.worker_filter_menu.pack(side="left", padx=(0, 6), pady=3)

        # Textbox Console
        self.log_box = ctk.CTkTextbox(self.log_frame, font=ctk.CTkFont(family="Consolas", size=11), fg_color="#121214")
        self.log_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Close protocol
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._update_mode_panel(self.mode_menu.get())

    def _trigger_hot_swap(self):
        """설정 변경 사항을 실행 중인 오케스트레이터에 즉시 핫스왑 반영"""
        self._apply_settings_to_config()
        self._update_custom_preview()
        if self.orchestrator and self.orchestrator.is_running:
            self.orchestrator.hot_swap_generator(self.config.target)

    def _update_mode_panel(self, mode_str: str):
        """탐색 모드에 맞춰 패널 타이틀, 배지, 설명, 컨트롤 노출 여부, 테두리 색상 및 미리보기를 동적 갱신"""
        mode_lower = mode_str.split()[0].lower()

        if "custom" in mode_lower or "mask" in mode_lower:
            mode_key = "custom"
            accent_color = "#00c8ff"
        elif "comb" in mode_lower or "비번" in mode_lower:
            mode_key = "comb"
            accent_color = "#39ff14"
        elif "recheck" in mode_lower or "재확인" in mode_lower or "verif" in mode_lower:
            mode_key = "recheck"
            accent_color = "#00e5ff"
        elif "num" in mode_lower:
            mode_key = "numeric"
            accent_color = "#ffaa00"
        elif "dict" in mode_lower:
            mode_key = "dict"
            accent_color = "#00ff7f"
        elif "patt" in mode_lower:
            mode_key = "pattern"
            accent_color = "#ff66cc"
        elif "perm" in mode_lower:
            mode_key = "perm"
            accent_color = "#aa88ff"
        elif "rand" in mode_lower:
            mode_key = "random"
            accent_color = "#00e5ff"
        else: # hybrid
            mode_key = "hybrid"
            accent_color = "#00c8ff"

        title_text = I18nManager.t(f"mode_title_{mode_key}") if mode_key != "recheck" else I18nManager.t("recheck_title")
        badge_text = I18nManager.t(f"mode_badge_{mode_key}") if mode_key != "recheck" else I18nManager.t("recheck_badge")
        desc_text = I18nManager.t(f"mode_desc_{mode_key}") if mode_key != "recheck" else ("기존에 발견된 닉네임들이 여전히 유효한지(AVAILABLE) 아니면 선점되었는지(TAKEN) 워커들이 순회 검증합니다." if self.current_lang == "ko" else "Verify whether previously discovered usernames are still AVAILABLE or have been TAKEN.")

        self.lbl_custom_title.configure(text=title_text, text_color=accent_color)
        self.lbl_custom_badge.configure(text=badge_text, text_color=accent_color)
        self.lbl_mode_desc.configure(text=desc_text)
        self.lbl_preview_title.configure(text_color=accent_color)
        self.custom_box.configure(border_width=1, border_color=accent_color)

        if mode_key == "custom":
            self.btn_reset_pattern.pack(side="right", padx=(4, 0))
            if hasattr(self, "recheck_controls_frame"):
                self.recheck_controls_frame.pack_forget()
            if hasattr(self, "comb_controls_frame"):
                self.comb_controls_frame.pack_forget()
            if hasattr(self, "perm_controls_frame"):
                self.perm_controls_frame.pack_forget()
            self.custom_controls_frame.pack(fill="x", padx=0, pady=(0, 4), before=self.preview_frame)
        elif mode_key == "recheck":
            self.btn_reset_pattern.pack_forget()
            self.custom_controls_frame.pack_forget()
            if hasattr(self, "comb_controls_frame"):
                self.comb_controls_frame.pack_forget()
            if hasattr(self, "perm_controls_frame"):
                self.perm_controls_frame.pack_forget()
            if hasattr(self, "recheck_controls_frame"):
                self.recheck_controls_frame.pack(fill="x", padx=0, pady=(0, 4), before=self.preview_frame)
                self._update_recheck_count_label()
        elif mode_key == "comb":
            self.btn_reset_pattern.pack_forget()
            self.custom_controls_frame.pack_forget()
            if hasattr(self, "recheck_controls_frame"):
                self.recheck_controls_frame.pack_forget()
            if hasattr(self, "perm_controls_frame"):
                self.perm_controls_frame.pack_forget()
            if hasattr(self, "comb_controls_frame"):
                self.comb_controls_frame.pack(fill="x", padx=0, pady=(0, 4), before=self.preview_frame)
        elif mode_key == "perm":
            self.btn_reset_pattern.pack_forget()
            self.custom_controls_frame.pack_forget()
            if hasattr(self, "recheck_controls_frame"):
                self.recheck_controls_frame.pack_forget()
            if hasattr(self, "comb_controls_frame"):
                self.comb_controls_frame.pack_forget()
            if hasattr(self, "perm_controls_frame"):
                self.perm_controls_frame.pack(fill="x", padx=0, pady=(0, 4), before=self.preview_frame)
                shard_val = self.perm_shard_menu.get() if hasattr(self, "perm_shard_menu") else ""
                if "직접" in shard_val or "Custom" in shard_val:
                    self.perm_custom_range_frame.pack(fill="x", padx=0, pady=(0, 4))
                else:
                    self.perm_custom_range_frame.pack_forget()
        else:
            self.btn_reset_pattern.pack_forget()
            self.custom_controls_frame.pack_forget()
            if hasattr(self, "recheck_controls_frame"):
                self.recheck_controls_frame.pack_forget()
            if hasattr(self, "comb_controls_frame"):
                self.comb_controls_frame.pack_forget()
            if hasattr(self, "perm_controls_frame"):
                self.perm_controls_frame.pack_forget()

        self._update_custom_preview()

    def _on_reset_custom_pattern(self):
        """커스텀 패턴 입력을 초기화하고 기본 하이브리드 모드로 복원"""
        self.prefix_entry.delete(0, "end")
        self.suffix_entry.delete(0, "end")
        self.mask_entry.delete(0, "end")
        self.middle_dot_menu.set(I18nManager.t("middle_dot_none"))
        hybrid_label = "Hybrid (사전+패턴+숫자+마스크)" if self.current_lang == "ko" else "Hybrid (Dict+Patt+Num+Mask)"
        self.mode_menu.set(hybrid_label)
        self._update_mode_panel(hybrid_label)
        self._trigger_hot_swap()

    def _update_custom_preview(self):
        """실시간 탐색 모드별 생성 템플릿 및 예시 닉네임 시각화"""
        try:
            mode_val = self.mode_menu.get().split()[0].lower()
            length = int(self.length_menu.get())

            pre = self.prefix_entry.get().strip()
            suf = self.suffix_entry.get().strip()
            msk = self.mask_entry.get().strip()
            dot_sel = self.middle_dot_menu.get()
            dot = "required" if ("필수" in dot_sel or "Required" in dot_sel) else ("optional" if ("선택" in dot_sel or "Optional" in dot_sel or "허용" in dot_sel) else "none")

            if "custom" in mode_val or "mask" in mode_val:
                gen = MaskPatternGenerator(length=length, prefix=pre, suffix=suf, middle_dot=dot, mask=msk)
                mask_template = gen._resolve_mask()
                samples = [gen.next_username() for _ in range(4)]
                samples = [s for s in samples if s]
                sample_str = ", ".join(samples) if samples else "생성 대기 중"
                self.lbl_preview_text.configure(
                    text=f"템플릿: {mask_template} ({len(mask_template)}자)\n예시: {sample_str}",
                    text_color="#00c8ff"
                )
            elif "recheck" in mode_val or "재확인" in mode_val or "verif" in mode_val:
                targets = self._get_recheck_targets()
                rng = self.recheck_range_menu.get() if hasattr(self, "recheck_range_menu") else "All"
                sample_str = ", ".join(targets[:4]) if targets else ("재확인 목록 없음" if self.current_lang == "ko" else "Empty")
                self.lbl_preview_text.configure(
                    text=f"모드: 기존 발견 닉네임 재확인 ({len(targets)}개 대상)\n범위: {rng}\n예시: {sample_str}",
                    text_color="#00e5ff"
                )
            elif "num" in mode_val:
                gen = NumericGenerator(length=length)
                samples = [gen.next_username() for _ in range(4)]
                samples = [s for s in samples if s]
                self.lbl_preview_text.configure(
                    text=f"모드: 0~9 순수 숫자닉 ({length}자리)\n예시: {', '.join(samples)}",
                    text_color="#ffaa00"
                )
            elif "dict" in mode_val:
                gen = DictionaryGenerator(length=length)
                samples = [gen.next_username() for _ in range(4)]
                samples = [s for s in samples if s]
                self.lbl_preview_text.configure(
                    text=f"모드: 사전 및 발음형 음절 ({length}자)\n예시: {', '.join(samples)}",
                    text_color="#00ff7f"
                )
            elif "patt" in mode_val:
                gen = PatternGenerator(length=length)
                samples = [gen.next_username() for _ in range(4)]
                samples = [s for s in samples if s]
                self.lbl_preview_text.configure(
                    text=f"모드: 대칭 및 반복 패턴 ({length}자)\n예시: {', '.join(samples)}",
                    text_color="#ff66cc"
                )
            elif "perm" in mode_val:
                shard_choice = self.perm_shard_menu.get() if hasattr(self, "perm_shard_menu") else "전체 탐색 (분할 없음)"
                shard_k = "none"
                start_c = None
                end_c = None
                for k, v in SHARD_PRESETS.items():
                    if v["label"] == shard_choice:
                        shard_k = k
                        start_c = v["start"]
                        end_c = v["end"]
                        break
                if "직접" in shard_choice or "Custom" in shard_choice:
                    start_c = self.perm_start_menu.get() if hasattr(self, "perm_start_menu") else "a"
                    end_c = self.perm_end_menu.get() if hasattr(self, "perm_end_menu") else "m"
                    shard_k = None

                gen = PermutationGenerator(length=length, start_char=start_c, end_char=end_c, shard_key=shard_k)
                samples = [gen.next_username() for _ in range(4)]
                samples = [s for s in samples if s]
                first_cnt = len(gen.first_chars)
                total_est = first_cnt * (38 ** (length - 1)) if length > 1 else first_cnt
                self.lbl_preview_text.configure(
                    text=f"모드: 전수순열 분할 ({length}자)\n샤딩: {shard_choice} (약 {total_est:,}개)\n예시: {', '.join(samples)} ...",
                    text_color="#aa88ff"
                )
            elif "comb" in mode_val or "비번" in mode_val:
                dir_sel = self.comb_direction_menu.get() if hasattr(self, "comb_direction_menu") else "오름차순"
                direction = "desc" if ("내림차순" in dir_sel or "Descending" in dir_sel) else "asc"
                cs_sel = self.comb_charset_menu.get() if hasattr(self, "comb_charset_menu") else "숫자 우선"
                charset_type = "alphanumeric_alpha_first" if ("영문 우선" in cs_sel or "Letters First" in cs_sel) else "alphanumeric_num_first"

                gen = CombinatorialGenerator(length=length, charset_type=charset_type, direction=direction)
                total_comb = gen.total_combinations
                samples = [gen.next_username() for _ in range(4)]
                samples = [s for s in samples if s]
                dir_label = "오름차순 (Asc)" if direction == "asc" else "내림차순 (Desc)"
                cs_label = "0-9 ➔ a-z" if "num_first" in charset_type else "a-z ➔ 0-9"
                self.lbl_preview_text.configure(
                    text=f"모드: 영숫자 전수조사 (총 {total_comb:,}개)\n방향: {dir_label} [{cs_label}]\n예시: {', '.join(samples)} ...",
                    text_color="#39ff14"
                )
            elif "rand" in mode_val:
                gen = RandomGenerator(length=length)
                samples = [gen.next_username() for _ in range(4)]
                samples = [s for s in samples if s]
                self.lbl_preview_text.configure(
                    text=f"모드: 고속 무작위 영숫자 ({length}자)\n예시: {', '.join(samples)}",
                    text_color="#00e5ff"
                )
            else: # hybrid
                gen = HybridGenerator(length=length, prefix=pre, suffix=suf, middle_dot=dot, mask=msk)
                samples = [gen.next_username() for _ in range(4)]
                samples = [s for s in samples if s]
                self.lbl_preview_text.configure(
                    text=f"모드: 하이브리드 스마트 복합 ({length}자)\n예시: {', '.join(samples)}",
                    text_color="#00c8ff"
                )
        except Exception as e:
            self.lbl_preview_text.configure(text=f"미리보기 오류: {e}", text_color="#ff6666")

    def _on_recheck_range_changed(self, choice: str):
        self._update_recheck_count_label()
        self._update_custom_preview()

    def _update_recheck_count_label(self):
        if hasattr(self, "lbl_recheck_count"):
            targets = self._get_recheck_targets()
            self.lbl_recheck_count.configure(
                text=f"재확인 대상: {len(targets)}개 선택됨" if self.current_lang == "ko" else f"Re-check pool: {len(targets)} selected"
            )

    def _get_recheck_targets(self) -> List[str]:
        all_names = []
        if hasattr(self, "tree"):
            for c in self.tree.get_children():
                vals = self.tree.item(c)["values"]
                if len(vals) > 1 and vals[1]:
                    all_names.append(str(vals[1]).strip().lower())

        if not all_names:
            try:
                avail_path = resolve_output_path("available.txt")
                if avail_path.exists():
                    all_names = StorageManager.load_usernames_from_file(avail_path)
            except Exception:
                pass

        if not hasattr(self, "recheck_range_menu"):
            return all_names

        rng = self.recheck_range_menu.get()
        if "1 ~ 50" in rng or "1_50" in rng or "Part 1" in rng:
            return all_names[:50]
        elif "51 ~ 100" in rng or "51_100" in rng or "Part 2" in rng:
            return all_names[50:100]
        elif "101 ~ 200" in rng or "101_200" in rng or "Part 3" in rng:
            return all_names[100:200]
        elif "선택" in rng or "Selected" in rng:
            sel = self.tree.selection()
            if sel:
                sel_names = []
                for s in sel:
                    vals = self.tree.item(s)["values"]
                    if len(vals) > 1 and vals[1]:
                        sel_names.append(str(vals[1]).strip().lower())
                return sel_names
            return all_names
        return all_names

    def _on_search_query_changed(self, event=None):
        self._refresh_discovered_table()

    def _clear_search_entry(self):
        if hasattr(self, "search_entry"):
            self.search_entry.delete(0, "end")
            self._refresh_discovered_table()

    def _on_filter_changed(self, choice=None):
        self._refresh_discovered_table()

    def _reset_all_filters(self):
        if hasattr(self, "search_entry"):
            self.search_entry.delete(0, "end")
        if hasattr(self, "filter_len_menu"):
            self.filter_len_menu.set(I18nManager.t("filter_len_all"))
        if hasattr(self, "filter_type_menu"):
            self.filter_type_menu.set(I18nManager.t("filter_type_all"))
        if hasattr(self, "filter_sort_menu"):
            self.filter_sort_menu.set(I18nManager.t("filter_sort_latest"))
        self._refresh_discovered_table()

    def _refresh_discovered_table(self):
        """마스터 인메모리 캐시(discovered_items)에서 검색어, 글자수, 유형 필터 및 정렬을 적용하여 LIVE 테이블 렌더링"""
        query = self.search_entry.get().strip().lower() if hasattr(self, "search_entry") else ""
        len_choice = self.filter_len_menu.get() if hasattr(self, "filter_len_menu") else ""
        type_choice = self.filter_type_menu.get() if hasattr(self, "filter_type_menu") else ""
        sort_choice = self.filter_sort_menu.get() if hasattr(self, "filter_sort_menu") else ""

        # 1. Filter items
        filtered = []
        for item in self.discovered_items:
            uname = str(item.get("username", "")).lower()
            patt = str(item.get("pattern", "")).lower()

            # (1) Text query match (supports wildcard * and ? or substring)
            if query:
                if "*" in query or "?" in query:
                    if not fnmatch.fnmatch(uname, query) and not fnmatch.fnmatch(patt, query):
                        continue
                else:
                    if query not in uname and query not in patt:
                        continue

            # (2) Length match
            l = item.get("length", len(uname))
            if "3" in len_choice and l != 3:
                continue
            elif "4" in len_choice and l != 4:
                continue
            elif "5" in len_choice and l != 5:
                continue
            elif ("6" in len_choice or "6+" in len_choice) and l < 6:
                continue

            # (3) Pattern / Type match
            if "사전" in type_choice or "Dict" in type_choice:
                if not any(k in patt for k in ("dict", "word", "cvcv")):
                    continue
            elif "대칭" in type_choice or "패턴" in type_choice or "Patt" in type_choice:
                if not any(k in patt for k in ("patt", "abba", "aabb", "abab", "symm")):
                    continue
            elif "숫자" in type_choice or "Numeric" in type_choice:
                if not ("num" in patt or uname.isdigit()):
                    continue
            elif "점" in type_choice or "Dot" in type_choice:
                if "." not in uname:
                    continue
            elif "조합" in type_choice or "Comb" in type_choice:
                if "comb" not in patt:
                    continue
            elif "커스텀" in type_choice or "Custom" in type_choice:
                if "mask" not in patt and "custom" not in patt:
                    continue

            filtered.append(item)

        # 2. Sort items
        if "A-Z" in sort_choice:
            filtered.sort(key=lambda x: str(x.get("username", "")).lower())
        elif "Z-A" in sort_choice:
            filtered.sort(key=lambda x: str(x.get("username", "")).lower(), reverse=True)
        elif "빠른순" in sort_choice or "Fast" in sort_choice:
            filtered.sort(key=lambda x: x.get("latency_val", 9999.0))
        # Default is latest (insertion order preserved)

        # 3. Render into self.tree
        if hasattr(self, "tree"):
            self.tree.delete(*self.tree.get_children())
            for it in filtered:
                self.tree.insert("", "end", values=(
                    it.get("time", ""),
                    it.get("username", ""),
                    it.get("pattern", ""),
                    it.get("latency", ""),
                    it.get("server", "")
                ))

        # 4. Update count badge
        total_cnt = len(self.discovered_items)
        filt_cnt = len(filtered)
        if hasattr(self, "lbl_table_filter_count"):
            if filt_cnt < total_cnt:
                self.lbl_table_filter_count.configure(
                    text=f"필터: {filt_cnt:,} / {total_cnt:,}개" if self.current_lang == "ko" else f"Filtered: {filt_cnt:,} / {total_cnt:,}",
                    text_color="#00e5ff"
                )
            else:
                self.lbl_table_filter_count.configure(
                    text=f"전체: {total_cnt:,}개" if self.current_lang == "ko" else f"Total: {total_cnt:,}",
                    text_color="#00ff7f"
                )

    def _restore_discovered_table(self):
        """프로그램 시작 시 과거 발견된 닉네임 목록을 SQLite DB 및 결과 파일에서 불러와 LIVE 테이블에 자동 복원"""
        try:
            storage = StorageManager(
                db_path=self.config.storage.get("db_path", "data/d4uc_results.db"),
                available_file=self.config.storage.get("available_file", "available.txt"),
                taken_file=self.config.storage.get("taken_file", "taken.txt")
            )
            self._local_storage = storage
            self._last_available_rowid = storage.get_max_rowid()
            self._last_available_sync_time = time.time()
            records = storage.get_discovered_available_records()
            existing = set()
            self.discovered_items.clear()
            for r in records:
                u = r.get("username", "").strip()
                if not u or u.lower() in existing:
                    continue
                existing.add(u.lower())
                lat_str = str(r.get("latency", "0.0ms"))
                lat_val = 0.0
                try:
                    lat_val = float(lat_str.replace("ms", "").strip())
                except Exception:
                    pass
                self.discovered_items.append({
                    "time": r.get("time", "Saved"),
                    "username": u,
                    "pattern": r.get("pattern", "restored"),
                    "latency": lat_str,
                    "server": r.get("server", "Saved"),
                    "latency_val": lat_val,
                    "length": len(u)
                })

            self._refresh_discovered_table()
            total_restored = len(self.discovered_items)
            self.lbl_autosave_indicator.configure(text=I18nManager.t("auto_save_indicator", count=total_restored))
            self.card_avail.configure(text=str(total_restored))
            self._update_recheck_count_label()
        except Exception:
            pass

    def _import_history_file(self):
        """외부 .txt, .csv, .json 파일에서 닉네임 목록을 불러와 LIVE 테이블에 등록하고 재확인 준비"""
        filepath = filedialog.askopenfilename(
            title="이전 닉네임 파일 불러오기" if self.current_lang == "ko" else "Import Usernames File",
            filetypes=[
                ("Supported files (*.txt;*.csv;*.json)", "*.txt;*.csv;*.json"),
                ("Text files (*.txt)", "*.txt"),
                ("CSV files (*.csv)", "*.csv"),
                ("JSON files (*.json)", "*.json"),
                ("All files (*.*)", "*.*")
            ],
            parent=self
        )
        if not filepath:
            return

        try:
            usernames = StorageManager.load_usernames_from_file(Path(filepath))
            if not usernames:
                messagebox.showinfo("Import", "불러올 유효한 닉네임이 파일에 없습니다." if self.current_lang == "ko" else "No valid usernames found in file.", parent=self)
                return

            existing = set(str(it["username"]).strip().lower() for it in self.discovered_items)
            added_count = 0
            ts_now = datetime.now().strftime("%H:%M:%S")
            for u in usernames:
                if u.lower() not in existing:
                    self.discovered_items.insert(0, {
                        "time": ts_now,
                        "username": u,
                        "pattern": "imported",
                        "latency": "0.0ms",
                        "server": f"File: {Path(filepath).name}",
                        "latency_val": 0.0,
                        "length": len(u)
                    })
                    existing.add(u.lower())
                    added_count += 1

            self._refresh_discovered_table()
            total_cnt = len(self.discovered_items)
            self.lbl_autosave_indicator.configure(text=I18nManager.t("auto_save_indicator", count=total_cnt))
            self.card_avail.configure(text=str(total_cnt))

            # Switch to Re-check mode automatically
            recheck_label = "Re-check (기존 닉네임 재확인)" if self.current_lang == "ko" else "Re-check (Verified List)"
            self.mode_menu.set(recheck_label)
            self._update_mode_panel(recheck_label)
            self._update_recheck_count_label()

            msg = f"닉네임 {added_count}개를 성공적으로 추가했습니다 (전체: {total_cnt}개).\n재확인(Re-check) 모드로 자동 전환되었습니다." if self.current_lang == "ko" else f"Successfully imported {added_count} usernames (Total: {total_cnt}).\nSwitched to Re-check mode."
            messagebox.showinfo("Import Success", msg, parent=self)
            self._append_log(f"📂 [IMPORT] {Path(filepath).name} -> {added_count}개 신규 로드 (누적 {total_cnt}개)", "SYSTEM")
        except Exception as e:
            messagebox.showerror("Import Error", f"파일 불러오기 실패:\n{e}", parent=self)

    def _recheck_selected_username(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Re-check", "재확인할 닉네임을 테이블에서 선택하세요." if self.current_lang == "ko" else "Please select a username row from the table.", parent=self)
            return
        recheck_label = "Re-check (기존 닉네임 재확인)" if self.current_lang == "ko" else "Re-check (Verified List)"
        self.mode_menu.set(recheck_label)
        self._update_mode_panel(recheck_label)
        if hasattr(self, "recheck_range_menu"):
            self.recheck_range_menu.set(I18nManager.t("recheck_range_custom"))
        self._update_recheck_count_label()
        if not self.orchestrator or not self.orchestrator.is_running:
            self._on_toggle_run()

    def _recheck_all_usernames(self):
        children = self.tree.get_children()
        if not children:
            messagebox.showinfo("Re-check", "재확인할 닉네임이 테이블에 없습니다." if self.current_lang == "ko" else "No usernames in table to re-check.", parent=self)
            return
        recheck_label = "Re-check (기존 닉네임 재확인)" if self.current_lang == "ko" else "Re-check (Verified List)"
        self.mode_menu.set(recheck_label)
        self._update_mode_panel(recheck_label)
        if hasattr(self, "recheck_range_menu"):
            self.recheck_range_menu.set(I18nManager.t("recheck_range_all"))
        self._update_recheck_count_label()
        if not self.orchestrator or not self.orchestrator.is_running:
            self._on_toggle_run()

    def _on_recheck_item_result(self, username: str, is_available: bool, latency_str: str, server_str: str):
        def _ui():
            u_low = username.strip().lower()
            ts_now = datetime.now().strftime("%H:%M:%S")
            stat_str = "AVAILABLE (재확인완료)" if is_available else "TAKEN (선점됨)"
            lat_val = 0.0
            try:
                lat_val = float(str(latency_str).replace("ms", "").strip())
            except Exception:
                pass

            found = False
            for it in self.discovered_items:
                if str(it.get("username", "")).lower() == u_low:
                    it["time"] = ts_now
                    it["pattern"] = stat_str
                    it["latency"] = latency_str
                    it["server"] = server_str
                    it["latency_val"] = lat_val
                    found = True
                    break
            if not found:
                self.discovered_items.insert(0, {
                    "time": ts_now,
                    "username": username,
                    "pattern": stat_str,
                    "latency": latency_str,
                    "server": server_str,
                    "latency_val": lat_val,
                    "length": len(username)
                })
            self._refresh_discovered_table()
        self.after(0, _ui)

    def _save_ui_to_config(self):
        try:
            self._apply_settings_to_config()
            self.config.ui["last_mode"] = self.mode_menu.get()
            self.config.ui["last_length"] = int(self.length_menu.get())
            self.config.ui["last_proxy"] = self.proxy_menu.get()
            self.config.ui["last_country"] = self.country_menu.get()
            self.config.ui["last_concurrency"] = int(self.concurrency_slider.get())
            self.config.ui["last_skip_already"] = bool(self.chk_skip_already.get())
            self.config.ui["last_prefix"] = self.prefix_entry.get().strip()
            self.config.ui["last_suffix"] = self.suffix_entry.get().strip()
            self.config.ui["last_mask"] = self.mask_entry.get().strip()
            self.config.ui["last_middle_dot"] = self.middle_dot_menu.get()
            self.config.ui["last_webhook"] = self.webhook_entry.get().strip()
            self.config.ui["last_lang"] = self.current_lang
            if hasattr(self, "recheck_range_menu"):
                self.config.ui["last_recheck_range"] = self.recheck_range_menu.get()
            if hasattr(self, "comb_direction_menu"):
                self.config.ui["last_comb_direction"] = self.comb_direction_menu.get()
            if hasattr(self, "comb_charset_menu"):
                self.config.ui["last_comb_charset"] = self.comb_charset_menu.get()
            if hasattr(self, "filter_sort_menu"):
                self.config.ui["last_discovered_sort"] = self.filter_sort_menu.get()
            self.config.save()
        except Exception:
            pass

    def _load_ui_from_config(self):
        try:
            # 1. Restore mode
            saved_mode = self.config.ui.get("last_mode") or self.config.target.get("mode")
            if saved_mode:
                for val in self.mode_menu.cget("values"):
                    if saved_mode.lower() in val.lower() or val.lower().startswith(saved_mode.lower()):
                        self.mode_menu.set(val)
                        self._update_mode_panel(val)
                        break
            # 2. Restore length
            saved_len = str(self.config.ui.get("last_length") or self.config.target.get("length", 4))
            if saved_len in ("3", "4", "5", "6"):
                self.length_menu.set(saved_len)
            # 3. Restore custom pattern
            saved_pre = self.config.ui.get("last_prefix") or self.config.target.get("prefix", "")
            if saved_pre:
                self.prefix_entry.delete(0, "end")
                self.prefix_entry.insert(0, saved_pre)
            saved_suf = self.config.ui.get("last_suffix") or self.config.target.get("suffix", "")
            if saved_suf:
                self.suffix_entry.delete(0, "end")
                self.suffix_entry.insert(0, saved_suf)
            saved_mask = self.config.ui.get("last_mask") or self.config.target.get("mask", "")
            if saved_mask:
                self.mask_entry.delete(0, "end")
                self.mask_entry.insert(0, saved_mask)
            saved_dot = self.config.ui.get("last_middle_dot")
            if saved_dot:
                for val in self.middle_dot_menu.cget("values"):
                    if saved_dot in val:
                        self.middle_dot_menu.set(val)
                        break
            # 4. Restore proxy & country
            saved_proxy = self.config.ui.get("last_proxy")
            if saved_proxy:
                for val in self.proxy_menu.cget("values"):
                    if saved_proxy.split()[0].lower() in val.lower():
                        self.proxy_menu.set(val)
                        break
            saved_country = self.config.ui.get("last_country") or self.config.proxy.get("surfshark", {}).get("preferred_country_label")
            if saved_country:
                for val in self.country_menu.cget("values"):
                    if saved_country in val or ("142" in saved_country and "142" in val):
                        self.country_menu.set(val)
                        break
            # 5. Restore concurrency
            saved_conc = self.config.ui.get("last_concurrency") or self.config.network.get("concurrency", 5)
            self.concurrency_slider.set(int(saved_conc))
            self._on_concurrency_changed(saved_conc)
            # 6. Restore skip already
            saved_skip = self.config.ui.get("last_skip_already")
            if saved_skip is not None:
                if saved_skip:
                    self.chk_skip_already.select()
                else:
                    self.chk_skip_already.deselect()
            # 7. Restore webhook
            saved_hook = self.config.ui.get("last_webhook") or self.config.webhook.get("url", "")
            if saved_hook:
                self.webhook_entry.delete(0, "end")
                self.webhook_entry.insert(0, saved_hook)
            # 8. Restore combinatorial options
            if hasattr(self, "comb_direction_menu"):
                saved_cdir = self.config.ui.get("last_comb_direction")
                if saved_cdir:
                    for val in self.comb_direction_menu.cget("values"):
                        if saved_cdir.split()[0].lower() in val.lower():
                            self.comb_direction_menu.set(val)
                            break
            if hasattr(self, "comb_charset_menu"):
                saved_cset = self.config.ui.get("last_comb_charset")
                if saved_cset:
                    for val in self.comb_charset_menu.cget("values"):
                        if saved_cset.split()[0].lower() in val.lower():
                            self.comb_charset_menu.set(val)
                            break
            # 9. Restore discovered sort
            if hasattr(self, "filter_sort_menu"):
                saved_sort = self.config.ui.get("last_discovered_sort")
                if saved_sort:
                    for val in self.filter_sort_menu.cget("values"):
                        if saved_sort.split()[0].lower() in val.lower() or val.lower().startswith(saved_sort.lower()[:3]):
                            self.filter_sort_menu.set(val)
                            break
        except Exception:
            pass

    def _on_mode_changed(self, choice: str):
        self._update_mode_panel(choice)
        self._trigger_hot_swap()

    def _on_length_changed(self, choice: str):
        self._trigger_hot_swap()

    def _on_comb_param_changed(self, choice: str = ""):
        comb_label = "Combinatorial (비번형 영숫자 0~z 조합)" if self.current_lang == "ko" else "Combinatorial (0-z Brute-force)"
        self.mode_menu.set(comb_label)
        self._update_mode_panel(comb_label)
        self._trigger_hot_swap()

    def _on_perm_param_changed(self, choice: str = ""):
        perm_label = "Permutation (전수순열)" if self.current_lang == "ko" else "Permutation (Full)"
        self.mode_menu.set(perm_label)
        self._update_mode_panel(perm_label)
        self._trigger_hot_swap()

    def _on_middle_dot_changed(self, choice: str):
        custom_label = "Custom Mask (커스텀 패턴)" if self.current_lang == "ko" else "Custom Mask (Pattern)"
        self.mode_menu.set(custom_label)
        self._update_mode_panel(custom_label)
        self._trigger_hot_swap()

    def _on_custom_pattern_input_changed(self, event=None):
        custom_label = "Custom Mask (커스텀 패턴)" if self.current_lang == "ko" else "Custom Mask (Pattern)"
        self.mode_menu.set(custom_label)
        self._update_mode_panel(custom_label)
        self._trigger_hot_swap()

    def _show_tree_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.tree_menu.post(event.x_root, event.y_root)

    def _copy_selected_username(self):
        sel = self.tree.selection()
        if sel:
            username = self.tree.item(sel[0])["values"][1]
            self.clipboard_clear()
            self.clipboard_append(str(username))
            messagebox.showinfo("Clipboard", f"'{username}' 클립보드 복사 완료" if self.current_lang == "ko" else f"Copied '{username}' to clipboard", parent=self)

    def _copy_all_discovered(self):
        children = self.tree.get_children()
        if not children:
            return
        names = [str(self.tree.item(c)["values"][1]) for c in children]
        text = "\n".join(names)
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Clipboard", f"총 {len(names)}개 닉네임 목록 복사 완료" if self.current_lang == "ko" else f"Copied {len(names)} usernames to clipboard", parent=self)

    def _export_discovered_usernames(self):
        total_count = len(self.discovered_items)
        visible_children = self.tree.get_children()
        visible_count = len(visible_children)

        if not self.discovered_items and not visible_children:
            messagebox.showinfo("Info", I18nManager.t("no_usernames_to_export"), parent=self)
            return

        export_filtered_only = True
        if visible_count < total_count and visible_count > 0:
            title = I18nManager.t("export_filter_dialog_title")
            msg = I18nManager.t("export_filter_dialog_msg", filtered=visible_count, total=total_count)
            res = messagebox.askyesnocancel(title, msg, parent=self)
            if res is None:
                return
            export_filtered_only = res

        if export_filtered_only:
            rows = [self.tree.item(c)["values"] for c in visible_children]
        else:
            rows = [
                (it["time"], it["username"], it["pattern"], it["latency"], it["server"])
                for it in self.discovered_items
            ]

        if not rows:
            messagebox.showinfo("Info", I18nManager.t("no_usernames_to_export"), parent=self)
            return

        ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"d4uc_available_{ts_str}.txt"
        default_dir = resolve_output_path("")

        filepath = filedialog.asksaveasfilename(
            initialdir=str(default_dir),
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[
                ("Text files (*.txt)", "*.txt"),
                ("CSV files (*.csv)", "*.csv"),
                ("JSON files (*.json)", "*.json"),
                ("All files (*.*)", "*.*")
            ],
            parent=self
        )
        if not filepath:
            return

        try:
            p = Path(filepath)
            if p.suffix.lower() == ".csv":
                with open(p, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["time", "username", "pattern", "latency", "server"])
                    writer.writerows(rows)
            elif p.suffix.lower() == ".json":
                data = [
                    {"time": r[0], "username": r[1], "pattern": r[2], "latency": r[3], "server": r[4]}
                    for r in rows
                ]
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else: # .txt
                with open(p, "w", encoding="utf-8") as f:
                    for r in rows:
                        f.write(f"{r[1]}\n")

            msg = I18nManager.t("export_success_msg", count=len(rows), path=str(p.resolve()))
            messagebox.showinfo("Success", msg, parent=self)
            self._append_log(f"💾 [EXPORT] {msg}", "SYSTEM")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}", parent=self)

    def _open_results_folder(self):
        try:
            folder = resolve_output_path("results")
            folder.mkdir(parents=True, exist_ok=True)
            os.startfile(str(folder))
        except Exception as e:
            err_msg = f"저장 폴더를 여는 중 오류가 발생했습니다:\n{e}" if self.current_lang == "ko" else f"Failed to open results folder:\n{e}"
            messagebox.showerror("Error", err_msg, parent=self)

    def _open_settings_modal(self):
        win = ctk.CTkToplevel(self)
        win.title(I18nManager.t("settings_modal_title"))
        win.geometry("640x540")
        win.minsize(560, 460)
        win.attributes("-topmost", True)

        header = ctk.CTkFrame(win, fg_color="#1e1e24", height=45)
        header.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(
            header,
            text=I18nManager.t("settings_modal_title"),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00c8ff"
        ).pack(side="left", padx=15, pady=8)

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=12, pady=5)

        # Current values
        surf_cfg = self.config.proxy.get("surfshark", {})
        cur_keys_list = surf_cfg.get("wireguard_keys")
        if not cur_keys_list:
            try:
                creds_p = Path("data/surfshark_credentials.json")
                if not creds_p.exists():
                    creds_p = Path(__file__).parent / "data" / "surfshark_credentials.json"
                if creds_p.exists():
                    with open(creds_p, "r", encoding="utf-8") as f:
                        cdat = json.load(f)
                        raw_k = cdat.get("wireguard_keys")
                        if isinstance(raw_k, list) and raw_k:
                            cur_keys_list = [str(k).strip() for k in raw_k if str(k).strip()]
            except Exception:
                pass
        if not cur_keys_list:
            single_k = surf_cfg.get("private_key", "YOUR_WIREGUARD_PRIVATE_KEY_HERE")
            cur_keys_list = [k.strip() for k in str(single_k).replace(",", "\n").splitlines() if k.strip()]
        cur_wg_text = "\n".join(cur_keys_list)
        cur_ovpn_user = surf_cfg.get("username", "YOUR_OPENVPN_USERNAME_HERE")
        cur_ovpn_pass = surf_cfg.get("password", "YOUR_OPENVPN_PASSWORD_HERE")
        cur_http_port = str(surf_cfg.get("http_port", 1081))
        cur_socks5_port = str(surf_cfg.get("socks5_port", 1080))
        cur_warmup = str(surf_cfg.get("warmup_delay", 1.0))

        # WireGuard Private Key(s) (Multi-Account Support)
        ctk.CTkLabel(scroll, text=I18nManager.t("sett_wg_key"), font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=6, pady=(6, 2))
        lbl_key_help = ctk.CTkLabel(
            scroll,
            text=I18nManager.t("sett_wg_key_tooltip"),
            text_color="#00e5ff",
            font=ctk.CTkFont(size=10),
            wraplength=480,
            justify="left"
        )
        lbl_key_help.pack(anchor="w", padx=6, pady=(0, 4))

        entry_wg = ctk.CTkTextbox(scroll, height=75, font=ctk.CTkFont(family="Consolas", size=11))
        entry_wg.insert("1.0", cur_wg_text)
        entry_wg.pack(fill="x", padx=6, pady=(0, 4))

        lbl_key_count = ctk.CTkLabel(
            scroll,
            text=I18nManager.t("sett_wg_key_count", count=len(cur_keys_list)),
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00ff7f"
        )
        lbl_key_count.pack(anchor="w", padx=6, pady=(0, 4))

        btn_launch_surf = ctk.CTkButton(
            scroll,
            text=I18nManager.t("sett_btn_open_surfshark"),
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#1f538d",
            hover_color="#163e69",
            command=self._launch_surfshark_login_browser
        )
        btn_launch_surf.pack(fill="x", padx=6, pady=(0, 6))
        CTkToolTip(btn_launch_surf, lambda: I18nManager.t("sett_btn_open_surfshark_tooltip"))

        def _on_keys_text_changed(event=None):
            raw = entry_wg.get("1.0", "end")
            parsed = [k.strip() for k in raw.replace(",", "\n").splitlines() if k.strip()]
            lbl_key_count.configure(text=I18nManager.t("sett_wg_key_count", count=max(1, len(parsed))))

        entry_wg.bind("<KeyRelease>", _on_keys_text_changed)

        # OpenVPN Username
        ctk.CTkLabel(scroll, text=I18nManager.t("sett_ovpn_user"), font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=6, pady=(4, 2))
        entry_user = ctk.CTkEntry(scroll, height=30)
        entry_user.insert(0, cur_ovpn_user)
        entry_user.pack(fill="x", padx=6, pady=(0, 6))

        # OpenVPN Password
        ctk.CTkLabel(scroll, text=I18nManager.t("sett_ovpn_pass"), font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=6, pady=(4, 2))
        entry_pass = ctk.CTkEntry(scroll, height=30)
        entry_pass.insert(0, cur_ovpn_pass)
        entry_pass.pack(fill="x", padx=6, pady=(0, 6))

        # Ports Row
        port_row = ctk.CTkFrame(scroll, fg_color="transparent")
        port_row.pack(fill="x", padx=6, pady=(4, 6))
        port_row.grid_columnconfigure(0, weight=1)
        port_row.grid_columnconfigure(1, weight=1)

        p1_frame = ctk.CTkFrame(port_row, fg_color="transparent")
        p1_frame.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ctk.CTkLabel(p1_frame, text=I18nManager.t("sett_http_port"), font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        entry_http = ctk.CTkEntry(p1_frame, height=30)
        entry_http.insert(0, cur_http_port)
        entry_http.pack(fill="x", pady=(2, 0))

        p2_frame = ctk.CTkFrame(port_row, fg_color="transparent")
        p2_frame.grid(row=0, column=1, sticky="ew", padx=(4, 0))
        ctk.CTkLabel(p2_frame, text=I18nManager.t("sett_socks5_port"), font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        entry_socks = ctk.CTkEntry(p2_frame, height=30)
        entry_socks.insert(0, cur_socks5_port)
        entry_socks.pack(fill="x", pady=(2, 0))

        # Warm-up delay
        ctk.CTkLabel(scroll, text=I18nManager.t("sett_warmup_delay"), font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=6, pady=(6, 2))
        entry_warmup = ctk.CTkEntry(scroll, height=30)
        entry_warmup.insert(0, cur_warmup)
        entry_warmup.pack(fill="x", padx=6, pady=(0, 6))
        CTkToolTip(entry_warmup, lambda: I18nManager.t("sett_warmup_tooltip"))

        # Action Buttons
        btn_bar = ctk.CTkFrame(win, fg_color="transparent", height=45)
        btn_bar.pack(fill="x", padx=12, pady=(6, 12))

        def _save_settings():
            try:
                raw_wg = entry_wg.get("1.0", "end")
                new_wg_keys = [k.strip() for k in raw_wg.replace(",", "\n").splitlines() if k.strip()]
                if not new_wg_keys:
                    new_wg_keys = ["YOUR_WIREGUARD_PRIVATE_KEY_HERE"]
                new_wg = new_wg_keys[0]

                new_user = entry_user.get().strip()
                new_pass = entry_pass.get().strip()
                new_http = int(entry_http.get().strip())
                new_socks = int(entry_socks.get().strip())
                new_warm = float(entry_warmup.get().strip())

                # Update in memory config
                self.config.proxy["surfshark"]["private_key"] = new_wg
                self.config.proxy["surfshark"]["wireguard_keys"] = new_wg_keys
                self.config.proxy["surfshark"]["username"] = new_user
                self.config.proxy["surfshark"]["password"] = new_pass
                self.config.proxy["surfshark"]["http_port"] = new_http
                self.config.proxy["surfshark"]["socks5_port"] = new_socks
                self.config.proxy["surfshark"]["warmup_delay"] = new_warm
                self.config.save()

                creds_path = resolve_resource("data/surfshark_credentials.json")
                try:
                    creds_path.parent.mkdir(parents=True, exist_ok=True)
                    creds_data = {
                        "account_email": os.environ.get("SURFSHARK_ACCOUNT_EMAIL", "your_email@example.com"),
                        "plan": "Surfshark Starter (Multi-Account Enabled)",
                        "wireguard_private_key": new_wg,
                        "wireguard_keys": new_wg_keys,
                        "http_port": new_http,
                        "socks5_port": new_socks,
                        "warmup_delay": new_warm,
                        "openvpn_credentials": {
                            "username": new_user,
                            "password": new_pass
                        },
                        "total_clusters": 142
                    }
                    with open(creds_path, "w", encoding="utf-8") as f:
                        json.dump(creds_data, f, indent=2, ensure_ascii=False)
                except Exception:
                    pass

                if self.orchestrator:
                    prov = self.orchestrator.proxy_manager.get_surfshark_provider()
                    if prov:
                        prov.update_and_save_credentials(
                            username=new_user,
                            password=new_pass,
                            private_key=new_wg,
                            http_port=new_http,
                            socks5_port=new_socks,
                            warmup_delay=new_warm,
                            private_keys=new_wg_keys
                        )

                messagebox.showinfo("Success", I18nManager.t("sett_saved_msg"), parent=win)
                self._append_log("⚙️ [SETTINGS] " + I18nManager.t("sett_saved_msg"), "SYSTEM")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save settings: {e}", parent=win)

        def _reset_defaults():
            entry_wg.delete("1.0", "end")
            entry_wg.insert("1.0", "YOUR_WIREGUARD_PRIVATE_KEY_HERE")
            _on_keys_text_changed()
            entry_http.delete(0, "end")
            entry_http.insert(0, "1081")
            entry_socks.delete(0, "end")
            entry_socks.insert(0, "1080")
            entry_warmup.delete(0, "end")
            entry_warmup.insert(0, "1.0")

        ctk.CTkButton(
            btn_bar,
            text=I18nManager.t("sett_btn_save"),
            fg_color="#00aa55",
            hover_color="#008844",
            font=ctk.CTkFont(weight="bold"),
            command=_save_settings
        ).pack(side="left", padx=(0, 6), expand=True, fill="x")

        ctk.CTkButton(
            btn_bar,
            text=I18nManager.t("sett_btn_reset"),
            fg_color="#3a3a46",
            hover_color="#4a4a58",
            command=_reset_defaults
        ).pack(side="left", padx=6, expand=True, fill="x")

        ctk.CTkButton(
            btn_bar,
            text=I18nManager.t("sett_btn_cancel"),
            fg_color="#2b2b34",
            hover_color="#3a3a44",
            command=win.destroy
        ).pack(side="left", padx=(6, 0), expand=True, fill="x")

    def _launch_surfshark_login_browser(self):
        """서프샤크 로그인 및 WireGuard 수동 키 발급을 위한 독립 브라우저 프로필을 화면에 즉시 팝업"""
        import os
        import subprocess
        import webbrowser

        url = "https://my.surfshark.com/vpn/manual-setup/main/wireguard"
        profile_dir = os.path.join(os.path.expanduser("~"), ".d4uc", "browser-profiles", "surfshark")
        try:
            os.makedirs(profile_dir, exist_ok=True)
        except Exception:
            pass

        chrome_candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        target_bin = None
        for p in chrome_candidates:
            if os.path.exists(p):
                target_bin = p
                break

        if target_bin:
            cmd = [
                target_bin,
                f"--user-data-dir={profile_dir}",
                "--no-first-run",
                "--no-default-browser-check",
                url
            ]
            try:
                subprocess.Popen(cmd)
                self._append_log("🌐 [BROWSER] 서프샤크 키 발급 전용 격리 브라우저 창을 기동했습니다.", "SYSTEM")
                return
            except Exception:
                pass

        webbrowser.open(url)
        self._append_log("🌐 [BROWSER] 기본 브라우저로 서프샤크 수동 키 발급 페이지를 열었습니다.", "SYSTEM")

    def _on_concurrency_changed(self, v):
        count = int(v)
        if count <= 8:
            tier_str = "안정" if self.current_lang == "ko" else "Safe"
            color = "#00ff7f"
            lbl_text = f"🟢 {count} Workers ({tier_str})"
        elif count <= 20:
            tier_str = "고속" if self.current_lang == "ko" else "Fast"
            color = "#ffcc00"
            lbl_text = f"🟡 {count} Workers ({tier_str})"
        else:
            tier_str = "터보" if self.current_lang == "ko" else "Turbo"
            color = "#ff4444"
            lbl_text = f"🚀 {count} Workers ({tier_str})"

        self.concurrency_label.configure(text=lbl_text, text_color=color)
        opts = [I18nManager.t("all_workers")] + [f"워커 {i+1}" if self.current_lang == "ko" else f"Worker {i+1}" for i in range(count)]
        self.worker_filter_menu.configure(values=opts)

        # Dynamic mid-run slider manipulation is disabled for stability
        if self.orchestrator and self.orchestrator.is_running:
            return

    def _create_kpi_card(self, parent, col, title_key, initial_value, text_color):
        card = ctk.CTkFrame(parent, fg_color="#1e1e24", corner_radius=8)
        card.grid(row=0, column=col, padx=3, pady=0, sticky="nsew")

        title_lbl = ctk.CTkLabel(card, text=I18nManager.t(title_key), font=ctk.CTkFont(size=11), text_color="#999999")
        title_lbl.pack(padx=8, pady=(8, 0))
        val_lbl = ctk.CTkLabel(card, text=initial_value, font=ctk.CTkFont(size=17, weight="bold"), text_color=text_color)
        val_lbl.pack(padx=8, pady=(0, 8))
        return title_lbl, val_lbl

    def _refresh_language(self):
        # Header & Subtitle
        self.app_title.configure(text=I18nManager.t("app_title"))
        self.app_subtitle.configure(text=I18nManager.t("app_subtitle"))
        self.btn_lang.configure(text=I18nManager.t("lang_switch"))
        self.btn_help.configure(text=I18nManager.t("help_btn"))
        self.btn_settings.configure(text=I18nManager.t("btn_settings"))
        self.node_badge.configure(text=I18nManager.t("proxy_badge"))

        # Sidebar labels
        self.lbl_mode.configure(text=I18nManager.t("target_mode"))
        self.lbl_length.configure(text=I18nManager.t("length_title"))
        self.lbl_custom_title.configure(text=I18nManager.t("custom_pattern_title"))
        self.btn_reset_pattern.configure(text=I18nManager.t("btn_custom_reset"))
        self.lbl_preview_title.configure(text=I18nManager.t("preview_title"))
        self.lbl_prefix.configure(text=I18nManager.t("prefix_label"))
        self.prefix_entry.configure(placeholder_text=I18nManager.t("prefix_placeholder"))
        self.lbl_suffix.configure(text=I18nManager.t("suffix_label"))
        self.suffix_entry.configure(placeholder_text=I18nManager.t("suffix_placeholder"))
        self.lbl_middle_dot.configure(text=I18nManager.t("middle_dot_label"))
        self.lbl_mask.configure(text=I18nManager.t("custom_mask_label"))
        self.mask_entry.configure(placeholder_text=I18nManager.t("custom_mask_placeholder"))
        self.chk_skip_already.configure(text=I18nManager.t("chk_skip_already"))

        self.lbl_proxy.configure(text=I18nManager.t("proxy_title"))
        self.lbl_country.configure(text=I18nManager.t("country_title"))
        self.lbl_concurrency.configure(text=I18nManager.t("concurrency_title"))
        self._on_concurrency_changed(self.concurrency_slider.get())
        self.lbl_webhook.configure(text=I18nManager.t("webhook_title"))

        if hasattr(self, "lbl_guide_title"):
            self.lbl_guide_title.configure(text=I18nManager.t("guide_banner_title"))
            self.lbl_guide_text.configure(text=I18nManager.t("guide_banner_content"))
            if hasattr(self, "guide_body") and self.guide_body.winfo_ismapped():
                self.btn_toggle_guide.configure(text=I18nManager.t("guide_banner_hide"))
            elif hasattr(self, "btn_toggle_guide"):
                self.btn_toggle_guide.configure(text=I18nManager.t("guide_banner_show"))

        if self.current_lang == "ko":
            self.mode_menu.configure(values=[
                "Hybrid (사전+패턴+숫자+마스크)",
                "Combinatorial (비번형 영숫자 0~z 조합)",
                "Custom Mask (커스텀 패턴)",
                "Re-check (기존 닉네임 재확인)",
                "Dictionary (사전/음절)",
                "Pattern (대칭/반복)",
                "Numeric (0~9 숫자닉)",
                "Permutation (전수순열)",
                "Random (무작위)"
            ])
            self.middle_dot_menu.configure(values=[
                I18nManager.t("middle_dot_none"),
                I18nManager.t("middle_dot_opt"),
                I18nManager.t("middle_dot_req")
            ])
            self.proxy_menu.configure(values=["Surfshark (격리 프록시)", "File Pool (proxies.txt)", "ThorData", "Direct (단일 IP)"])
            self.country_menu.configure(values=["전세계 142개 전체", "한국 + 일본 + 싱가포르", "한국 (KR)", "일본 (JP)", "미국 (US)", "유럽 (독일/영국)"])
        else:
            self.mode_menu.configure(values=[
                "Hybrid (Dict+Patt+Num+Mask)",
                "Combinatorial (0-z Brute-force)",
                "Custom Mask (Pattern)",
                "Re-check (Verified List)",
                "Dictionary (Words/CVCV)",
                "Pattern (Symmetry)",
                "Numeric (0-9 Digits)",
                "Permutation (Full)",
                "Random (Alphanumeric)"
            ])
            self.middle_dot_menu.configure(values=[
                I18nManager.t("middle_dot_none"),
                I18nManager.t("middle_dot_opt"),
                I18nManager.t("middle_dot_req")
            ])
            self.proxy_menu.configure(values=["Surfshark (Isolated Proxy)", "File Pool (proxies.txt)", "ThorData", "Direct (Single IP)"])
            self.country_menu.configure(values=["All 142 Global Clusters", "Korea + Japan + Singapore", "Korea (KR)", "Japan (JP)", "United States (US)", "Europe (DE/UK)"])

        if hasattr(self, "lbl_comb_direction"):
            self.lbl_comb_direction.configure(text=I18nManager.t("comb_direction_label"))
            self.comb_direction_menu.configure(values=[
                I18nManager.t("comb_direction_asc"),
                I18nManager.t("comb_direction_desc")
            ])
            self.lbl_comb_charset.configure(text=I18nManager.t("comb_charset_label"))
            self.comb_charset_menu.configure(values=[
                I18nManager.t("comb_charset_num_first"),
                I18nManager.t("comb_charset_alpha_first")
            ])

        if hasattr(self, "lbl_perm_shard"):
            self.lbl_perm_shard.configure(text="다중 창 분할(샤딩)" if self.current_lang == "ko" else "Multi-Window Sharding")
            perm_shard_options = [v["label"] for v in SHARD_PRESETS.values()] + [
                "직접 글자 범위 지정" if self.current_lang == "ko" else "Custom Letter Range"
            ]
            self.perm_shard_menu.configure(values=perm_shard_options)

        if hasattr(self, "btn_load_history"):
            self.btn_load_history.configure(text=I18nManager.t("btn_load_history"))
        if hasattr(self, "lbl_recheck_range"):
            self.lbl_recheck_range.configure(text=I18nManager.t("recheck_range_label"))
            self.recheck_range_menu.configure(values=[
                I18nManager.t("recheck_range_all"),
                I18nManager.t("recheck_range_1_50"),
                I18nManager.t("recheck_range_51_100"),
                I18nManager.t("recheck_range_101_200"),
                I18nManager.t("recheck_range_custom")
            ])
            self.btn_recheck_import_sub.configure(text=I18nManager.t("btn_load_history"))

        self._update_mode_panel(self.mode_menu.get())

        if self.orchestrator and self.orchestrator.is_running:
            self.btn_toggle.configure(text=I18nManager.t("btn_stop"))
            self.status_badge.configure(text=I18nManager.t("status_running"))
        else:
            self.btn_toggle.configure(text=I18nManager.t("btn_start"))
            self.status_badge.configure(text=I18nManager.t("status_idle"))

        # KPI Titles
        self.card_total_title.configure(text=I18nManager.t("kpi_total"))
        self.card_rps_title.configure(text=I18nManager.t("kpi_rps"))
        self.card_avail_title.configure(text=I18nManager.t("kpi_avail"))
        self.card_taken_title.configure(text=I18nManager.t("kpi_taken"))
        self.card_429_title.configure(text=I18nManager.t("kpi_429"))
        self.card_skip_title.configure(text=I18nManager.t("kpi_skipped"))

        # Discovered Table
        self.lbl_table_title.configure(text=I18nManager.t("table_title"))
        saved_count = 0
        if self.orchestrator and self.orchestrator.storage:
            saved_count = self.orchestrator.storage.get_saved_count()
        elif hasattr(self, "tree"):
            saved_count = len(self.tree.get_children())
        self.lbl_autosave_indicator.configure(text=I18nManager.t("auto_save_indicator", count=saved_count))
        if hasattr(self, "btn_open_folder"):
            self.btn_open_folder.configure(text=I18nManager.t("btn_open_folder"))
        self.btn_open_reg.configure(text=I18nManager.t("btn_open_reg"))
        self.btn_export.configure(text=I18nManager.t("btn_export_avail"))
        self.tree.heading("time", text=I18nManager.t("col_time"))
        self.tree.heading("username", text=I18nManager.t("col_username"))
        self.tree.heading("pattern", text=I18nManager.t("col_pattern"))
        self.tree.heading("latency", text=I18nManager.t("col_latency"))
        self.tree.heading("server", text=I18nManager.t("col_server"))

        # Search & Multi-Filter Toolbar
        if hasattr(self, "search_entry"):
            self.search_entry.configure(placeholder_text=I18nManager.t("search_placeholder"))

        if hasattr(self, "filter_len_menu"):
            len_vals = [
                I18nManager.t("filter_len_all"),
                I18nManager.t("filter_len_3"),
                I18nManager.t("filter_len_4"),
                I18nManager.t("filter_len_5"),
                I18nManager.t("filter_len_6p")
            ]
            cur_len = self.filter_len_menu.get()
            old_len_vals = self.filter_len_menu.cget("values")
            idx = 0
            if cur_len in old_len_vals:
                idx = old_len_vals.index(cur_len)
            self.filter_len_menu.configure(values=len_vals)
            if 0 <= idx < len(len_vals):
                self.filter_len_menu.set(len_vals[idx])

        if hasattr(self, "filter_type_menu"):
            type_vals = [
                I18nManager.t("filter_type_all"),
                I18nManager.t("filter_type_dict"),
                I18nManager.t("filter_type_patt"),
                I18nManager.t("filter_type_num"),
                I18nManager.t("filter_type_dot"),
                I18nManager.t("filter_type_comb"),
                I18nManager.t("filter_type_custom")
            ]
            cur_type = self.filter_type_menu.get()
            old_type_vals = self.filter_type_menu.cget("values")
            idx = 0
            if cur_type in old_type_vals:
                idx = old_type_vals.index(cur_type)
            self.filter_type_menu.configure(values=type_vals)
            if 0 <= idx < len(type_vals):
                self.filter_type_menu.set(type_vals[idx])

        if hasattr(self, "filter_sort_menu"):
            sort_vals = [
                I18nManager.t("filter_sort_latest"),
                I18nManager.t("filter_sort_alpha_asc"),
                I18nManager.t("filter_sort_alpha_desc"),
                I18nManager.t("filter_sort_latency_fast")
            ]
            cur_sort = self.filter_sort_menu.get()
            old_sort_vals = self.filter_sort_menu.cget("values")
            idx = 0
            if cur_sort in old_sort_vals:
                idx = old_sort_vals.index(cur_sort)
            self.filter_sort_menu.configure(values=sort_vals)
            if 0 <= idx < len(sort_vals):
                self.filter_sort_menu.set(sort_vals[idx])

        if hasattr(self, "discovered_items"):
            self._refresh_discovered_table()

        # Tree Context Menu labels
        self.tree_menu.entryconfigure(0, label=I18nManager.t("ctx_recheck_selected"))
        self.tree_menu.entryconfigure(1, label=I18nManager.t("ctx_recheck_all"))
        self.tree_menu.entryconfigure(3, label=I18nManager.t("ctx_copy_username"))
        self.tree_menu.entryconfigure(4, label=I18nManager.t("ctx_copy_all"))
        self.tree_menu.entryconfigure(6, label=I18nManager.t("ctx_export_file"))
        self.tree_menu.entryconfigure(7, label=I18nManager.t("ctx_open_discord"))

        # Log Console & Filters
        self.lbl_log_title.configure(text=I18nManager.t("log_title"))
        self.chk_worker.configure(text=I18nManager.t("log_filter_worker"))
        self.chk_success.configure(text=I18nManager.t("log_filter_success"))
        self.chk_proxy.configure(text=I18nManager.t("log_filter_proxy"))
        self.chk_system.configure(text=I18nManager.t("log_filter_system"))
        self.lbl_worker_select.configure(text=I18nManager.t("log_worker_select"))
        self.btn_clear_log.configure(text=I18nManager.t("btn_clear_log"))
        self.btn_save_log.configure(text=I18nManager.t("btn_save_log"))
        collapse_text = I18nManager.t("btn_expand_log") if self._is_log_collapsed else I18nManager.t("btn_collapse_log")
        self.btn_toggle_log.configure(text=collapse_text)

        # Status Line
        if not self.orchestrator or not self.orchestrator.is_running:
            self.lbl_status_text.configure(text=I18nManager.t("status_bar_idle"))

    def _toggle_language(self):
        new_lang = "en" if self.current_lang == "ko" else "ko"
        self.current_lang = new_lang
        I18nManager.set_language(new_lang)
        self._refresh_language()

    def _open_help_modal(self):
        help_win = ctk.CTkToplevel(self)
        help_win.title(I18nManager.t("help_modal_title"))
        help_win.geometry("800x600")
        help_win.minsize(700, 500)
        help_win.attributes("-topmost", True)

        header = ctk.CTkFrame(help_win, fg_color="#1e1e24", height=45)
        header.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(
            header,
            text=I18nManager.t("help_modal_title"),
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#00c8ff"
        ).pack(side="left", padx=15, pady=10)

        content_box = ctk.CTkTextbox(help_win, font=ctk.CTkFont(family="Segoe UI", size=12), wrap="word")
        content_box.pack(fill="both", expand=True, padx=10, pady=5)
        content_box.insert("1.0", I18nManager.t("help_modal_content").strip())
        content_box.configure(state="disabled")

        btn_close = ctk.CTkButton(
            help_win,
            text=I18nManager.t("help_close"),
            width=120,
            height=32,
            font=ctk.CTkFont(weight="bold"),
            command=help_win.destroy
        )
        btn_close.pack(pady=(5, 12))

    def _toggle_guide_banner(self):
        """프로그램 상단 빠른 사용법 배너 접기 / 펼치기 토글"""
        if hasattr(self, "guide_body") and self.guide_body.winfo_ismapped():
            self.guide_body.pack_forget()
            self.btn_toggle_guide.configure(text=I18nManager.t("guide_banner_show"))
        elif hasattr(self, "guide_body"):
            self.guide_body.pack(fill="x", padx=12, pady=(0, 8))
            self.btn_toggle_guide.configure(text=I18nManager.t("guide_banner_hide"))

    def _toggle_log_collapse(self):
        if not self._is_log_collapsed:
            # Collapse
            self.filter_bar.pack_forget()
            self.log_box.pack_forget()
            self.content.grid_rowconfigure(2, weight=10)
            self.content.grid_rowconfigure(4, weight=0)
            self._is_log_collapsed = True
            self.btn_toggle_log.configure(text=I18nManager.t("btn_expand_log"))
        else:
            # Expand
            self.filter_bar.pack(fill="x", padx=8, pady=(0, 4))
            self.log_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))
            self.content.grid_rowconfigure(2, weight=3)
            self.content.grid_rowconfigure(4, weight=2)
            self._is_log_collapsed = False
            self.btn_toggle_log.configure(text=I18nManager.t("btn_collapse_log"))

    def _clear_logs(self):
        self._raw_logs.clear()
        if hasattr(self, "_pending_logs"):
            self._pending_logs.clear()
        self.log_box.delete("1.0", "end")

    def _save_logs_to_file(self):
        log_content = self.log_box.get("1.0", "end").strip()
        if not log_content:
            messagebox.showinfo("Info", "저장할 로그 내용이 없습니다." if self.current_lang == "ko" else "No log content to save.", parent=self)
            return

        ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"d4uc_log_{ts_str}.log"
        default_dir = resolve_output_path("logs")

        filepath = filedialog.asksaveasfilename(
            initialdir=str(default_dir),
            initialfile=default_filename,
            defaultextension=".log",
            filetypes=[("Log files (*.log)", "*.log"), ("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")],
            parent=self
        )

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(log_content + "\n")
                msg = I18nManager.t("log_saved_msg", path=filepath)
                messagebox.showinfo("Success", msg, parent=self)
                self._append_log(f"💾 [EXPORT] {msg}", "SYSTEM")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save log: {e}", parent=self)

    def _set_inputs_locked(self, locked: bool):
        """검사 실행 중(RUNNING) 워커 수 슬라이더 및 주요 입력 설정을 잠가(disabled) 안정성 보장"""
        st = "disabled" if locked else "normal"
        if hasattr(self, "concurrency_slider"):
            self.concurrency_slider.configure(state=st)
        if hasattr(self, "concurrency_label"):
            if locked:
                count = int(self.concurrency_slider.get())
                lock_msg = f"🔒 {count} Workers (검사 중 고정)" if self.current_lang == "ko" else f"🔒 {count} Workers (Locked during run)"
                self.concurrency_label.configure(text=lock_msg, text_color="#888888")
            else:
                self._on_concurrency_changed(self.concurrency_slider.get())
        if hasattr(self, "mode_menu"):
            self.mode_menu.configure(state=st)
        if hasattr(self, "length_menu"):
            self.length_menu.configure(state=st)
        if hasattr(self, "proxy_menu"):
            self.proxy_menu.configure(state=st)
        if hasattr(self, "country_menu"):
            self.country_menu.configure(state=st)
        if hasattr(self, "prefix_entry"):
            self.prefix_entry.configure(state=st)
        if hasattr(self, "suffix_entry"):
            self.suffix_entry.configure(state=st)
        if hasattr(self, "mask_entry"):
            self.mask_entry.configure(state=st)
        if hasattr(self, "middle_dot_menu"):
            self.middle_dot_menu.configure(state=st)
        if hasattr(self, "chk_skip_already"):
            self.chk_skip_already.configure(state=st)
        if hasattr(self, "comb_direction_menu"):
            self.comb_direction_menu.configure(state=st)
        if hasattr(self, "comb_charset_menu"):
            self.comb_charset_menu.configure(state=st)
        if hasattr(self, "perm_shard_menu"):
            self.perm_shard_menu.configure(state=st)
        if hasattr(self, "perm_start_menu"):
            self.perm_start_menu.configure(state=st)
        if hasattr(self, "perm_end_menu"):
            self.perm_end_menu.configure(state=st)
        if hasattr(self, "recheck_range_menu"):
            self.recheck_range_menu.configure(state=st)
        if hasattr(self, "btn_load_history"):
            self.btn_load_history.configure(state=st)
        if hasattr(self, "btn_recheck_import_sub"):
            self.btn_recheck_import_sub.configure(state=st)
        if hasattr(self, "btn_reset_pattern"):
            self.btn_reset_pattern.configure(state=st)

    def _on_toggle_run(self):
        if self.orchestrator and self.orchestrator.is_running:
            # Stop
            self.btn_toggle.configure(text=I18nManager.t("status_stopping"), state="disabled")
            self.status_badge.configure(text=I18nManager.t("status_stopping"), text_color="#ffcc00")
            self.lbl_status_text.configure(text=I18nManager.t("status_bar_stopping"))
            self.progress_bar.stop()

            def _stop_async():
                self.orchestrator.stop()
                self.after(500, self._on_stopped)

            threading.Thread(target=_stop_async, daemon=True).start()
        else:
            # Start
            self._apply_settings_to_config()
            is_recheck = (self.config.target.get("mode") == "recheck")
            recheck_targets = []
            if is_recheck:
                recheck_targets = self._get_recheck_targets()
                if not recheck_targets:
                    warn_msg = "재확인할 닉네임 목록이 없습니다.\n먼저 닉네임을 발견하거나 [📂 이전 발견/파일 불러오기] 버튼으로 파일을 불러오세요." if self.current_lang == "ko" else "No usernames to re-check.\nPlease discover usernames first or click [📂 Import History] to load a file."
                    messagebox.showwarning("Re-check Notice", warn_msg, parent=self)
                    return

            self.orchestrator = GuiOrchestrator(
                config=self.config,
                on_result_cb=self._add_discovered_result,
                on_log_cb=self._append_log,
                recheck_list=recheck_targets,
                on_recheck_result_cb=self._on_recheck_item_result
            )

            # Reset live KPI counters to 0 immediately for the fresh run
            self.card_total.configure(text="0")
            self.card_rps.configure(text="0.0 req/s")
            self.card_avail.configure(text="0")
            self.card_taken.configure(text="0")
            self.card_429.configure(text="0")
            self.card_skip.configure(text="0")

            # Add clear run separator in the log window
            run_title = f"🚀 [새 실시간 검사 가동] 모드: {self.config.target.get('mode', 'hybrid').upper()} | {self.config.target.get('length', 4)}자 | 워커: {self.orchestrator.concurrency}개"
            self._append_log("=" * 65, "START")
            self._append_log(run_title, "START")
            self._append_log("=" * 65, "START")

            self.orchestrator.start_thread()
            self._set_inputs_locked(True)
            self.btn_toggle.configure(text=I18nManager.t("btn_stop"), fg_color="#cc2222", hover_color="#991111", state="normal")
            self.status_badge.configure(text=I18nManager.t("status_running"), text_color="#00ff7f")
            self.progress_bar.start()

    def _on_stopped(self):
        self._set_inputs_locked(False)
        self.btn_toggle.configure(text=I18nManager.t("btn_start"), fg_color="#00aa55", hover_color="#008844", state="normal")
        self.status_badge.configure(text=I18nManager.t("status_idle"), text_color="#888888")
        self.lbl_status_text.configure(text=I18nManager.t("status_bar_idle"))
        self.progress_bar.stop()
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.set(0)

    def _apply_settings_to_config(self):
        # Custom pattern fields
        pre = self.prefix_entry.get().strip()
        suf = self.suffix_entry.get().strip()
        msk = self.mask_entry.get().strip()
        self.config.target["prefix"] = pre
        self.config.target["suffix"] = suf
        dot_sel = self.middle_dot_menu.get()
        if "필수" in dot_sel or "Required" in dot_sel:
            self.config.target["middle_dot"] = "required"
        elif "허용" in dot_sel or "선택" in dot_sel or "Optional" in dot_sel:
            self.config.target["middle_dot"] = "optional"
        else:
            self.config.target["middle_dot"] = "none"
        self.config.target["mask"] = msk
        self.config.target["skip_already_checked"] = bool(self.chk_skip_already.get())

        has_custom = bool(pre or suf or msk or self.config.target["middle_dot"] != "none")
        mode_val = self.mode_menu.get().split()[0].lower()

        if "recheck" in mode_val or "재확인" in mode_val or "verif" in mode_val:
            self.config.target["mode"] = "recheck"
        elif "comb" in mode_val or "비번" in mode_val:
            self.config.target["mode"] = "combinatorial"
            dir_sel = self.comb_direction_menu.get() if hasattr(self, "comb_direction_menu") else "오름차순"
            self.config.target["direction"] = "desc" if ("내림차순" in dir_sel or "Descending" in dir_sel) else "asc"
            cs_sel = self.comb_charset_menu.get() if hasattr(self, "comb_charset_menu") else "숫자 우선"
            self.config.target["charset_type"] = "alphanumeric_alpha_first" if ("영문 우선" in cs_sel or "Letters First" in cs_sel) else "alphanumeric_num_first"
        elif "custom" in mode_val or "mask" in mode_val:
            self.config.target["mode"] = "custom"
        elif "hybrid" in mode_val:
            self.config.target["mode"] = "hybrid"
        elif "dict" in mode_val:
            self.config.target["mode"] = "dictionary"
        elif "patt" in mode_val:
            self.config.target["mode"] = "pattern"
        elif "num" in mode_val:
            self.config.target["mode"] = "numeric"
        elif "perm" in mode_val:
            self.config.target["mode"] = "permutation"
            shard_choice = self.perm_shard_menu.get() if hasattr(self, "perm_shard_menu") else "전체 탐색 (분할 없음)"
            shard_k = "none"
            start_c = None
            end_c = None
            for k, v in SHARD_PRESETS.items():
                if v["label"] == shard_choice:
                    shard_k = k
                    start_c = v["start"]
                    end_c = v["end"]
                    break
            if "직접" in shard_choice or "Custom" in shard_choice:
                start_c = self.perm_start_menu.get() if hasattr(self, "perm_start_menu") else "a"
                end_c = self.perm_end_menu.get() if hasattr(self, "perm_end_menu") else "m"
                shard_k = None
            self.config.target["shard_key"] = shard_k
            self.config.target["start_char"] = start_c
            self.config.target["end_char"] = end_c
        else:
            self.config.target["mode"] = "random"

        self.config.target["length"] = int(self.length_menu.get())
        self.config.network["concurrency"] = int(self.concurrency_slider.get())

        p_mode = self.proxy_menu.get()
        if "Surfshark" in p_mode:
            self.config.proxy["mode"] = "surfshark"
        elif "File" in p_mode:
            self.config.proxy["mode"] = "file"
        elif "Thor" in p_mode:
            self.config.proxy["mode"] = "thordata"
        else:
            self.config.proxy["mode"] = "direct"

        country = self.country_menu.get()
        if "한국" in country and "일본" in country:
            self.config.proxy["surfshark"]["preferred_countries"] = ["KR", "JP", "SG"]
            self.config.proxy["surfshark"]["preferred_country_label"] = "한국 + 일본 + 싱가포르"
        elif "한국" in country or "KR" in country:
            self.config.proxy["surfshark"]["preferred_countries"] = ["KR"]
            self.config.proxy["surfshark"]["preferred_country_label"] = "한국 (KR)"
        elif "일본" in country or "JP" in country:
            self.config.proxy["surfshark"]["preferred_countries"] = ["JP"]
            self.config.proxy["surfshark"]["preferred_country_label"] = "일본 (JP)"
        elif "미국" in country or "US" in country:
            self.config.proxy["surfshark"]["preferred_countries"] = ["US"]
            self.config.proxy["surfshark"]["preferred_country_label"] = "미국 (US)"
        elif "유럽" in country or "Europe" in country or "DE" in country:
            self.config.proxy["surfshark"]["preferred_countries"] = ["DE", "GB", "NL", "FR"]
            self.config.proxy["surfshark"]["preferred_country_label"] = "유럽 (독일/영국)"
        else: # "전세계" or "All" or "142"
            self.config.proxy["surfshark"]["preferred_countries"] = []
            self.config.proxy["surfshark"]["preferred_country_label"] = "전세계 142개 전체"

        webhook_url = self.webhook_entry.get().strip()
        if webhook_url:
            self.config.webhook["url"] = webhook_url
            self.config.webhook["enabled"] = True

    def _add_discovered_result(self, ts, username, pattern, latency, server):
        def _ui():
            lat_val = 0.0
            try:
                lat_val = float(str(latency).replace("ms", "").strip())
            except Exception:
                pass
            item = {
                "time": str(ts),
                "username": str(username),
                "pattern": str(pattern),
                "latency": str(latency),
                "server": str(server),
                "latency_val": lat_val,
                "length": len(str(username))
            }
            self.discovered_items.insert(0, item)
            self._refresh_discovered_table()
            cnt = self.orchestrator.storage.get_saved_count() if (self.orchestrator and self.orchestrator.storage) else len(self.discovered_items)
            self.lbl_autosave_indicator.configure(text=I18nManager.t("auto_save_indicator", count=cnt))
        self.after(0, _ui)

    def _should_display_log(self, level: str, worker_id: Optional[int]) -> bool:
        if level == "WORKER" and not self.chk_worker.get():
            return False
        if level == "SUCCESS" and not self.chk_success.get():
            return False
        if level in ("RATELIMIT", "PROXY") and not self.chk_proxy.get():
            return False
        if level in ("START", "STOP", "STORAGE", "NETWORK", "TLS", "RUNNING", "PROGRESS", "COMPLETED", "WARN", "ERROR") and not self.chk_system.get():
            return False

        if worker_id is not None:
            sel = self.worker_filter_menu.get()
            if "전체" not in sel and "All" not in sel:
                if str(worker_id) not in sel:
                    return False

        return True

    def _append_log(self, text: str, level: str = "INFO", worker_id: Optional[int] = None):
        self._raw_logs.append((text, level, worker_id))
        if len(self._raw_logs) > 3000:
            self._raw_logs.pop(0)

        if self._should_display_log(level, worker_id):
            if hasattr(self, "_pending_logs"):
                self._pending_logs.append(text)
                if not getattr(self, "_log_flush_scheduled", False):
                    self._log_flush_scheduled = True
                    self.after(30, self._flush_pending_logs)
            else:
                def _insert():
                    self.log_box.insert("end", text + "\n")
                    self.log_box.see("end")
                self.after(0, _insert)

    def _flush_pending_logs(self):
        """고속 로그 30ms 일괄 버퍼링 플러시: UI 스터터 및 CPU 점유율 80% 이상 절감"""
        self._log_flush_scheduled = False
        if not hasattr(self, "_pending_logs") or not self._pending_logs:
            return
        batch = self._pending_logs
        self._pending_logs = []
        try:
            self.log_box.insert("end", "\n".join(batch) + "\n")
            self.log_box.see("end")
        except Exception:
            pass

    def _apply_log_filters(self):
        self.log_box.delete("1.0", "end")
        for text, level, wid in self._raw_logs:
            if self._should_display_log(level, wid):
                self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def _start_telemetry_loop(self):
        def _update():
            if self.orchestrator and self.orchestrator.is_running:
                m = self.orchestrator.metrics
                self.card_total.configure(text=f"{m.total_checked:,}")
                self.card_rps.configure(text=f"{m.rps:.1f} req/s")
                self.card_avail.configure(text=f"{m.available_count}")
                self.card_taken.configure(text=f"{m.taken_count:,}")
                self.card_429.configure(text=f"{m.rate_limited_count}")
                self.card_skip.configure(text=f"{m.skipped_count:,}")

                elapsed = self.orchestrator.get_elapsed_str()
                status_txt = I18nManager.t(
                    "status_bar_running",
                    workers=self.orchestrator.concurrency,
                    elapsed=elapsed
                )

                total_comb = getattr(self.orchestrator.generator, "total_combinations", None)
                if total_comb and total_comb > 0:
                    checked = m.total_checked
                    pct = min(100.0, (checked / total_comb) * 100)
                    if self.progress_bar.cget("mode") != "determinate":
                        self.progress_bar.stop()
                        self.progress_bar.configure(mode="determinate")
                    self.progress_bar.set(min(1.0, checked / total_comb))
                    prog_info = f" | 진행률: {checked:,} / {total_comb:,} ({pct:.2f}%)" if self.current_lang == "ko" else f" | Progress: {checked:,} / {total_comb:,} ({pct:.2f}%)"
                    status_txt = f"{status_txt}{prog_info}"
                else:
                    if self.progress_bar.cget("mode") != "indeterminate":
                        self.progress_bar.configure(mode="indeterminate")
                        self.progress_bar.start()

                self.lbl_status_text.configure(text=status_txt)

                tunnel_txt = f"🛡️ 다중 터널 ({self.orchestrator.concurrency} Nodes)" if self.current_lang == "ko" else f"🛡️ Multi-Tunnel ({self.orchestrator.concurrency} Nodes)"
                self.node_badge.configure(text=tunnel_txt)
            else:
                tunnel_txt = "🛡️ 격리 터널 준비" if self.current_lang == "ko" else "🛡️ Tunnel Ready"
                self.node_badge.configure(text=tunnel_txt)

            # 3. Cross-window live sync for discovered available usernames (every 1.5s)
            self._sync_external_available_usernames()

            self.after(250, _update)

        self.after(250, _update)

    def _sync_external_available_usernames(self):
        """다중 프로그램 실행 시 다른 창에서 발견된 사용 가능 닉네임을 SQLite에서 실시간 감지하여 LIVE 테이블에 자동 추가"""
        now = time.time()
        if now - getattr(self, "_last_available_sync_time", 0.0) < 1.5:
            return
        self._last_available_sync_time = now

        try:
            storage = None
            if self.orchestrator and self.orchestrator.storage:
                storage = self.orchestrator.storage
            elif hasattr(self, "_local_storage") and self._local_storage:
                storage = self._local_storage
            else:
                db_p = self.config.storage.get("db_path", "data/d4uc_results.db")
                self._local_storage = StorageManager(db_path=db_p)
                storage = self._local_storage

            if not storage:
                return

            if not hasattr(self, "_last_available_rowid"):
                self._last_available_rowid = storage.get_max_rowid()

            new_records, new_max_id = storage.fetch_new_available_since(self._last_available_rowid)
            if new_records:
                self._last_available_rowid = new_max_id
                added_any = False
                existing_names = {item["username"].lower() for item in self.discovered_items}
                for rec in new_records:
                    u = rec["username"]
                    if u.lower() not in existing_names:
                        lat_val = 0.0
                        try:
                            lat_val = float(rec["latency"].replace("ms", "").strip())
                        except Exception:
                            pass
                        item = {
                            "time": rec["time"],
                            "username": u,
                            "pattern": rec["pattern"],
                            "latency": rec["latency"],
                            "server": rec["server"],
                            "latency_val": lat_val,
                            "length": len(u)
                        }
                        self.discovered_items.insert(0, item)
                        existing_names.add(u.lower())
                        added_any = True

                if added_any:
                    self._refresh_discovered_table()
                    total_cnt = len(self.discovered_items)
                    self.lbl_autosave_indicator.configure(text=I18nManager.t("auto_save_indicator", count=total_cnt))
        except Exception:
            pass

    def _on_close(self):
        self._save_ui_to_config()
        if self.orchestrator:
            self.orchestrator.stop()
        self.destroy()


def main():
    parser = argparse.ArgumentParser(description="Discord Username Checker V2 GUI")
    parser.add_argument("--lang", choices=["ko", "en"], default=None, help="Default UI language (ko or en)")
    args, _ = parser.parse_known_args()

    default_lang = args.lang
    if not default_lang:
        exe_name = Path(sys.executable).stem.lower()
        if "_en" in exe_name or "english" in exe_name:
            default_lang = "en"
        else:
            default_lang = "ko"

    app = DiscordCheckerGui(default_lang=default_lang)
    app.mainloop()


if __name__ == "__main__":
    main()
