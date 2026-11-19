# src/proxy/manager.py
import os
from typing import Optional, List, Tuple
from src.proxy.base import BaseProxyProvider, ProxyEndpoint
from src.proxy.thordata import ThorDataProxyProvider
from src.proxy.file_pool import FileProxyProvider
from src.proxy.surfshark import SurfsharkProxyProvider
from src.proxy.free_proxy import FreeProxyProvider

class UnifiedProxyManager:
    def __init__(self, proxy_config: dict):
        self.config = proxy_config
        self.mode = proxy_config.get("mode", "direct").lower()
        self.cooldown_429 = float(proxy_config.get("health", {}).get("cooldown_429_seconds", 15.0))
        self.providers: List[BaseProxyProvider] = []
        self._provider_idx = 0
        self._init_providers()

    def _init_providers(self):
        if self.mode == "direct":
            return

        thordata_cfg = self.config.get("thordata", {})
        if self.mode in ("thordata", "hybrid") and thordata_cfg.get("enabled", False):
            if thordata_cfg.get("server") and thordata_cfg.get("username"):
                self.providers.append(
                    ThorDataProxyProvider(
                        server=thordata_cfg.get("server", ""),
                        username=thordata_cfg.get("username", ""),
                        password=thordata_cfg.get("password", ""),
                        rotate_interval=int(thordata_cfg.get("rotate_interval", 3))
                    )
                )

        file_cfg = self.config.get("file", {})
        if self.mode in ("file", "hybrid") and file_cfg.get("enabled", False):
            file_path = file_cfg.get("path", "proxies.txt")
            self.providers.append(
                FileProxyProvider(
                    file_path=file_path,
                    default_protocol=file_cfg.get("default_protocol", "http"),
                    shuffle=file_cfg.get("shuffle", True)
                )
            )

        free_cfg = self.config.get("free", {})
        if self.mode in ("free", "free_public") or (self.mode == "hybrid" and free_cfg.get("enabled", False)):
            free_prov = FreeProxyProvider(
                cache_file=free_cfg.get("cache_file", "data/free_proxies_verified.json"),
                max_latency_ms=float(free_cfg.get("max_latency_ms", 3500.0)),
                validation_timeout=float(free_cfg.get("validation_timeout", 2.5)),
                auto_refresh_minutes=int(free_cfg.get("auto_refresh_minutes", 15))
            )
            if free_cfg.get("auto_refresh", True):
                free_prov.start_auto_refresher()
            self.providers.append(free_prov)

        surfshark_cfg = self.config.get("surfshark", {})
        if self.mode in ("surfshark", "hybrid") or (self.mode not in ("direct", "file", "thordata", "free", "free_public")):
            warmup_delay = float(surfshark_cfg.get("warmup_delay", 1.0))
            self.providers.append(
                SurfsharkProxyProvider(
                    username=surfshark_cfg.get("username", ""),
                    password=surfshark_cfg.get("password", ""),
                    private_key=(
                        surfshark_cfg.get("private_keys")
                        or surfshark_cfg.get("private_key")
                        or os.environ.get("SURFSHARK_PRIVATE_KEYS")
                        or os.environ.get("SURFSHARK_PRIVATE_KEY", "YOUR_WIREGUARD_PRIVATE_KEY_HERE")
                    ),
                    preferred_countries=surfshark_cfg.get("preferred_countries", []),
                    http_port=int(surfshark_cfg.get("http_port", 1081)),
                    socks5_port=int(surfshark_cfg.get("socks5_port", 1080)),
                    warmup_delay=warmup_delay
                )
            )

    def get_surfshark_provider(self) -> Optional[SurfsharkProxyProvider]:
        for p in self.providers:
            if isinstance(p, SurfsharkProxyProvider):
                return p
        return None

    def get_free_provider(self) -> Optional[FreeProxyProvider]:
        for p in self.providers:
            if isinstance(p, FreeProxyProvider):
                return p
        return None

    def lease_proxy(self, worker_id: int = 1) -> Optional[ProxyEndpoint]:
        if not self.providers:
            return None

        total = len(self.providers)
        for _ in range(total):
            provider = self.providers[self._provider_idx]
            self._provider_idx = (self._provider_idx + 1) % total
            if isinstance(provider, SurfsharkProxyProvider):
                endpoint = provider.get_proxy(worker_id=worker_id)
            else:
                endpoint = provider.get_proxy()
            if endpoint:
                return endpoint

        return None

    def release_proxy(self, endpoint: Optional[ProxyEndpoint], success: bool, rate_limited: bool = False):
        if not endpoint:
            return

        for provider in self.providers:
            provider.report_result(
                endpoint=endpoint,
                success=success,
                rate_limited=rate_limited,
                cooldown=self.cooldown_429
            )

    def get_pool_summary(self) -> Tuple[int, int, int]:
        """Returns aggregated (alive, cooldown, dead) count"""
        if not self.providers:
            return 0, 0, 0

        alive_sum, cooldown_sum, dead_sum = 0, 0, 0
        for p in self.providers:
            if isinstance(p, FileProxyProvider):
                a, c, d = p.get_stats()
                alive_sum += a
                cooldown_sum += c
                dead_sum += d
            elif isinstance(p, FreeProxyProvider):
                a, c, d = p.get_stats_tuple()
                alive_sum += a
                cooldown_sum += c
                dead_sum += d
            elif isinstance(p, ThorDataProxyProvider):
                if p.has_available_proxies():
                    alive_sum += 1
            elif isinstance(p, SurfsharkProxyProvider):
                alive_sum += len(p.clusters)
        return alive_sum, cooldown_sum, dead_sum

    def is_rotating(self, worker_id: int = 1) -> bool:
        for p in self.providers:
            if isinstance(p, SurfsharkProxyProvider):
                if p.is_rotating(worker_id=worker_id):
                    return True
        return False

    def wait_until_ready(self, worker_id: int = 1, timeout: float = 6.0) -> bool:
        for p in self.providers:
            if isinstance(p, SurfsharkProxyProvider):
                return p.wait_until_ready(worker_id=worker_id, timeout=timeout)
        return True

    def rotate_surfshark(self, worker_id: int = 1, cooldown_seconds: float = 300.0):
        for p in self.providers:
            if isinstance(p, SurfsharkProxyProvider):
                return p.rotate_cluster(worker_id=worker_id, cooldown_seconds=cooldown_seconds)
        return None

    def close(self):
        for provider in self.providers:
            if hasattr(provider, "stop"):
                provider.stop()
