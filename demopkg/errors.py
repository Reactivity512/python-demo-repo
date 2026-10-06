"""Исключения demopkg."""


class DemopkgError(Exception):
    """Базовое исключение пакета."""


class ApiError(DemopkgError):
    def __init__(self, status_code: int, message: str = "") -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code


class RateLimitError(ApiError):
    def __init__(self, retry_after: int = 60) -> None:
        super().__init__(429, f"retry after {retry_after}s")
        self.retry_after = retry_after
