# src/network/exceptions.py

class CheckerException(Exception):
    """Base exception for Discord Username Checker"""
    pass

class RateLimitedException(CheckerException):
    def __init__(self, retry_after: float = 1.0, message: str = "Rate limited by Discord/Cloudflare"):
        super().__init__(message)
        self.retry_after = retry_after

class WafBlockedException(CheckerException):
    """Triggered when Cloudflare Turnstile / 403 Challenge is detected"""
    pass

class ProxyFailedException(CheckerException):
    """Triggered on proxy connection failure or handshake error"""
    pass

class InvalidUsernameException(CheckerException):
    """Triggered when Discord API returns 400 Bad Request (reserved / invalid characters)"""
    pass
