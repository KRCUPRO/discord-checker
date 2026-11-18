# src/network/client.py
import time
import json
from typing import Optional, Tuple, Dict, Any
from enum import Enum
from curl_cffi.requests import AsyncSession
from src.network.headers import get_discord_headers
from src.network.exceptions import (
    RateLimitedException,
    WafBlockedException,
    ProxyFailedException,
    InvalidUsernameException
)

API_ENDPOINT = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

class CheckStatus(str, Enum):
    AVAILABLE = "available"
    TAKEN = "taken"
    RATE_LIMITED = "rate_limited"
    WAF_BLOCKED = "waf_blocked"
    INVALID = "invalid"
    ERROR = "error"

class CheckResult:
    def __init__(
        self,
        username: str,
        status: CheckStatus,
        latency_ms: float = 0.0,
        proxy_used: Optional[str] = None,
        error_message: Optional[str] = None,
        pattern_type: str = "random"
    ):
        self.username = username
        self.status = status
        self.latency_ms = latency_ms
        self.proxy_used = proxy_used
        self.error_message = error_message
        self.pattern_type = pattern_type

    def is_available(self) -> bool:
        return self.status == CheckStatus.AVAILABLE

class DiscordApiClient:
    def __init__(
        self,
        impersonate: str = "chrome131",
        timeout: float = 4.0
    ):
        self.impersonate = impersonate
        self.timeout = timeout
        self.headers = get_discord_headers(impersonate=impersonate)

    async def check(
        self,
        session: AsyncSession,
        username: str,
        proxy: Optional[str] = None,
        pattern_type: str = "random",
        require_proxy: bool = False
    ) -> CheckResult:
        if require_proxy and not proxy:
            raise ProxyFailedException("Zero Host Leak Hard Gate: Direct connection strictly blocked when proxy is required.")

        payload = {"username": username}
        kwargs: Dict[str, Any] = {
            "headers": self.headers,
            "json": payload,
            "timeout": self.timeout,
            "impersonate": self.impersonate
        }

        if proxy:
            kwargs["proxy"] = proxy

        start_time = time.perf_counter()
        try:
            resp = await session.post(API_ENDPOINT, **kwargs)
            latency_ms = (time.perf_counter() - start_time) * 1000.0

            if resp.status_code == 200:
                try:
                    data = resp.json()
                except Exception:
                    return CheckResult(
                        username=username,
                        status=CheckStatus.ERROR,
                        latency_ms=latency_ms,
                        proxy_used=proxy,
                        error_message="Invalid JSON response",
                        pattern_type=pattern_type
                    )

                if "taken" not in data:
                    return CheckResult(
                        username=username,
                        status=CheckStatus.ERROR,
                        latency_ms=latency_ms,
                        proxy_used=proxy,
                        error_message="Missing 'taken' key in response",
                        pattern_type=pattern_type
                    )

                status = CheckStatus.AVAILABLE if not data["taken"] else CheckStatus.TAKEN
                return CheckResult(
                    username=username,
                    status=status,
                    latency_ms=latency_ms,
                    proxy_used=proxy,
                    pattern_type=pattern_type
                )

            elif resp.status_code == 429:
                retry_after = 1.0
                try:
                    data = resp.json()
                    retry_after = float(data.get("retry_after", 1.0))
                except Exception:
                    pass
                raise RateLimitedException(retry_after=retry_after)

            elif resp.status_code == 403:
                raise WafBlockedException("Cloudflare WAF / 403 Forbidden")

            elif resp.status_code == 400:
                # Reserved, illegal characters or length violation
                return CheckResult(
                    username=username,
                    status=CheckStatus.INVALID,
                    latency_ms=latency_ms,
                    proxy_used=proxy,
                    error_message="400 Bad Request (Reserved or Invalid)",
                    pattern_type=pattern_type
                )

            else:
                return CheckResult(
                    username=username,
                    status=CheckStatus.ERROR,
                    latency_ms=latency_ms,
                    proxy_used=proxy,
                    error_message=f"HTTP {resp.status_code}",
                    pattern_type=pattern_type
                )

        except (RateLimitedException, WafBlockedException) as e:
            raise e
        except Exception as e:
            err_str = repr(e).lower()
            if "proxy" in err_str or "connect" in err_str:
                raise ProxyFailedException(str(e))
            return CheckResult(
                username=username,
                status=CheckStatus.ERROR,
                latency_ms=(time.perf_counter() - start_time) * 1000.0,
                proxy_used=proxy,
                error_message=repr(e),
                pattern_type=pattern_type
            )
