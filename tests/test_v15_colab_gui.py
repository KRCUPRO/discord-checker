# tests/test_v15_colab_gui.py
# Unit test for D4UC Colab-Native Interactive Web GUI
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('Discord-4Character-Usernames-Checker'))
from src.ui.colab_gui import ColabDashboard
from src.ui.i18n import SUPPORTED_LANGUAGES


class TestColabDashboard(unittest.TestCase):
    def test_dashboard_instantiation(self):
        dash = ColabDashboard(lang="ko", title="Test Checker")
        self.assertEqual(dash.lang, "ko")
        self.assertTrue(dash.container_id.startswith("d4uc_dashboard_"))

    def test_dashboard_html_contains_required_components(self):
        dash = ColabDashboard(lang="en")
        html = dash.get_html()
        
        # Check container and styling
        self.assertIn(dash.container_id, html)
        self.assertIn("d4uc-wrapper", html)
        
        # Check 6 KPI cards
        self.assertIn("d4uc-kpi-card", html)
        self.assertIn("_val_rps", html)
        self.assertIn("_val_total", html)
        self.assertIn("_val_avail", html)
        self.assertIn("_val_taken", html)
        self.assertIn("_val_429", html)
        self.assertIn("_val_skip", html)
        
        # Check visual progress bar
        self.assertIn("d4uc-progress-bar-fill", html)
        
        # Check discovered table
        self.assertIn("d4uc-table-scroll", html)
        self.assertIn("_tbody", html)
        
        # Check log console and control buttons
        self.assertIn("d4uc-log-box", html)
        self.assertIn("d4uc_toggle_log", html)
        self.assertIn("d4uc_clear_log", html)
        self.assertIn("d4uc_download_log", html)
        
        # Check 10-language options in select
        for code in SUPPORTED_LANGUAGES:
            self.assertIn(f'value="{code}"', html)

    def test_dashboard_data_addition(self):
        dash = ColabDashboard()
        dash.add_username("test", "2026-11-23 00:00:00", 85, "4char")
        self.assertEqual(len(dash._usernames), 1)
        self.assertEqual(dash._usernames[0]["username"], "test")

        dash.append_log("[SYSTEM] Unit test log line")
        self.assertEqual(len(dash._logs), 1)
        self.assertIn("Unit test log line", dash._logs[0])


if __name__ == '__main__':
    unittest.main()
