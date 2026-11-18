# tests/test_v7_high_perf_50workers.py
import sqlite3
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.proxy.surfshark import SurfsharkProxyProvider, SingleTunnelNode, SurfsharkCluster
from src.network.client import CheckResult, CheckStatus
from src.storage.db import StorageManager

class TestV7HighPerf50Workers(unittest.TestCase):
    def test_single_tunnel_node_fast_ensure_running(self):
        cluster = SurfsharkCluster({
            "id": "np-ktm",
            "country": "Nepal",
            "city": "Kathmandu",
            "pubKey": "UKMTmY99xrUwchQNucd1SW6CmIFsDH1JpxQStRWA1V4=",
            "host": "np-ktm.prod.surfshark.com"
        })
        node = SingleTunnelNode(
            node_id=1,
            cluster=cluster,
            http_port=1081,
            socks5_port=2081,
            private_key="test_key",
            warmup_delay=0.0
        )
        fake_proc = MagicMock()
        fake_proc.poll.return_value = None
        node.proc = fake_proc

        with patch.object(node, "_is_port_open") as mock_port:
            self.assertTrue(node.ensure_running())
            mock_port.assert_not_called()

    def test_get_proxy_includes_readable_country_city_port(self):
        provider = SurfsharkProxyProvider(
            private_key=["key1", "key2"],
            preferred_countries=[]
        )
        c1 = SurfsharkCluster({"id": "np-ktm", "country": "Nepal", "city": "Kathmandu", "load": 10})
        c2 = SurfsharkCluster({"id": "pk-khi", "country": "Pakistan", "city": "Karachi", "load": 15})
        provider.clusters = [c1, c2]

        with patch.object(SingleTunnelNode, "ensure_running", return_value=True):
            ep1 = provider.get_proxy(worker_id=1)
            self.assertIsNotNone(ep1)
            self.assertIn("Nepal", ep1.provider_name)
            self.assertIn(str(provider._port_base + 1), ep1.provider_name)

            ep2 = provider.get_proxy(worker_id=2)
            self.assertIsNotNone(ep2)
            self.assertIn("Pakistan", ep2.provider_name)
            self.assertIn(str(provider._port_base + 2), ep2.provider_name)

    def test_cloudflare_trace_connectivity_parser(self):
        cluster = SurfsharkCluster({"id": "np-ktm", "country": "Nepal", "city": "Kathmandu"})
        node = SingleTunnelNode(
            node_id=1,
            cluster=cluster,
            http_port=1081,
            socks5_port=2081,
            private_key="test_key",
            warmup_delay=0.0
        )
        sample_cf_trace = (
            "fl=34f374\n"
            "h=1.1.1.1\n"
            "ip=194.169.170.55\n"
            "ts=1794825372.000\n"
            "loc=NP\n"
        ).encode("utf-8")

        mock_resp = MagicMock()
        mock_resp.read.return_value = sample_cf_trace
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.OpenerDirector.open", return_value=mock_resp):
            ok, ip = node.verify_connectivity(timeout=1.0)
            self.assertTrue(ok)
            self.assertEqual(ip, "194.169.170.55")
            self.assertEqual(node.last_verified_ip, "194.169.170.55")

    def test_result_proxy_used_friendly_binding(self):
        db_path = Path("tests/test_v7.db")
        if db_path.exists():
            db_path.unlink()
        storage = StorageManager(
            db_path=str(db_path),
            available_file="tests/test_v7_avail.txt"
        )
        storage.results_dir = Path("tests/non_existent_results")
        storage.available_csv_file = Path("tests/non_existent_avail.csv")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO checked_usernames (username, status, pattern_type, length, latency_ms, proxy_used)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("v7test", "available", "custom_test", 6, 120.5, "Surfshark [Nepal - Kathmandu (194.169.170.55) (:1081)]"))
        conn.commit()
        conn.close()

        records = storage.get_discovered_available_records()
        self.assertTrue(any(r["username"] == "v7test" and "Nepal" in r["server"] for r in records))
        if db_path.exists():
            db_path.unlink()

if __name__ == "__main__":
    unittest.main()
