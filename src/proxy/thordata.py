# src/proxy/thordata.py
import random
import urllib.parse
from typing import Optional
from src.proxy.base import BaseProxyProvider, ProxyEndpoint

class ThorDataProxyProvider(BaseProxyProvider):
    def __init__(
        self,
        server: str,
        username: str,
        password: str,
        rotate_interval: int = 3
    ):
        self.server = server
        self.username = username
        self.password = password
        self.rotate_interval = rotate_interval
        self.request_counter = 0
        self.current_endpoint: Optional[ProxyEndpoint] = None
        self._renew_session()

    def _renew_session(self):
        session_id = random.randint(100000, 999999)
        quoted_user = urllib.parse.quote(self.username)
        quoted_pass = urllib.parse.quote(self.password)
        url = f"http://{quoted_user}:{quoted_pass}@{self.server}?session_id={session_id}"
        self.current_endpoint = ProxyEndpoint(
            url=url,
            provider_name="ThorData"
        )

    def get_proxy(self) -> Optional[ProxyEndpoint]:
        if not self.server or not self.username:
            return None

        self.request_counter += 1
        if self.request_counter % self.rotate_interval == 0 or not self.current_endpoint.is_available():
            self._renew_session()

        return self.current_endpoint

    def report_result(self, endpoint: ProxyEndpoint, success: bool, rate_limited: bool = False, cooldown: float = 15.0):
        if rate_limited:
            endpoint.mark_rate_limited(cooldown_seconds=cooldown)
            self._renew_session()
        elif success:
            endpoint.mark_success()
        else:
            endpoint.mark_failure()
            self._renew_session()

    def has_available_proxies(self) -> bool:
        return bool(self.server and self.username)
