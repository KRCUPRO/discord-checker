# src/network/headers.py
from typing import Dict

def get_discord_headers(impersonate: str = "chrome131") -> Dict[str, str]:
    if "android" in impersonate.lower():
        return {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 15; Pixel 9) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Mobile Safari/537.36"
            ),
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/register",
            "X-Discord-Locale": "ko",
            "X-Discord-Timezone": "Asia/Seoul"
        }

    return {
        "Accept": "*/*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/register",
        "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24", "Google Chrome";v="131"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Discord-Locale": "ko",
        "X-Discord-Timezone": "Asia/Seoul",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
    }
