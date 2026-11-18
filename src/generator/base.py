# src/generator/base.py
import re
import string
from abc import ABC, abstractmethod
from typing import Optional, Set

ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + "_."
DISCORD_RESERVED_USERNAMES: Set[str] = {
    "discord", "everyone", "here", "clyde", "nitro", "system",
    "admin", "administrator", "moderator", "mod", "help",
    "support", "community", "official", "trust", "safety"
}

class DiscordRuleValidator:
    @staticmethod
    def is_valid(username: str, min_len: int = 2, max_len: int = 32, check_reserved: bool = True) -> bool:
        if not username:
            return False

        u = username.lower()
        if len(u) < min_len or len(u) > max_len:
            return False

        # Discord username restrictions:
        # 1. No consecutive dots allowed
        if ".." in u:
            return False

        # 2. Cannot start or end with a dot
        if u.startswith(".") or u.endswith("."):
            return False

        # 3. Must only contain allowed characters
        for ch in u:
            if ch not in ALLOWED_CHARACTERS:
                return False

        # 4. Cannot be a reserved username
        if check_reserved and u in DISCORD_RESERVED_USERNAMES:
            return False

        return True

class BaseGenerator(ABC):
    @abstractmethod
    def next_username(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_pattern_type(self) -> str:
        pass
