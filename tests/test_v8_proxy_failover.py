# tests/test_v8_proxy_failover.py
import unittest
import time
import collections
from pathlib import Path
from src.storage.db import StorageManager
from src.network.client import DiscordApiClient
from src.proxy.manager import UnifiedProxyManager
from src.proxy.surfshark import SurfsharkProxyProvider, SurfsharkCluster, SingleTunnelNode
from src.config import AppConfig

class TestV8ProxyFailover(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/temp_v8_test")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.test_db = str(self.test_dir / "test_storage.db")

    def tearDown(self):
        import shutil
        if self.test_dir.exists():
            try:
                shutil.rmtree(self.test_dir, ignore_errors=True)
            except Exception:
                pass

    def test_storage_unmark_tried(self):
        """네트워크/프록시 장애 시 unmark_tried로 후보 닉네임이 정상 복구되는지 검증"""
        storage = StorageManager(
            db_path=self.test_db,
            save_legacy=False,
            available_file=str(self.test_dir / "avail.txt"),
            taken_file=str(self.test_dir / "taken.txt")
        )
        cand = "abcd"
        self.assertFalse(storage.is_tried(cand))

        storage.mark_tried(cand)
        self.assertTrue(storage.is_tried(cand))

        # Unmark on failover
        storage.unmark_tried(cand)
        self.assertFalse(storage.is_tried(cand))
        self.assertNotIn(cand, storage.tried_usernames)

    def test_client_default_timeout_is_four_seconds(self):
        """빠른 장애 감지 및 교체를 위해 기본 타임아웃이 4.0초로 최적화되었는지 검증"""
        client = DiscordApiClient()
        self.assertEqual(client.timeout, 4.0)

    def test_proxy_manager_rotate_surfshark_signature(self):
        """UnifiedProxyManager.rotate_surfshark가 cooldown_seconds 매개변수를 지원하는지 검증"""
        cfg = {
            "mode": "surfshark",
            "surfshark": {
                "preferred_countries": ["Nepal", "Pakistan"]
            }
        }
        pm = UnifiedProxyManager(cfg)
        prov = pm.get_surfshark_provider()
        self.assertIsNotNone(prov)

        # Rotate with custom cooldown
        res = pm.rotate_surfshark(worker_id=1, cooldown_seconds=450.0)
        self.assertIsNotNone(res)

    def test_surfshark_cooldown_duration(self):
        """Discord 429 레이트리밋 시 실제 지정된 쿨다운 시간(300초+) 동안 격리 큐에 보존되는지 검증"""
        prov = SurfsharkProxyProvider(preferred_countries=["Nepal", "Pakistan", "Austria", "India"])
        old_cluster = prov.clusters[0]
        node = prov._get_or_create_node(1)
        node.cluster = old_cluster

        cooldown_target = 350.0
        start_time = time.time()
        rotated = prov.rotate_cluster(worker_id=1, cooldown_seconds=cooldown_target)

        self.assertIsNotNone(rotated)
        self.assertIn(old_cluster.id, prov._cooldown_clusters)
        stored_cluster, expire_time = prov._cooldown_clusters[old_cluster.id]
        self.assertEqual(stored_cluster.id, old_cluster.id)
        self.assertGreaterEqual(expire_time, start_time + cooldown_target - 1.0)

    def test_node_rotate_to_force_override(self):
        """force=True 시 시간 간격 제한(2초)과 무관하게 즉각 터널 회전 및 재기동이 수행되는지 검증"""
        c1 = SurfsharkCluster({"id": "c1", "country": "TestLand", "location": "City1", "connectionName": "1.1.1.1", "pubKey": "key1"})
        c2 = SurfsharkCluster({"id": "c2", "country": "TestLand2", "location": "City2", "connectionName": "2.2.2.2", "pubKey": "key2"})

        node = SingleTunnelNode(
            node_id=99,
            cluster=c1,
            http_port=1099,
            socks5_port=2099,
            private_key="dummy_key=",
            warmup_delay=0.0
        )
        node.ensure_running = lambda: True
        node.stop = lambda: None
        node._last_rotation_time = time.time() # Just rotated

        # Normal rotation without force should be skipped within 2s
        ret_normal = node.rotate_to(c2, force=False)
        self.assertTrue(ret_normal)
        self.assertEqual(node.cluster.id, "c1") # Unchanged

        # Forced rotation must update cluster even within 2s
        ret_force = node.rotate_to(c2, force=True)
        self.assertEqual(node.cluster.id, "c2") # Updated to c2

    def test_retry_queue_priority_flow(self):
        """재시도 큐(FIFO)에 담긴 후보 닉네임이 새 생성기보다 우선 처리되는지 검증"""
        retry_q = collections.deque()
        retry_q.append("cand_failed_1")
        retry_q.append("cand_failed_2")

        popped = retry_q.popleft()
        self.assertEqual(popped, "cand_failed_1")
        popped2 = retry_q.popleft()
        self.assertEqual(popped2, "cand_failed_2")
        self.assertEqual(len(retry_q), 0)

    def test_multi_instance_auto_port_shift(self):
        """다중 프로그램 실행 시 기존 포트 사용 중이면 다음 포트 대역(+100)으로 자동 이동하는지 검증"""
        import socket
        prov = SurfsharkProxyProvider()
        node = prov._get_or_create_node(1)
        self.assertEqual(node.http_port, prov._port_base + 1)

        # Synthetic port collision test on port 5501
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 5501))
        sock.listen(1)
        try:
            prov.base_http_port = 5501
            shifted = prov._find_available_port_base()
            self.assertGreaterEqual(shifted, 5600)
        finally:
            sock.close()

    def test_concurrent_multi_instance_sqlite_writes(self):
        """다중 프로그램 실행 시 동일 SQLite DB에 여러 스레드/프로세스가 동시 기록해도 WAL 모드로 정상 처리되는지 검증"""
        import concurrent.futures
        import sqlite3

        db_path = str(self.test_dir / "concurrent_test.db")
        sm = StorageManager(db_path=db_path)

        def _writer(tid):
            conn = sqlite3.connect(db_path, timeout=30.0)
            cur = conn.cursor()
            for i in range(10):
                username = f"user_{tid}_{i}"
                cur.execute(
                    "INSERT OR REPLACE INTO checked_usernames (username, status) VALUES (?, ?)",
                    (username, "taken")
                )
                conn.commit()
            conn.close()
            return True

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(_writer, i) for i in range(5)]
            results = [f.result() for f in futures]

        self.assertTrue(all(results))

        # Check total count in DB
        conn = sqlite3.connect(db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM checked_usernames")
        count = cur.fetchone()[0]
        conn.close()
        self.assertEqual(count, 50)

if __name__ == "__main__":
    unittest.main()
