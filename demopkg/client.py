"""HTTP-клиент демо-API."""

from __future__ import annotations

from dataclasses import dataclass, field

import requests

from .errors import ApiError, RateLimitError

DEFAULT_TIMEOUT = 30


@dataclass
class Page:
    """Страница результатов list_items()."""

    items: list[dict] = field(default_factory=list)
    total: int = 0


class Client:
    """Клиент демо-API.

    :param token: API-токен (заголовок Authorization).
    :param base_url: базовый URL API.
    """

    def __init__(self, token: str, base_url: str = "https://api.demo.dev/v1",
                 timeout: int = DEFAULT_TIMEOUT) -> None:
        if not token:
            raise ValueError("token is required")
        self._session = requests.Session()
        self._session.headers["Authorization"] = f"Bearer {token}"
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def list_items(self, page_size: int = 20, cursor: str | None = None) -> Page:
        """Постраничный список элементов.

        :param page_size: размер страницы (1..100).
        :param cursor: курсор следующей страницы из предыдущего ответа.
        """
        if not 1 <= page_size <= 100:
            raise ValueError("page_size must be in 1..100")
        params = {"page_size": page_size}
        if cursor:
            params["cursor"] = cursor
        resp = self._session.get(f"{self.base_url}/items", params=params,
                                 timeout=self.timeout)
        self._raise_for_status(resp)
        data = resp.json()
        return Page(items=data.get("items", []), total=data.get("total", 0))

    def get_item(self, item_id: str) -> dict:
        """Получить элемент по id; KeyError->ApiError при 404."""
        resp = self._session.get(f"{self.base_url}/items/{item_id}",
                                 timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    @staticmethod
    def _raise_for_status(resp: requests.Response) -> None:
        if resp.status_code == 429:
            raise RateLimitError(retry_after=int(
                resp.headers.get("Retry-After", "60")))
        if resp.status_code >= 400:
            raise ApiError(resp.status_code, resp.text[:200])
