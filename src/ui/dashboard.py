# src/ui/dashboard.py
import time
from typing import List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.live import Live

class DashboardMetrics:
    def __init__(self):
        self.total_checked = 0
        self.available_count = 0
        self.taken_count = 0
        self.rate_limited_count = 0
        self.error_count = 0
        self.skipped_count = 0
        self.start_time = time.time()
        self.recent_available: List[Tuple[str, str, float]] = [] # (username, pattern, latency)

    @property
    def rps(self) -> float:
        elapsed = time.time() - self.start_time
        return self.total_checked / elapsed if elapsed > 0 else 0.0

class RichDashboard:
    def __init__(self, console: Console, mode_str: str, length: int, concurrency: int, impersonate: str):
        self.console = console
        self.mode_str = mode_str
        self.length = length
        self.concurrency = concurrency
        self.impersonate = impersonate

    def generate_layout(self, metrics: DashboardMetrics, proxy_stats: Tuple[int, int, int]) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="stats", size=6),
            Layout(name="proxy", size=4),
            Layout(name="recent", size=8)
        )

        # 1. Header
        header_text = Text(
            f"⚡ Discord Username Checker V2 | 모드: {self.mode_str} | 자릿수: {self.length}자 | 동시성: {self.concurrency} | TLS: {self.impersonate}",
            style="bold cyan"
        )
        layout["header"].update(Panel(header_text, style="cyan"))

        # 2. Stats Table
        stats_table = Table(expand=True, box=None)
        stats_table.add_column("총 검사수", justify="center", style="bold white")
        stats_table.add_column("RPS (속도)", justify="center", style="bold yellow")
        stats_table.add_column("✅ 사용가능", justify="center", style="bold green")
        stats_table.add_column("❌ 사용중", justify="center", style="dim white")
        stats_table.add_column("⚠️ 429 쿨다운", justify="center", style="bold magenta")
        stats_table.add_column("💥 오류", justify="center", style="bold red")

        stats_table.add_row(
            f"{metrics.total_checked:,} 개",
            f"{metrics.rps:.1f} req/s",
            f"{metrics.available_count} 개",
            f"{metrics.taken_count:,} 개",
            f"{metrics.rate_limited_count} 회",
            f"{metrics.error_count} 회"
        )
        layout["stats"].update(Panel(stats_table, title="실시간 검사 지표", style="blue"))

        # 3. Proxy Status
        alive, cooldown, dead = proxy_stats
        total_p = alive + cooldown + dead
        health_ratio = (alive / total_p * 100.0) if total_p > 0 else 100.0
        proxy_text = Text(
            f"활성 프록시: {alive}개  |  429 쿨다운 대기: {cooldown}개  |  폐기(Dead): {dead}개  |  가용률: {health_ratio:.1f}%",
            style="bold green" if health_ratio > 80 else "bold yellow"
        )
        layout["proxy"].update(Panel(proxy_text, title="프록시 풀 인프라 상태", style="magenta"))

        # 4. Recent Available
        recent_table = Table(expand=True, box=None)
        recent_table.add_column("시각", style="dim")
        recent_table.add_column("사용자명", style="bold green")
        recent_table.add_column("패턴 분류", style="cyan")
        recent_table.add_column("응답 지연", style="yellow")

        if not metrics.recent_available:
            recent_table.add_row("-", "사용 가능 닉네임 탐색 중...", "-", "-")
        else:
            for item in metrics.recent_available[-4:]:
                recent_table.add_row(item[0], item[1], item[2], f"{item[3]:.1f}ms")

        layout["recent"].update(Panel(recent_table, title="최근 발견된 사용 가능 닉네임 (LIVE)", style="green"))

        return layout
