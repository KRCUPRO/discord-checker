# tests/test_all_modules.py
import sys
import unittest
import asyncio
import os
import shutil
from pathlib import Path

_ROOT = Path(__file__).parent.parent.resolve()
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.config import AppConfig
from src.generator.base import DiscordRuleValidator
from src.generator.random_gen import RandomGenerator
from src.generator.pattern_gen import PatternGenerator
from src.generator.dictionary_gen import DictionaryGenerator
from src.generator.permutation_gen import PermutationGenerator
from src.generator import create_generator, HybridGenerator
from src.proxy.file_pool import FileProxyProvider
from src.proxy.thordata import ThorDataProxyProvider
from src.proxy.surfshark import SurfsharkProxyProvider
from src.proxy.manager import UnifiedProxyManager
from src.storage.db import StorageManager
from src.network.client import CheckResult, CheckStatus

class TestDiscordCheckerV2(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/tmp").resolve()
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_discord_rule_validator(self):
        # Valid
        self.assertTrue(DiscordRuleValidator.is_valid("test"))
        self.assertTrue(DiscordRuleValidator.is_valid("a.1b"))
        self.assertTrue(DiscordRuleValidator.is_valid("x_o_x"))
        self.assertTrue(DiscordRuleValidator.is_valid("xoxo"))
        
        # Invalid: leading / trailing dot
        self.assertFalse(DiscordRuleValidator.is_valid("a_1."))
        self.assertFalse(DiscordRuleValidator.is_valid(".test"))
        # Invalid: consecutive dots
        self.assertFalse(DiscordRuleValidator.is_valid("a..b"))
        # Invalid: reserved word
        self.assertFalse(DiscordRuleValidator.is_valid("discord"))
        self.assertFalse(DiscordRuleValidator.is_valid("clyde"))
        # Invalid: length out of bounds
        self.assertFalse(DiscordRuleValidator.is_valid("a", min_len=2))
        self.assertFalse(DiscordRuleValidator.is_valid("a" * 33, max_len=32))
        # Invalid characters
        self.assertFalse(DiscordRuleValidator.is_valid("ab@c"))
        self.assertFalse(DiscordRuleValidator.is_valid("한글12"))

    def test_generators(self):
        # Random Generator
        rgen = RandomGenerator(length=4)
        for _ in range(20):
            uname = rgen.next_username()
            self.assertEqual(len(uname), 4)
            self.assertTrue(DiscordRuleValidator.is_valid(uname, min_len=4, max_len=4))

        # Pattern Generator
        pgen = PatternGenerator(length=4)
        for _ in range(20):
            uname = pgen.next_username()
            self.assertEqual(len(uname), 4)
            self.assertTrue(DiscordRuleValidator.is_valid(uname, min_len=4, max_len=4))

        # Dictionary Generator
        dgen = DictionaryGenerator(length=4)
        for _ in range(20):
            uname = dgen.next_username()
            self.assertEqual(len(uname), 4)
            self.assertTrue(DiscordRuleValidator.is_valid(uname, min_len=4, max_len=4))

        # Permutation Generator
        permgen = PermutationGenerator(length=3, start_index=0)
        u1 = permgen.next_username()
        u2 = permgen.next_username()
        self.assertNotEqual(u1, u2)
        self.assertEqual(len(u1), 3)

        # Hybrid Generator (4-letter & 5-letter)
        hgen = create_generator({"mode": "hybrid", "length": 4})
        uname = hgen.next_username()
        self.assertEqual(len(uname), 4)

        hgen5 = create_generator({"mode": "hybrid", "length": 5})
        for _ in range(10):
            u5 = hgen5.next_username()
            self.assertEqual(len(u5), 5)
            self.assertTrue(DiscordRuleValidator.is_valid(u5, min_len=5, max_len=5))

        # Numeric Generator (5-letter)
        from src.generator.numeric_gen import NumericGenerator
        numgen = NumericGenerator(length=5)
        for _ in range(10):
            num = numgen.next_username()
            self.assertEqual(len(num), 5)
            self.assertTrue(num.isdigit())
            self.assertTrue(DiscordRuleValidator.is_valid(num, min_len=5, max_len=5))

        # Dictionary Generator (5-letter)
        dgen5 = DictionaryGenerator(length=5)
        for _ in range(10):
            d5 = dgen5.next_username()
            self.assertEqual(len(d5), 5)
            self.assertTrue(DiscordRuleValidator.is_valid(d5, min_len=5, max_len=5))

        # Mask / Custom Pattern Generator
        from src.generator.mask_gen import MaskPatternGenerator
        # 1. Prefix 'kr', len 4
        mgen1 = MaskPatternGenerator(length=4, prefix="kr")
        for _ in range(10):
            u = mgen1.next_username()
            self.assertEqual(len(u), 4)
            self.assertTrue(u.startswith("kr"))
            self.assertTrue(DiscordRuleValidator.is_valid(u))

        # 2. Suffix '99', len 5
        mgen2 = MaskPatternGenerator(length=5, suffix="99")
        for _ in range(10):
            u = mgen2.next_username()
            self.assertEqual(len(u), 5)
            self.assertTrue(u.endswith("99"))
            self.assertTrue(DiscordRuleValidator.is_valid(u))

        # 3. Middle dot required, len 4 (e.g. a.bc or ab.c)
        mgen3 = MaskPatternGenerator(length=4, middle_dot="required")
        for _ in range(10):
            u = mgen3.next_username()
            self.assertEqual(len(u), 4)
            self.assertIn(".", u)
            self.assertFalse(u.startswith("."))
            self.assertFalse(u.endswith("."))
            self.assertTrue(DiscordRuleValidator.is_valid(u))

    def test_proxy_file_pool(self):
        proxy_file = self.test_dir / "test_proxies.txt"
        with open(proxy_file, "w") as f:
            f.write("127.0.0.1:8080\n")
            f.write("user:pass@127.0.0.1:8081\n")
            f.write("127.0.0.1:8082:myuser:mypass\n")
            f.write("socks5://user:pass@127.0.0.1:1080\n")

        provider = FileProxyProvider(file_path=str(proxy_file), shuffle=False)
        self.assertEqual(len(provider.endpoints), 4)
        ep1 = provider.get_proxy()
        self.assertEqual(ep1.url, "http://127.0.0.1:8080")
        
        # Test cooldown
        provider.report_result(ep1, success=False, rate_limited=True, cooldown=10.0)
        self.assertFalse(ep1.is_available())

    def test_storage_db(self):
        db_file = self.test_dir / "test.db"
        avail_file = self.test_dir / "avail.txt"
        taken_file = self.test_dir / "taken.txt"

        storage = StorageManager(
            db_path=str(db_file),
            save_legacy=True,
            available_file=str(avail_file),
            taken_file=str(taken_file)
        )

        async def run_storage():
            await storage.start_worker()
            r1 = CheckResult(username="kaze", status=CheckStatus.AVAILABLE, latency_ms=105.0)
            r2 = CheckResult(username="used", status=CheckStatus.TAKEN, latency_ms=88.0)
            await storage.enqueue_result(r1)
            await storage.enqueue_result(r2)
            await storage.close()

        asyncio.run(run_storage())

        self.assertTrue(storage.is_tried("kaze"))
        self.assertTrue(storage.is_tried("used"))
        self.assertTrue(avail_file.exists())
        self.assertTrue(taken_file.exists())

        with open(avail_file, "r") as f:
            content = f.read()
            self.assertIn("kaze", content)

    def test_surfshark_provider(self):
        provider_all = SurfsharkProxyProvider(preferred_countries=[])
        self.assertTrue(provider_all.has_available_proxies())
        self.assertGreaterEqual(len(provider_all.clusters), 100)

        provider = SurfsharkProxyProvider()
        self.assertTrue(provider.has_available_proxies())
        
        # Test cluster lookup
        kr_cluster = provider.get_cluster_by_country("KR")
        self.assertIsNotNone(kr_cluster)
        self.assertIn("kr-seo", kr_cluster.host)
        
        # Test export config
        conf_path = provider._generate_wireproxy_conf(kr_cluster)
        self.assertTrue(conf_path.exists())

    def test_i18n_and_paths(self):
        from src.ui.i18n import I18nManager
        from src.utils.paths import get_app_dir, resolve_resource, resolve_output_path, find_wireproxy_bin

        # Test I18nManager
        I18nManager.set_language("ko")
        self.assertIn("D4UC", I18nManager.t("app_title"))
        self.assertIn("검사 시작", I18nManager.t("btn_start"))

        I18nManager.set_language("en")
        self.assertIn("Checker", I18nManager.t("app_title"))
        self.assertIn("Start Checking", I18nManager.t("btn_start"))

        # Test paths
        app_dir = get_app_dir()
        self.assertTrue(app_dir.exists())

        res_path = resolve_resource("config.yaml") if resolve_resource("config.yaml").exists() else resolve_resource("config.example.yaml")
        self.assertTrue(res_path.exists())

        out_path = resolve_output_path("tests/tmp_out.txt")
        self.assertIsNotNone(out_path)

        wireproxy_bin = find_wireproxy_bin()
        self.assertTrue(wireproxy_bin.exists())

if __name__ == "__main__":
    unittest.main()
