# src/proxy/base.py
import time
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass

@dataclass
class ProxyEndpoint:
    url: str
    provider_name: str
    success_count: int = 0
    fail_count: int = 0
    rate_limited_count: int = 0
    cooldown_until: float = 0.0
    is_dead: bool = False

    def is_available(self) -> bool:
        if self.is_dead:
            return False
        return time.time() >= self.cooldown_until

    def mark_success(self):
        self.success_count += 1

    def mark_rate_limited(self, cooldown_seconds: float = 15.0):
        self.rate_limited_count += 1
        self.cooldown_until = time.time() + cooldown_seconds

    def mark_failure(self, max_fails: int = 3):
        self.fail_count += 1
        if self.fail_count >= max_fails:
            self.is_dead = True

class BaseProxyProvider(ABC):
    @abstractmethod
    def get_proxy(self) -> Optional[ProxyEndpoint]:
        pass

    @abstractmethod
    def report_result(self, endpoint: ProxyEndpoint, success: bool, rate_limited: bool = False, cooldown: float = 15.0):
        pass

    @abstractmethod
    def has_available_proxies(self) -> bool:
        pass
