import subprocess
import time
import json
import urllib.request
from pathlib import Path
import base64
import socket
import struct

root = Path(r"C:\Users\Administrator\Desktop\D4UC\github-ready")
chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def capture_mobile(url, out_path):
    proc = subprocess.Popen([
        chrome_bin,
        "--headless=new",
        "--remote-debugging-port=9229",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        url
    ])
    try:
        time.sleep(1.5)
        tabs = json.loads(urllib.request.urlopen("http://localhost:9229/json").read())
        page_tabs = [t for t in tabs if t.get("type") == "page"]
        tab = page_tabs[0]
        ws_url = tab["webSocketDebuggerUrl"]
        path = ws_url.split("localhost:9229")[1]

        s = socket.create_connection(("localhost", 9229))
        req = f"GET {path} HTTP/1.1\r\nHost: localhost:9229\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n"
        s.sendall(req.encode())
        s.recv(4096)

        def send_cdp(method, params=None, msg_id=1):
            payload = json.dumps({"id": msg_id, "method": method, "params": params or {}}).encode("utf-8")
            length = len(payload)
            mask = b"\x12\x34\x56\x78"
            masked_payload = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
            if length < 126:
                header = bytearray([0x81, 0x80 | length]) + mask
            elif length < 65536:
                header = bytearray([0x81, 0x80 | 126]) + struct.pack("!H", length) + mask
            else:
                header = bytearray([0x81, 0x80 | 127]) + struct.pack("!Q", length) + mask
            s.sendall(header + masked_payload)

            while True:
                h = s.recv(2)
                if not h: break
                l = h[1] & 0x7F
                if l == 126:
                    l = struct.unpack("!H", s.recv(2))[0]
                elif l == 127:
                    l = struct.unpack("!Q", s.recv(8))[0]
                data = bytearray()
                while len(data) < l:
                    chunk = s.recv(l - len(data))
                    if not chunk: break
                    data.extend(chunk)
                msg = json.loads(data.decode("utf-8", errors="ignore"))
                if msg.get("id") == msg_id:
                    return msg

        send_cdp("Page.enable", msg_id=1)
        send_cdp("Emulation.setDeviceMetricsOverride", {
            "width": 390,
            "height": 844,
            "deviceScaleFactor": 2.0,
            "mobile": True,
            "fitWindow": False
        }, msg_id=2)
        time.sleep(1.0)
        shot_res = send_cdp("Page.captureScreenshot", {"format": "png"}, msg_id=3)
        img_b64 = shot_res["result"]["data"]
        out_path.write_bytes(base64.b64decode(img_b64))
        print(f"✅ Real Mobile CDP screenshot saved to {out_path} ({out_path.stat().st_size} bytes)")
    finally:
        proc.terminate()

if __name__ == "__main__":
    import threading
    import sys
    sys.path.insert(0, str(root))
    from src.web_gui import WebGuiServer

    server = WebGuiServer(host="127.0.0.1", port=5007)
    t = threading.Thread(target=server.start, kwargs={"block": False}, daemon=True)
    t.start()
    time.sleep(1.0)

    try:
        capture_mobile("http://127.0.0.1:5007/", root / "docs" / "mobile_preview.png")
    finally:
        server.stop()
