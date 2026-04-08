"""Shared HTTP session, retry logic, and error handling for iiko API clients."""
from __future__ import annotations

import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import IikoAPIError

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10
_RETRY_TOTAL = 3
_RETRY_BACKOFF = 0.5
_RETRY_STATUS_CODES = (500, 502, 503, 504)


class BaseIikoClient:
    """Base class for all iiko API clients.

    Provides a shared requests.Session with automatic retries on transient
    server errors, structured logging, and uniform HTTP error handling.

    Supports use as a context manager::

        with IikoServer(ip=..., login=..., password=...) as client:
            data = client.departments()
    """

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = self._build_session()

    @staticmethod
    def _build_session() -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=_RETRY_TOTAL,
            backoff_factor=_RETRY_BACKOFF,
            status_forcelist=list(_RETRY_STATUS_CODES),
            allowed_methods=["GET", "POST"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self._base_url}/{path.lstrip('/')}"
        logger.debug("%s %s", method.upper(), url)
        try:
            response = self._session.request(
                method, url, timeout=self._timeout, **kwargs
            )
            response.raise_for_status()
            return response
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            raise IikoAPIError(
                f"HTTP {status} from {url}",
                status_code=status,
            ) from exc

    def _get(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def _post(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> BaseIikoClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
