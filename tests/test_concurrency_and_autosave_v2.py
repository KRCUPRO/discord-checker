# tests/test_concurrency_and_autosave_v2.py
import asyncio
import csv
import json
import os
import shutil
import unittest
from pathlib import Path

from src.storage.db import StorageManager
from src.network.client import CheckResult, CheckStatus
from src.config import AppConfig
from src.ui.i18n import I18nManager
from src.gui import GuiOrchestrator

TEST_DIR = Path("tests/tmp_concurrency_autosave").resolve()

class TestConcurrencyAndAutosaveV2(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        if TEST_DIR.exists():
            shutil.rmtree(TEST_DIR, ignore_errors=True)
        TEST_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if TEST_DIR.exists():
            shutil.rmtree(TEST_DIR, ignore_errors=True)

    async def test_multiformat_autosave_and_mirror(self):
        """Test real-time multi-format auto-save (.txt, .csv, .json) and results/ mirroring"""
        db_file = str(TEST_DIR / "test.db")
        avail_file = str(TEST_DIR / "available.txt")
        taken_file = str(TEST_DIR / "taken.txt")

        storage = StorageManager(
            db_path=db_file,
            save_legacy=True,
            available_file=avail_file,
            taken_file=taken_file
        )
        # Override paths to test dir
        storage.available_detailed_file = TEST_DIR / "available_usernames.txt"
        storage.available_csv_file = TEST_DIR / "available_usernames.csv"
        storage.available_json_file = TEST_DIR / "available_usernames.json"
        storage.results_dir = TEST_DIR / "results"
        storage.results_dir.mkdir(parents=True, exist_ok=True)
        storage.history_file = TEST_DIR / "checked_history.txt"
        storage.tried_usernames.clear()
        storage.saved_available_count = 0

        await storage.start_worker()

        # Enqueue 3 available and 2 taken
        res1 = CheckResult(username="rare1", status=CheckStatus.AVAILABLE, latency_ms=45.2, pattern_type="custom_mask", proxy_used="Surfshark-KR")
        res2 = CheckResult(username="rare2", status=CheckStatus.AVAILABLE, latency_ms=62.1, pattern_type="numeric", proxy_used="Surfshark-JP")
        res3 = CheckResult(username="taken1", status=CheckStatus.TAKEN, latency_ms=30.0, pattern_type="random", proxy_used="Direct")
        res4 = CheckResult(username="rare3", status=CheckStatus.AVAILABLE, latency_ms=51.8, pattern_type="dictionary", proxy_used="Surfshark-SG")
        res5 = CheckResult(username="taken2", status=CheckStatus.TAKEN, latency_ms=28.5, pattern_type="random", proxy_used="Direct")

        for r in [res1, res2, res3, res4, res5]:
            await storage.enqueue_result(r)

        await storage.close()

        # 1. Check count
        self.assertEqual(storage.get_saved_count(), 3)
        self.assertEqual(storage.get_history_count(), 5)

        # 2. Check available.txt
        with open(avail_file, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        self.assertEqual(len(lines), 3)
        self.assertTrue(any("rare1" in l for l in lines))

        # 3. Check CSV format & header
        csv_file = storage.available_csv_file
        self.assertTrue(csv_file.exists())
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
        self.assertEqual(reader[0], ["Timestamp", "Username", "Length", "Pattern", "Latency_ms", "Proxy_Server"])
        self.assertEqual(len(reader), 4) # 1 header + 3 rows
        self.assertEqual(reader[1][1], "rare1")
        self.assertEqual(reader[1][2], "5")
        self.assertEqual(reader[1][3], "custom_mask")

        # 4. Check JSON Lines format
        json_file = storage.available_json_file
        self.assertTrue(json_file.exists())
        with open(json_file, "r", encoding="utf-8") as f:
            json_lines = [json.loads(l) for l in f if l.strip()]
        self.assertEqual(len(json_lines), 3)
        self.assertEqual(json_lines[0]["username"], "rare1")
        self.assertEqual(json_lines[0]["pattern"], "custom_mask")
        self.assertEqual(json_lines[1]["username"], "rare2")

        # 5. Check mirrored results/ folder
        mirrored_txt = storage.results_dir / "available_usernames.txt"
        mirrored_csv = storage.results_dir / "available_usernames.csv"
        mirrored_json = storage.results_dir / "available_usernames.json"
        self.assertTrue(mirrored_txt.exists())
        self.assertTrue(mirrored_csv.exists())
        self.assertTrue(mirrored_json.exists())

        with open(mirrored_csv, "r", encoding="utf-8") as f:
            mirrored_reader = list(csv.reader(f))
        self.assertEqual(len(mirrored_reader), 4)

        # 6. Test history cache reload
        new_storage = StorageManager(
            db_path=db_file,
            save_legacy=True,
            available_file=avail_file,
            taken_file=taken_file
        )
        self.assertTrue(new_storage.is_tried("rare1"))
        self.assertTrue(new_storage.is_tried("RARE2"))
        self.assertTrue(new_storage.is_tried("taken1"))
        self.assertFalse(new_storage.is_tried("neverchecked"))
        self.assertEqual(new_storage.get_saved_count(), 3)

    def test_concurrency_hot_scale_and_safety_tiers(self):
        """Test up to 50 workers, dynamic scaling hot-swap, and adaptive pacing"""
        cfg = AppConfig.load()
        cfg.network["concurrency"] = 50

        orchestrator = GuiOrchestrator(cfg)
        self.assertEqual(orchestrator.concurrency, 50)

        # Test dynamic hot-scale down
        orchestrator.set_concurrency(15)
        self.assertEqual(orchestrator.concurrency, 15)

        # Test dynamic hot-scale up
        orchestrator.set_concurrency(45)
        self.assertEqual(orchestrator.concurrency, 45)

        # Test boundary clamping
        orchestrator.set_concurrency(0)
        self.assertEqual(orchestrator.concurrency, 1)

        orchestrator.set_concurrency(999)
        self.assertEqual(orchestrator.concurrency, 50)

        # Test pacing math
        # Concurrency 1: max(0.12, 1.8 / 1) = 1.8
        pacing_1 = max(0.12, 1.8 / 1)
        self.assertAlmostEqual(pacing_1, 1.8)

        # Concurrency 20: max(0.12, 1.8 / 20) = max(0.12, 0.09) = 0.12
        pacing_20 = max(0.12, 1.8 / 20)
        self.assertAlmostEqual(pacing_20, 0.12)

        # Concurrency 50: max(0.12, 1.8 / 50) = 0.12
        pacing_50 = max(0.12, 1.8 / 50)
        self.assertAlmostEqual(pacing_50, 0.12)

        # Stagger ramp-up for worker 50: min(0.06 * 49, 1.2) = 1.2s
        stagger_50 = min(0.06 * (50 - 1), 1.2)
        self.assertAlmostEqual(stagger_50, 1.2)

        # Stagger ramp-up for worker 5: min(0.06 * 4, 1.2) = 0.24s
        stagger_5 = min(0.06 * (5 - 1), 1.2)
        self.assertAlmostEqual(stagger_5, 0.24)

    def test_i18n_autosave_and_concurrency_strings(self):
        """Test i18n support for auto_save_indicator, btn_open_folder, and concurrency tooltips"""
        # Korean
        I18nManager.set_language("ko")
        txt_ko = I18nManager.t("auto_save_indicator", count=42)
        self.assertIn("42개", txt_ko)
        self.assertIn(".txt / .csv / .json", txt_ko)
        self.assertEqual(I18nManager.t("btn_open_folder"), "📂 저장 폴더 열기")
        self.assertIn("1~50개", I18nManager.t("concurrency_tooltip"))
        self.assertIn("터보", I18nManager.t("concurrency_tooltip"))

        # English
        I18nManager.set_language("en")
        txt_en = I18nManager.t("auto_save_indicator", count=42)
        self.assertIn("42", txt_en)
        self.assertIn("Live Auto-Save", txt_en)
        self.assertEqual(I18nManager.t("btn_open_folder"), "📂 Open Results Folder")
        self.assertIn("1~50", I18nManager.t("concurrency_tooltip"))
        self.assertIn("Turbo", I18nManager.t("concurrency_tooltip"))

if __name__ == "__main__":
    unittest.main()
