# src/proxy/free_proxy.py
"""
Free Public Proxy Scraper & Live Multi-Threaded Validator Engine.
Scrapes reliable, continually updated open-source proxy lists from GitHub and public endpoints,
validates candidate proxies via high-speed asynchronous connection tests against real Discord/Cloudflare
endpoints, filters out dead, high-latency (>3500ms), or 403-blocked proxies, and provides round-robin
leasing, 429 cooldowns, and automatic background pool refresh.
"""

import asyncio
import json
import logging
import os
import re
import threading
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

from curl_cffi.requests import AsyncSession
from src.proxy.base import BaseProxyProvider, ProxyEndpoint
from src.utils.paths import resolve_resource, resolve_output_path

logger = logging.getLogger("D4UC.FreeProxy")

# Verified reliable open-source proxy sources (HTTP, HTTPS, SOCKS4, SOCKS5)
PUBLIC_PROXY_SOURCES = [
    # monosans repository (updated hourly)
    {"url": "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt", "protocol": "http", "label": "monosans-HTTP"},
    {"url": "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt", "protocol": "socks5", "label": "monosans-SOCKS5"},
    {"url": "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt", "protocol": "socks4", "label": "monosans-SOCKS4"},
    # TheSpeedX repository (continually updated)
    {"url": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "protocol": "http", "label": "TheSpeedX-HTTP"},
    {"url": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt", "protocol": "socks5", "label": "TheSpeedX-SOCKS5"},
    {"url": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt", "protocol": "socks4", "label": "TheSpeedX-SOCKS4"},
    # proxifly 11,000+ proxy multi-protocol pool
    {"url": "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt", "protocol": "http", "label": "proxifly-ALL"},
    # vakhov fresh proxy list (hourly refreshed)
    {"url": "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt", "protocol": "http", "label": "vakhov-HTTP"},
    {"url": "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt", "protocol": "socks5", "label": "vakhov-SOCKS5"},
    {"url": "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt", "protocol": "socks4", "label": "vakhov-SOCKS4"},
    # zloi-user hideip.me verified lists (15-min interval)
    {"url": "https://raw.githubusercontent.com/zloi-user/hideip.me/master/http.txt", "protocol": "http", "label": "zloi-HTTP"},
    {"url": "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks5.txt", "protocol": "socks5", "label": "zloi-SOCKS5"},
    {"url": "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks4.txt", "protocol": "socks4", "label": "zloi-SOCKS4"},
    # hookzof SOCKS5 repository
    {"url": "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt", "protocol": "socks5", "label": "hookzof-SOCKS5"},
    # roosterkid OpenProxyList
    {"url": "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt", "protocol": "https", "label": "roosterkid-HTTPS"},
    {"url": "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt", "protocol": "socks5", "label": "roosterkid-SOCKS5"},
    # ShiftyTR Proxy-List
    {"url": "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt", "protocol": "https", "label": "ShiftyTR-HTTPS"},
    # sunny9577 Proxy-Scraper (hourly generated)
    {"url": "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt", "protocol": "http", "label": "sunny9577-HTTP"},
]

DISCORD_CHECK_ENDPOINT = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
CLOUDFLARE_TRACE_ENDPOINT = "https://cloudflare.com/cdn-cgi/trace"

IP_PORT_PATTERN = re.compile(
    r"^(?:(?P<proto>https?|socks[45])://)?(?:(?P<user>[^:@]+):(?P<pass>[^@]+)@)?(?P<host>[0-9]{1,3}(?:\.[0-9]{1,3}){3}):(?P<port>[0-9]{1,5})$"
)
HOST_PORT_USER_PASS_PATTERN = re.compile(
    r"^(?P<host>[0-9]{1,3}(?:\.[0-9]{1,3}){3}):(?P<port>[0-9]{1,5}):(?P<user>[^:]+):(?P<pass>.+)$"
)


@dataclass
class VerifiedProxyData:
    url: str
    protocol: str
    host: str
    port: int
    latency_ms: float
    source: str
    country: str = "??"
    verified_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "protocol": self.protocol,
            "host": self.host,
            "port": self.port,
            "latency_ms": round(self.latency_ms, 1),
            "source": self.source,
            "country": self.country,
            "verified_at": self.verified_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VerifiedProxyData":
        return cls(
            url=data["url"],
            protocol=data.get("protocol", "http"),
            host=data.get("host", ""),
            port=int(data.get("port", 0)),
            latency_ms=float(data.get("latency_ms", 999.0)),
            source=data.get("source", "cache"),
            country=data.get("country", "??"),
            verified_at=float(data.get("verified_at", time.time())),
        )


def parse_proxy_line(line: str, default_protocol: str = "http", source_label: str = "unknown") -> Optional[Tuple[str, str, str, int]]:
    """
    Parses a single raw line into (normalized_url, protocol, host, port).
    Supports formats:
      - host:port
      - protocol://host:port
      - host:port:user:pass
      - protocol://user:pass@host:port
    Note: For 'https' proxy lists, libcurl requires 'http://host:port' to establish HTTP CONNECT tunnels.
    """
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("//"):
        return None

    # Format: host:port:user:pass
    m_quad = HOST_PORT_USER_PASS_PATTERN.match(line)
    if m_quad:
        host = m_quad.group("host")
        port = int(m_quad.group("port"))
        user = m_quad.group("user")
        pwd = m_quad.group("pass")
        proto = default_protocol.lower()
        if 1 <= port <= 65535:
            # Normalize https to http for curl proxy url
            scheme = "http" if proto == "https" else proto
            url = f"{scheme}://{user}:{pwd}@{host}:{port}"
            return url, proto, host, port

    # Format: [proto://][user:pass@]host:port
    m = IP_PORT_PATTERN.match(line)
    if m:
        host = m.group("host")
        port = int(m.group("port"))
        proto = (m.group("proto") or default_protocol).lower()
        user = m.group("user")
        pwd = m.group("pass")
        if 1 <= port <= 65535:
            # Normalize https to http for curl proxy url
            scheme = "http" if proto == "https" else proto
            if user and pwd:
                url = f"{scheme}://{user}:{pwd}@{host}:{port}"
            else:
                url = f"{scheme}://{host}:{port}"
            return url, proto, host, port

    return None


def fetch_source_sync(source: Dict[str, str], timeout: float = 6.0) -> List[Tuple[str, str, str, int]]:
    """Fetches candidate proxies from a single remote source URL synchronously."""
    url = source["url"]
    protocol = source.get("protocol", "http")
    label = source.get("label", url)
    results: List[Tuple[str, str, str, int]] = []
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/plain, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_text = resp.read().decode("utf-8", errors="ignore")
            for line in raw_text.splitlines():
                parsed = parse_proxy_line(line, default_protocol=protocol, source_label=label)
                if parsed:
                    results.append(parsed)
    except Exception as e:
        logger.debug("Failed to fetch proxy source %s: %s", url, e)
    return results


class FreeProxyScraper:
    """Scrapes raw public proxy lists from multiple GitHub, Hugging Face, and public sources."""

    def __init__(self, sources: Optional[List[Dict[str, str]]] = None):
        self.sources = sources or PUBLIC_PROXY_SOURCES

    def scrape_all(self, max_candidates_per_source: int = 1500) -> List[Tuple[str, str, str, int, str]]:
        """
        Scrapes all sources in parallel and returns deduplicated candidates:
        List of (url, protocol, host, port, source_label)
        """
        seen: Set[str] = set()
        candidates: List[Tuple[str, str, str, int, str]] = []

        threads: List[threading.Thread] = []
        source_results: Dict[str, List[Tuple[str, str, str, int]]] = {}

        def _worker(s: Dict[str, str]):
            lbl = s.get("label", s["url"])
            res = fetch_source_sync(s)
            source_results[lbl] = res[:max_candidates_per_source]

        for src in self.sources:
            t = threading.Thread(target=_worker, args=(src,), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=8.0)

        for src in self.sources:
            lbl = src.get("label", src["url"])
            items = source_results.get(lbl, [])
            for item in items:
                url, proto, host, port = item
                key = f"{host}:{port}"
                if key not in seen:
                    seen.add(key)
                    candidates.append((url, proto, host, port, lbl))

        return candidates


class FreeProxyValidator:
    """High-speed asynchronous connection tester verifying non-blocked Discord/Cloudflare status."""

    def __init__(
        self,
        timeout: float = 2.5,
        max_latency_ms: float = 3500.0,
        impersonate: str = "chrome131",
    ):
        self.timeout = timeout
        self.max_latency_ms = max_latency_ms
        self.impersonate = impersonate

    async def test_single_proxy(
        self,
        candidate_url: str,
        protocol: str,
        host: str,
        port: int,
        source: str,
        session: AsyncSession,
    ) -> Optional[VerifiedProxyData]:
        """
        Tests a candidate proxy against Discord and Cloudflare endpoints.
        Primary: Tests Cloudflare CDN Edge Trace endpoint (lightweight GET, validates HTTPS tunneling,
                 confirms non-blocked WAF status, measures real latency, and extracts country location).
        Secondary: Tests Discord username attempt endpoint (POST) for direct Discord API validation.
        Filters out dead, high-latency (>max_latency_ms), connection-failed, and 403 Cloudflare WAF blocked proxies.
        """
        # Primary check: Cloudflare CDN Edge Trace
        try:
            t0 = time.perf_counter()
            resp = await session.get(
                CLOUDFLARE_TRACE_ENDPOINT,
                proxy=candidate_url,
                timeout=self.timeout,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000.0

            if elapsed_ms <= self.max_latency_ms and resp.status_code == 200 and "visit_scheme=" in getattr(resp, "text", ""):
                country = "??"
                for line in resp.text.splitlines():
                    if line.startswith("loc="):
                        country = line.split("=", 1)[1].strip()
                        break
                return VerifiedProxyData(
                    url=candidate_url,
                    protocol=protocol,
                    host=host,
                    port=port,
                    latency_ms=elapsed_ms,
                    source=source,
                    country=country,
                    verified_at=time.time(),
                )
        except Exception:
            pass

        # Secondary check: Discord username check endpoint (e.g. unit test mocks or Discord-specific testing)
        t0 = time.perf_counter()
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }
        payload = {"username": "d4uc_free_probe_chk"}

        try:
            resp = await session.post(
                DISCORD_CHECK_ENDPOINT,
                headers=headers,
                json=payload,
                proxy=candidate_url,
                timeout=self.timeout,
                impersonate=self.impersonate,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000.0

            if elapsed_ms > self.max_latency_ms:
                return None

            # Status 200: Successfully reached Discord API through Cloudflare!
            # Status 400: Discord API responded with bad request / invalid format (also unblocked)
            if resp.status_code in (200, 400):
                try:
                    data = resp.json() if callable(getattr(resp, "json", None)) else resp.json
                    if isinstance(data, dict) and ("taken" in data or "message" in data or "code" in data):
                        return VerifiedProxyData(
                            url=candidate_url,
                            protocol=protocol,
                            host=host,
                            port=port,
                            latency_ms=elapsed_ms,
                            source=source,
                            country="??",
                            verified_at=time.time(),
                        )
                except Exception:
                    pass

            return None

        except Exception:
            return None

    async def validate_batch(
        self,
        candidates: List[Tuple[str, str, str, int, str]],
        concurrency: int = 40,
        progress_cb: Optional[Any] = None,
        max_verified_needed: int = 150,
    ) -> List[VerifiedProxyData]:
        """
        Validates candidate proxies concurrently using an async worker pool.
        Stops early once max_verified_needed is satisfied or all candidates are tested.
        """
        sem = asyncio.Semaphore(concurrency)
        verified_results: List[VerifiedProxyData] = []
        lock = asyncio.Lock()
        total_checked = 0
        total_count = len(candidates)

        async with AsyncSession(impersonate=self.impersonate) as session:
            async def _check_item(item):
                nonlocal total_checked
                if len(verified_results) >= max_verified_needed:
                    return

                url, proto, host, port, src = item
                async with sem:
                    res = await self.test_single_proxy(url, proto, host, port, src, session)
                    async with lock:
                        total_checked += 1
                        if res:
                            verified_results.append(res)
                        if progress_cb:
                            try:
                                progress_cb(total_checked, len(verified_results), total_count)
                            except Exception:
                                pass

            tasks = [_check_item(c) for c in candidates]
            # Execute tasks
            await asyncio.gather(*tasks, return_exceptions=True)

        # Sort verified proxies by lowest latency
        verified_results.sort(key=lambda x: x.latency_ms)
        return verified_results


class FreeProxyProvider(BaseProxyProvider):
    """
    Unified Free Public Proxy Provider implementing BaseProxyProvider.
    Features:
      - Mode: 'free' / 'free_public'
      - High-speed async validation against Discord / Cloudflare
      - Round-robin leasing with lowest-latency prioritization
      - 429 hot-swap rotation & cooldown isolation
      - Persistent JSON caching for instant cold restarts
      - Background auto-refresher thread when pool degrades
    """

    def __init__(
        self,
        cache_file: str = "data/free_proxies_verified.json",
        max_latency_ms: float = 3500.0,
        validation_timeout: float = 2.5,
        auto_refresh_minutes: int = 15,
        min_pool_size: int = 5,
        max_pool_size: int = 100,
    ):
        self.cache_path = resolve_output_path(cache_file)
        self.max_latency_ms = max_latency_ms
        self.validation_timeout = validation_timeout
        self.auto_refresh_interval = max(60.0, float(auto_refresh_minutes * 60))
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size

        self.scraper = FreeProxyScraper()
        self.validator = FreeProxyValidator(
            timeout=self.validation_timeout,
            max_latency_ms=self.max_latency_ms,
        )

        self.endpoints: List[ProxyEndpoint] = []
        self._verified_data: Dict[str, VerifiedProxyData] = {}
        self._index: int = 0
        self._lock = threading.RLock()

        self.is_scraping: bool = False
        self.last_scraped_time: Optional[float] = None
        self.total_scraped_candidates: int = 0
        self.verified_active_count: int = 0

        self._auto_refresher_running: bool = False
        self._refresher_thread: Optional[threading.Thread] = None

        # Load persisted proxies from disk if available
        self.load_cache()

    def load_cache(self):
        """Loads cached verified proxies from disk."""
        with self._lock:
            if not self.cache_path.exists():
                return
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        now = time.time()
                        for item in data:
                            vp = VerifiedProxyData.from_dict(item)
                            # Only keep cache entries from the last 24 hours
                            if (now - vp.verified_at) < 86400:
                                self._verified_data[vp.url] = vp
                                ep_label = f"FreePublic [{vp.country} - {vp.host}:{vp.port}] ({vp.latency_ms:.0f}ms)"
                                ep = ProxyEndpoint(url=vp.url, provider_name=ep_label)
                                self.endpoints.append(ep)
                        self.verified_active_count = len(self.endpoints)
                        logger.info("Loaded %d verified free proxies from cache: %s", len(self.endpoints), self.cache_path)
            except Exception as e:
                logger.warning("Failed to load free proxy cache: %s", e)

    def save_cache(self):
        """Persists currently verified proxies to disk."""
        with self._lock:
            try:
                self.cache_path.parent.mkdir(parents=True, exist_ok=True)
                export_list = [vp.to_dict() for vp in self._verified_data.values()]
                with open(self.cache_path, "w", encoding="utf-8") as f:
                    json.dump(export_list, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.warning("Failed to save free proxy cache: %s", e)

    def get_proxy(self) -> Optional[ProxyEndpoint]:
        """
        Leases an available proxy endpoint with round-robin rotation.
        If all proxies are cooling down, returns the one whose cooldown will expire soonest.
        If pool is completely empty, triggers synchronous or cached lease.
        """
        with self._lock:
            if not self.endpoints:
                if not self.is_scraping:
                    self.trigger_background_scrape()
                return None

            total = len(self.endpoints)
            now = time.time()

            # 1. Round-robin search for immediately available proxy
            for _ in range(total):
                ep = self.endpoints[self._index]
                self._index = (self._index + 1) % total
                if ep.is_available():
                    return ep

            # 2. If all ready are cooling down, return the one closest to expiring cooldown
            alive = [ep for ep in self.endpoints if not ep.is_dead]
            if alive:
                alive.sort(key=lambda x: x.cooldown_until)
                return alive[0]

            # 3. If alive count is below threshold, trigger background scrape if not running
            if len(alive) < self.min_pool_size and not self.is_scraping:
                self.trigger_background_scrape()

            return None

    def report_result(
        self,
        endpoint: ProxyEndpoint,
        success: bool,
        rate_limited: bool = False,
        cooldown: float = 15.0,
    ):
        """Handles result reporting, 429 rate limit cooldown, and dead proxy removal."""
        with self._lock:
            if rate_limited:
                endpoint.mark_rate_limited(cooldown_seconds=cooldown)
            elif success:
                endpoint.mark_success()
            else:
                endpoint.mark_failure(max_fails=2)
                if endpoint.is_dead:
                    # Remove from active verified data
                    self._verified_data.pop(endpoint.url, None)
                    self.verified_active_count = sum(1 for ep in self.endpoints if not ep.is_dead)

    def has_available_proxies(self) -> bool:
        """Returns True if at least one proxy in the pool is alive."""
        with self._lock:
            return any(not ep.is_dead for ep in self.endpoints)

    def get_stats_tuple(self) -> Tuple[int, int, int]:
        """Returns (alive_count, cooldown_count, dead_count)."""
        with self._lock:
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

    def get_stats(self) -> Dict[str, Any]:
        """Returns comprehensive telemetry dictionary for Web API and GUI."""
        with self._lock:
            alive, cooldown, dead = self.get_stats_tuple()
            latencies = [vp.latency_ms for vp in self._verified_data.values()]
            avg_lat = round(sum(latencies) / len(latencies), 1) if latencies else 0.0

            top_proxies = [
                {
                    "url": vp.url,
                    "latency_ms": vp.latency_ms,
                    "protocol": vp.protocol,
                    "host": vp.host,
                    "port": vp.port,
                    "source": vp.source,
                }
                for vp in sorted(self._verified_data.values(), key=lambda x: x.latency_ms)[:10]
            ]

            last_time_str = (
                time.strftime("%H:%M:%S", time.localtime(self.last_scraped_time))
                if self.last_scraped_time
                else None
            )

            return {
                "status": "ok",
                "is_scraping": self.is_scraping,
                "total_scraped": self.total_scraped_candidates,
                "verified_count": len(self._verified_data),
                "alive_count": alive,
                "cooldown_count": cooldown,
                "dead_count": dead,
                "avg_latency_ms": avg_lat,
                "last_scraped_time": last_time_str,
                "top_proxies": top_proxies,
            }

    def scrape_and_verify_sync(
        self,
        max_candidates: int = 400,
        timeout: Optional[float] = None,
        progress_cb: Optional[Any] = None,
    ) -> int:
        """
        Synchronously executes proxy scraping and multi-threaded async validation.
        Safe to call from a worker thread. Updates self.endpoints with verified proxies.
        Returns the count of newly verified active proxies.
        """
        with self._lock:
            if self.is_scraping:
                return len(self.endpoints)
            self.is_scraping = True

        try:
            logger.info("Beginning free public proxy scraping from %d sources...", len(self.scraper.sources))
            raw_candidates = self.scraper.scrape_all()
            with self._lock:
                self.total_scraped_candidates = len(raw_candidates)

            if not raw_candidates:
                logger.warning("No proxy candidates found from remote sources.")
                return 0

            # Shuffle candidates to distribute testing across sources
            import random
            random.shuffle(raw_candidates)
            candidates_to_test = raw_candidates[:max_candidates]

            validator = self.validator
            if timeout:
                validator = FreeProxyValidator(
                    timeout=timeout,
                    max_latency_ms=self.max_latency_ms,
                )

            # Run asynchronous batch validation
            loop = asyncio.new_event_loop()
            try:
                verified_list = loop.run_until_complete(
                    validator.validate_batch(
                        candidates_to_test,
                        concurrency=40,
                        progress_cb=progress_cb,
                        max_verified_needed=self.max_pool_size,
                    )
                )
            finally:
                loop.close()

            with self._lock:
                self.last_scraped_time = time.time()
                for vp in verified_list:
                    self._verified_data[vp.url] = vp

                # Rebuild endpoints sorted by latency
                new_endpoints: List[ProxyEndpoint] = []
                for vp in sorted(self._verified_data.values(), key=lambda x: x.latency_ms):
                    ep_label = f"FreePublic [{vp.country} - {vp.host}:{vp.port}] ({vp.latency_ms:.0f}ms)"
                    new_endpoints.append(ProxyEndpoint(url=vp.url, provider_name=ep_label))

                self.endpoints = new_endpoints
                self.verified_active_count = len(self.endpoints)
                self.save_cache()
                logger.info(
                    "Free proxy validation completed: %d active proxies verified (avg latency: %.1f ms)",
                    len(self.endpoints),
                    self.get_stats()["avg_latency_ms"],
                )
                return len(self.endpoints)

        finally:
            with self._lock:
                self.is_scraping = False

    def trigger_background_scrape(self, progress_cb: Optional[Any] = None):
        """Launches scraping & verification in an independent daemon thread."""
        with self._lock:
            if self.is_scraping:
                return
        t = threading.Thread(
            target=self.scrape_and_verify_sync,
            kwargs={"progress_cb": progress_cb},
            daemon=True,
            name="D4UC-FreeProxyScraper",
        )
        t.start()

    def start_auto_refresher(self):
        """Starts periodic background auto-refresher loop."""
        with self._lock:
            if self._auto_refresher_running:
                return
            self._auto_refresher_running = True

        def _refresher_loop():
            while self._auto_refresher_running:
                time.sleep(self.auto_refresh_interval)
                if not self._auto_refresher_running:
                    break
                try:
                    alive, _, _ = self.get_stats_tuple()
                    if alive < self.min_pool_size * 2:
                        self.scrape_and_verify_sync()
                except Exception as e:
                    logger.debug("Auto-refresher error: %s", e)

        self._refresher_thread = threading.Thread(target=_refresher_loop, daemon=True, name="D4UC-FreeProxyAutoRefresher")
        self._refresher_thread.start()

    def stop(self):
        """Stops background threads and flushes cache."""
        self._auto_refresher_running = False
        self.save_cache()
