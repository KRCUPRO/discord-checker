"""
Integration test for DiscordCheckerGui search and filter UI controls.
Directly instantiates GUI and verifies live Treeview updates, sorting, and 0% data loss.
"""

import sys
import unittest
from pathlib import Path
from typing import Dict, Any

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


class TestGuiTableSearchIntegration(unittest.TestCase):
    def test_gui_search_and_filter_live(self):
        # Import gui inside test
        from src import gui
        from src.ui.i18n import I18nManager

        # Instantiate GUI in Korean
        app = gui.DiscordCheckerGui(default_lang="ko")
        app.withdraw() # Hide window during test

        try:
            # 1. Verify search and filter widgets exist
            self.assertTrue(hasattr(app, "search_entry"))
            self.assertTrue(hasattr(app, "btn_clear_search"))
            self.assertTrue(hasattr(app, "filter_len_menu"))
            self.assertTrue(hasattr(app, "filter_type_menu"))
            self.assertTrue(hasattr(app, "filter_sort_menu"))
            self.assertTrue(hasattr(app, "btn_reset_filters"))
            self.assertTrue(hasattr(app, "lbl_table_filter_count"))

            # 2. Inject mock discovered items
            mock_items = [
                {"time": "12:00:01", "username": "ace", "pattern": "cvcv_dict", "latency": "150.0ms", "latency_val": 150.0, "server": "KR", "length": 3},
                {"time": "12:00:02", "username": "vip1", "pattern": "mask:vip?", "latency": "250.0ms", "latency_val": 250.0, "server": "JP", "length": 4},
                {"time": "12:00:03", "username": "8888", "pattern": "num_repeating", "latency": "80.0ms", "latency_val": 80.0, "server": "US", "length": 4},
                {"time": "12:00:04", "username": "abba", "pattern": "abba_symm", "latency": "190.0ms", "latency_val": 190.0, "server": "KR", "length": 4},
                {"time": "12:00:05", "username": "x.one", "pattern": "dot_isolated", "latency": "320.0ms", "latency_val": 320.0, "server": "SG", "length": 5},
                {"time": "12:00:06", "username": "0a1b", "pattern": "comb_asc", "latency": "95.0ms", "latency_val": 95.0, "server": "KR", "length": 4},
                {"time": "12:00:07", "username": "legend_kr", "pattern": "word_compound", "latency": "550.0ms", "latency_val": 550.0, "server": "DE", "length": 9},
                {"time": "12:00:08", "username": "vip99", "pattern": "custom_pre", "latency": "175.0ms", "latency_val": 175.0, "server": "US", "length": 5},
            ]
            app.discovered_items = list(mock_items)

            # 3. Initial render
            app._refresh_discovered_table()
            self.assertEqual(len(app.tree.get_children()), 8)
            self.assertIn("전체: 8개", app.lbl_table_filter_count.cget("text"))

            # 4. Text search: "vip"
            app.search_entry.delete(0, "end")
            app.search_entry.insert(0, "vip")
            app._on_search_query_changed(None)

            tree_unames = [str(app.tree.item(c)["values"][1]) for c in app.tree.get_children()]
            self.assertEqual(len(tree_unames), 2)
            self.assertIn("vip1", tree_unames)
            self.assertIn("vip99", tree_unames)
            self.assertIn("필터: 2 / 8개", app.lbl_table_filter_count.cget("text"))

            # 5. Clear search button [✕]
            app._clear_search_entry()
            self.assertEqual(len(app.tree.get_children()), 8)
            self.assertEqual(app.search_entry.get(), "")

            # 6. Wildcard search: "*_kr"
            app.search_entry.insert(0, "*_kr")
            app._on_search_query_changed(None)
            tree_unames_wc = [str(app.tree.item(c)["values"][1]) for c in app.tree.get_children()]
            self.assertEqual(tree_unames_wc, ["legend_kr"])

            app._clear_search_entry()

            # 7. Length filter: "[4글자]"
            app.filter_len_menu.set("[4글자]")
            app._on_filter_changed(None)
            tree_unames_l4 = [str(app.tree.item(c)["values"][1]) for c in app.tree.get_children()]
            self.assertEqual(len(tree_unames_l4), 4) # vip1, 8888, abba, 0a1b
            for u in tree_unames_l4:
                self.assertEqual(len(str(u)), 4)

            # 8. Pattern/Type filter: "[순수 숫자닉]"
            app.filter_type_menu.set("[순수 숫자닉]")
            app._on_filter_changed(None)
            tree_unames_num = [str(app.tree.item(c)["values"][1]) for c in app.tree.get_children()]
            self.assertEqual(tree_unames_num, ["8888"])

            # 9. Reset all filters [🔄]
            app._reset_all_filters()
            self.assertEqual(len(app.tree.get_children()), 8)
            self.assertIn(I18nManager.t("filter_len_all"), app.filter_len_menu.get())
            self.assertIn(I18nManager.t("filter_type_all"), app.filter_type_menu.get())

            # 10. Sort filter: A-Z
            app.filter_sort_menu.set("[닉네임 (A-Z)]")
            app._on_filter_changed(None)
            unames_sorted = [str(app.tree.item(c)["values"][1]).lower() for c in app.tree.get_children()]
            self.assertEqual(unames_sorted, sorted(unames_sorted))

            # 11. Sort filter: Latency fast
            app.filter_sort_menu.set("[지연시간 빠른순]")
            app._on_filter_changed(None)
            fastest_uname = str(app.tree.item(app.tree.get_children()[0])["values"][1])
            self.assertEqual(fastest_uname, "8888") # 80.0ms is fastest

            # 12. Zero Data Loss assertion
            self.assertEqual(len(app.discovered_items), 8)

        finally:
            app.destroy()


if __name__ == "__main__":
    unittest.main()
