import unittest
import os
import sys
import tempfile
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import AppConfig
from src.network.client import CheckStatus, CheckResult
from src.notify.webhook import DiscordWebhookNotifier
from src.storage.drive_sync import GoogleDriveSyncManager
from run import apply_env_and_args_to_config

class TestV14WebhookAndDriveSync(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp_dir.name)
        self.drive_dir = self.tmp_path / "GoogleDrive_D4UC"
        self.drive_dir.mkdir(parents=True, exist_ok=True)

        self.local_dir = self.tmp_path / "local"
        self.local_dir.mkdir(parents=True, exist_ok=True)
        self.local_data_dir = self.local_dir / "data"
        self.local_data_dir.mkdir(parents=True, exist_ok=True)

        self.local_available = self.local_dir / "available.txt"
        self.local_db = self.local_data_dir / "d4uc_results.db"

        # Create dummy initial local DB
        with open(self.local_db, "wb") as f:
            f.write(b"local_sqlite_db_data")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_webhook_notifier_methods(self):
        notifier = DiscordWebhookNotifier(
            webhook_url="https://discord.com/api/webhooks/dummy/url",
            enabled=True,
            mention="@here"
        )

        with patch.object(notifier, "_post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = True

            result = CheckResult(
                username="covo",
                status=CheckStatus.AVAILABLE,
                latency_ms=120.5,
                pattern_type="cvcv"
            )

            # 1. Test send_alert
            asyncio.run(notifier.send_alert(result))
            self.assertTrue(mock_post.called)
            payload = mock_post.call_args[0][0]
            self.assertEqual(payload["content"], "@here")
            self.assertIn("covo", payload["embeds"][0]["description"])
            self.assertEqual(payload["embeds"][0]["color"], 0x00FF7F)

            # 2. Test send_progress_report
            mock_post.reset_mock()
            asyncio.run(notifier.send_progress_report(
                total_checked=1500,
                available_count=3,
                taken_count=1497,
                rate_limited_count=2,
                skipped_count=50,
                rps=18.4,
                mode="hybrid",
                length=4,
                workers=5,
                drive_status="동기화 정상"
            ))
            self.assertTrue(mock_post.called)
            progress_payload = mock_post.call_args[0][0]
            self.assertIn("진행 상황", progress_payload["embeds"][0]["title"])
            fields = {f["name"]: f["value"] for f in progress_payload["embeds"][0]["fields"]}
            self.assertIn("1,500", fields["총 검사 완료"])
            self.assertIn("3", fields["🟢 가용 닉네임 (된거)"])

            # 3. Test send_session_start
            mock_post.reset_mock()
            asyncio.run(notifier.send_session_start(
                mode="HYBRID",
                length=4,
                workers=5,
                proxy_mode="surfshark",
                shard="2_1",
                drive_enabled=True
            ))
            self.assertTrue(mock_post.called)
            start_payload = mock_post.call_args[0][0]
            self.assertIn("세션 가동 시작", start_payload["embeds"][0]["title"])

            # 4. Test send_session_stop
            mock_post.reset_mock()
            asyncio.run(notifier.send_session_stop(
                total_checked=3000,
                available_count=5,
                taken_count=2995,
                rate_limited_count=1,
                drive_path=str(self.drive_dir)
            ))
            self.assertTrue(mock_post.called)
            stop_payload = mock_post.call_args[0][0]
            self.assertIn("세션 종료", stop_payload["embeds"][0]["title"])

    def test_drive_sync_restore_and_sync(self):
        # 1. Prepare previous history in Google Drive
        drive_db = self.drive_dir / "d4uc_results.db"
        with open(drive_db, "wb") as f:
            f.write(b"drive_previous_sqlite_large_data_1234567890")

        drive_avail = self.drive_dir / "available.txt"
        with open(drive_avail, "w", encoding="utf-8") as f:
            f.write("prev_name1\nprev_name2\n")

        # 2. Initialize Drive Sync Manager
        manager = GoogleDriveSyncManager(
            drive_dir=str(self.drive_dir),
            local_data_dir=str(self.local_data_dir),
            local_available_file=str(self.local_available),
            local_db_file=str(self.local_db),
            sync_interval_seconds=1.0
        )
        self.assertTrue(manager.is_enabled)

        # 3. Restore from Drive
        restored = manager.restore_from_drive()
        self.assertGreater(restored, 0)
        # Check local DB updated from drive
        with open(self.local_db, "rb") as f:
            self.assertEqual(f.read(), b"drive_previous_sqlite_large_data_1234567890")
        # Check local available restored
        with open(self.local_available, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            self.assertIn("prev_name1", lines)
            self.assertIn("prev_name2", lines)

        # 4. Immediate Available sync
        manager.sync_available_immediately("new_rare_gold")
        with open(drive_avail, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("new_rare_gold", content)

        # 5. Sync to drive
        with open(self.local_db, "wb") as f:
            f.write(b"updated_local_db_bytes")
        manager.sync_to_drive(force_checkpoint=False)
        with open(drive_db, "rb") as f:
            self.assertEqual(f.read(), b"updated_local_db_bytes")

    def test_cli_and_env_drive_and_webhook_options(self):
        config = AppConfig({
            "network": {"concurrency": 5},
            "proxy": {"mode": "surfshark"},
            "target": {"mode": "hybrid", "length": 4},
            "storage": {"db_path": "data/d4uc_results.db"},
            "ui": {"rich_dashboard": True},
            "webhook": {"url": "", "enabled": False}
        })

        # Test CLI args
        args = MagicMock()
        args.mode = None
        args.length = None
        args.workers = None
        args.proxy = None
        args.shard = None
        args.start_char = None
        args.end_char = None
        args.prefix = None
        args.suffix = None
        args.middle_dot = None
        args.mask = None
        args.webhook = "https://discord.com/api/webhooks/test/url"
        args.webhook_interval = 120.0
        args.webhook_progress = True
        args.drive_dir = "/content/drive/MyDrive/D4UC"
        args.keys = None
        args.no_dashboard = False

        cfg = apply_env_and_args_to_config(config, args)
        self.assertEqual(cfg.webhook["url"], "https://discord.com/api/webhooks/test/url")
        self.assertTrue(cfg.webhook["enabled"])
        self.assertEqual(cfg.webhook["progress_interval"], 120.0)
        self.assertTrue(cfg.webhook["progress_enabled"])
        self.assertEqual(cfg.storage["drive_dir"], "/content/drive/MyDrive/D4UC")

        # Test Env Vars
        env = {
            "D4UC_WEBHOOK": "https://discord.com/api/webhooks/env/url",
            "D4UC_WEBHOOK_INTERVAL": "60",
            "D4UC_WEBHOOK_PROGRESS": "1",
            "D4UC_DRIVE_DIR": "/content/drive/MyDrive/EnvD4UC"
        }
        with patch.dict(os.environ, env):
            args.webhook = None
            args.webhook_interval = None
            args.webhook_progress = None
            args.drive_dir = None
            cfg2 = apply_env_and_args_to_config(config, args)
            self.assertEqual(cfg2.webhook["url"], "https://discord.com/api/webhooks/env/url")
            self.assertEqual(cfg2.webhook["progress_interval"], 60.0)
            self.assertTrue(cfg2.webhook["progress_enabled"])
            self.assertEqual(cfg2.storage["drive_dir"], "/content/drive/MyDrive/EnvD4UC")

        # Test CLI disable flag (--no-webhook-progress)
        args.webhook_progress = False
        cfg3 = apply_env_and_args_to_config(config, args)
        self.assertFalse(cfg3.webhook["progress_enabled"])

if __name__ == "__main__":
    unittest.main()
