# src/generator/numeric_gen.py
import random
from typing import Optional
from src.generator.base import BaseGenerator, DiscordRuleValidator

class NumericGenerator(BaseGenerator):
    """
    Dedicated Pure Numeric & Number-Pattern Generator (0~9)
    Generates high-value Discord numeric handles:
    - Sequential numbers (00000, 00001, 12345, ...)
    - Repeating digits (11111, 77777, 00000, ...)
    - Symmetrical / Palindromic digits (12321, 01010, 70007, ...)
    - Leading-zero formatted numeric identifiers
    """
    def __init__(self, length: int = 5, sequential: bool = False, start_val: int = 0, exclude_reserved: bool = True):
        self.length = length
        self.sequential = sequential
        self.current_val = start_val
        self.max_val = (10 ** length) - 1
        self.exclude_reserved = exclude_reserved
        self._special_patterns = [
            "repeating", "sequential_asc", "sequential_desc", "sandwich", "alternating", "trailing_zeroes", "leading_zeroes"
        ]

    def _generate_pattern_numeric(self) -> str:
        ptype = random.choice(self._special_patterns)
        d1 = str(random.randint(0, 9))
        d2 = str(random.randint(0, 9))

        if ptype == "repeating":
            return d1 * self.length

        elif ptype == "sequential_asc":
            start = random.randint(0, max(0, 10 - self.length))
            return "".join(str((start + i) % 10) for i in range(self.length))

        elif ptype == "sequential_desc":
            start = random.randint(min(9, self.length - 1), 9)
            return "".join(str((start - i) % 10) for i in range(self.length))

        elif ptype == "sandwich":
            if self.length >= 3:
                inner = d2 * (self.length - 2)
                return f"{d1}{inner}{d1}"
            return f"{d1}{d2}{d1}"

        elif ptype == "alternating":
            return (d1 + d2) * (self.length // 2) + (d1 if self.length % 2 != 0 else "")

        elif ptype == "trailing_zeroes":
            prefix = str(random.randint(1, 99))[:self.length - 1]
            return prefix.ljust(self.length, '0')

        elif ptype == "leading_zeroes":
            suffix = str(random.randint(1, 99))
            return suffix.zfill(self.length)

        # Fallback: random integer with leading zeroes
        val = random.randint(0, self.max_val)
        return f"{val:0{self.length}d}"

    def next_username(self) -> Optional[str]:
        if self.sequential:
            while self.current_val <= self.max_val:
                candidate = f"{self.current_val:0{self.length}d}"
                self.current_val += 1
                if DiscordRuleValidator.is_valid(candidate, min_len=self.length, max_len=self.length, check_reserved=self.exclude_reserved):
                    return candidate
            return None

        # Random / Pattern-weighted numeric generation
        for _ in range(50):
            if random.random() < 0.65:
                candidate = self._generate_pattern_numeric()
            else:
                val = random.randint(0, self.max_val)
                candidate = f"{val:0{self.length}d}"

            if DiscordRuleValidator.is_valid(candidate, min_len=self.length, max_len=self.length, check_reserved=self.exclude_reserved):
                return candidate

        return f"{random.randint(0, self.max_val):0{self.length}d}"

    def get_pattern_type(self) -> str:
        return f"numeric_{self.length}digit"
