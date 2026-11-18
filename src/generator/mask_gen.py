# src/generator/mask_gen.py
import random
import re
import string
from typing import Optional, List
from src.generator.base import BaseGenerator, DiscordRuleValidator

ALPHANUMERIC = string.ascii_lowercase + string.digits
LETTERS = string.ascii_lowercase
DIGITS = string.digits

class MaskPatternGenerator(BaseGenerator):
    """
    고급 커스텀 마스크 및 위치별(앞/뒤/중간 점) 사용자명 생성기
    - 앞에 N글자 / 고정 접두사 (Prefix)
    - 뒤에 N글자 / 고정 접미사 (Suffix)
    - 중간 dot(.) 여부: 'none' (미포함), 'optional' (선택적), 'required' (필수 1개 포함)
    - 또는 직접 패턴 마스크 입력 지원:
      '?' = 영문+숫자 [a-z0-9]
      '@' = 영문자 [a-z]
      '#' = 숫자 [0-9]
      '.' = 점 (Discord 규칙 준수: 첫글자/끝글자 불가, 연속 '..' 불가)
      그 외 일반 문자 = 고정 문자 (e.g. 'kr', 'vip', '77')
    """
    def __init__(
        self,
        length: int = 4,
        prefix: str = "",
        suffix: str = "",
        middle_dot: str = "none",  # "none", "optional", "required"
        mask: str = "",
        exclude_reserved: bool = True
    ):
        self.length = max(3, length)
        self.prefix = prefix.strip().lower()
        self.suffix = suffix.strip().lower()
        self.middle_dot = middle_dot.lower()  # "none", "optional", "required"
        self.custom_mask = mask.strip().lower()
        self.exclude_reserved = exclude_reserved

    def update_params(self, length: int, prefix: str, suffix: str, middle_dot: str, mask: str):
        """런타임 핫스왑(Hot-swap) 파라미터 동적 갱신"""
        self.length = max(3, length)
        self.prefix = prefix.strip().lower()
        self.suffix = suffix.strip().lower()
        self.middle_dot = middle_dot.lower()
        self.custom_mask = mask.strip().lower()

    def _resolve_mask(self) -> str:
        """
        지정된 prefix, suffix, middle_dot, length를 종합하여
        목표 길이에 정확히 일치하는 유효한 마스크 템플릿 생성
        """
        if self.custom_mask:
            return self.custom_mask

        p = self.prefix
        s = self.suffix
        target_len = self.length

        if self.middle_dot == "required":
            # 중간 점(.)이 필수인 경우: 시작/끝에 올 수 없으므로 최소 앞뒤로 1글자씩 보장
            left_fixed = p
            right_fixed = s
            min_left = 1 if len(left_fixed) == 0 else 0
            min_right = 1 if len(right_fixed) == 0 else 0

            # 최소 요구 길이 = 앞고정 + (앞최소1) + 점(1) + (뒤최소1) + 뒤고정
            min_len = len(left_fixed) + min_left + 1 + min_right + len(right_fixed)
            eff_len = max(target_len, min_len)
            rem = eff_len - (len(left_fixed) + 1 + len(right_fixed))

            # 남은 와일드카드를 점 좌우로 균등 분할
            left_wildcards = min_left + (rem - min_left - min_right) // 2
            right_wildcards = rem - left_wildcards
            return left_fixed + ("?" * left_wildcards) + "." + ("?" * right_wildcards) + right_fixed

        elif self.middle_dot == "optional":
            min_len = len(p) + len(s)
            eff_len = max(target_len, min_len)
            rem = eff_len - (len(p) + len(s))

            # 35% 확률로 점 포함 (단, 최소 3자 이상이고 와일드카드가 1개 이상 존재할 때)
            if random.random() < 0.35 and eff_len >= 3 and rem >= 1:
                min_left = 1 if len(p) == 0 else 0
                min_right = 1 if len(s) == 0 else 0
                rem_wild = rem - 1  # 점을 위해 1자리 사용
                if rem_wild >= (min_left + min_right):
                    left_w = min_left + (rem_wild - min_left - min_right) // 2
                    right_w = rem_wild - left_w
                    return p + ("?" * left_w) + "." + ("?" * right_w) + s

            return p + ("?" * rem) + s

        else: # "none"
            min_len = len(p) + len(s)
            eff_len = max(target_len, min_len)
            rem = eff_len - (len(p) + len(s))
            return p + ("?" * rem) + s

    def _generate_candidate_from_mask(self, mask: str) -> str:
        chars = []
        for ch in mask:
            if ch == '?':
                chars.append(random.choice(ALPHANUMERIC))
            elif ch == '@':
                chars.append(random.choice(LETTERS))
            elif ch == '#':
                chars.append(random.choice(DIGITS))
            else:
                chars.append(ch)
        return "".join(chars)

    def next_username(self) -> Optional[str]:
        mask = self._resolve_mask()
        expected_len = len(mask)
        for _ in range(50):
            cand = self._generate_candidate_from_mask(mask)
            # Discord 규정 검증 (정확한 목표 길이, 시작/끝 점 불가, 연속 점 불가)
            if DiscordRuleValidator.is_valid(cand, min_len=expected_len, max_len=expected_len, check_reserved=self.exclude_reserved):
                return cand
        return None

    def get_pattern_type(self) -> str:
        if self.custom_mask:
            return f"mask:{self.custom_mask}"
        dot_str = "+dot" if self.middle_dot == "required" else ("~dot" if self.middle_dot == "optional" else "")
        return f"custom(pre='{self.prefix}',suf='{self.suffix}'{dot_str})"
