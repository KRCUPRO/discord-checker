# src/notify/webhook.py
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from curl_cffi.requests import AsyncSession
from src.network.client import CheckResult

class DiscordWebhookNotifier:
    """
    Discord Webhook Notifier
    - '된거' (AVAILABLE) 실시간 알림 (초록색 임베드 + @here 멘션)
    - '안된거' / 진행상황 (PROGRESS) 주기적 리포트 (통계, RPS, 사용중, 429)
    - 세션 라이프사이클 (START / STOP) 알림
    """
    def __init__(
        self,
        webhook_url: str,
        enabled: bool = True,
        mention: str = "@here",
        notify_only_available: bool = True
    ):
        self.webhook_url = webhook_url.strip() if webhook_url else ""
        self.enabled = enabled and bool(self.webhook_url)
        self.mention = mention
        self.notify_only_available = notify_only_available

    async def _post(self, payload: Dict[str, Any], session: Optional[AsyncSession] = None) -> bool:
        if not self.enabled or not self.webhook_url:
            return False

        try:
            if session is not None:
                resp = await session.post(
                    self.webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=6.0
                )
                return resp.status_code in (200, 204)
            else:
                async with AsyncSession() as temp_session:
                    resp = await temp_session.post(
                        self.webhook_url,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=6.0
                    )
                    return resp.status_code in (200, 204)
        except Exception:
            return False

    async def send_alert(self, result: CheckResult, session: Optional[AsyncSession] = None) -> bool:
        """
        '된거' (AVAILABLE) 희귀 닉네임 발견 시 실시간 전송
        """
        embed = {
            "title": "🎉 희귀 Discord 사용자명 발견! (Available)",
            "description": f"사용 가능한 고유 사용자명 **`{result.username}`**을(를) 확인했습니다.",
            "color": 0x00FF7F,  # Spring Green
            "fields": [
                {"name": "사용자명", "value": f"`{result.username}`", "inline": True},
                {"name": "글자수", "value": f"{len(result.username)}자리", "inline": True},
                {"name": "패턴 유형", "value": f"`{result.pattern_type}`", "inline": True},
                {"name": "응답 지연", "value": f"{result.latency_ms:.1f} ms", "inline": True},
                {"name": "발견 시각", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True},
                {"name": "등록 바로가기", "value": "[Discord 회원가입](https://discord.com/register)", "inline": False}
            ],
            "footer": {"text": "D4UC High-Performance Engine • Cloud Edition"}
        }

        payload = {
            "content": self.mention if self.mention else None,
            "embeds": [embed]
        }
        return await self._post(payload, session)

    async def notify_available(self, session: Optional[AsyncSession], result: CheckResult) -> bool:
        """하위 호환성 별칭"""
        return await self.send_alert(result, session)

    async def send_progress_report(
        self,
        total_checked: int,
        available_count: int,
        taken_count: int,
        rate_limited_count: int,
        skipped_count: int,
        rps: float,
        mode: str = "HYBRID",
        length: int = 4,
        workers: int = 5,
        drive_status: str = "정상 동기화 중",
        session: Optional[AsyncSession] = None
    ) -> bool:
        """
        '안된거' 및 주기적 진행 상황 종합 리포트 전송 (Heartbeat)
        """
        embed = {
            "title": "📊 D4UC 클라우드 검사 진행 상황 종합 리포트",
            "description": f"D4UC 엔진이 클라우드에서 정상 가동 중입니다. (속도: **{rps:.1f} req/s**)",
            "color": 0x5865F2,  # Discord Blurple
            "fields": [
                {"name": "총 검사 완료", "value": f"**{total_checked:,}** 건", "inline": True},
                {"name": "🟢 가용 닉네임 (된거)", "value": f"**{available_count}** 개", "inline": True},
                {"name": "🔴 사용 중 (안된거)", "value": f"{taken_count:,} 건", "inline": True},
                {"name": "⚠️ 429 레이트리밋", "value": f"{rate_limited_count} 회", "inline": True},
                {"name": "⚡ 중복 건너뜀 (스킵)", "value": f"{skipped_count:,} 건", "inline": True},
                {"name": "🛡️ Google Drive 동기화", "value": f"`{drive_status}`", "inline": True},
                {"name": "⚙️ 동작 조건", "value": f"모드: `{mode.upper()}` | `{length}자리` | 워커 `{workers}개`", "inline": False}
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "footer": {"text": "D4UC Continuous Monitoring • 5분 주기 자동 리포트"}
        }

        payload = {
            "embeds": [embed]
        }
        return await self._post(payload, session)

    async def send_session_start(
        self,
        mode: str,
        length: int,
        workers: int,
        proxy_mode: str,
        shard: Optional[str] = None,
        drive_enabled: bool = False,
        session: Optional[AsyncSession] = None
    ) -> bool:
        """
        세션 시작 알림
        """
        embed = {
            "title": "🚀 D4UC 클라우드 검사 세션 가동 시작",
            "description": "구글 코랩 / 클라우드 환경에서 D4UC 검사 엔진이 성공적으로 기동되었습니다.",
            "color": 0x00BFFF,  # Deep Sky Blue
            "fields": [
                {"name": "탐색 모드", "value": f"`{mode.upper()}` ({length}자리)", "inline": True},
                {"name": "동시성", "value": f"워커 `{workers}`개", "inline": True},
                {"name": "프록시 모드", "value": f"`{proxy_mode}`", "inline": True},
                {"name": "다중 샤딩 분할", "value": f"`{shard if shard else '전체 탐색'}`", "inline": True},
                {"name": "Google Drive 백업", "value": f"`{'활성화됨 (/D4UC/)' if drive_enabled else '비활성'}`", "inline": True},
                {"name": "시작 시각", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True}
            ],
            "footer": {"text": "D4UC Cloud Lifecycle Manager"}
        }

        payload = {
            "embeds": [embed]
        }
        return await self._post(payload, session)

    async def send_session_stop(
        self,
        total_checked: int,
        available_count: int,
        taken_count: int,
        rate_limited_count: int,
        drive_path: Optional[str] = None,
        session: Optional[AsyncSession] = None
    ) -> bool:
        """
        세션 종료 및 최종 통계 알림
        """
        desc = "D4UC 검사 세션이 정상적으로 종료되었습니다."
        if drive_path:
            desc += f"\n모든 결과가 Google Drive(`{drive_path}`)에 안전하게 보존되었습니다."

        embed = {
            "title": "🛑 D4UC 검사 세션 종료 및 최종 결과 통계",
            "description": desc,
            "color": 0xFFA500,  # Orange
            "fields": [
                {"name": "총 검사 수", "value": f"**{total_checked:,}** 건", "inline": True},
                {"name": "🎉 발견된 가용 닉네임", "value": f"**{available_count}** 개", "inline": True},
                {"name": "사용 중 닉네임", "value": f"{taken_count:,} 건", "inline": True},
                {"name": "429 레이트리밋 발생", "value": f"{rate_limited_count} 회", "inline": True},
                {"name": "종료 시각", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": False}
            ],
            "footer": {"text": "D4UC Session Summary Report"}
        }

        payload = {
            "embeds": [embed]
        }
        return await self._post(payload, session)
