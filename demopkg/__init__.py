"""demopkg — минимальный демо-пакет для тестов DocScribe."""

from .client import Client
from .errors import ApiError, RateLimitError

__all__ = ["Client", "ApiError", "RateLimitError"]
__version__ = "0.1.0"
