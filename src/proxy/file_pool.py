# src/proxy/file_pool.py
import random
import time
from pathlib import Path
from typing import List, Optional
from src.proxy.base import BaseProxyProvider, ProxyEndpoint

class FileProxyProvider(BaseProxyProvider):
    def __init__(
        self,
        file_path: str = "proxies.txt",
        default_protocol: str = "http",
        shuffle: bool = True
    ):
        self.file_path = Path(file_path)
        self.default_protocol = default_protocol
        self.shuffle = shuffle
        self.endpoints: List[ProxyEndpoint] = []
        self._index = 0
        self.load_proxies()

    def _normalize_line(self, line: str) -> Optional[str]:
        line = line.strip()
        if not line or line.startswith("#"):
            return None

        # Already has protocol scheme
        if "://" in line:
            return line

        parts = line.split(":")
        # Format: host:port
        if len(parts) == 2:
            return f"{self.default_protocol}://{parts[0]}:{parts[1]}"
        # Format: host:port:user:pass
        elif len(parts) == 4:
            host, port, user, password = parts
            return f"{self.default_protocol}://{user}:{password}@{host}:{port}"
        # Format: user:pass@host:port
        elif "@" in line:
            return f"{self.default_protocol}://{line}"

        return None

    def load_proxies(self):
        if not self.file_path.exists():
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                norm = self._normalize_line(line)
                if norm:
                    self.endpoints.append(ProxyEndpoint(url=norm, provider_name="FilePool"))

        if self.shuffle:
            random.shuffle(self.endpoints)

    def get_proxy(self) -> Optional[ProxyEndpoint]:
        if not self.endpoints:
            return None

        total = len(self.endpoints)
        now = time.time()
        for _ in range(total):
            endpoint = self.endpoints[self._index]
            self._index = (self._index + 1) % total
            if endpoint.is_available():
                return endpoint

        # If none currently ready, return the one closest to expiring cooldown
        alive = [ep for ep in self.endpoints if not ep.is_dead]
        if alive:
            alive.sort(key=lambda ep: ep.cooldown_until)
            return alive[0]

        return None

    def report_result(self, endpoint: ProxyEndpoint, success: bool, rate_limited: bool = False, cooldown: float = 15.0):
        if rate_limited:
            endpoint.mark_rate_limited(cooldown_seconds=cooldown)
        elif success:
            endpoint.mark_success()
        else:
            endpoint.mark_failure()

    def has_available_proxies(self) -> bool:
        return any(not ep.is_dead for ep in self.endpoints)

    def get_stats(self) -> tuple[int, int, int]:
        """Returns (alive_count, cooldown_count, dead_count)"""
        alive = 0
        cooldown = 0
        dead = 0
        now = time.time()
        for ep in self.endpoints:
            if ep.is_dead:
                dead += 1
            elif ep.cooldown_until > now:
                cooldown += 1
            else:
                alive += 1
        return alive, cooldown, dead
