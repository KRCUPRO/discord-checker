import unittest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import AppConfig
from src.utils.paths import ensure_wireproxy_firewall_rule, find_wireproxy_bin
from src.proxy.surfshark import SurfsharkProxyProvider
from run import apply_env_and_args_to_config

class TestV11LinuxAndCli(unittest.TestCase):
    def setUp(self):
        self.orig_env = dict(os.environ)
        os.environ.pop("SURFSHARK_PRIVATE_KEYS", None)
        os.environ.pop("SURFSHARK_PRIVATE_KEY", None)
        self.config = AppConfig({
            "network": {"concurrency": 5, "timeout_seconds": 8.0, "impersonate": "chrome131"},
            "proxy": {"mode": "surfshark", "surfshark": {"private_key": "", "private_keys": []}},
            "target": {"mode": "hybrid", "length": 4},
            "storage": {"db_path": "data/test.db"},
            "ui": {"rich_dashboard": True},
            "webhook": {"url": "", "enabled": False}
        })

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.orig_env)

    def test_cli_args_override_config(self):
        args = MagicMock()
        args.mode = "permutation"
        args.length = 3
        args.workers = 10
        args.proxy = "file"
        args.shard = "2_1"
        args.start_char = None
        args.end_char = None
        args.prefix = None
        args.suffix = None
        args.middle_dot = None
        args.mask = None
        args.webhook = "https://discord.com/api/webhooks/123/abc"
        args.keys = "key_alpha,key_beta"
        args.no_dashboard = True

        cfg = apply_env_and_args_to_config(self.config, args)
        self.assertEqual(cfg.target["mode"], "permutation")
        self.assertEqual(cfg.target["length"], 3)
        self.assertEqual(cfg.network["concurrency"], 10)
        self.assertEqual(cfg.proxy["mode"], "file")
        self.assertEqual(cfg.target["shard_key"], "2_1")
        self.assertEqual(cfg.webhook["url"], "https://discord.com/api/webhooks/123/abc")
        self.assertTrue(cfg.webhook["enabled"])
        self.assertIn("key_alpha", cfg.proxy["surfshark"]["private_keys"])
        self.assertIn("key_beta", cfg.proxy["surfshark"]["private_keys"])
        self.assertFalse(cfg.ui["rich_dashboard"])

    def test_env_vars_override_config(self):
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
        args.webhook = None
        args.keys = None
        args.no_dashboard = False

        env = {
            "D4UC_MODE": "random",
            "D4UC_LENGTH": "5",
            "D4UC_WORKERS": "8",
            "D4UC_PROXY": "direct",
            "D4UC_SHARD": "3_2",
            "D4UC_WEBHOOK": "https://discord.com/api/webhooks/env_hook",
            "SURFSHARK_PRIVATE_KEYS": "env_key1,env_key2",
            "D4UC_NO_DASHBOARD": "1"
        }
        with patch.dict(os.environ, env):
            cfg = apply_env_and_args_to_config(self.config, args)
            # D4UC_SHARD sets mode to permutation
            self.assertEqual(cfg.target["mode"], "permutation")
            self.assertEqual(cfg.target["shard_key"], "3_2")
            self.assertEqual(cfg.target["length"], 5)
            self.assertEqual(cfg.network["concurrency"], 8)
            self.assertEqual(cfg.proxy["mode"], "direct")
            self.assertEqual(cfg.webhook["url"], "https://discord.com/api/webhooks/env_hook")
            self.assertTrue(cfg.webhook["enabled"])
            self.assertIn("env_key1", cfg.proxy["surfshark"]["private_keys"])
            self.assertIn("env_key2", cfg.proxy["surfshark"]["private_keys"])
            self.assertFalse(cfg.ui["rich_dashboard"])

    def test_linux_firewall_rule_skipped_on_posix(self):
        with patch("sys.platform", "linux"):
            with patch("subprocess.run") as mock_subproc:
                ensure_wireproxy_firewall_rule("wireproxy")
                mock_subproc.assert_not_called()

    def test_linux_find_wireproxy_bin(self):
        with patch("sys.platform", "linux"):
            with patch("shutil.which", return_value="/usr/bin/wireproxy"):
                with patch.object(Path, "is_file", return_value=True):
                    with patch("src.utils.paths._make_executable_if_posix"):
                        path = find_wireproxy_bin()
                        self.assertTrue(str(path).replace("\\", "/").endswith("wireproxy"))

    def test_surfshark_linux_popen_kwargs(self):
        with patch("sys.platform", "linux"):
            provider = SurfsharkProxyProvider(
                private_key="test_key",
                http_port=1081
            )
            self.assertIn("test_key", provider.private_keys)

    def test_surfshark_env_keys_priority(self):
        with patch.dict(os.environ, {"SURFSHARK_PRIVATE_KEYS": "k_env_1, k_env_2"}):
            provider = SurfsharkProxyProvider(
                private_key="fallback_key",
                http_port=1081
            )
            self.assertIn("k_env_1", provider.private_keys)
            self.assertIn("k_env_2", provider.private_keys)

if __name__ == "__main__":
    unittest.main()
