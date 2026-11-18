# tests/test_v4_rotation_and_combinatorial.py
import unittest
import asyncio
import time
import threading
from unittest.mock import MagicMock, AsyncMock, patch

from src.generator.combinatorial_gen import CombinatorialGenerator
from src.generator import create_generator
from src.proxy.surfshark import SurfsharkProxyProvider, SurfsharkCluster
from src.network.client import DiscordApiClient
from src.network.exceptions import ProxyFailedException


class TestCombinatorialGenerator(unittest.TestCase):
    """영숫자 전수조사 조합 생성기 (CombinatorialGenerator) 검증"""

    def test_ascending_num_first_samples(self):
        """0-9 a-z 숫자 우선 오름차순 생성 검증 (0000, 000a, 00a1, zzzz 등)"""
        gen = CombinatorialGenerator(length=2, charset_type="alphanumeric_num_first", direction="asc")
        self.assertEqual(gen.total_combinations, 36 * 36)
        
        first = gen.next_username()
        self.assertEqual(first, "00")
        
        # Advance to index 10 -> '0a'
        for _ in range(9):
            gen.next_username()
        self.assertEqual(gen.next_username(), "0a")

        # Create fresh generator for length 4
        gen4 = CombinatorialGenerator(length=4, charset_type="alphanumeric_num_first", direction="asc")
        first4 = gen4.next_username()
        self.assertEqual(first4, "0000")
        self.assertEqual(gen4.total_combinations, 36**4)

    def test_descending_num_first_samples(self):
        """내림차순 생성 검증 (zzzz ➔ 0000)"""
        gen = CombinatorialGenerator(length=2, charset_type="alphanumeric_num_first", direction="desc")
        first = gen.next_username()
        self.assertEqual(first, "zz")
        second = gen.next_username()
        self.assertEqual(second, "zy")

        gen4 = CombinatorialGenerator(length=4, charset_type="alphanumeric_num_first", direction="desc")
        self.assertEqual(gen4.next_username(), "zzzz")
        self.assertEqual(gen4.next_username(), "zzzy")

    def test_alpha_first_ordering(self):
        """a-z 0-9 영문 우선 순서 검증"""
        gen = CombinatorialGenerator(length=2, charset_type="alphanumeric_alpha_first", direction="asc")
        self.assertEqual(gen.next_username(), "aa")
        self.assertEqual(gen.next_username(), "ab")

    def test_prefix_and_suffix(self):
        """Prefix / Suffix 바인딩 검증 (예: kr00 ~ krzz)"""
        gen = CombinatorialGenerator(length=4, prefix="kr", charset_type="alphanumeric_num_first", direction="asc")
        self.assertEqual(gen.total_combinations, 36 * 36)
        self.assertEqual(gen.next_username(), "kr00")
        self.assertEqual(gen.next_username(), "kr01")

    def test_multithreaded_unique_consumption(self):
        """멀티스레드 동시 소비 시 중복 0% 무결성 검증"""
        gen = CombinatorialGenerator(length=3, charset_type="alphanumeric_num_first", direction="asc")
        consumed = []
        lock = threading.Lock()

        def worker():
            for _ in range(500):
                uname = gen.next_username()
                if uname:
                    with lock:
                        consumed.append(uname)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(consumed), 5000)
        self.assertEqual(len(set(consumed)), 5000, "동시 워커 간 중복 발급이 없어야 함")

    def test_create_generator_factory(self):
        """create_generator 팩토리 연동 검증"""
        cfg = {
            "mode": "combinatorial",
            "length": 5,
            "direction": "desc",
            "charset_type": "num_first"
        }
        gen = create_generator(cfg)
        self.assertIsInstance(gen, CombinatorialGenerator)
        self.assertEqual(gen.length, 5)
        self.assertEqual(gen.direction, "desc")


class Test429PenaltyRotationQueue(unittest.TestCase):
    """429 레이트리밋 감지 국가 페널티 큐 및 신선한 국가 우선 매칭 검증"""

    def setUp(self):
        self.mock_clusters = [
            SurfsharkCluster({"id": "c1", "country": "Korea", "countryCode": "KR", "city": "Seoul", "host": "kr.surfshark.com", "pubKey": "kpk=", "load": 10}),
            SurfsharkCluster({"id": "c2", "country": "Japan", "countryCode": "JP", "city": "Tokyo", "host": "jp.surfshark.com", "pubKey": "jpk=", "load": 20}),
            SurfsharkCluster({"id": "c3", "country": "Singapore", "countryCode": "SG", "city": "Singapore", "host": "sg.surfshark.com", "pubKey": "sgk=", "load": 30}),
            SurfsharkCluster({"id": "c4", "country": "United States", "countryCode": "US", "city": "New York", "host": "us.surfshark.com", "pubKey": "usk=", "load": 40}),
            SurfsharkCluster({"id": "c5", "country": "Germany", "countryCode": "DE", "city": "Frankfurt", "host": "de.surfshark.com", "pubKey": "dek=", "load": 50}),
        ]

    @patch("src.proxy.surfshark.find_wireproxy_bin")
    def test_fresh_cluster_initial_1_to_1_matching(self, mock_bin):
        mock_bin.return_value = None
        provider = SurfsharkProxyProvider()
        provider.clusters = list(self.mock_clusters)
        with provider._cluster_lock:
            provider._available_clusters = type(provider._available_clusters)(provider.clusters)
            provider._cooldown_clusters.clear()
            provider._assigned_clusters.clear()

        c_w1 = provider._acquire_fresh_cluster(worker_id=1)
        c_w2 = provider._acquire_fresh_cluster(worker_id=2)
        c_w3 = provider._acquire_fresh_cluster(worker_id=3)

        self.assertEqual(c_w1.country_code, "KR")
        self.assertEqual(c_w2.country_code, "JP")
        self.assertEqual(c_w3.country_code, "SG")
        # Ensure 1:1 uniqueness
        self.assertEqual(len({c_w1.id, c_w2.id, c_w3.id}), 3)

    @patch("src.proxy.surfshark.find_wireproxy_bin")
    def test_429_moves_cluster_to_cooldown_and_tail(self, mock_bin):
        mock_bin.return_value = None
        provider = SurfsharkProxyProvider()
        provider.clusters = list(self.mock_clusters)
        with provider._cluster_lock:
            provider._available_clusters = type(provider._available_clusters)(provider.clusters)
            provider._cooldown_clusters.clear()
            provider._assigned_clusters.clear()

        # Worker 1 gets KR (c1)
        w1_init = provider._acquire_fresh_cluster(worker_id=1)
        self.assertEqual(w1_init.id, "c1")

        # Worker 1 hits 429 with 0.1s cooldown for fast test
        with patch.object(provider, "_get_or_create_node") as mock_node_fn:
            mock_node = MagicMock()
            mock_node_fn.return_value = mock_node

            fresh = provider.rotate_cluster(worker_id=1, cooldown_seconds=0.2)
            # Worker 1 should immediately get next FRESH cluster (c2: JP)
            self.assertEqual(fresh.id, "c2")
            self.assertIn("c1", provider._cooldown_clusters)

            # Available clusters currently has c3, c4, c5 (c1 is in cooldown, c2 is assigned)
            avail_ids = [c.id for c in provider._available_clusters]
            self.assertNotIn("c1", avail_ids)

            # Wait for cooldown to expire
            time.sleep(0.25)
            # Next reclaim should move c1 to the TAIL (맨 뒤)
            provider._reclaim_expired_cooldowns(time.time())
            tail_cluster = provider._available_clusters[-1]
            self.assertEqual(tail_cluster.id, "c1", "429 감지 클러스터는 쿨다운 만료 후 큐의 맨 마지막(Tail)으로 복귀해야 함")


class TestZeroHostLeakHardGate(unittest.TestCase):
    """호스트 공인 IP 직접 누출 방지 하드게이트 (Zero Host Leak Invariant) 검증"""

    def test_require_proxy_blocks_none_proxy(self):
        """require_proxy=True 상태에서 proxy=None 전달 시 즉각 예외 차단"""
        client = DiscordApiClient()
        session = MagicMock()

        async def _run():
            await client.check(
                session=session,
                username="test",
                proxy=None,
                require_proxy=True
            )

        with self.assertRaises(ProxyFailedException) as ctx:
            asyncio.run(_run())

        self.assertIn("Zero Host Leak Hard Gate", str(ctx.exception))
        # Verify no network post was made on session
        session.post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
