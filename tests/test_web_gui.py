# tests/test_web_gui.py
import json
import sys
import time
import unittest
import urllib.request
import urllib.parse
from pathlib import Path

_ROOT = Path(__file__).parent.parent.resolve()
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.config import AppConfig
from src.web_gui import WebGuiServer, WebGuiState
from src.network.client import CheckResult, CheckStatus

class TestWebGui(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 5899
        cls.config = AppConfig.load()
        cls.server = WebGuiServer(host="127.0.0.1", port=cls.port, config=cls.config)
        cls.server.start(block=False)
        time.sleep(0.6)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        time.sleep(0.3)

    def _get(self, path: str):
        url = f"http://127.0.0.1:{self.port}{path}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            data = res.read()
            return res.status, res.headers, data

    def _post(self, path: str, payload: dict):
        url = f"http://127.0.0.1:{self.port}{path}"
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as res:
            data = res.read()
            return res.status, json.loads(data.decode("utf-8"))

    def test_pwa_index_html(self):
        status, headers, body = self._get("/")
        self.assertEqual(status, 200)
        self.assertIn(b"D4UC Mobile Web", body)
        self.assertIn(b"manifest.json", body)
        self.assertIn(b"sw.js", body)

    def test_pwa_manifest_json(self):
        status, headers, body = self._get("/manifest.json")
        self.assertEqual(status, 200)
        manifest = json.loads(body.decode("utf-8"))
        self.assertEqual(manifest["short_name"], "D4UC Web")
        self.assertEqual(manifest["display"], "standalone")
        self.assertTrue(len(manifest["icons"]) >= 2)

    def test_pwa_service_worker(self):
        status, headers, body = self._get("/sw.js")
        self.assertEqual(status, 200)
        self.assertIn(b"d4uc-v12.2.0-cache", body)
        self.assertIn(b"addEventListener('fetch'", body)

    def test_pwa_icons(self):
        status_svg, _, body_svg = self._get("/icons/favicon.svg")
        self.assertEqual(status_svg, 200)
        self.assertIn(b"<svg", body_svg)

        status_png, _, body_png = self._get("/icons/icon-192.png")
        self.assertEqual(status_png, 200)
        self.assertTrue(len(body_png) > 100)

    def test_api_status(self):
        status, _, body = self._get("/api/status")
        self.assertEqual(status, 200)
        data = json.loads(body.decode("utf-8"))
        self.assertIn("running", data)
        self.assertIn("metrics", data)
        self.assertIn("rps", data["metrics"])
        self.assertIn("total_checked", data["metrics"])
        self.assertIn("available_count", data["metrics"])

    def test_api_config_get_and_post(self):
        # 1. GET
        status, _, body = self._get("/api/config")
        self.assertEqual(status, 200)
        cfg = json.loads(body.decode("utf-8"))
        self.assertIn("target", cfg)

        # 2. POST update
        status, res = self._post("/api/config", {
            "concurrency": 8,
            "target": {"mode": "numeric", "length": 4}
        })
        self.assertEqual(status, 200)
        self.assertEqual(res["status"], "ok")

        # Verify updated in state
        status_after, _, body_after = self._get("/api/status")
        data_after = json.loads(body_after.decode("utf-8"))
        self.assertEqual(data_after["concurrency"], 8)

    def test_api_results_and_logs(self):
        # Manually inject test result into state
        dummy_result = CheckResult(
            username="test_vip",
            status=CheckStatus.AVAILABLE,
            latency_ms=45.2,
            pattern_type="custom_mask"
        )
        self.server.state.on_result(dummy_result)
        self.server.state.on_log("Test log entry for unit test", "INFO")

        # GET /api/results
        status, _, body = self._get("/api/results")
        self.assertEqual(status, 200)
        results = json.loads(body.decode("utf-8"))
        self.assertTrue(any(r["username"] == "test_vip" for r in results))

        # GET /api/logs
        status, _, body = self._get("/api/logs")
        self.assertEqual(status, 200)
        logs = json.loads(body.decode("utf-8"))
        self.assertTrue(any("Test log entry" in l for l in logs))

    def test_api_exports(self):
        for fmt in ["txt", "csv", "json"]:
            status, headers, body = self._get(f"/api/export?format={fmt}")
            self.assertEqual(status, 200)
            self.assertIn("attachment", headers.get("Content-Disposition", ""))
            self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")
            self.assertTrue(len(body) > 0)

    def test_options_cors_preflight(self):
        """Verifies CORS preflight OPTIONS handling for Android WebView & remote web clients."""
        for endpoint in ["/api/config", "/api/start", "/api/stop", "/api/restart", "/api/proxy/scrape"]:
            url = f"http://127.0.0.1:{self.port}{endpoint}"
            req = urllib.request.Request(
                url,
                method="OPTIONS",
                headers={
                    "Origin": "file://",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            with urllib.request.urlopen(req) as res:
                self.assertEqual(res.status, 204)
                self.assertEqual(res.headers.get("Access-Control-Allow-Origin"), "*")
                self.assertIn("OPTIONS", res.headers.get("Access-Control-Allow-Methods", ""))
                self.assertIn("Content-Type", res.headers.get("Access-Control-Allow-Headers", ""))

    def test_web_index_html_js_syntax(self):
        """Verifies all embedded JavaScript in index.html is syntactically valid."""
        import shutil
        import subprocess
        import re
        node_bin = shutil.which("node")
        if not node_bin:
            self.skipTest("node.js not available")

        index_path = _ROOT / "src" / "ui" / "web" / "index.html"
        html = index_path.read_text(encoding="utf-8")
        scripts = re.findall(r"<script(?:\s+[^>]*)?>([\s\S]*?)</script>", html, re.IGNORECASE)
        self.assertGreater(len(scripts), 0)
        for idx, script in enumerate(scripts):
            res = subprocess.run([node_bin, "-e", "new Function(process.argv[1])", script], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"Script block {idx} syntax error:\n{res.stderr}")

    def test_api_free_proxy_endpoints(self):
        # 1. GET /api/proxy/free_status
        status, _, body = self._get("/api/proxy/free_status")
        self.assertEqual(status, 200)
        data = json.loads(body.decode("utf-8"))
        self.assertEqual(data["status"], "ok")
        self.assertIn("verified_count", data)
        self.assertIn("alive_count", data)
        self.assertIn("is_scraping", data)

        # 2. POST /api/proxy/scrape
        status_post, res_post = self._post("/api/proxy/scrape", {})
        self.assertEqual(status_post, 200)
        self.assertIn(res_post["status"], ["ok", "busy"])

if __name__ == "__main__":
    unittest.main()
