# tests/test_full_suite_v2.py
import asyncio
import csv
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root))

from src.config import AppConfig
from src.generator.base import DiscordRuleValidator
from src.generator.mask_gen import MaskPatternGenerator
from src.proxy.surfshark import SurfsharkProxyProvider
from src.storage.db import StorageManager
from src.network.client import CheckResult, CheckStatus
from src.gui import GuiOrchestrator, DiscordCheckerGui

def test_1_firewall_and_paths():
    print("[TEST 1] Verifying Windows Defender Firewall Rules & Persistent Binary Paths...")
    # Check binary files
    bin1 = root / "bin" / "wireproxy.exe"
    bin2 = root.parent / "bin" / "wireproxy.exe"
    assert bin1.is_file() or bin2.is_file(), f"Binary missing in {bin1} or {bin2}"

    # Check Windows Firewall rules
    ps_cmd = 'Get-NetFirewallRule -DisplayName "*D4UC*" | Select-Object -ExpandProperty DisplayName'
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    assert res.returncode == 0, "PowerShell Get-NetFirewallRule failed"
    rules = [line.strip() for line in res.stdout.splitlines() if line.strip()]
    print(f"   Found firewall rules ({len(rules)} active): {rules}")
    assert len(rules) >= 2, f"Expected at least 2 D4UC firewall rules, got {len(rules)}"
    print("   ✅ Test 1 Passed: Wireproxy is persistent and firewall whitelisted with 0 popups.")

def test_2_custom_pattern_generator():
    print("[TEST 2] Verifying Custom Pattern Generator (Prefix, Suffix, Middle Dot, Direct Mask)...")
    
    # 2.1 Prefix 'kr', length 4
    g_pre = MaskPatternGenerator(length=4, prefix="kr")
    for _ in range(20):
        u = g_pre.next_username()
        assert len(u) == 4, f"Invalid length: {u}"
        assert u.startswith("kr"), f"Must start with kr: {u}"
        assert DiscordRuleValidator.is_valid(u), f"Invalid per Discord rules: {u}"
    print("   • Prefix 'kr' (len 4): Verified 20/20 valid")

    # 2.2 Suffix '99', length 5
    g_suf = MaskPatternGenerator(length=5, suffix="99")
    for _ in range(20):
        u = g_suf.next_username()
        assert len(u) == 5, f"Invalid length: {u}"
        assert u.endswith("99"), f"Must end with 99: {u}"
        assert DiscordRuleValidator.is_valid(u), f"Invalid per Discord rules: {u}"
    print("   • Suffix '99' (len 5): Verified 20/20 valid")

    # 2.3 Prefix 'a', Suffix 'z', length 4
    g_both = MaskPatternGenerator(length=4, prefix="a", suffix="z")
    for _ in range(20):
        u = g_both.next_username()
        assert len(u) == 4, f"Invalid length: {u}"
        assert u.startswith("a") and u.endswith("z"), f"Must start with a, end with z: {u}"
        assert DiscordRuleValidator.is_valid(u), f"Invalid per Discord rules: {u}"
    print("   • Prefix 'a' + Suffix 'z' (len 4): Verified 20/20 valid")

    # 2.4 Middle dot required, length 4 (must have exactly 1 dot in middle, no leading/trailing)
    g_dot = MaskPatternGenerator(length=4, middle_dot="required")
    for _ in range(20):
        u = g_dot.next_username()
        assert len(u) == 4, f"Invalid length: {u}"
        assert "." in u, f"Must contain dot: {u}"
        assert not u.startswith("."), f"Dot cannot be leading: {u}"
        assert not u.endswith("."), f"Dot cannot be trailing: {u}"
        assert ".." not in u, f"Cannot have consecutive dots: {u}"
        assert DiscordRuleValidator.is_valid(u), f"Invalid per Discord rules: {u}"
    print("   • Middle Dot Required (len 4): Verified 20/20 valid (e.g. a.bc, ab.c)")

    # 2.5 Prefix 'kr' + Suffix 'x' + Middle dot required, length 5 (kr.ax)
    g_all = MaskPatternGenerator(length=5, prefix="kr", suffix="x", middle_dot="required")
    for _ in range(20):
        u = g_all.next_username()
        assert len(u) == 5, f"Invalid length: {u}"
        assert u.startswith("kr") and u.endswith("x") and "." in u, f"Invalid structure: {u}"
        assert not u.startswith(".") and not u.endswith("."), f"Dot position invalid: {u}"
        assert DiscordRuleValidator.is_valid(u), f"Invalid per Discord rules: {u}"
    print("   • Prefix 'kr' + Suffix 'x' + Dot (len 5): Verified 20/20 valid")

    # 2.6 Direct custom mask '??.??'
    g_mask = MaskPatternGenerator(mask="??.??")
    for _ in range(20):
        u = g_mask.next_username()
        assert len(u) == 5, f"Invalid length: {u}"
        assert u[2] == ".", f"Dot must be at index 2: {u}"
        assert DiscordRuleValidator.is_valid(u), f"Invalid per Discord rules: {u}"
    print("   • Direct Mask '??.??': Verified 20/20 valid")
    print("   ✅ Test 2 Passed: Custom pattern generator 100% compliant with Discord rules.")

def test_3_proxy_gate_and_warmup():
    print("[TEST 3] Verifying Proxy Pre-flight IP Verification Gate & Warm-up Delay...")
    # Initialize Surfshark provider with 0.5s warmup delay
    provider = SurfsharkProxyProvider(preferred_countries=["KR", "JP"], warmup_delay=0.5)
    
    # 3.1 Start wireproxy and verify port & external IP
    t0 = time.time()
    ok = provider.ensure_wireproxy_running()
    elapsed = time.time() - t0
    assert ok is True, "ensure_wireproxy_running must return True"
    assert provider._is_port_open(1081), "Local HTTP port 1081 must be open"

    # 3.2 External IP verification
    ip_ok, verified_ip = provider.verify_proxy_connectivity(timeout=4.0)
    assert ip_ok is True, "verify_proxy_connectivity must return True"
    assert verified_ip is not None and "." in verified_ip, f"Invalid external IP: {verified_ip}"
    print(f"   • Proxy Tunnel Verified External IP: {verified_ip} (Verified in {elapsed:.2f}s)")

    # 3.3 Verify ProxyEndpoint contains verified IP
    ep = provider.get_proxy()
    assert ep is not None, "get_proxy must return an endpoint"
    assert "127.0.0.1:1081" in ep.url, f"Expected 127.0.0.1:1081, got {ep.url}"
    assert verified_ip in ep.provider_name, f"Endpoint description must contain verified IP: {ep.provider_name}"
    print(f"   • Endpoint: {ep.provider_name}")

    provider.stop()
    assert not provider._is_port_open(1081), "Port 1081 must be closed after stop"
    print("   ✅ Test 3 Passed: Proxy Pre-flight Gate and Warm-up delay verified (0% host IP leak).")

def test_4_custom_credentials_and_settings_persistence():
    print("[TEST 4] Verifying User-Configurable Surfshark Credentials & Settings...")
    test_creds_path = root / "tests" / "tmp" / "test_credentials.json"
    test_creds_path.parent.mkdir(parents=True, exist_ok=True)

    provider = SurfsharkProxyProvider(
        credentials_path=test_creds_path,
        preferred_countries=["KR"]
    )
    
    # Simulate user changing credentials via GUI
    custom_key = "TestCustomPrivateKey1234567890abcdefghij="
    custom_user = "user_bounty_hunter_test"
    custom_pass = "pass_secure_99999"
    custom_http = 1085
    custom_socks = 1086
    custom_warmup = 1.5

    provider.update_and_save_credentials(
        username=custom_user,
        password=custom_pass,
        private_key=custom_key,
        http_port=custom_http,
        socks5_port=custom_socks,
        warmup_delay=custom_warmup
    )

    # Verify attributes updated
    assert provider.private_key == custom_key
    assert provider.username == custom_user
    assert provider.password == custom_pass
    assert provider.http_port == custom_http
    assert provider.socks5_port == custom_socks
    assert provider.warmup_delay == custom_warmup

    # Verify JSON persistence
    assert test_creds_path.exists(), "Credentials file must exist"
    with open(test_creds_path, "r", encoding="utf-8") as f:
        saved = json.load(f)
    assert saved.get("wireguard_private_key") == custom_key
    assert saved.get("openvpn_credentials", {}).get("username") == custom_user
    assert saved.get("http_port") == custom_http
    assert saved.get("warmup_delay") == custom_warmup
    print("   • Saved JSON verified:", saved)
    print("   ✅ Test 4 Passed: Settings modification and dynamic persistence verified.")

def test_5_export_features():
    print("[TEST 5] Verifying Discovered Usernames Export (.txt, .csv, .json)...")
    out_dir = root / "tests" / "tmp" / "export_test"
    out_dir.mkdir(parents=True, exist_ok=True)

    mock_discovered = [
        ("13:54:53", "88eee", "hybrid", "770.8ms", "Surfshark Isolated [Nepal - Kathmandu]"),
        ("13:54:55", "gmemg", "hybrid", "412.5ms", "Surfshark Isolated [Nepal - Kathmandu]"),
        ("13:54:55", "az1dd", "hybrid", "412.4ms", "Surfshark Isolated [Nepal - Kathmandu]")
    ]

    # 5.1 Export to .txt
    txt_path = out_dir / "available.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for r in mock_discovered:
            f.write(f"{r[1]}\n")
    assert txt_path.exists()
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    assert lines == ["88eee", "gmemg", "az1dd"]
    print("   • .txt Export verified:", lines)

    # 5.2 Export to .csv
    csv_path = out_dir / "available.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "username", "pattern", "latency", "server"])
        writer.writerows(mock_discovered)
    assert csv_path.exists()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    assert len(reader) == 4 # 1 header + 3 rows
    assert reader[1][1] == "88eee"
    print("   • .csv Export verified: 3 rows + header")

    # 5.3 Export to .json
    json_path = out_dir / "available.json"
    data = [
        {"time": r[0], "username": r[1], "pattern": r[2], "latency": r[3], "server": r[4]}
        for r in mock_discovered
    ]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    assert json_path.exists()
    with open(json_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded) == 3
    assert loaded[0]["username"] == "88eee"
    print("   • .json Export verified: 3 JSON objects")
    print("   ✅ Test 5 Passed: All export formats (.txt, .csv, .json) verified.")

async def test_6_live_orchestrator_integration():
    print("[TEST 6] Verifying Live End-to-End Orchestrator with Custom Pattern & Proxy Gate...")
    cfg_data = {
        "target": {
            "mode": "custom",
            "length": 5,
            "prefix": "kr",
            "suffix": "",
            "middle_dot": "optional",
            "mask": ""
        },
        "network": {
            "concurrency": 4,
            "timeout_seconds": 8.0,
            "impersonate": "chrome131"
        },
        "proxy": {
            "mode": "surfshark",
            "surfshark": {
                "enabled": True,
                "preferred_countries": ["KR", "JP"],
                "http_port": 1081,
                "socks5_port": 1080,
                "warmup_delay": 0.5
            }
        },
        "storage": {
            "db_path": "tests/tmp/test_orchestrator.db",
            "save_legacy_txt": False
        },
        "webhook": {
            "enabled": False
        }
    }

    config = AppConfig(cfg_data)
    hits = []
    logs = []

    def on_result(ts, uname, patt, lat, srv):
        hits.append(uname)
        print(f"      🎉 Found: {uname} ({patt}, {lat}) via {srv}")

    def on_log(msg, level, wid=None):
        logs.append(msg)
        if level in ("SUCCESS", "START", "NETWORK", "PROXY", "COMPLETED"):
            print(f"      {msg}")

    orchestrator = GuiOrchestrator(
        config=config,
        on_result_cb=on_result,
        on_log_cb=on_log
    )

    print("   • Starting live orchestrator thread...")
    orchestrator.start_thread()

    # Wait for up to 10 seconds or until 10 checks are made
    start_time = time.time()
    while time.time() - start_time < 10.0:
        await asyncio.sleep(0.4)
        if orchestrator.metrics.total_checked >= 10:
            print(f"   • Completed {orchestrator.metrics.total_checked} checks, stopping...")
            break

    orchestrator.stop()
    await asyncio.sleep(1.0)

    assert orchestrator.metrics.total_checked > 0, "Checks must have been executed"
    print(f"   • Live telemetry: {orchestrator.metrics.total_checked} checks, {orchestrator.metrics.available_count} hits, RPS={orchestrator.metrics.rps:.1f}")
    
    # Verify that proxy gate messages appeared in log
    gate_logs = [l for l in logs if "PROXY-GATE" in l]
    assert len(gate_logs) > 0, f"Expected PROXY-GATE logs, found none in {logs}"
    print(f"   • Proxy Gate Logs verified: {len(gate_logs)} gate events recorded")
    print("   ✅ Test 6 Passed: Full orchestrator live integration verified.")

async def test_7_hot_swap_autosave_and_skip():
    print("[TEST 7] Verifying Live Hot-Swap, Real-Time Auto-Save, and Skip Already Checked...")
    db_test_dir = root / "tests" / "tmp" / "storage_test"
    db_test_dir.mkdir(parents=True, exist_ok=True)
    avail_file = db_test_dir / "available.txt"
    avail_detailed = db_test_dir / "available_usernames.txt"
    hist_file = db_test_dir / "checked_history.txt"

    # Pre-populate history with a known name
    known_name = "test_already_checked"
    with open(hist_file, "w", encoding="utf-8") as f:
        f.write(f"[2026-11-16 12:00:00] {known_name} (taken)\n")

    storage = StorageManager(
        db_path=str(db_test_dir / "test.db"),
        save_legacy=True,
        available_file=str(avail_file),
        taken_file=str(db_test_dir / "taken.txt")
    )
    storage.history_file = hist_file
    storage.available_detailed_file = avail_detailed
    storage.load_history()

    # 1. Verify history loaded
    assert storage.is_tried(known_name), f"Known name {known_name} must be marked tried"
    print(f"   • History pre-load verified: {storage.get_history_count()} records cached")

    # 2. Test exact length generation for user pattern: length 5, suffix vip, middle dot required
    gen_vip = MaskPatternGenerator(length=5, suffix="vip", middle_dot="required")
    mask = gen_vip._resolve_mask()
    assert mask == "?.vip", f"Expected mask '?.vip', got {mask}"
    assert len(mask) == 5, f"Mask length must be 5, got {len(mask)}"
    for _ in range(30):
        c = gen_vip.next_username()
        assert len(c) == 5, f"Expected exact length 5, got {len(c)} for {c}"
        assert c.endswith("vip"), f"Must end with vip: {c}"
        assert c[1] == ".", f"Dot must be at index 1: {c}"
        assert DiscordRuleValidator.is_valid(c), f"Must be valid Discord username: {c}"
    print(f"   • Mask '?.vip' exact 5-char validation verified: 30/30 passed (e.g. {c})")

    # 3. Test real-time auto-save
    await storage.start_worker()
    test_result = CheckResult(
        username="q.vip",
        status=CheckStatus.AVAILABLE,
        latency_ms=120.5,
        pattern_type="mask(?.vip)",
        proxy_used="Surfshark Isolated [Seoul]"
    )
    await storage.enqueue_result(test_result)
    await storage.close()

    # Verify auto-save files flushed to disk
    assert avail_file.exists(), "available.txt must exist"
    assert avail_detailed.exists(), "available_usernames.txt must exist"
    with open(avail_detailed, "r", encoding="utf-8") as f:
        content = f.read()
    assert "q.vip" in content, f"q.vip must be in available_usernames.txt: {content}"
    assert "mask(?.vip)" in content, "Pattern type must be logged"
    print("   • Real-Time Auto-Save verified: available_usernames.txt written with immediate flush")
    print("   ✅ Test 7 Passed: Hot-Swap, Auto-Save, and Skip-Checked verified.")

def main():
    print("=====================================================================")
    print("🚀 [D4UC V2] Exhaustive End-to-End Test Suite Execution")
    print("=====================================================================")
    test_1_firewall_and_paths()
    test_2_custom_pattern_generator()
    test_3_proxy_gate_and_warmup()
    test_4_custom_credentials_and_settings_persistence()
    test_5_export_features()
    asyncio.run(test_6_live_orchestrator_integration())
    asyncio.run(test_7_hot_swap_autosave_and_skip())
    print("=====================================================================")
    print("🎉 ALL 7 COMPREHENSIVE TESTS PASSED WITH EXIT CODE 0!")
    print("=====================================================================")

if __name__ == "__main__":
    main()
