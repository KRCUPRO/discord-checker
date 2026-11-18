# tests/test_v3_recheck_multitunnel_persistence.py
import os
import sys
import json
import tempfile
import unittest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import AppConfig
from src.proxy.surfshark import SurfsharkProxyProvider, SurfsharkCluster, SingleTunnelNode
from src.storage.db import StorageManager
from src.network.client import CheckStatus, CheckResult


class TestV3RecheckMultiTunnelPersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_app_config_persistence_roundtrip(self):
        """Test AppConfig save and load round-trip with all V3 UI settings"""
        cfg_file = self.test_dir / "test_config.yaml"
        sample_data = {
            "target": {
                "mode": "recheck",
                "length": 5,
                "prefix": "kr",
                "suffix": "vip",
                "middle_dot": "required",
                "mask": "kr?.vip",
                "skip_already_checked": True
            },
            "network": {
                "concurrency": 8,
                "timeout_seconds": 6.0
            },
            "proxy": {
                "mode": "surfshark",
                "surfshark": {
                    "preferred_countries": [],
                    "preferred_country_label": "전세계 142개 전체",
                    "http_port": 1081
                }
            },
            "webhook": {
                "enabled": True,
                "url": "https://discord.com/api/webhooks/test/123"
            },
            "ui": {
                "last_mode": "Re-check (기존 닉네임 재확인)",
                "last_length": 5,
                "last_proxy": "Surfshark (격리 프록시)",
                "last_country": "전세계 142개 전체",
                "last_concurrency": 8,
                "last_lang": "ko"
            }
        }
        cfg = AppConfig(sample_data)
        cfg.save(cfg_file)
        self.assertTrue(cfg_file.exists())

        loaded_cfg = AppConfig.load(cfg_file)
        self.assertEqual(loaded_cfg.target["mode"], "recheck")
        self.assertEqual(loaded_cfg.target["length"], 5)
        self.assertEqual(loaded_cfg.target["prefix"], "kr")
        self.assertEqual(loaded_cfg.network["concurrency"], 8)
        self.assertEqual(loaded_cfg.proxy["surfshark"]["preferred_countries"], [])
        self.assertEqual(loaded_cfg.ui["last_country"], "전세계 142개 전체")

    def test_surfshark_1_to_1_multi_tunnel_allocation(self):
        """Test that SurfsharkProxyProvider allocates unique ports and clusters to each worker"""
        clusters_data = [
            {"id": "kr-sel", "country": "South Korea", "countryCode": "KR", "city": "Seoul", "host": "kr-sel.prod.surfshark.com", "pubKey": "key1", "load": 10},
            {"id": "jp-tok", "country": "Japan", "countryCode": "JP", "city": "Tokyo", "host": "jp-tok.prod.surfshark.com", "pubKey": "key2", "load": 15},
            {"id": "us-nyc", "country": "United States", "countryCode": "US", "city": "New York", "host": "us-nyc.prod.surfshark.com", "pubKey": "key3", "load": 20},
            {"id": "de-fra", "country": "Germany", "countryCode": "DE", "city": "Frankfurt", "host": "de-fra.prod.surfshark.com", "pubKey": "key4", "load": 25},
            {"id": "sg-sin", "country": "Singapore", "countryCode": "SG", "city": "Singapore", "host": "sg-sin.prod.surfshark.com", "pubKey": "key5", "load": 30},
        ]
        clusters_file = self.test_dir / "clusters.json"
        import json
        with open(clusters_file, "w", encoding="utf-8") as f:
            json.dump(clusters_data, f)

        prov = SurfsharkProxyProvider(
            clusters_path=str(clusters_file),
            preferred_countries=[] # All global clusters
        )

        # Allocate 5 workers
        summary = prov.get_workers_summary(5)
        self.assertEqual(len(summary), 5)

        # Check port uniqueness based on dynamic port base
        ports = [prov.nodes[wid].http_port for wid in range(1, 6)]
        expected_ports = [prov._port_base + wid for wid in range(1, 6)]
        self.assertEqual(ports, expected_ports)
        self.assertEqual(len(set(ports)), 5)

        # Check cluster uniqueness per worker
        cluster_ids = [prov.nodes[wid].cluster.id for wid in range(1, 6)]
        self.assertEqual(len(set(cluster_ids)), 5)

    def test_storage_load_usernames_from_file(self):
        """Test loading usernames from .txt, .csv, and .json files with deduplication"""
        # 1. TXT format
        txt_path = self.test_dir / "names.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("user1\n[12:00:00] user2\nuser3 | detail\nuser1\n")
        names_txt = StorageManager.load_usernames_from_file(txt_path)
        self.assertEqual(names_txt, ["user1", "user2", "user3"])

        # 2. CSV format
        csv_path = self.test_dir / "names.csv"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("time,username,pattern,latency,server\n12:00:00,rare1,4char,10ms,KR\n12:01:00,rare2,4char,12ms,JP\n")
        names_csv = StorageManager.load_usernames_from_file(csv_path)
        self.assertIn("rare1", names_csv)
        self.assertIn("rare2", names_csv)

        # 3. JSON format
        json_path = self.test_dir / "names.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([{"username": "json1"}, {"username": "json2"}], f)
        names_json = StorageManager.load_usernames_from_file(json_path)
        self.assertEqual(names_json, ["json1", "json2"])

    def test_storage_update_recheck_status(self):
        """Test DB and taken.txt update when re-checking an available username that became TAKEN"""
        db_path = self.test_dir / "test.db"
        taken_file = self.test_dir / "taken.txt"
        storage = StorageManager(
            db_path=str(db_path),
            taken_file=str(taken_file)
        )

        # Insert dummy available item directly in DB
        import sqlite3
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO checked_usernames (username, status, pattern_type, latency_ms, proxy_used) VALUES (?, ?, ?, ?, ?)",
                  ("target_nick", "available", "4char", 50.0, "KR"))
        conn.commit()
        conn.close()

        # Execute re-check status update to TAKEN
        storage.update_recheck_status("target_nick", CheckStatus.TAKEN, 45.0, "Surfshark US")

        # Verify DB updated
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT status, proxy_used FROM checked_usernames WHERE username = 'target_nick'")
        row = c.fetchone()
        conn.close()
        self.assertEqual(row[0], "taken")
        self.assertEqual(row[1], "Surfshark US")

        # Verify taken.txt appended
        self.assertTrue(taken_file.exists())
        with open(taken_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("target_nick", content)
            self.assertIn("Recheck: TAKEN", content)


if __name__ == "__main__":
    unittest.main()
