# tests/test_v9_multi_instance_sharding_and_sync.py
import sys
import unittest
import string
import shutil
import asyncio
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.generator.permutation_gen import (
    PermutationGenerator,
    SHARD_PRESETS,
    FIRST_CHARACTERS,
    get_sharded_first_characters
)
from src.generator import create_generator
from src.storage.db import StorageManager, safe_append_text, safe_append_csv
from src.network.client import CheckResult, CheckStatus

class TestV9MultiInstanceShardingAndSync(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/temp_v9_test")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = str(self.test_dir / "test_sync.db")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_permutation_sharding_2_way_split_disjoint(self):
        """2분할 (1번 창: a~m vs 2번 창: n~_)이 100% 겹치지 않는 상호 배타적 닉네임을 생성하는지 검증"""
        g1 = PermutationGenerator(length=4, shard_key="2_1")
        g2 = PermutationGenerator(length=4, shard_key="2_2")

        names1 = [g1.next_username() for _ in range(50)]
        names2 = [g2.next_username() for _ in range(50)]

        self.assertEqual(len(names1), 50)
        self.assertEqual(len(names2), 50)

        # Disjoint check
        intersection = set(names1).intersection(set(names2))
        self.assertEqual(intersection, set())

        # Check first char checks
        self.assertTrue(all(name[0] in "abcdefghijklm" for name in names1))
        self.assertTrue(all(name[0] in string.ascii_lowercase[13:] + string.digits + "_" for name in names2))

    def test_permutation_sharding_total_combinations_math(self):
        """2분할 1번창과 2번창의 total_combinations 합이 전체 4글자 순열 수와 일치하는지 수학적 무결성 검증"""
        g_all = PermutationGenerator(length=4)
        g1 = PermutationGenerator(length=4, shard_key="2_1")
        g2 = PermutationGenerator(length=4, shard_key="2_2")

        self.assertEqual(g1.total_combinations + g2.total_combinations, g_all.total_combinations)
        self.assertEqual(g_all.total_combinations, 37 * (38 ** 3))
        self.assertEqual(g1.total_combinations, 13 * (38 ** 3))
        self.assertEqual(g2.total_combinations, 24 * (38 ** 3))

    def test_permutation_sharding_4_way_split_disjoint(self):
        """4분할 (1~4번 창) 생성기 4개가 상호 간 0% 교집합을 보장하는지 검증"""
        generators = [PermutationGenerator(length=4, shard_key=f"4_{i}") for i in range(1, 5)]
        sampled_sets = []
        for g in generators:
            names = [g.next_username() for _ in range(30)]
            sampled_sets.append(set(names))

        for i in range(4):
            for j in range(i + 1, 4):
                common = sampled_sets[i].intersection(sampled_sets[j])
                self.assertEqual(common, set(), f"Shard 4_{i+1} and 4_{j+1} intersected: {common}")

    def test_permutation_custom_range(self):
        """커스텀 글자 범위 (예: k ~ p) 지정 시 해당 범위 글자로만 시작하는지 검증"""
        gen = PermutationGenerator(length=4, start_char="k", end_char="p")
        first_chars = gen.first_chars
        self.assertEqual(first_chars, ["k", "l", "m", "n", "o", "p"])

        names = [gen.next_username() for _ in range(25)]
        self.assertTrue(all(name[0] in "klmnop" for name in names))

    def test_create_generator_with_permutation_sharding(self):
        """create_generator 팩토리 함수가 config target의 shard_key 및 start/end_char를 정상 반영하는지 검증"""
        cfg = {
            "mode": "permutation",
            "length": 4,
            "shard_key": "2_2"
        }
        gen = create_generator(cfg)
        self.assertIsInstance(gen, PermutationGenerator)
        self.assertEqual(gen.start_char, "n")
        self.assertEqual(gen.end_char, "_")

    def test_storage_cross_instance_checked_delta_sync(self):
        """창 A가 SQLite DB에 검사 결과를 기록하면 창 B가 fetch_new_checked_since로 즉각 감지하는지 검증"""
        storage_a = StorageManager(db_path=self.db_path)
        storage_b = StorageManager(db_path=self.db_path)

        initial_rowid = storage_b.get_max_rowid()

        # Window A writes 5 checked usernames
        async def _test():
            await storage_a.start_worker()
            for i in range(5):
                res = CheckResult(
                    username=f"testuser_{i}",
                    status=CheckStatus.TAKEN,
                    pattern_type="permutation_4char",
                    latency_ms=120.0
                )
                await storage_a.enqueue_result(res)
            await storage_a.close()

        asyncio.run(_test())

        # Window B fetches newly checked delta
        new_names, next_rowid = storage_b.fetch_new_checked_since(initial_rowid)
        self.assertEqual(len(new_names), 5)
        for i in range(5):
            self.assertIn(f"testuser_{i}", new_names)
        self.assertGreater(next_rowid, initial_rowid)

    def test_storage_cross_instance_available_delta_sync(self):
        """창 A가 발견한 사용 가능 닉네임을 창 B가 fetch_new_available_since로 세부 메타데이터와 함께 정상 감지하는지 검증"""
        storage_a = StorageManager(db_path=self.db_path)
        storage_b = StorageManager(db_path=self.db_path)

        start_rowid = storage_b.get_max_rowid()

        # Window A finds an available username
        async def _test():
            await storage_a.start_worker()
            res = CheckResult(
                username="cool_name",
                status=CheckStatus.AVAILABLE,
                pattern_type="custom_mask",
                latency_ms=85.5,
                proxy_used="http://127.0.0.1:1081"
            )
            await storage_a.enqueue_result(res)
            await storage_a.close()

        asyncio.run(_test())

        # Window B queries new available usernames
        new_available, new_max_id = storage_b.fetch_new_available_since(start_rowid)
        self.assertEqual(len(new_available), 1)
        rec = new_available[0]
        self.assertEqual(rec["username"], "cool_name")
        self.assertEqual(rec["pattern"], "custom_mask")
        self.assertEqual(rec["latency"], "85.5ms")
        self.assertEqual(rec["server"], "http://127.0.0.1:1081")

    def test_safe_append_concurrent_file_writes(self):
        """다중 스레드가 safe_append_text 및 safe_append_csv를 동시 호출해도 충돌 없이 100% 정상 기록되는지 검증"""
        txt_path = self.test_dir / "concurrent_append.txt"
        csv_path = self.test_dir / "concurrent_append.csv"

        def _worker(wid):
            for i in range(10):
                safe_append_text(txt_path, f"worker_{wid}_line_{i}\n")
                safe_append_csv(csv_path, "col1,col2\n", f"worker_{wid},{i}\n")
            return True

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(_worker, w) for w in range(8)]
            results = [f.result() for f in futures]

        self.assertTrue(all(results))

        # Check total lines written: 8 workers * 10 lines = 80 lines
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        self.assertEqual(len(lines), 80)

        with open(csv_path, "r", encoding="utf-8") as f:
            csv_lines = [l.strip() for l in f if l.strip()]
        # 1 header + 80 rows = 81 lines
        self.assertEqual(len(csv_lines), 81)

if __name__ == "__main__":
    unittest.main()
