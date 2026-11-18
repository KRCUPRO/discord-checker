# src/generator/combinatorial_gen.py
import threading
from typing import Optional, Tuple
from src.generator.base import BaseGenerator, DiscordRuleValidator

CHARSETS = {
    "alphanumeric_num_first": "0123456789abcdefghijklmnopqrstuvwxyz",
    "alphanumeric_alpha_first": "abcdefghijklmnopqrstuvwxyz0123456789",
    "alpha_only": "abcdefghijklmnopqrstuvwxyz",
    "numeric_only": "0123456789"
}

class CombinatorialGenerator(BaseGenerator):
    """
    고속 순차 영숫자 조합 생성기 (O(1) 수학적 Base-36 진법 변환 인덱싱)
    - 0~9, a~z 영숫자 조합 탐색 (비밀번호 크래킹형 전수조사)
    - 오름차순 (Ascending) 및 내림차순 (Descending) 탐색 방향 지원
    - 메모리 누수 0% ($O(1)$ 공간 복잡도), 수천만 개 조합 실시간 진행률(%) 산출
    - 멀티스레드 안전한 인덱스 발급 (경쟁 상태 0%)
    """
    def __init__(
        self,
        length: int = 4,
        charset_type: str = "alphanumeric_num_first",
        direction: str = "asc",
        prefix: str = "",
        suffix: str = "",
        start_index: int = 0,
        exclude_reserved: bool = True
    ):
        self.length = max(2, min(int(length), 32))
        self.charset_type = charset_type.lower()
        if self.charset_type in ("num_first", "num_alpha", "0-z", "0~z", "alphanumeric"):
            self.charset_type = "alphanumeric_num_first"
        elif self.charset_type in ("alpha_first", "a-z_0-9", "a~z_0~9"):
            self.charset_type = "alphanumeric_alpha_first"
        elif self.charset_type in ("alpha", "letters"):
            self.charset_type = "alpha_only"
        elif self.charset_type in ("num", "numeric", "digits"):
            self.charset_type = "numeric_only"

        self.charset = CHARSETS.get(self.charset_type, CHARSETS["alphanumeric_num_first"])
        self.base = len(self.charset)
        self.direction = "desc" if direction.lower() in ("desc", "descending", "내림차순") else "asc"

        self.prefix = prefix.strip().lower()
        self.suffix = suffix.strip().lower()
        self.exclude_reserved = exclude_reserved

        # Calculate variable length
        self.var_len = max(0, self.length - len(self.prefix) - len(self.suffix))
        self.total_combinations = (self.base ** self.var_len) if self.var_len > 0 else 1

        self._current_index = max(0, min(int(start_index), self.total_combinations))
        self._lock = threading.RLock()

    def _index_to_string(self, index: int, length: int) -> str:
        if length <= 0:
            return ""
        chars = []
        val = index
        for _ in range(length):
            chars.append(self.charset[val % self.base])
            val //= self.base
        return "".join(reversed(chars))

    def next_username(self) -> Optional[str]:
        while True:
            with self._lock:
                if self._current_index >= self.total_combinations:
                    return None
                idx = self._current_index
                self._current_index += 1

            if self.direction == "desc":
                eff_idx = (self.total_combinations - 1) - idx
            else:
                eff_idx = idx

            core = self._index_to_string(eff_idx, self.var_len)
            candidate = f"{self.prefix}{core}{self.suffix}"

            if not DiscordRuleValidator.is_valid(candidate, min_len=2, max_len=32, check_reserved=self.exclude_reserved):
                continue

            return candidate

    @property
    def current_index(self) -> int:
        with self._lock:
            return self._current_index

    @property
    def progress_info(self) -> Tuple[int, int, float]:
        with self._lock:
            cur = self._current_index
            total = self.total_combinations
            pct = (cur / max(1, total)) * 100.0
            return cur, total, pct

    def get_pattern_type(self) -> str:
        dir_label = "asc" if self.direction == "asc" else "desc"
        cs_label = "0z" if "num_first" in self.charset_type else "za"
        return f"comb_{dir_label}_{cs_label}_{self.length}c"
