"""
D4UC V5 Unit Tests - Discovered Available Usernames Real-Time Search & Multi-Filter Engine
Tests substring/wildcard searching, multi-criteria filtering, sorting, and 0% data loss master store.
"""

import fnmatch
import unittest
from typing import List, Dict, Any


def filter_and_sort_discovered(
    items: List[Dict[str, Any]],
    query: str = "",
    len_choice: str = "전체",
    type_choice: str = "전체",
    sort_choice: str = "최신순"
) -> List[Dict[str, Any]]:
    """Standalone pure-function logic replicating DiscordCheckerGui._refresh_discovered_table"""
    q = query.strip().lower()
    filtered = []

    for item in items:
        uname = str(item.get("username", "")).lower()
        patt = str(item.get("pattern", "")).lower()

        # (1) Text query match (supports wildcard * and ? or substring)
        if q:
            if "*" in q or "?" in q:
                if not fnmatch.fnmatch(uname, q) and not fnmatch.fnmatch(patt, q):
                    continue
            else:
                if q not in uname and q not in patt:
                    continue

        # (2) Length match
        l = item.get("length", len(uname))
        if "3" in len_choice and l != 3:
            continue
        elif "4" in len_choice and l != 4:
            continue
        elif "5" in len_choice and l != 5:
            continue
        elif ("6" in len_choice or "6+" in len_choice) and l < 6:
            continue

        # (3) Pattern / Type match
        if "사전" in type_choice or "Dict" in type_choice:
            if not any(k in patt for k in ("dict", "word", "cvcv")):
                continue
        elif "대칭" in type_choice or "패턴" in type_choice or "Patt" in type_choice:
            if not any(k in patt for k in ("patt", "abba", "aabb", "abab", "symm")):
                continue
        elif "숫자" in type_choice or "Numeric" in type_choice:
            if not ("num" in patt or uname.isdigit()):
                continue
        elif "점" in type_choice or "Dot" in type_choice:
            if "." not in uname:
                continue
        elif "조합" in type_choice or "Comb" in type_choice:
            if "comb" not in patt:
                continue
        elif "커스텀" in type_choice or "Custom" in type_choice:
            if "mask" not in patt and "custom" not in patt:
                continue

        filtered.append(item)

    # (4) Sorting
    if "A-Z" in sort_choice:
        filtered.sort(key=lambda x: str(x.get("username", "")).lower())
    elif "Z-A" in sort_choice:
        filtered.sort(key=lambda x: str(x.get("username", "")).lower(), reverse=True)
    elif "빠른순" in sort_choice or "Fast" in sort_choice:
        filtered.sort(key=lambda x: x.get("latency_val", 9999.0))

    return filtered


class TestDiscoveredSearchAndFilter(unittest.TestCase):
    def setUp(self):
        self.sample_items = [
            {"time": "10:00:01", "username": "ace", "pattern": "cvcv_dict", "latency": "120.0ms", "latency_val": 120.0, "length": 3},
            {"time": "10:00:02", "username": "vip1", "pattern": "custom_mask", "latency": "350.5ms", "latency_val": 350.5, "length": 4},
            {"time": "10:00:03", "username": "7777", "pattern": "num_repeating", "latency": "85.2ms", "latency_val": 85.2, "length": 4},
            {"time": "10:00:04", "username": "abba", "pattern": "abba_symm", "latency": "210.0ms", "latency_val": 210.0, "length": 4},
            {"time": "10:00:05", "username": "k.one", "pattern": "dot_isolated", "latency": "450.0ms", "latency_val": 450.0, "length": 5},
            {"time": "10:00:06", "username": "0a1b", "pattern": "comb_asc", "latency": "99.0ms", "latency_val": 99.0, "length": 4},
            {"time": "10:00:07", "username": "crypto_kr", "pattern": "word_compound", "latency": "600.0ms", "latency_val": 600.0, "length": 9},
            {"time": "10:00:08", "username": "vip99", "pattern": "prefix_vip", "latency": "180.0ms", "latency_val": 180.0, "length": 5},
        ]

    def test_substring_search(self):
        # Substring "vip" matches vip1 and vip99
        res = filter_and_sort_discovered(self.sample_items, query="vip")
        unames = [r["username"] for r in res]
        self.assertEqual(len(res), 2)
        self.assertIn("vip1", unames)
        self.assertIn("vip99", unames)

        # Case-insensitive "VIP"
        res_ci = filter_and_sort_discovered(self.sample_items, query="VIP")
        self.assertEqual(len(res_ci), 2)

    def test_wildcard_search(self):
        # Wildcard "vip*" -> starts with vip
        res1 = filter_and_sort_discovered(self.sample_items, query="vip*")
        self.assertEqual(len(res1), 2)

        # Wildcard "*_kr" -> ends with _kr
        res2 = filter_and_sort_discovered(self.sample_items, query="*_kr")
        self.assertEqual(len(res2), 1)
        self.assertEqual(res2[0]["username"], "crypto_kr")

        # Wildcard "?vip*" -> 1 char before vip (none here)
        res3 = filter_and_sort_discovered(self.sample_items, query="?vip*")
        self.assertEqual(len(res3), 0)

        # Wildcard "???" -> exactly 3 characters
        res4 = filter_and_sort_discovered(self.sample_items, query="???")
        self.assertEqual(len(res4), 1)
        self.assertEqual(res4[0]["username"], "ace")

    def test_length_filter(self):
        # 3 chars
        res3 = filter_and_sort_discovered(self.sample_items, len_choice="[3글자]")
        self.assertEqual([r["username"] for r in res3], ["ace"])

        # 4 chars: vip1, 7777, abba, 0a1b
        res4 = filter_and_sort_discovered(self.sample_items, len_choice="[4글자]")
        self.assertEqual(len(res4), 4)
        self.assertIn("7777", [r["username"] for r in res4])

        # 5 chars: k.one, vip99
        res5 = filter_and_sort_discovered(self.sample_items, len_choice="[5글자]")
        self.assertEqual(len(res5), 2)
        self.assertIn("k.one", [r["username"] for r in res5])

        # 6+ chars: crypto_kr (9)
        res6p = filter_and_sort_discovered(self.sample_items, len_choice="[6글자+]")
        self.assertEqual(len(res6p), 1)
        self.assertEqual(res6p[0]["username"], "crypto_kr")

    def test_pattern_and_type_filter(self):
        # Dictionary
        res_dict = filter_and_sort_discovered(self.sample_items, type_choice="[사전단어/음절]")
        unames = [r["username"] for r in res_dict]
        self.assertIn("ace", unames)
        self.assertIn("crypto_kr", unames)

        # Pattern / Symmetry
        res_patt = filter_and_sort_discovered(self.sample_items, type_choice="[대칭/패턴]")
        self.assertEqual([r["username"] for r in res_patt], ["abba"])

        # Numeric
        res_num = filter_and_sort_discovered(self.sample_items, type_choice="[순수 숫자닉]")
        self.assertEqual([r["username"] for r in res_num], ["7777"])

        # Dot
        res_dot = filter_and_sort_discovered(self.sample_items, type_choice="[점(.) 포함]")
        self.assertEqual([r["username"] for r in res_dot], ["k.one"])

        # Combinatorial
        res_comb = filter_and_sort_discovered(self.sample_items, type_choice="[조합(0~z)]")
        self.assertEqual([r["username"] for r in res_comb], ["0a1b"])

        # Custom Mask
        res_mask = filter_and_sort_discovered(self.sample_items, type_choice="[커스텀 마스크]")
        self.assertEqual([r["username"] for r in res_mask], ["vip1"])

    def test_sorting(self):
        # A-Z
        res_asc = filter_and_sort_discovered(self.sample_items, sort_choice="[닉네임 (A-Z)]")
        unames_asc = [r["username"] for r in res_asc]
        self.assertEqual(unames_asc, sorted(unames_asc))

        # Z-A
        res_desc = filter_and_sort_discovered(self.sample_items, sort_choice="[닉네임 (Z-A)]")
        unames_desc = [r["username"] for r in res_desc]
        self.assertEqual(unames_desc, sorted(unames_desc, reverse=True))

        # Latency fast
        res_lat = filter_and_sort_discovered(self.sample_items, sort_choice="[지연시간 빠른순]")
        latencies = [r["latency_val"] for r in res_lat]
        self.assertEqual(latencies, sorted(latencies))
        self.assertEqual(res_lat[0]["username"], "7777") # 85.2ms

    def test_zero_data_loss_master_store(self):
        # Filtering should not mutate the original master list
        initial_len = len(self.sample_items)
        _ = filter_and_sort_discovered(self.sample_items, query="none_existing_xyz")
        _ = filter_and_sort_discovered(self.sample_items, len_choice="[3글자]")
        _ = filter_and_sort_discovered(self.sample_items, sort_choice="[닉네임 (A-Z)]")
        self.assertEqual(len(self.sample_items), initial_len)

        # Full reset yields 100% of items
        res_all = filter_and_sort_discovered(self.sample_items, query="", len_choice="전체", type_choice="전체")
        self.assertEqual(len(res_all), initial_len)


if __name__ == "__main__":
    unittest.main()
