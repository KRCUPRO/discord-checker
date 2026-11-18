"""
Unit tests for D4UC V6:
- Multi-Account WireGuard Key Round-Robin Distribution
- 50-Worker Parallel Startup & Auto-Healing on Failed Nodes
- UI Input Locking during RUNNING
- High-Throughput Worker Pacing Optimization
"""

import unittest
from unittest.mock import MagicMock, patch
from src.proxy.surfshark import SurfsharkProxyProvider, SurfsharkCluster, SingleTunnelNode


class TestMultiAccountAnd50Workers(unittest.TestCase):
    def test_multi_account_key_round_robin_distribution(self):
        """다중 WireGuard 키 등록 시 워커들에게 라운드로빈(Round-Robin) 방식으로 균등 분산 배정되는지 검증"""
        keys = [
            "KEY_ACCOUNT_1_AAAAAAAAAAAAAAAAAAAAAA=",
            "KEY_ACCOUNT_2_BBBBBBBBBBBBBBBBBBBBBB=",
            "KEY_ACCOUNT_3_CCCCCCCCCCCCCCCCCCCCCC="
        ]
        provider = SurfsharkProxyProvider(private_key=keys)
        self.assertEqual(len(provider.private_keys), 3)

        # Worker 1 -> Key 1
        n1 = provider._get_or_create_node(1)
        self.assertEqual(n1.private_key, keys[0])

        # Worker 2 -> Key 2
        n2 = provider._get_or_create_node(2)
        self.assertEqual(n2.private_key, keys[1])

        # Worker 3 -> Key 3
        n3 = provider._get_or_create_node(3)
        self.assertEqual(n3.private_key, keys[2])

        # Worker 4 -> Key 1 (Loop back)
        n4 = provider._get_or_create_node(4)
        self.assertEqual(n4.private_key, keys[0])

        # Worker 50 -> Key 2 ((50 - 1) % 3 = 1 -> keys[1])
        n50 = provider._get_or_create_node(50)
        self.assertEqual(n50.private_key, keys[(50 - 1) % 3])

    def test_auto_healing_on_50_workers_startup(self):
        """50개 워커 기동 시 일부 노드가 실패해도 대체 클러스터로 자동 교체(Auto-Healing)하여 생존하는지 검증"""
        provider = SurfsharkProxyProvider()
        # Provide 60 mock clusters so replacements are available
        provider.clusters = [
            SurfsharkCluster({"id": f"c{i}", "country": f"Country{i}", "countryCode": f"C{i}", "city": f"City{i}", "host": f"c{i}.com", "pubKey": "pk=", "load": i})
            for i in range(1, 70)
        ]
        with provider._cluster_lock:
            provider._available_clusters = type(provider._available_clusters)(provider.clusters)

        # Pre-create 50 nodes with mock ensure_running
        attempt_counts = {}
        for wid in range(1, 51):
            node = provider._get_or_create_node(wid)
            attempt_counts[wid] = 0

            def make_mock(w=wid, n=node):
                def _ensure():
                    attempt_counts[w] += 1
                    # Workers 5 and 17 fail on attempt 1, but succeed on attempt 2 (Auto-Healing)
                    if w in (5, 17) and attempt_counts[w] == 1:
                        return False
                    n._is_port_open = MagicMock(return_value=True)
                    return True
                return _ensure

            node.ensure_running = make_mock()
            node._is_port_open = MagicMock(return_value=False)

        ok = provider.ensure_workers_running(worker_count=50)
        self.assertTrue(ok, "Auto-healing must heal failed nodes and allow 50 workers to run")
        # Workers 5 and 17 should have been called twice (1st fail, 2nd healed)
        self.assertEqual(attempt_counts[5], 2)
        self.assertEqual(attempt_counts[17], 2)

    def test_ui_input_locking(self):
        """검사 실행 중(RUNNING) 워커 수 슬라이더 및 주요 입력이 비활성화(disabled)되는지 검증"""
        from src import gui
        app = gui.DiscordCheckerGui(default_lang="ko")
        app.withdraw()

        try:
            # 1. Initial IDLE state -> normal
            self.assertEqual(app.concurrency_slider.cget("state"), "normal")
            self.assertEqual(app.mode_menu.cget("state"), "normal")
            self.assertEqual(app.proxy_menu.cget("state"), "normal")

            # 2. Lock UI
            app._set_inputs_locked(True)
            self.assertEqual(app.concurrency_slider.cget("state"), "disabled")
            self.assertEqual(app.mode_menu.cget("state"), "disabled")
            self.assertEqual(app.proxy_menu.cget("state"), "disabled")
            self.assertEqual(app.country_menu.cget("state"), "disabled")
            self.assertEqual(app.length_menu.cget("state"), "disabled")

            # 3. Unlock UI
            app._set_inputs_locked(False)
            self.assertEqual(app.concurrency_slider.cget("state"), "normal")
            self.assertEqual(app.mode_menu.cget("state"), "normal")
            self.assertEqual(app.proxy_menu.cget("state"), "normal")

        finally:
            app.destroy()

    def test_load_persisted_multi_keys_from_json(self):
        """data/surfshark_credentials.json 또는 임시 credentials.json에 저장된 다중 키가 Provider에 자동 로드되는지 검증"""
        import json
        import tempfile
        from pathlib import Path
        temp_creds = {
            "wireguard_keys": [
                "dummy_key_1_alpha_bravo_charlie_delta_echo_1=",
                "dummy_key_2_alpha_bravo_charlie_delta_echo_2="
            ]
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(temp_creds, f)
            temp_path = Path(f.name)

        try:
            provider = SurfsharkProxyProvider(credentials_path=temp_path)
            self.assertGreaterEqual(len(provider.private_keys), 2)
            self.assertIn("dummy_key_1_alpha_bravo_charlie_delta_echo_1=", provider.private_keys)
            self.assertIn("dummy_key_2_alpha_bravo_charlie_delta_echo_2=", provider.private_keys)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_launch_surfshark_browser_helper(self):
        """서프샤크 키 발급 전용 격리 브라우저 팝업 트리거 호출 검증"""
        from src import gui
        app = gui.DiscordCheckerGui(default_lang="ko")
        app.withdraw()

        try:
            with patch("subprocess.Popen") as mock_popen, patch("os.path.exists", return_value=True):
                app._launch_surfshark_login_browser()
                mock_popen.assert_called_once()
                call_args = mock_popen.call_args[0][0]
                self.assertIn("https://my.surfshark.com/vpn/manual-setup/main/wireguard", call_args)
                self.assertTrue(any("--user-data-dir=" in arg for arg in call_args))
        finally:
            app.destroy()


if __name__ == "__main__":
    unittest.main()
