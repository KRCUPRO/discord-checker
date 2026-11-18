"""
Unit tests verifying that SingleTunnelNode and SurfsharkProxyProvider
do not deadlock on 429 rotation and parallel worker startup.
"""

import unittest
import threading
import time
from unittest.mock import MagicMock, patch
from src.proxy.surfshark import SingleTunnelNode, SurfsharkCluster, SurfsharkProxyProvider


class TestSurfsharkDeadlockPrevention(unittest.TestCase):
    def setUp(self):
        self.cluster1 = SurfsharkCluster({
            "id": "c1", "country": "Korea", "countryCode": "KR", "city": "Seoul",
            "host": "kr.surfshark.com", "pubKey": "kpk=", "load": 10
        })
        self.cluster2 = SurfsharkCluster({
            "id": "c2", "country": "Japan", "countryCode": "JP", "city": "Tokyo",
            "host": "jp.surfshark.com", "pubKey": "jpk=", "load": 20
        })

    def test_single_tunnel_node_lock_is_rlock(self):
        """SingleTunnelNode._lock must be re-entrant (RLock) to allow rotate_to -> ensure_running"""
        node = SingleTunnelNode(
            node_id=1,
            cluster=self.cluster1,
            http_port=1081,
            socks5_port=2081,
            private_key="test_key",
            warmup_delay=0.1
        )
        self.assertIsInstance(node._lock, type(threading.RLock()), "SingleTunnelNode._lock must be threading.RLock")

        # Test acquiring lock multiple times in the same thread (re-entrancy proof)
        with node._lock:
            acquired_again = False
            with node._lock:
                acquired_again = True
            self.assertTrue(acquired_again, "Lock must allow re-entrant acquisition in the same thread")

    def test_rotate_to_calls_ensure_running_without_deadlock(self):
        """Simulate rotate_to calling ensure_running under lock with mock subprocess/port"""
        node = SingleTunnelNode(
            node_id=1,
            cluster=self.cluster1,
            http_port=1081,
            socks5_port=2081,
            private_key="test_key",
            warmup_delay=0.0
        )

        with patch.object(node, "_generate_conf") as mock_conf, \
             patch("src.proxy.surfshark.find_wireproxy_bin") as mock_bin, \
             patch("subprocess.Popen") as mock_popen, \
             patch.object(node, "_is_port_open", return_value=True), \
             patch.object(node, "verify_connectivity", return_value=(True, "1.2.3.4")):

            mock_conf.return_value = "/tmp/dummy.conf"
            mock_bin.return_value = MagicMock(exists=lambda: True)
            mock_proc = MagicMock()
            mock_proc.poll.return_value = None
            mock_popen.return_value = mock_proc

            # Run rotate_to in a thread with a strict timeout (e.g., 2.0s).
            # If a deadlock exists, the thread will hang and time out.
            result = []
            def _run():
                ok = node.rotate_to(self.cluster2)
                result.append(ok)

            t = threading.Thread(target=_run)
            t.start()
            t.join(timeout=2.0)

            self.assertFalse(t.is_alive(), "rotate_to thread MUST finish within timeout (Deadlock detected if alive!)")
            self.assertEqual(len(result), 1)
            self.assertTrue(result[0])
            self.assertEqual(node.cluster.id, "c2")
            self.assertFalse(node.is_rotating)
            self.assertTrue(node._ready_event.is_set())

    def test_concurrent_multi_worker_rotations(self):
        """Simulate 5 workers concurrently rotating clusters under heavy rate limiting"""
        provider = SurfsharkProxyProvider()
        provider.clusters = [
            SurfsharkCluster({"id": f"c{i}", "country": f"Country{i}", "countryCode": f"C{i}", "city": f"City{i}", "host": f"c{i}.com", "pubKey": "pk=", "load": i})
            for i in range(1, 15)
        ]
        with provider._cluster_lock:
            provider._available_clusters = type(provider._available_clusters)(provider.clusters)
            provider._cooldown_clusters.clear()
            provider._assigned_clusters.clear()

        # Mock node operations to avoid spawning real wireproxy
        def mock_node_ensure(node):
            node.ensure_running = MagicMock(return_value=True)
            node._is_port_open = MagicMock(return_value=True)
            node.verify_connectivity = MagicMock(return_value=(True, f"10.0.0.{node.node_id}"))

        # Pre-create 5 nodes
        for wid in range(1, 6):
            n = provider._get_or_create_node(wid)
            mock_node_ensure(n)

        # Concurrently rotate 5 workers 5 times each (25 total rotations)
        completed = []
        lock = threading.Lock()

        def worker_task(wid):
            for _ in range(5):
                cl = provider.rotate_cluster(worker_id=wid, cooldown_seconds=0.1)
                with lock:
                    completed.append((wid, cl.id if cl else None))
                time.sleep(0.01)

        threads = [threading.Thread(target=worker_task, args=(i,)) for i in range(1, 6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5.0)

        for t in threads:
            self.assertFalse(t.is_alive(), "All worker rotation threads must complete without deadlocks")

        self.assertEqual(len(completed), 25, "All 25 rotations must successfully complete")

    def test_ensure_workers_running_parallelism(self):
        """Test that ensure_workers_running starts workers in parallel"""
        provider = SurfsharkProxyProvider()
        provider.clusters = [
            SurfsharkCluster({"id": f"c{i}", "country": f"Country{i}", "countryCode": f"C{i}", "city": f"City{i}", "host": f"c{i}.com", "pubKey": "pk=", "load": i})
            for i in range(1, 10)
        ]
        with provider._cluster_lock:
            provider._available_clusters = type(provider._available_clusters)(provider.clusters)

        # Mock each node.ensure_running to take 0.1s
        for wid in range(1, 6):
            node = provider._get_or_create_node(wid)
            node.ensure_running = MagicMock(side_effect=lambda: time.sleep(0.1) or True)

        start = time.time()
        ok = provider.ensure_workers_running(worker_count=5)
        elapsed = time.time() - start

        self.assertTrue(ok)
        # If sequential: 5 * 0.1s = 0.5s+. If parallel: ~0.1s - 0.25s
        self.assertLess(elapsed, 0.45, f"ensure_workers_running must run in parallel, took {elapsed:.2f}s")


if __name__ == "__main__":
    unittest.main()
