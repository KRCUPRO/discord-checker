# tests/test_exclusion_rules.py
"""
Unit tests for username exclusion rules and validation:
- Enforce strict exclusion of consecutive dots ('..', e.g. 'ab..', 'a..1')
- Enforce exclusion of leading/trailing dots ('.abc', 'abc.')
- Enforce exclusion of disallowed characters (hyphens, special symbols, unicode)
- Enforce exclusion of reserved Discord usernames
- Verify all generators strictly yield only valid Discord usernames
"""
import unittest
from src.generator.base import DiscordRuleValidator, DISCORD_RESERVED_USERNAMES
from src.generator.random_gen import RandomGenerator
from src.generator.pattern_gen import PatternGenerator
from src.generator.mask_gen import MaskPatternGenerator
from src.generator.combinatorial_gen import CombinatorialGenerator
from src.generator.numeric_gen import NumericGenerator
from src.generator.permutation_gen import PermutationGenerator
from src.generator import HybridGenerator, create_generator

class TestExclusionRules(unittest.TestCase):
    def test_consecutive_dots_strictly_rejected(self):
        """'..'이 포함된 사용자명(ab.., a..1 등)은 절대 허용되지 않아야 함"""
        invalid_samples = [
            "ab..", "a..1", "..12", "1..a", "a..b", "x..y",
            "..", "...", "....", "a..", "..a", "test..name",
            "k..r", "9..9", "_.._", "._._.", "a...b"
        ]
        for name in invalid_samples:
            with self.subTest(name=name):
                self.assertFalse(
                    DiscordRuleValidator.is_valid(name, min_len=2, max_len=32),
                    f"'{name}' contains consecutive dots and must be rejected"
                )

    def test_leading_and_trailing_dots_strictly_rejected(self):
        """점(.)으로 시작하거나 점(.)으로 끝나는 사용자명은 절대 허용되지 않아야 함"""
        invalid_samples = [
            ".abc", ".123", "._ab", ".xyz.", "abc.", "123.", "ab_.",
            ".a.b", "a.b.", ".kr.", ".test."
        ]
        for name in invalid_samples:
            with self.subTest(name=name):
                self.assertFalse(
                    DiscordRuleValidator.is_valid(name, min_len=2, max_len=32),
                    f"'{name}' starts/ends with dot and must be rejected"
                )

    def test_disallowed_characters_rejected(self):
        """영문 소문자, 숫자, 언더바(_), 단일 점(.) 이외의 모든 특수문자/공백/비ASCII 거부"""
        invalid_samples = [
            "ab-c", "ab!c", "ab@c", "ab#c", "ab$c", "ab%c",
            "ab^c", "ab&c", "ab*c", "ab+c", "ab=c", "ab c",
            "ab/c", "ab\\c", "ab?c", "ab<c", "ab>c", "ab,c",
            "한글테스트", "조선", "kr🔥", "abc~"
        ]
        for name in invalid_samples:
            with self.subTest(name=name):
                self.assertFalse(
                    DiscordRuleValidator.is_valid(name, min_len=2, max_len=32),
                    f"'{name}' contains disallowed characters and must be rejected"
                )

    def test_reserved_usernames_rejected(self):
        """Discord 공식 예약어는 생성 및 검사 대상에서 제외"""
        for reserved in DISCORD_RESERVED_USERNAMES:
            with self.subTest(reserved=reserved):
                self.assertFalse(
                    DiscordRuleValidator.is_valid(reserved, min_len=2, max_len=32, check_reserved=True),
                    f"Reserved name '{reserved}' must be rejected"
                )

    def test_valid_usernames_accepted(self):
        """규칙에 부합하는 정상 사용자명은 유효 판정"""
        valid_samples = [
            "abcd", "ab12", "a.b1", "ab_c", "_abc", "abc_",
            "1234", "a1b2", "kr99", "v.ip", "x_y_z", "a.b.c"
        ]
        for name in valid_samples:
            with self.subTest(name=name):
                self.assertTrue(
                    DiscordRuleValidator.is_valid(name, min_len=2, max_len=32),
                    f"'{name}' is valid but was rejected"
                )

    def test_mask_generator_exclusion_invariance(self):
        """MaskPatternGenerator가 생성한 모든 후보는 연속 점 및 시작/끝 점이 없어야 함"""
        gen = MaskPatternGenerator(length=4, prefix="a", middle_dot="optional")
        for _ in range(100):
            cand = gen.next_username()
            if cand:
                self.assertNotIn("..", cand)
                self.assertFalse(cand.startswith("."))
                self.assertFalse(cand.endswith("."))
                self.assertTrue(DiscordRuleValidator.is_valid(cand, min_len=4, max_len=4))

    def test_combinatorial_generator_exclusion_invariance(self):
        """CombinatorialGenerator가 생성한 모든 후보는 유효 규칙 준수"""
        gen = CombinatorialGenerator(length=4, prefix="", suffix="", direction="asc")
        for _ in range(100):
            cand = gen.next_username()
            if cand:
                self.assertNotIn("..", cand)
                self.assertFalse(cand.startswith("."))
                self.assertFalse(cand.endswith("."))
                self.assertTrue(DiscordRuleValidator.is_valid(cand, min_len=4, max_len=4))

    def test_permutation_generator_exclusion_invariance(self):
        """PermutationGenerator가 생성한 모든 후보는 유효 규칙 준수"""
        gen = PermutationGenerator(length=4, shard_key="2_1")
        for _ in range(100):
            cand = gen.next_username()
            if cand:
                self.assertNotIn("..", cand)
                self.assertFalse(cand.startswith("."))
                self.assertFalse(cand.endswith("."))
                self.assertTrue(DiscordRuleValidator.is_valid(cand, min_len=4, max_len=4))

    def test_pattern_generator_exclusion_invariance(self):
        """PatternGenerator가 생성한 모든 후보는 유효 규칙 준수"""
        for length in [3, 4, 5, 6]:
            gen = PatternGenerator(length=length)
            for _ in range(50):
                cand = gen.next_username()
                if cand:
                    self.assertNotIn("..", cand)
                    self.assertFalse(cand.startswith("."))
                    self.assertFalse(cand.endswith("."))
                    self.assertTrue(DiscordRuleValidator.is_valid(cand, min_len=length, max_len=length))

    def test_factory_custom_mask_mapping(self):
        """create_generator with mode='custom_mask' properly instantiates MaskPatternGenerator"""
        gen = create_generator({"mode": "custom_mask", "length": 4, "prefix": "kr"})
        self.assertIsInstance(gen, MaskPatternGenerator)
        cand = gen.next_username()
        self.assertIsNotNone(cand)
        self.assertTrue(cand.startswith("kr"))

if __name__ == "__main__":
    unittest.main()
