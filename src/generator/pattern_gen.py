# src/generator/pattern_gen.py
import random
import string
import re
from typing import Optional, List
from src.generator.base import BaseGenerator, DiscordRuleValidator

ALPHANUMERIC = string.ascii_lowercase + string.digits
LETTERS = string.ascii_lowercase
DIGITS = string.digits

class PatternGenerator(BaseGenerator):
    """
    Symmetrical, Repeating, and High-aesthetic Pattern Generator for lengths 3, 4, 5, 6.
    Patterns:
    - 3-char: AAA, ABA, AAB, ABB, 123, 111, 777
    - 4-char: AAAA, ABAB, AABB, ABBA, 1111, 1234, 0001, A1A1
    - 5-char: AAAAA, ABABA, AABBA, AAABB, AABBB, ABCBA, 11111, 12345, 00001, 01010
    - 6-char: AAAAAA, ABABAB, AABBCC, ABCABC, 111111, 123456, 000001
    """
    def __init__(self, length: int = 4, custom_regex: str = "", exclude_reserved: bool = True):
        self.length = length
        self.custom_regex = custom_regex
        self.compiled_regex = re.compile(custom_regex) if custom_regex else None
        self.exclude_reserved = exclude_reserved

    def _generate_pattern_3(self) -> str:
        c1 = random.choice(ALPHANUMERIC)
        c2 = random.choice(ALPHANUMERIC)
        d1 = random.choice(DIGITS)
        ptype = random.choice(["aaa", "aba", "aab", "abb", "repeat_digit", "sequence"])
        if ptype == "aaa":
            return c1 * 3
        elif ptype == "aba":
            return f"{c1}{c2}{c1}"
        elif ptype == "aab":
            return f"{c1}{c1}{c2}"
        elif ptype == "abb":
            return f"{c1}{c2}{c2}"
        elif ptype == "repeat_digit":
            return d1 * 3
        elif ptype == "sequence":
            s = random.randint(0, 7)
            return f"{s}{s+1}{s+2}"
        return f"{c1}{c2}{c1}"

    def _generate_pattern_4(self) -> str:
        c1 = random.choice(ALPHANUMERIC)
        c2 = random.choice(ALPHANUMERIC)
        d1 = random.choice(DIGITS)
        ptype = random.choice(["aaaa", "abab", "aabb", "abba", "repeat_digit", "wrap_underscore", "palindrome", "a1a1"])
        if ptype == "aaaa":
            return c1 * 4
        elif ptype == "abab":
            return f"{c1}{c2}{c1}{c2}"
        elif ptype == "aabb":
            return f"{c1}{c1}{c2}{c2}"
        elif ptype == "abba":
            return f"{c1}{c2}{c2}{c1}"
        elif ptype == "repeat_digit":
            return d1 * 4
        elif ptype == "wrap_underscore":
            return f"_{c1}{c2}_"
        elif ptype == "palindrome":
            return f"{c1}{c2}{c2}{c1}"
        elif ptype == "a1a1":
            l = random.choice(LETTERS)
            d = random.choice(DIGITS)
            return f"{l}{d}{l}{d}"
        return f"{c1}{c2}{c1}{c2}"

    def _generate_pattern_5(self) -> str:
        c1 = random.choice(ALPHANUMERIC)
        c2 = random.choice(ALPHANUMERIC)
        c3 = random.choice(ALPHANUMERIC)
        d1 = random.choice(DIGITS)
        ptype = random.choice(["aaaaa", "ababa", "aabba", "aaabb", "aabbb", "abcba", "11111", "00001", "01010", "sequence"])

        if ptype == "aaaaa":
            return c1 * 5
        elif ptype == "ababa":
            return f"{c1}{c2}{c1}{c2}{c1}"
        elif ptype == "aabba":
            return f"{c1}{c1}{c2}{c2}{c1}"
        elif ptype == "aaabb":
            return f"{c1}{c1}{c1}{c2}{c2}"
        elif ptype == "aabbb":
            return f"{c1}{c1}{c2}{c2}{c2}"
        elif ptype == "abcba":
            return f"{c1}{c2}{c3}{c2}{c1}"
        elif ptype == "11111":
            return d1 * 5
        elif ptype == "00001":
            return f"{d1 * 4}{c1}"
        elif ptype == "01010":
            d2 = random.choice(DIGITS)
            return f"{d1}{d2}{d1}{d2}{d1}"
        elif ptype == "sequence":
            s = random.randint(0, 5)
            return "".join(str((s + i) % 10) for i in range(5))
        return f"{c1}{c2}{c1}{c2}{c1}"

    def _generate_pattern_6(self) -> str:
        c1 = random.choice(ALPHANUMERIC)
        c2 = random.choice(ALPHANUMERIC)
        c3 = random.choice(ALPHANUMERIC)
        d1 = random.choice(DIGITS)
        ptype = random.choice(["aaaaaa", "ababab", "aabbcc", "abcabc", "abccba", "111111", "000001", "sequence"])

        if ptype == "aaaaaa":
            return c1 * 6
        elif ptype == "ababab":
            return f"{c1}{c2}{c1}{c2}{c1}{c2}"
        elif ptype == "aabbcc":
            return f"{c1}{c1}{c2}{c2}{c3}{c3}"
        elif ptype == "abcabc":
            return f"{c1}{c2}{c3}{c1}{c2}{c3}"
        elif ptype == "abccba":
            return f"{c1}{c2}{c3}{c3}{c2}{c1}"
        elif ptype == "111111":
            return d1 * 6
        elif ptype == "000001":
            return f"{d1 * 5}{c1}"
        elif ptype == "sequence":
            s = random.randint(0, 4)
            return "".join(str((s + i) % 10) for i in range(6))
        return f"{c1}{c2}{c1}{c2}{c1}{c2}"

    def next_username(self) -> Optional[str]:
        for _ in range(50):
            if self.compiled_regex:
                candidate = ''.join(random.choice(ALPHANUMERIC) for _ in range(self.length))
                if self.compiled_regex.match(candidate):
                    if DiscordRuleValidator.is_valid(candidate, min_len=self.length, max_len=self.length, check_reserved=self.exclude_reserved):
                        return candidate
            else:
                if self.length == 3:
                    candidate = self._generate_pattern_3()
                elif self.length == 4:
                    candidate = self._generate_pattern_4()
                elif self.length == 5:
                    candidate = self._generate_pattern_5()
                elif self.length == 6:
                    candidate = self._generate_pattern_6()
                else:
                    c1 = random.choice(ALPHANUMERIC)
                    c2 = random.choice(ALPHANUMERIC)
                    candidate = (c1 + c2) * (self.length // 2)
                    if len(candidate) < self.length:
                        candidate += c1

                if DiscordRuleValidator.is_valid(candidate, min_len=self.length, max_len=self.length, check_reserved=self.exclude_reserved):
                    return candidate

        c = random.choice(ALPHANUMERIC)
        return c * self.length

    def get_pattern_type(self) -> str:
        return f"pattern_{self.length}char"
