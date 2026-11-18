# src/generator/random_gen.py
import random
from typing import Optional
from src.generator.base import BaseGenerator, ALLOWED_CHARACTERS, DiscordRuleValidator

class RandomGenerator(BaseGenerator):
    def __init__(self, length: int = 4, exclude_reserved: bool = True):
        self.length = length
        self.exclude_reserved = exclude_reserved

    def next_username(self) -> Optional[str]:
        while True:
            candidate = ''.join(random.choice(ALLOWED_CHARACTERS) for _ in range(self.length))
            if DiscordRuleValidator.is_valid(
                candidate,
                min_len=self.length,
                max_len=self.length,
                check_reserved=self.exclude_reserved
            ):
                return candidate

    def get_pattern_type(self) -> str:
        return f"random_{self.length}char"
