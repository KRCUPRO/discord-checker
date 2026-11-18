# src/notify/webhook.py
import json
from datetime import datetime
from typing import Optional
from curl_cffi.requests import AsyncSession
from src.network.client import CheckResult

class DiscordWebhookNotifier:
    def __init__(
        self,
        webhook_url: str,
        enabled: bool = True,
        mention: str = "@here",
        notify_only_available: bool = True
    ):
        self.webhook_url = webhook_url
        self.enabled = enabled and bool(webhook_url)
        self.mention = mention
        self.notify_only_available = notify_only_available

    async def notify_available(self, session: AsyncSession, result: CheckResult):
        if not self.enabled or not self.webhook_url:
            return

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
            "footer": {"text": "Discord Username Checker V2 • Bug Bounty Edition"}
        }

        payload = {
            "content": self.mention if self.mention else None,
            "embeds": [embed]
        }

        try:
            await session.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5.0
            )
        except Exception:
            pass
