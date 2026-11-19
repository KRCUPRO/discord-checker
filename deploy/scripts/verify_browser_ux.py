import os
import sys
import time
import subprocess
import threading
from pathlib import Path
import urllib.request
import json

root = Path(r"C:\Users\Administrator\Desktop\D4UC\github-ready")
sys.path.insert(0, str(root))

from src.web_gui import WebGuiServer

def run_test():
    server = WebGuiServer(host="127.0.0.1", port=5005)
    t = threading.Thread(target=server.start, kwargs={"block": False}, daemon=True)
    t.start()
    time.sleep(1.0)

    # 1. Verify /api/ping
    res = urllib.request.urlopen("http://127.0.0.1:5005/api/ping")
    ping_data = json.loads(res.read().decode("utf-8"))
    assert ping_data["status"] == "ok"
    print("✅ /api/ping responded HTTP 200 with pong")

    # 2. Verify /api/network_info
    res_net = urllib.request.urlopen("http://127.0.0.1:5005/api/network_info")
    net_data = json.loads(res_net.read().decode("utf-8"))
    assert net_data["status"] == "ok"
    assert len(net_data["lan_ips"]) > 0
    print(f"✅ /api/network_info detected IPs: {net_data['lan_ips']}")

    # 3. Headless Chrome browser capture
    chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    desktop_shot = docs_dir / "desktop_preview.png"

    # Desktop viewport (1280x800)
    subprocess.run([
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--window-size=1280,800",
        f"--screenshot={desktop_shot}",
        "http://127.0.0.1:5005/"
    ], capture_output=True, timeout=15)
    assert desktop_shot.exists() and desktop_shot.stat().st_size > 10000
    print(f"✅ Desktop viewport (1280x800) captured to {desktop_shot} ({desktop_shot.stat().st_size} bytes)")

    server.stop()
    print("🎉 Browser UX verification completed successfully!")

if __name__ == "__main__":
    run_test()
