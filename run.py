# run.py
import argparse
import asyncio
import os
import signal
import sys
import time
from datetime import datetime
from rich.console import Console
from rich.live import Live

from src.config import AppConfig
from src.network.client import DiscordApiClient, CheckStatus, CheckResult
from src.network.exceptions import RateLimitedException, WafBlockedException, ProxyFailedException
from src.proxy.manager import UnifiedProxyManager
from src.generator import create_generator
from src.storage.db import StorageManager
from src.storage.drive_sync import GoogleDriveSyncManager
from src.notify.webhook import DiscordWebhookNotifier
from src.ui.dashboard import RichDashboard, DashboardMetrics
from curl_cffi.requests import AsyncSession

console = Console()

class Orchestrator:
    def __init__(self, config: AppConfig, force_no_dashboard: bool = False):
        self.config = config
        self.force_no_dashboard = force_no_dashboard
        self.metrics = DashboardMetrics()
        self.proxy_manager = UnifiedProxyManager(config.proxy)
        self.generator = create_generator(config.target)

        # Google Drive Sync Manager (Pre-restore before StorageManager loads SQLite cache)
        drive_path = config.storage.get("drive_dir")
        self.drive_sync = GoogleDriveSyncManager(
            drive_dir=drive_path,
            local_data_dir=os.path.dirname(config.storage.get("db_path", "data/d4uc_results.db")),
            local_available_file=config.storage.get("available_file", "available.txt"),
            local_db_file=config.storage.get("db_path", "data/d4uc_results.db")
        )
        if self.drive_sync.is_enabled:
            restored = self.drive_sync.restore_from_drive()
            if restored > 0:
                console.print(f"[bold green]💾 [Google Drive] 이전 세션의 검사 이력 {restored}건을 복원했습니다.[/bold green]")

        self.storage = StorageManager(
            db_path=config.storage.get("db_path", "data/d4uc_results.db"),
            save_legacy=config.storage.get("save_legacy_txt", True),
            available_file=config.storage.get("available_file", "available.txt"),
            taken_file=config.storage.get("taken_file", "taken.txt")
        )
        self.client = DiscordApiClient(
            impersonate=config.network.get("impersonate", "chrome131"),
            timeout=float(config.network.get("timeout_seconds", 8.0))
        )
        self.webhook = DiscordWebhookNotifier(
            webhook_url=config.webhook.get("url", ""),
            enabled=config.webhook.get("enabled", False),
            mention=config.webhook.get("mention", "@here")
        )
        self.webhook_interval = float(config.webhook.get("progress_interval", 300.0))
        self.webhook_progress_enabled = bool(config.webhook.get("progress_enabled", True)) and self.webhook.enabled

        self.concurrency = int(config.network.get("concurrency", 5))
        self.is_running = True
        self.dashboard = RichDashboard(
            console=console,
            mode_str=config.target.get("mode", "hybrid"),
            length=int(config.target.get("length", 4)),
            concurrency=self.concurrency,
            impersonate=config.network.get("impersonate", "chrome131")
        )

    async def worker_loop(self, worker_id: int):
        async with AsyncSession() as session:
            while self.is_running:
                # 1. Generate unique candidate
                username = None
                for _ in range(50):
                    cand = self.generator.next_username()
                    if not cand:
                        break
                    if not self.storage.is_already_tried(cand):
                        username = cand
                        break
                    self.metrics.skipped_count += 1

                if not username:
                    await asyncio.sleep(0.1)
                    continue

                # 2. Acquire Proxy
                endpoint = self.proxy_manager.get_proxy()
                proxy_url = endpoint.url if endpoint else None

                # 3. Check Discord
                t0 = time.time()
                try:
                    result = await self.client.check_username(
                        session=session,
                        username=username,
                        proxy=proxy_url,
                        pattern_type=self.generator.get_pattern_type()
                    )
                    latency = (time.time() - t0) * 1000

                    if result.status == CheckStatus.AVAILABLE:
                        self.metrics.available_count += 1
                        self.metrics.total_checked += 1
                        await self.storage.enqueue_result(result)
                        self.drive_sync.sync_available_immediately(result.username)
                        await self.webhook.send_alert(result, session)
                    elif result.status == CheckStatus.TAKEN:
                        self.metrics.taken_count += 1
                        self.metrics.total_checked += 1
                        await self.storage.enqueue_result(result)

                    if endpoint:
                        self.proxy_manager.report_success(endpoint, latency)

                except RateLimitedException:
                    self.metrics.rate_limited_count += 1
                    if endpoint:
                        self.proxy_manager.report_429(endpoint)
                    await asyncio.sleep(2.0)

                except (WafBlockedException, ProxyFailedException):
                    self.metrics.error_count += 1
                    if endpoint:
                        self.proxy_manager.report_failure(endpoint)
                    await asyncio.sleep(1.0)

                except Exception:
                    self.metrics.error_count += 1
                    await asyncio.sleep(0.5)

    async def run(self):
        mode_val = self.config.target.get("mode", "hybrid").upper()
        len_val = self.config.target.get("length", 4)
        shard_val = self.config.target.get("shard_key", "None")
        console.print(
            f"[bold green]🚀 D4UC Headless Engine 기동 시작[/bold green] | "
            f"[cyan]모드: {mode_val}[/cyan] | [yellow]길이: {len_val}자[/yellow] | "
            f"[magenta]워커: {self.concurrency}개[/magenta] | [blue]샤딩: {shard_val}[/blue]"
        )
        if self.drive_sync.is_enabled:
            console.print(f"[bold cyan]📁 Google Drive 저장소:[/bold cyan] {self.drive_sync.drive_dir}")

        await self.storage.start_worker()
        self.drive_sync.start_background_sync()

        # Send Session Start Webhook
        await self.webhook.send_session_start(
            mode=mode_val,
            length=len_val,
            workers=self.concurrency,
            proxy_mode=self.config.proxy.get("mode", "surfshark"),
            shard=shard_val if shard_val != "None" else None,
            drive_enabled=self.drive_sync.is_enabled
        )

        workers = [
            asyncio.create_task(self.worker_loop(i + 1))
            for i in range(self.concurrency)
        ]

        is_tty = sys.stdout.isatty() and not self.force_no_dashboard
        use_rich = self.config.ui.get("rich_dashboard", True) and is_tty
        last_progress_webhook = time.time()

        if use_rich:
            with Live(console=console, refresh_per_second=4, screen=False) as live:
                while self.is_running:
                    proxy_stats = self.proxy_manager.get_pool_summary()
                    layout = self.dashboard.generate_layout(self.metrics, proxy_stats)
                    live.update(layout)

                    # Periodic Progress Webhook
                    now = time.time()
                    if self.webhook_progress_enabled and (now - last_progress_webhook >= self.webhook_interval):
                        last_progress_webhook = now
                        await self.webhook.send_progress_report(
                            total_checked=self.metrics.total_checked,
                            available_count=self.metrics.available_count,
                            taken_count=self.metrics.taken_count,
                            rate_limited_count=self.metrics.rate_limited_count,
                            skipped_count=self.metrics.skipped_count,
                            rps=self.metrics.rps,
                            mode=mode_val,
                            length=len_val,
                            workers=self.concurrency,
                            drive_status=self.drive_sync.last_sync_status
                        )
                    await asyncio.sleep(0.25)
        else:
            console.print("[dim]ℹ️ TTY 미지원 또는 --no-dashboard 모드로 스트리밍 로그를 출력합니다.[/dim]")
            while self.is_running:
                await asyncio.sleep(2.0)
                m = self.metrics
                ts = datetime.now().strftime("%H:%M:%S")
                console.print(
                    f"[{ts}] 📊 [RPS: {m.rps:.1f}] 총: {m.total_checked:,} | "
                    f"[green]가용: {m.available_count}[/green] | [dim]사용중: {m.taken_count:,}[/dim] | "
                    f"[yellow]429: {m.rate_limited_count}[/yellow] | [cyan]스킵: {m.skipped_count:,}[/cyan]"
                )

                # Periodic Progress Webhook
                now = time.time()
                if self.webhook_progress_enabled and (now - last_progress_webhook >= self.webhook_interval):
                    last_progress_webhook = now
                    await self.webhook.send_progress_report(
                        total_checked=m.total_checked,
                        available_count=m.available_count,
                        taken_count=m.taken_count,
                        rate_limited_count=m.rate_limited_count,
                        skipped_count=m.skipped_count,
                        rps=m.rps,
                        mode=mode_val,
                        length=len_val,
                        workers=self.concurrency,
                        drive_status=self.drive_sync.last_sync_status
                    )

        # Cancellation and cleanup
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

        # Finalize Drive Sync & Send Session Stop Webhook
        await self.drive_sync.stop()
        await self.storage.close()
        self.proxy_manager.close()

        await self.webhook.send_session_stop(
            total_checked=self.metrics.total_checked,
            available_count=self.metrics.available_count,
            taken_count=self.metrics.taken_count,
            rate_limited_count=self.metrics.rate_limited_count,
            drive_path=str(self.drive_sync.drive_dir) if self.drive_sync.is_enabled else None
        )

def parse_args():
    parser = argparse.ArgumentParser(
        description="D4UC (Discord 4-Character Usernames Checker) - High-Performance Cross-Platform Headless CLI"
    )
    parser.add_argument("--mode", "-m", choices=["hybrid", "dictionary", "pattern", "permutation", "numeric", "custom_mask", "combinatorial", "recheck"], help="Username generation mode")
    parser.add_argument("--length", "-l", type=int, choices=[3, 4, 5, 6], help="Target username length")
    parser.add_argument("--workers", "-w", type=int, help="Number of concurrent workers (1-50)")
    parser.add_argument("--proxy", "-p", choices=["surfshark", "file", "thordata", "direct"], help="Proxy provider to use")
    parser.add_argument("--shard", "-s", help="Permutation sharding key (e.g. 2_1, 2_2, 3_1, 3_2, 3_3, 4_1, 4_2, 4_3, 4_4)")
    parser.add_argument("--start-char", help="Start character for custom letter range (a-z, 0-9, _)")
    parser.add_argument("--end-char", help="End character for custom letter range (a-z, 0-9, _)")
    parser.add_argument("--prefix", help="Custom mask prefix (e.g. 'kr')")
    parser.add_argument("--suffix", help="Custom mask suffix (e.g. '99')")
    parser.add_argument("--middle-dot", choices=["none", "optional", "required"], help="Middle dot rule")
    parser.add_argument("--mask", help="Direct mask string (e.g. '??99')")
    parser.add_argument("--webhook", help="Discord webhook URL for live alerts")
    parser.add_argument("--webhook-interval", type=float, default=300.0, help="Periodic progress report interval in seconds (default: 300s = 5min)")
    parser.add_argument("--webhook-progress", dest="webhook_progress", action="store_true", default=None, help="Enable periodic status & progress report embed to Discord")
    parser.add_argument("--no-webhook-progress", dest="webhook_progress", action="store_false", help="Disable periodic status & progress report embed to Discord")
    parser.add_argument("--drive-dir", help="Path to Google Drive sync folder (e.g. /content/drive/MyDrive/D4UC)")
    parser.add_argument("--keys", help="Surfshark WireGuard private keys (comma-separated)")
    parser.add_argument("--config", "-c", help="Path to custom config.yaml file")
    parser.add_argument("--no-dashboard", action="store_true", help="Disable rich live dashboard and use plain streaming stdout logging")
    return parser.parse_args()

def apply_env_and_args_to_config(config: AppConfig, args) -> AppConfig:
    # 1. Environment variables (Docker, Colab & Termux Friendly)
    if "D4UC_MODE" in os.environ:
        config.target["mode"] = os.environ["D4UC_MODE"].strip().lower()
    if "D4UC_LENGTH" in os.environ:
        try:
            config.target["length"] = int(os.environ["D4UC_LENGTH"])
        except ValueError:
            pass
    if "D4UC_WORKERS" in os.environ:
        try:
            config.network["concurrency"] = int(os.environ["D4UC_WORKERS"])
        except ValueError:
            pass
    if "D4UC_PROXY" in os.environ:
        config.proxy["mode"] = os.environ["D4UC_PROXY"].strip().lower()
    if "D4UC_SHARD" in os.environ:
        config.target["shard_key"] = os.environ["D4UC_SHARD"].strip()
        config.target["mode"] = "permutation"
    if "D4UC_START_CHAR" in os.environ:
        config.target["start_char"] = os.environ["D4UC_START_CHAR"].strip()
        config.target["mode"] = "permutation"
    if "D4UC_END_CHAR" in os.environ:
        config.target["end_char"] = os.environ["D4UC_END_CHAR"].strip()
        config.target["mode"] = "permutation"
    if "D4UC_PREFIX" in os.environ:
        config.target["prefix"] = os.environ["D4UC_PREFIX"].strip()
    if "D4UC_SUFFIX" in os.environ:
        config.target["suffix"] = os.environ["D4UC_SUFFIX"].strip()
    if "D4UC_MIDDLE_DOT" in os.environ:
        config.target["middle_dot"] = os.environ["D4UC_MIDDLE_DOT"].strip()
    if "D4UC_MASK" in os.environ:
        config.target["mask"] = os.environ["D4UC_MASK"].strip()
    if "D4UC_WEBHOOK" in os.environ:
        wh = os.environ["D4UC_WEBHOOK"].strip()
        config.webhook["url"] = wh
        config.webhook["enabled"] = bool(wh)
    if "D4UC_WEBHOOK_INTERVAL" in os.environ:
        try:
            config.webhook["progress_interval"] = float(os.environ["D4UC_WEBHOOK_INTERVAL"])
        except ValueError:
            pass
    if "D4UC_WEBHOOK_PROGRESS" in os.environ:
        config.webhook["progress_enabled"] = os.environ["D4UC_WEBHOOK_PROGRESS"].strip().lower() in ("1", "true", "yes")
    if "D4UC_DRIVE_DIR" in os.environ:
        config.storage["drive_dir"] = os.environ["D4UC_DRIVE_DIR"].strip()
    if "SURFSHARK_PRIVATE_KEYS" in os.environ or "SURFSHARK_PRIVATE_KEY" in os.environ:
        ek = os.environ.get("SURFSHARK_PRIVATE_KEYS") or os.environ.get("SURFSHARK_PRIVATE_KEY")
        parsed_keys = [k.strip() for k in ek.replace(";", ",").replace("\n", ",").split(",") if k.strip()]
        if parsed_keys:
            config.proxy.setdefault("surfshark", {})["private_keys"] = parsed_keys
    if os.environ.get("D4UC_NO_DASHBOARD") or os.environ.get("NO_DASHBOARD"):
        config.ui["rich_dashboard"] = False

    # 2. CLI arguments (Highest priority)
    if args.mode:
        config.target["mode"] = args.mode.lower()
    if args.length:
        config.target["length"] = args.length
    if args.workers:
        config.network["concurrency"] = max(1, min(50, args.workers))
    if args.proxy:
        config.proxy["mode"] = args.proxy.lower()
    if args.shard:
        config.target["shard_key"] = args.shard
        config.target["mode"] = "permutation"
    if args.start_char:
        config.target["start_char"] = args.start_char
        config.target["mode"] = "permutation"
    if args.end_char:
        config.target["end_char"] = args.end_char
        config.target["mode"] = "permutation"
    if args.prefix:
        config.target["prefix"] = args.prefix
    if args.suffix:
        config.target["suffix"] = args.suffix
    if args.middle_dot:
        config.target["middle_dot"] = args.middle_dot
    if args.mask:
        config.target["mask"] = args.mask
    if args.webhook:
        config.webhook["url"] = args.webhook
        config.webhook["enabled"] = True
    if getattr(args, "webhook_interval", None):
        config.webhook["progress_interval"] = args.webhook_interval
    if getattr(args, "webhook_progress", None) is not None:
        config.webhook["progress_enabled"] = args.webhook_progress
    if getattr(args, "drive_dir", None):
        config.storage["drive_dir"] = args.drive_dir
    if args.keys:
        os.environ["SURFSHARK_PRIVATE_KEYS"] = args.keys
        parsed_keys = [k.strip() for k in args.keys.replace(";", ",").replace("\n", ",").split(",") if k.strip()]
        if parsed_keys:
            config.proxy.setdefault("surfshark", {})["private_keys"] = parsed_keys
    if getattr(args, "no_dashboard", False):
        config.ui["rich_dashboard"] = False

    return config

def main():
    args = parse_args()
    config_path = args.config if args.config else "config.yaml"
    config = AppConfig.load(config_path)
    config = apply_env_and_args_to_config(config, args)

    orch = Orchestrator(config, force_no_dashboard=args.no_dashboard)

    def handle_exit(sig, frame):
        orch.is_running = False

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    try:
        asyncio.run(orch.run())
    except KeyboardInterrupt:
        pass
    finally:
        console.print("\n[bold yellow]⏹️ 정상 종료되었습니다. 최종 데이터가 안전하게 저장되었습니다.[/bold yellow]")

if __name__ == "__main__":
    main()
