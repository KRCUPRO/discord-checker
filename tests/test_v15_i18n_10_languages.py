# tests/test_v15_i18n_10_languages.py
# Unit test for D4UC 10-Language 1:1 Matching System
import unittest
import re
import sys
import os

# Ensure package path
sys.path.insert(0, os.path.abspath('Discord-4Character-Usernames-Checker'))
from src.ui.i18n import I18nManager, STRINGS, SUPPORTED_LANGUAGES, LANG_NAMES, LANG_FLAGS


class TestI18n10Languages(unittest.TestCase):
    def test_supported_languages_list(self):
        expected_langs = ['ko', 'en', 'ja', 'zh', 'es', 'ru', 'fr', 'de', 'pt', 'vi']
        self.assertEqual(SUPPORTED_LANGUAGES, expected_langs)
        self.assertEqual(len(I18nManager.get_supported_languages()), 10)

    def test_all_10_languages_have_exact_196_keys(self):
        ko_keys = set(STRINGS['ko'].keys())
        self.assertEqual(len(ko_keys), 196, f"KO keys should be 196, got {len(ko_keys)}")

        for lang in SUPPORTED_LANGUAGES:
            self.assertIn(lang, STRINGS, f"Language {lang} missing from STRINGS")
            lang_keys = set(STRINGS[lang].keys())
            self.assertEqual(len(lang_keys), 196, f"Language {lang} has {len(lang_keys)} keys instead of 196")
            
            missing = ko_keys - lang_keys
            extra = lang_keys - ko_keys
            self.assertEqual(missing, set(), f"Language {lang} missing keys: {missing}")
            self.assertEqual(extra, set(), f"Language {lang} extra keys: {extra}")

    def test_placeholders_exact_match(self):
        placeholder_regex = re.compile(r'\{([a-zA-Z0-9_]+)\}')
        ko_dict = STRINGS['ko']
        
        for lang in SUPPORTED_LANGUAGES:
            lang_dict = STRINGS[lang]
            for key, val in ko_dict.items():
                ko_placeholders = set(placeholder_regex.findall(val))
                if ko_placeholders:
                    target_val = lang_dict.get(key, '')
                    target_placeholders = set(placeholder_regex.findall(target_val))
                    self.assertEqual(
                        ko_placeholders, 
                        target_placeholders,
                        f"Placeholder mismatch for key '{key}' in lang '{lang}': expected {ko_placeholders}, got {target_placeholders}"
                    )

    def test_i18n_manager_switching_and_formatting(self):
        # Test switching across all 10 languages
        for lang in SUPPORTED_LANGUAGES:
            I18nManager.set_language(lang)
            self.assertEqual(I18nManager.get_language(), lang)
            title = I18nManager.t('app_title')
            self.assertTrue(len(title) > 0)
            
            flag = I18nManager.get_language_flag(lang)
            self.assertTrue(len(flag) > 0)
            
            name = I18nManager.get_language_name(lang)
            self.assertTrue(len(name) > 0)

        # Test formatting
        I18nManager.set_language('ko')
        status = I18nManager.t('status_bar_running', workers=5, elapsed='01:23')
        self.assertIn('5', status)
        self.assertIn('01:23', status)

        I18nManager.set_language('en')
        status_en = I18nManager.t('status_bar_running', workers=10, elapsed='02:45')
        self.assertIn('10', status_en)
        self.assertIn('02:45', status_en)

        # Reset to default
        I18nManager.set_language('ko')


if __name__ == '__main__':
    unittest.main()
