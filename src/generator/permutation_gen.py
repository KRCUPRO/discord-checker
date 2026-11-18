# src/generator/permutation_gen.py
import itertools
import string
from typing import Optional, Iterator, List, Tuple
from src.generator.base import BaseGenerator, ALLOWED_CHARACTERS, DiscordRuleValidator

# Discord username rule: Cannot start with a dot '.'
# Valid first characters (37 chars): a-z, 0-9, _
FIRST_CHARACTERS = string.ascii_lowercase + string.digits + "_"

SHARD_PRESETS = {
    "none": {"label": "전체 탐색 (분할 없음)", "start": None, "end": None},
    "2_1": {"label": "2분할 - [1번 창: a ~ m]", "start": "a", "end": "m"},
    "2_2": {"label": "2분할 - [2번 창: n ~ _]", "start": "n", "end": "_"},
    "3_1": {"label": "3분할 - [1번 창: a ~ i]", "start": "a", "end": "i"},
    "3_2": {"label": "3분할 - [2번 창: j ~ r]", "start": "j", "end": "r"},
    "3_3": {"label": "3분할 - [3번 창: s ~ _]", "start": "s", "end": "_"},
    "4_1": {"label": "4분할 - [1번 창: a ~ g]", "start": "a", "end": "g"},
    "4_2": {"label": "4분할 - [2번 창: h ~ n]", "start": "h", "end": "n"},
    "4_3": {"label": "4분할 - [3번 창: o ~ u]", "start": "o", "end": "u"},
    "4_4": {"label": "4분할 - [4번 창: v ~ _]", "start": "v", "end": "_"},
}

def get_sharded_first_characters(start_char: Optional[str] = None, end_char: Optional[str] = None) -> List[str]:
    all_first = list(FIRST_CHARACTERS)
    if not start_char and not end_char:
        return all_first
    s_idx = all_first.index(start_char) if start_char in all_first else 0
    e_idx = all_first.index(end_char) if end_char in all_first else len(all_first) - 1
    if s_idx > e_idx:
        s_idx, e_idx = e_idx, s_idx
    return all_first[s_idx:e_idx + 1]

class PermutationGenerator(BaseGenerator):
    """
    고성능 순열 전수조사 생성기 (다중 창 분할 샤딩 지원)
    - start_char, end_char를 통한 독립 범위 분할 생성 (충돌 0%)
    - 2분할, 3분할, 4분할 프리셋 및 커스텀 범위 완벽 지원
    """
    def __init__(
        self,
        length: int = 4,
        start_index: int = 0,
        exclude_reserved: bool = True,
        start_char: Optional[str] = None,
        end_char: Optional[str] = None,
        shard_key: Optional[str] = None
    ):
        self.length = length
        self.start_index = start_index
        self.exclude_reserved = exclude_reserved
        self.current_index = start_index
        
        # Handle preset lookup if shard_key provided
        if shard_key and shard_key in SHARD_PRESETS:
            preset = SHARD_PRESETS[shard_key]
            start_char = preset["start"]
            end_char = preset["end"]

        self.start_char = start_char
        self.end_char = end_char
        self.first_chars = get_sharded_first_characters(start_char, end_char)
        self._iterator: Optional[Iterator] = None
        self._init_iterator()

    def _init_iterator(self):
        if self.length <= 1:
            # Single character
            prod = ((ch,) for ch in self.first_chars)
        else:
            # First character restricted to sharded first_chars, rest from ALLOWED_CHARACTERS
            prod = (
                (fc,) + rest
                for fc in self.first_chars
                for rest in itertools.product(ALLOWED_CHARACTERS, repeat=self.length - 1)
            )

        # Advance iterator to start_index
        self._iterator = itertools.islice(prod, self.start_index, None)

    def next_username(self) -> Optional[str]:
        if not self._iterator:
            return None

        while True:
            try:
                char_tuple = next(self._iterator)
                self.current_index += 1
                candidate = "".join(char_tuple)

                if DiscordRuleValidator.is_valid(
                    candidate,
                    min_len=self.length,
                    max_len=self.length,
                    check_reserved=self.exclude_reserved
                ):
                    return candidate
            except StopIteration:
                self._iterator = None
                return None

    @property
    def total_combinations(self) -> int:
        """분할 샤딩된 첫 글자 기준 전체 순열 조합 수 (전수검사 분모)"""
        if not self.first_chars:
            return 0
        if self.length <= 1:
            return len(self.first_chars)
        return len(self.first_chars) * (len(ALLOWED_CHARACTERS) ** (self.length - 1))

    def get_pattern_type(self) -> str:
        if self.start_char or self.end_char:
            sc = self.start_char or "a"
            ec = self.end_char or "_"
            return f"permutation_{self.length}char[{sc}-{ec}]"
        return f"permutation_{self.length}char"

    def get_checkpoint(self) -> int:
        return self.current_index
