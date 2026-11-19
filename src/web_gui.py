# src/web_gui.py
"""
D4UC Mobile Touch-Optimized Responsive Web GUI & PWA Engine
Provides a full-featured, Discord-dark-themed Mobile Web App accessible via phone browser
at http://<host>:5000 with PWA Add to Home Screen, touch controls, and live telemetry.
"""
import argparse
import collections
import csv
import json
import os
import signal
import sys
import threading
import time
import urllib.parse
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional, Dict, Any, List

_ROOT_DIR = Path(__file__).resolve().parent.parent
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from src.config import AppConfig
from src.gui import GuiOrchestrator
from src.network.client import CheckStatus, CheckResult
from src.proxy.free_proxy import FreeProxyProvider
from src.proxy.manager import UnifiedProxyManager
from src.utils.paths import get_bundle_dir, resolve_resource, resolve_output_path


class WebGuiState:
    """Thread-safe state container shared between Web API and Checker Engine"""
    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig.load()
        self.orchestrator: Optional[GuiOrchestrator] = None
        self.lock = threading.RLock()
        self.start_time: Optional[float] = None
        self.results_feed: collections.deque = collections.deque(maxlen=500)
        self.logs_feed: collections.deque = collections.deque(maxlen=200)
        self.proxy_manager = UnifiedProxyManager(self.config.proxy)
        self.free_proxy_provider = self.proxy_manager.get_free_provider() or FreeProxyProvider()
        self._load_existing_results()

    def _load_existing_results(self):
        """Preload previously found available usernames from available_usernames.json / db if present"""
        try:
            json_file = resolve_output_path("available_usernames.json")
            if json_file.exists():
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data[-50:]:
                            self.results_feed.append(item)
        except Exception:
            pass

    def on_result(self, result: CheckResult):
        if result.status == CheckStatus.AVAILABLE:
            entry = {
                "username": result.username,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "latency_ms": round(result.latency_ms, 1),
                "pattern_type": result.pattern_type or "unknown",
            }
            with self.lock:
                self.results_feed.append(entry)

    def on_log(self, text: str, level: str = "INFO", worker_id: Optional[int] = None):
        with self.lock:
            self.logs_feed.append(text)

    def scrape_free_proxies_async(self) -> Dict[str, Any]:
        with self.lock:
            if self.free_proxy_provider.is_scraping:
                return {"status": "busy", "message": "Scraping already in progress", "is_scraping": True}
        self.on_log("🌐 [WEB-API] 모바일 웹 제어기로부터 무료 프록시 수집 및 실시간 검증 요청 수신", "PROXY")
        self.free_proxy_provider.trigger_background_scrape(
            progress_cb=lambda c, v, t: self.on_log(f"⏳ [FREE-PROXY] 검증 진행 중: {v}개 유효 / {c}개 완료", "PROXY")
        )
        return {"status": "ok", "message": "Free proxy scraping and verification launched in background", "is_scraping": True}

    def get_free_proxy_status(self) -> Dict[str, Any]:
        return self.free_proxy_provider.get_stats()

    def start_engine(self):
        with self.lock:
            if self.orchestrator and self.orchestrator.is_running:
                return True
            # Pre-flight check for Free Proxy mode
            if self.config.proxy.get("mode") == "free":
                if not self.free_proxy_provider.has_available_proxies():
                    self.on_log("🌐 [WEB-GUI] 무료 프록시 풀 활성 노드가 없어 검사 시작 전 자동 수집 및 실시간 검증을 선행합니다...", "PROXY")
                    self.free_proxy_provider.scrape_and_verify_sync(max_candidates=250)

            self.start_time = time.time()
            self.orchestrator = GuiOrchestrator(
                config=self.config,
                on_result_cb=self.on_result,
                on_log_cb=self.on_log,
                proxy_manager=self.proxy_manager,
            )
            self.orchestrator.start_thread()
            self.on_log(f"⚡ [WEB-GUI] 모바일 웹 제어기로부터 탐색 엔진 가동 시작 ({self.orchestrator.concurrency}워커)", "START")
            return True

    def stop_engine(self):
        with self.lock:
            if self.orchestrator and self.orchestrator.is_running:
                self.orchestrator.stop()
                self.on_log("⏹️ [WEB-GUI] 모바일 웹 제어기로부터 탐색 엔진 중지 요청 수신", "STOP")
                return True
            return False

    def restart_engine(self):
        self.stop_engine()
        time.sleep(0.4)
        return self.start_engine()

    def get_status_dict(self) -> Dict[str, Any]:
        with self.lock:
            is_running = bool(self.orchestrator and self.orchestrator.is_running)
            metrics_dict = {
                "rps": 0.0,
                "total_checked": 0,
                "available_count": len(self.results_feed),
                "taken_count": 0,
                "rate_limited_count": 0,
                "skipped_count": 0,
                "error_count": 0,
                "avg_latency_ms": 0.0,
            }
            active_workers = int(self.config.network.get("concurrency", 5))
            if self.orchestrator:
                m = self.orchestrator.metrics
                active_workers = self.orchestrator.concurrency
                metrics_dict = {
                    "rps": round(m.rps, 1),
                    "total_checked": m.total_checked,
                    "available_count": m.available_count,
                    "taken_count": m.taken_count,
                    "rate_limited_count": m.rate_limited_count,
                    "skipped_count": m.skipped_count,
                    "error_count": m.error_count,
                    "avg_latency_ms": round(m.avg_latency_ms, 1),
                }

            uptime = 0.0
            if is_running and self.start_time:
                uptime = round(time.time() - self.start_time, 1)

            return {
                "running": is_running,
                "uptime_seconds": uptime,
                "active_workers": active_workers,
                "concurrency": active_workers,
                "metrics": metrics_dict,
                "results": list(self.results_feed),
                "logs": list(self.logs_feed),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }

    def update_config(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        with self.lock:
            # Concurrency update
            if "concurrency" in updates:
                new_conc = int(updates["concurrency"])
                self.config.network["concurrency"] = new_conc
                if self.orchestrator:
                    self.orchestrator.set_concurrency(new_conc)

            # Target update
            if "target" in updates and isinstance(updates["target"], dict):
                for k, v in updates["target"].items():
                    self.config.target[k] = v
                if self.orchestrator and self.orchestrator.is_running:
                    self.orchestrator.hot_swap_generator(self.config.target)

            # Proxy update
            if "proxy" in updates and isinstance(updates["proxy"], dict):
                for k, v in updates["proxy"].items():
                    self.config.proxy[k] = v
                self.proxy_manager = UnifiedProxyManager(self.config.proxy)
                self.free_proxy_provider = self.proxy_manager.get_free_provider() or self.free_proxy_provider

            # Webhook update
            if "webhook" in updates and isinstance(updates["webhook"], dict):
                for k, v in updates["webhook"].items():
                    self.config.webhook[k] = v

            # Persist updated configuration to disk
            try:
                self.config.save()
            except Exception as e:
                self.on_log(f"⚠️ 설정 파일 저장 실패: {e}", "WARN")

            return {"status": "ok", "message": "Settings updated and saved successfully"}


class D4UCWebHandler(BaseHTTPRequestHandler):
    """Zero-dependency HTTP Handler for Mobile Web GUI & PWA REST API"""
    server_state: WebGuiState

    def log_message(self, format, *args):
        # Silence routine access log spam
        pass

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """Handle CORS preflight requests from Android WebView and remote web clients."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Access-Control-Max-Age", "86400")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _serve_file(self, relative_path: str, content_type: str):
        path = resolve_resource(relative_path)
        if not path.exists():
            # Fallback check relative to script dir
            fallback = Path(__file__).resolve().parent / "ui" / "web" / Path(relative_path).name
            if fallback.exists():
                path = fallback
            else:
                self.send_error(HTTPStatus.NOT_FOUND, f"File not found: {relative_path}")
                return

        try:
            with open(path, "rb") as f:
                content = f.read()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            if "icons" in relative_path or relative_path.endswith(".js"):
                self.send_header("Cache-Control", "public, max-age=86400")
            else:
                self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Error reading file: {e}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        clean_path = parsed.path

        # Static PWA Files
        if clean_path in ("/", "/index.html"):
            self._serve_file("src/ui/web/index.html", "text/html; charset=utf-8")
        elif clean_path == "/manifest.json":
            self._serve_file("src/ui/web/manifest.json", "application/manifest+json; charset=utf-8")
        elif clean_path == "/sw.js":
            self._serve_file("src/ui/web/sw.js", "application/javascript; charset=utf-8")
        elif clean_path == "/icons/favicon.svg":
            self._serve_file("src/ui/web/icons/favicon.svg", "image/svg+xml")
        elif clean_path == "/icons/icon-192.png":
            self._serve_file("src/ui/web/icons/icon-192.png", "image/png")
        elif clean_path == "/icons/icon-512.png":
            self._serve_file("src/ui/web/icons/icon-512.png", "image/png")

        # REST APIs
        elif clean_path == "/api/status":
            self._send_json(self.server_state.get_status_dict())
        elif clean_path == "/api/proxy/free_status":
            self._send_json(self.server_state.get_free_proxy_status())
        elif clean_path == "/api/config":
            self._send_json(self.server_state.config.to_dict())
        elif clean_path == "/api/results":
            with self.server_state.lock:
                self._send_json(list(self.server_state.results_feed))
        elif clean_path == "/api/logs":
            with self.server_state.lock:
                self._send_json(list(self.server_state.logs_feed))
        elif clean_path == "/api/export":
            query = urllib.parse.parse_qs(parsed.query)
            fmt = query.get("format", ["txt"])[0].lower()
            self._handle_export(fmt)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Path not found")

    def do_POST(self):
        clean_path = urllib.parse.urlparse(self.path).path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            payload = {}

        if clean_path == "/api/start":
            res = self.server_state.start_engine()
            self._send_json({"status": "ok", "running": True, "message": "Engine started"})
        elif clean_path == "/api/stop":
            res = self.server_state.stop_engine()
            self._send_json({"status": "ok", "running": False, "message": "Engine stopped"})
        elif clean_path == "/api/restart":
            res = self.server_state.restart_engine()
            self._send_json({"status": "ok", "running": True, "message": "Engine restarted"})
        elif clean_path == "/api/config":
            result = self.server_state.update_config(payload)
            self._send_json(result)
        elif clean_path == "/api/proxy/scrape":
            result = self.server_state.scrape_free_proxies_async()
            self._send_json(result)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "API endpoint not found")

    def _handle_export(self, fmt: str):
        with self.server_state.lock:
            items = list(self.server_state.results_feed)

        # If in-memory results feed is empty, try loading from disk
        if not items:
            disk_json = resolve_output_path("available_usernames.json")
            if disk_json.exists():
                try:
                    with open(disk_json, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                        if isinstance(loaded, list):
                            items = loaded
                except Exception:
                    pass

        if fmt == "csv":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="available_usernames.csv"')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()
            import io
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(["username", "timestamp", "latency_ms", "pattern_type"])
            for r in items:
                writer.writerow([r.get("username", ""), r.get("timestamp", ""), r.get("latency_ms", ""), r.get("pattern_type", "")])
            self.wfile.write(buf.getvalue().encode("utf-8"))
        elif fmt == "json":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="available_usernames.json"')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()
            self.wfile.write(json.dumps(items, ensure_ascii=False, indent=2).encode("utf-8"))
        else: # txt
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="available_usernames.txt"')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()
            if items:
                lines = [r.get("username", "") for r in items if r.get("username")]
                out_txt = "\n".join(lines)
            else:
                disk_avail = resolve_output_path("available.txt")
                if disk_avail.exists():
                    out_txt = disk_avail.read_text(encoding="utf-8")
                else:
                    out_txt = "# D4UC v12.2.0 - No available usernames yet\n"
            self.wfile.write(out_txt.encode("utf-8"))


class WebGuiServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 5000, config: Optional[AppConfig] = None):
        self.host = host
        self.port = port
        self.state = WebGuiState(config=config)
        
        class BoundHandler(D4UCWebHandler):
            server_state = self.state

        self.httpd = HTTPServer((self.host, self.port), BoundHandler)
        self.is_running = False
        self._thread: Optional[threading.Thread] = None

    def start(self, block: bool = True):
        self.is_running = True
        print("=====================================================================")
        print(f"🚀 [D4UC Mobile Web GUI] Server running at http://localhost:{self.port}")
        print(f"📱 Access from Mobile (iPhone / Android) on same Wi-Fi: http://<PC_IP>:{self.port}")
        print(f"✨ PWA Add to Home Screen: Enabled (manifest.json & service worker active)")
        print("=====================================================================")

        if block:
            try:
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n⏹️ Stopping Mobile Web GUI Server...")
            finally:
                self.stop()
        else:
            self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self._thread.start()

    def stop(self):
        self.is_running = False
        self.state.stop_engine()
        self.httpd.shutdown()
        self.httpd.server_close()
        print("✅ Mobile Web GUI Server stopped safely.")


def main():
    parser = argparse.ArgumentParser(description="D4UC Mobile Touch-Optimized Responsive Web GUI & PWA Engine")
    parser.add_argument("--host", default="0.0.0.0", help="Host address to bind (default: 0.0.0.0)")
    parser.add_argument("--port", "-p", type=int, default=5000, help="Port to listen on (default: 5000)")
    parser.add_argument("--open-browser", action="store_true", help="Automatically open browser on startup")
    parser.add_argument("--config", "-c", help="Path to custom config.yaml file")
    args = parser.parse_args()

    cfg = AppConfig.load(args.config) if args.config else AppConfig.load()
    server = WebGuiServer(host=args.host, port=args.port, config=cfg)

    if args.open_browser:
        webbrowser.open(f"http://localhost:{args.port}")

    server.start(block=True)


if __name__ == "__main__":
    main()
