# tests/verify_user_request.py
import asyncio
import os
import sys
import time
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root))

from src.config import AppConfig
from src.gui import GuiOrchestrator

async def run_verification():
    print("=====================================================================")
    print("🔍 [TEST VERIFICATION] User-Specified Exact Parameters")
    print("   • Proxy: Surfshark Isolated Wireproxy (127.0.0.1:1081)")
    print("   • Preferred Countries: ALL 142 Global Clusters")
    print("   • Username Length: 5 Characters")
    print("   • Async Workers: 5 Workers")
    print("=====================================================================")

    # 1. Prepare configuration with user's exact parameters
    cfg_data = {
        "target": {
            "mode": "hybrid",
            "length": 5,
            "exclude_reserved": True
        },
        "network": {
            "concurrency": 5,
            "timeout_seconds": 8.0,
            "impersonate": "chrome131"
        },
        "proxy": {
            "mode": "surfshark",
            "surfshark": {
                "enabled": True,
                "preferred_countries": [],  # ALL 142 global clusters
                "http_port": 1081,
                "socks5_port": 1080
            }
        },
        "storage": {
            "db_path": "tests/tmp/test_user_verify.db",
            "save_legacy_txt": False
        },
        "webhook": {
            "enabled": False
        }
    }

    config = AppConfig(cfg_data)

    captured_logs = []
    worker_checks = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    queried_usernames = []
    duplicate_names = []
    invalid_length_names = []

    def on_log(text, level, worker_id=None):
        import re
        captured_logs.append((text, level, worker_id))
        print(text)
        if worker_id in worker_checks:
            worker_checks[worker_id] += 1
            # Extract username from "[워커 X] ... 'xxxxx' (5자)"
            m = re.search(r"\'([a-z0-9_.]+)\'", text)
            if m:
                uname = m.group(1)
                if len(uname) != 5:
                    invalid_length_names.append(uname)
                if uname in queried_usernames:
                    duplicate_names.append(uname)
                else:
                    queried_usernames.append(uname)

    def on_result(ts, username, pattern, latency, server):
        print(f"🎉 HIT: {username} ({pattern}) in {latency} via {server}")

    orchestrator = GuiOrchestrator(
        config=config,
        on_result_cb=on_result,
        on_log_cb=on_log
    )

    # 2. Verify all clusters loaded
    surf_provider = None
    for p in orchestrator.proxy_manager.providers:
        if hasattr(p, "clusters"):
            surf_provider = p
            break

    assert surf_provider is not None, "SurfsharkProxyProvider must be initialized"
    print(f"✅ Surfshark loaded clusters: {len(surf_provider.clusters)} total (Preferred: ALL)")
    assert len(surf_provider.clusters) >= 140, f"Expected 140+ clusters, got {len(surf_provider.clusters)}"

    # 3. Start orchestrator
    print("🚀 Starting 5 async workers...")
    orchestrator.start_thread()

    # 4. Monitor for up to 12 seconds
    start_t = time.time()
    while time.time() - start_t < 12.0:
        await asyncio.sleep(0.5)
        if orchestrator.metrics.total_checked >= 15:
            print(f"🎯 Reached {orchestrator.metrics.total_checked} checks, wrapping up...")
            break

    # 5. Stop orchestrator
    print("⏹️ Stopping orchestrator...")
    orchestrator.stop()
    await asyncio.sleep(1.5)

    print("=====================================================================")
    print("📊 [TEST RESULTS SUMMARY]")
    print(f"• Total Checks Completed: {orchestrator.metrics.total_checked}")
    print(f"• Unique Usernames Checked: {len(queried_usernames)}")
    print(f"• Duplicate Checks: {len(duplicate_names)}")
    print(f"• Invalid Lengths (!= 5): {len(invalid_length_names)}")
    print(f"• Worker Check Distribution: {worker_checks}")
    print(f"• 429 RateLimit Rotations: {orchestrator.metrics.rate_limited_count}")
    print("=====================================================================")

    # Assertions
    assert len(invalid_length_names) == 0, f"Found names not 5 chars: {invalid_length_names}"
    assert len(duplicate_names) == 0, f"Found duplicates: {duplicate_names}"
    assert orchestrator.metrics.total_checked > 0, "At least some checks must have executed"
    print("🎉 ALL TEST ASSERTIONS PASSED WITH EXIT CODE 0!")

if __name__ == "__main__":
    asyncio.run(run_verification())
