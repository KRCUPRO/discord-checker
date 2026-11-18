# tests/test_v10_gui_ux_onboarding_and_tooltips.py
import unittest
from src.ui.i18n import I18nManager
from src.generator.permutation_gen import PermutationGenerator, SHARD_PRESETS, ALLOWED_CHARACTERS

class TestV10GuiUxOnboardingAndTooltips(unittest.TestCase):
    def test_i18n_guide_banner_keys_exist_in_ko_and_en(self):
        """한국어 및 영어 딕셔너리에 상단 안내 배너 키가 완벽히 등록되어 있는지 검증"""
        for lang in ["ko", "en"]:
            I18nManager.set_language(lang)
            title = I18nManager.t("guide_banner_title")
            content = I18nManager.t("guide_banner_content")
            hide = I18nManager.t("guide_banner_hide")
            show = I18nManager.t("guide_banner_show")

            self.assertTrue(len(title) > 5, f"Missing guide_banner_title in {lang}")
            self.assertTrue(len(content) > 30, f"Missing guide_banner_content in {lang}")
            self.assertTrue(len(hide) > 0, f"Missing guide_banner_hide in {lang}")
            self.assertTrue(len(show) > 0, f"Missing guide_banner_show in {lang}")

    def test_i18n_sharding_keys_exist_in_ko_and_en(self):
        """다중 창 분할(샤딩) 툴팁 및 다국어 키가 ko/en에 정상 존재하는지 검증"""
        for lang in ["ko", "en"]:
            I18nManager.set_language(lang)
            shard_title = I18nManager.t("perm_shard_title")
            shard_tip = I18nManager.t("perm_shard_tooltip")
            custom_tip = I18nManager.t("perm_custom_range_tooltip")

            self.assertTrue(len(shard_title) > 3, f"Missing perm_shard_title in {lang}")
            self.assertTrue(len(shard_tip) > 10, f"Missing perm_shard_tooltip in {lang}")
            self.assertTrue(len(custom_tip) > 10, f"Missing perm_custom_range_tooltip in {lang}")

    def test_help_modal_content_contains_sharding_guide(self):
        """내장 도움말 모달(help_modal_content)에 다중 창 분할 가이드가 포함되어 있는지 검증"""
        for lang in ["ko", "en"]:
            I18nManager.set_language(lang)
            help_text = I18nManager.t("help_modal_content")
            if lang == "ko":
                self.assertIn("다중 창 분할", help_text)
                self.assertIn("초보자 3단계", help_text)
            else:
                self.assertIn("Multi-Window Sharding", help_text)
                self.assertIn("3-Step Quick Start", help_text)

    def test_permutation_total_combinations_mathematical_precision(self):
        """순열 생성기의 total_combinations 프로퍼티가 수학적으로 정확히 계산되는지 검증"""
        # 4-character full space: 37 first characters * (38 ** 3)
        gen_all = PermutationGenerator(length=4)
        expected_full = 37 * (len(ALLOWED_CHARACTERS) ** 3)
        self.assertEqual(gen_all.total_combinations, expected_full)

        # 2-way split
        gen_2_1 = PermutationGenerator(length=4, shard_key="2_1")
        gen_2_2 = PermutationGenerator(length=4, shard_key="2_2")
        self.assertEqual(gen_2_1.total_combinations, 13 * (38 ** 3))
        self.assertEqual(gen_2_2.total_combinations, 24 * (38 ** 3))
        self.assertEqual(gen_2_1.total_combinations + gen_2_2.total_combinations, expected_full)

        # 3-way split
        gen_3_1 = PermutationGenerator(length=4, shard_key="3_1")
        gen_3_2 = PermutationGenerator(length=4, shard_key="3_2")
        gen_3_3 = PermutationGenerator(length=4, shard_key="3_3")
        self.assertEqual(
            gen_3_1.total_combinations + gen_3_2.total_combinations + gen_3_3.total_combinations,
            expected_full
        )

        # 4-way split
        splits_4 = [PermutationGenerator(length=4, shard_key=f"4_{i}") for i in range(1, 5)]
        self.assertEqual(sum(g.total_combinations for g in splits_4), expected_full)

if __name__ == "__main__":
    unittest.main()
