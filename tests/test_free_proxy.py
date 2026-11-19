# tests/test_free_proxy.py
"""
Unit Test Suite for Free Public Proxy Scraper & Live Multi-Threaded Validator.
Tests parsing, deduplication, async validation mocking, leasing, cooldown, and manager integration.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add project root to sys.path
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from src.proxy.base import ProxyEndpoint
from src.proxy.free_proxy import (
    FreeProxyProvider,
    FreeProxyScraper,
    FreeProxyValidator,
    VerifiedProxyData,
    parse_proxy_line,
)
from src.proxy.manager import UnifiedProxyManager


def test_parse_proxy_line_formats():
    """Verify robust parsing of various public proxy line formats."""
    # 1. Standard host:port with default protocol
    p1 = parse_proxy_line("192.168.1.100:8080", default_protocol="http")
    assert p1 is not None
    assert p1[0] == "http://192.168.1.100:8080"
    assert p1[1] == "http"
    assert p1[2] == "192.168.1.100"
    assert p1[3] == 8080

    # 2. Scheme-prefixed SOCKS5
    p2 = parse_proxy_line("socks5://10.0.0.1:1080")
    assert p2 is not None
    assert p2[0] == "socks5://10.0.0.1:1080"
    assert p2[1] == "socks5"
    assert p2[2] == "10.0.0.1"
    assert p2[3] == 1080

    # 3. Scheme-prefixed SOCKS4
    p3 = parse_proxy_line("socks4://10.0.0.2:1080")
    assert p3 is not None
    assert p3[0] == "socks4://10.0.0.2:1080"
    assert p3[1] == "socks4"

    # 4. host:port:user:pass quad format
    p4 = parse_proxy_line("1.2.3.4:3128:testuser:secretpass", default_protocol="http")
    assert p4 is not None
    assert p4[0] == "http://testuser:secretpass@1.2.3.4:3128"
    assert p4[2] == "1.2.3.4"
    assert p4[3] == 3128

    # 5. protocol://user:pass@host:port format
    p5 = parse_proxy_line("http://myuser:mypass@5.6.7.8:8000")
    assert p5 is not None
    assert p5[0] == "http://myuser:mypass@5.6.7.8:8000"
    assert p5[2] == "5.6.7.8"
    assert p5[3] == 8000

    # 6. Invalid lines (comments, whitespace, invalid port)
    assert parse_proxy_line("# This is a comment") is None
    assert parse_proxy_line("   ") is None
    assert parse_proxy_line("invalid_no_port") is None
    assert parse_proxy_line("999.999.999.999:99999") is None  # Port > 65535


def test_scraper_deduplication():
    """Verify that FreeProxyScraper removes duplicate IP:Port candidates across sources."""
    mock_sources = [
        {"url": "mock://source1", "protocol": "http", "label": "src1"},
        {"url": "mock://source2", "protocol": "socks5", "label": "src2"},
    ]
    scraper = FreeProxyScraper(sources=mock_sources)

    with patch("src.proxy.free_proxy.fetch_source_sync") as mock_fetch:
        # Source 1 returns 2 proxies
        # Source 2 returns 2 proxies, 1 overlapping with Source 1
        mock_fetch.side_effect = [
            [("http://1.1.1.1:80", "http", "1.1.1.1", 80), ("http://2.2.2.2:80", "http", "2.2.2.2", 80)],
            [("socks5://1.1.1.1:80", "socks5", "1.1.1.1", 80), ("socks5://3.3.3.3:1080", "socks5", "3.3.3.3", 1080)],
        ]
        candidates = scraper.scrape_all()

    # 1.1.1.1:80 is duplicated, so total should be 3 unique hosts
    assert len(candidates) == 3
    hosts = [c[2] for c in candidates]
    assert "1.1.1.1" in hosts
    assert "2.2.2.2" in hosts
    assert "3.3.3.3" in hosts


@pytest.mark.asyncio
async def test_async_validation_success():
    """Verify that FreeProxyValidator accepts responsive Discord 200 responses."""
    validator = FreeProxyValidator(timeout=2.0, max_latency_ms=3000.0)

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"taken": False}

    mock_session = AsyncMock()
    mock_session.post.return_value = mock_resp

    result = await validator.test_single_proxy(
        candidate_url="http://1.2.3.4:8080",
        protocol="http",
        host="1.2.3.4",
        port=8080,
        source="unit_test",
        session=mock_session,
    )

    assert result is not None
    assert result.url == "http://1.2.3.4:8080"
    assert result.host == "1.2.3.4"
    assert result.port == 8080
    assert result.latency_ms > 0
    assert result.latency_ms <= 3000.0


@pytest.mark.asyncio
async def test_async_validation_filters_waf_and_errors():
    """Verify that 403 (Cloudflare block), 429 (rate limit), and exceptions are discarded."""
    validator = FreeProxyValidator(timeout=2.0, max_latency_ms=3000.0)

    # 1. Test 403 Cloudflare WAF block
    resp_403 = MagicMock()
    resp_403.status_code = 403
    session_403 = AsyncMock()
    session_403.post.return_value = resp_403

    r1 = await validator.test_single_proxy(
        "http://1.2.3.4:8080", "http", "1.2.3.4", 8080, "test", session_403
    )
    assert r1 is None, "403 Cloudflare block must be rejected"

    # 2. Test 429 Discord Rate Limit
    resp_429 = MagicMock()
    resp_429.status_code = 429
    session_429 = AsyncMock()
    session_429.post.return_value = resp_429

    r2 = await validator.test_single_proxy(
        "http://1.2.3.4:8080", "http", "1.2.3.4", 8080, "test", session_429
    )
    assert r2 is None, "429 Rate limited IP must be rejected during verification"

    # 3. Test Network Exception / Timeout
    session_err = AsyncMock()
    session_err.post.side_effect = TimeoutError("Connection timed out")

    r3 = await validator.test_single_proxy(
        "http://1.2.3.4:8080", "http", "1.2.3.4", 8080, "test", session_err
    )
    assert r3 is None, "Timed out proxy must be rejected"


def test_free_proxy_provider_leasing_and_cooldown(tmp_path):
    """Verify round-robin leasing, cooldown handling, and dead removal in FreeProxyProvider."""
    cache_file = tmp_path / "test_free_proxies.json"
    provider = FreeProxyProvider(cache_file=str(cache_file), min_pool_size=2)

    # Inject mock verified endpoints
    ep1 = ProxyEndpoint(url="http://1.1.1.1:8080", provider_name="FreePublic [1.1.1.1:8080] (120ms)")
    ep2 = ProxyEndpoint(url="http://2.2.2.2:8080", provider_name="FreePublic [2.2.2.2:8080] (150ms)")
    provider.endpoints = [ep1, ep2]
    provider._verified_data = {
        ep1.url: VerifiedProxyData(url=ep1.url, protocol="http", host="1.1.1.1", port=8080, latency_ms=120.0, source="test"),
        ep2.url: VerifiedProxyData(url=ep2.url, protocol="http", host="2.2.2.2", port=8080, latency_ms=150.0, source="test"),
    }
    provider.verified_active_count = 2

    # 1. Round-robin lease
    leased1 = provider.get_proxy()
    leased2 = provider.get_proxy()
    assert leased1 is not None and leased2 is not None
    assert leased1.url != leased2.url

    # 2. Test 429 rate limit reporting (sets cooldown)
    provider.report_result(leased1, success=False, rate_limited=True, cooldown=10.0)
    assert leased1.cooldown_until > time.time()
    assert not leased1.is_available()

    # Next lease should be leased2
    leased3 = provider.get_proxy()
    assert leased3.url == leased2.url

    # 3. Test dead proxy removal
    provider.report_result(leased2, success=False, rate_limited=False)
    provider.report_result(leased2, success=False, rate_limited=False)
    assert leased2.is_dead is True

    # 4. Save and Load cache
    provider.save_cache()
    assert cache_file.exists()

    new_provider = FreeProxyProvider(cache_file=str(cache_file))
    assert len(new_provider.endpoints) > 0


def test_unified_proxy_manager_free_mode_integration(tmp_path):
    """Verify UnifiedProxyManager initializes FreeProxyProvider with mode='free'."""
    cache_file = tmp_path / "test_manager_cache.json"
    proxy_config = {
        "mode": "free",
        "free": {
            "cache_file": str(cache_file),
            "max_latency_ms": 3000.0,
            "auto_refresh": False,
        },
        "health": {
            "cooldown_429_seconds": 15.0,
        },
    }

    manager = UnifiedProxyManager(proxy_config)
    assert manager.mode == "free"

    free_prov = manager.get_free_provider()
    assert free_prov is not None
    assert isinstance(free_prov, FreeProxyProvider)

    # Populate mock proxy
    ep = ProxyEndpoint(url="socks5://9.9.9.9:1080", provider_name="FreePublic [9.9.9.9:1080] (90ms)")
    free_prov.endpoints = [ep]

    # Test lease through manager
    leased = manager.lease_proxy()
    assert leased is not None
    assert leased.url == "socks5://9.9.9.9:1080"

    # Test release through manager
    manager.release_proxy(leased, success=True)
    assert leased.success_count == 1

    # Test stats aggregation
    alive, cooldown, dead = manager.get_pool_summary()
    assert alive == 1
    assert cooldown == 0
    assert dead == 0

    manager.close()
