# src/generator/__init__.py
import random
from typing import Optional
from src.generator.base import BaseGenerator, DiscordRuleValidator
from src.generator.random_gen import RandomGenerator
from src.generator.pattern_gen import PatternGenerator
from src.generator.dictionary_gen import DictionaryGenerator
from src.generator.permutation_gen import PermutationGenerator
from src.generator.numeric_gen import NumericGenerator
from src.generator.mask_gen import MaskPatternGenerator
from src.generator.combinatorial_gen import CombinatorialGenerator

class HybridGenerator(BaseGenerator):
    def __init__(
        self,
        length: int = 4,
        custom_regex: str = "",
        prefix: str = "",
        suffix: str = "",
        middle_dot: str = "none",
        mask: str = "",
        exclude_reserved: bool = True
    ):
        self.dict_gen = DictionaryGenerator(length=length, exclude_reserved=exclude_reserved)
        self.pattern_gen = PatternGenerator(length=length, custom_regex=custom_regex, exclude_reserved=exclude_reserved)
        self.numeric_gen = NumericGenerator(length=length, exclude_reserved=exclude_reserved)
        self.random_gen = RandomGenerator(length=length, exclude_reserved=exclude_reserved)
        self.mask_gen = MaskPatternGenerator(
            length=length,
            prefix=prefix,
            suffix=suffix,
            middle_dot=middle_dot,
            mask=mask,
            exclude_reserved=exclude_reserved
        )
        self.has_custom_pattern = bool(prefix or suffix or middle_dot != "none" or mask)

    def next_username(self) -> Optional[str]:
        if self.has_custom_pattern:
            # 50% custom mask, 25% dictionary, 25% pattern
            roll = random.random()
            if roll < 0.50:
                return self.mask_gen.next_username()
            elif roll < 0.75:
                return self.dict_gen.next_username()
            else:
                return self.pattern_gen.next_username()

        # Default distribution: 40% dictionary/phonetic, 30% pattern, 20% numeric, 10% random
        roll = random.random()
        if roll < 0.40:
            return self.dict_gen.next_username()
        elif roll < 0.70:
            return self.pattern_gen.next_username()
        elif roll < 0.90:
            return self.numeric_gen.next_username()
        else:
            return self.random_gen.next_username()

    def get_pattern_type(self) -> str:
        if self.has_custom_pattern:
            return f"hybrid+{self.mask_gen.get_pattern_type()}"
        return "hybrid"

def create_generator(config: dict) -> BaseGenerator:
    mode = config.get("mode", "hybrid").lower()
    length = int(config.get("length", 4))
    custom_regex = config.get("custom_regex", "")
    prefix = config.get("prefix", "")
    suffix = config.get("suffix", "")
    middle_dot = config.get("middle_dot", "none")
    mask = config.get("mask", "")
    exclude_reserved = config.get("exclude_reserved", True)

    direction = config.get("direction", "asc")
    charset_type = config.get("charset_type", "alphanumeric_num_first")

    if mode in ("comb", "combinatorial", "bruteforce", "combo", "순차조합"):
        return CombinatorialGenerator(
            length=length,
            charset_type=charset_type,
            direction=direction,
            prefix=prefix,
            suffix=suffix,
            exclude_reserved=exclude_reserved
        )
    elif mode in ("mask", "custom", "pattern_mask"):
        return MaskPatternGenerator(
            length=length,
            prefix=prefix,
            suffix=suffix,
            middle_dot=middle_dot,
            mask=mask,
            exclude_reserved=exclude_reserved
        )
    elif mode in ("dict", "dictionary"):
        return DictionaryGenerator(length=length, exclude_reserved=exclude_reserved)
    elif mode in ("patt", "pattern"):
        return PatternGenerator(length=length, custom_regex=custom_regex, exclude_reserved=exclude_reserved)
    elif mode in ("num", "numeric", "number"):
        return NumericGenerator(length=length, exclude_reserved=exclude_reserved)
    elif mode in ("perm", "permutation"):
        return PermutationGenerator(
            length=length,
            exclude_reserved=exclude_reserved,
            start_char=config.get("start_char"),
            end_char=config.get("end_char"),
            shard_key=config.get("shard_key")
        )
    elif mode in ("rand", "random"):
        return RandomGenerator(length=length, exclude_reserved=exclude_reserved)
    else:
        return HybridGenerator(
            length=length,
            custom_regex=custom_regex,
            prefix=prefix,
            suffix=suffix,
            middle_dot=middle_dot,
            mask=mask,
            exclude_reserved=exclude_reserved
        )
