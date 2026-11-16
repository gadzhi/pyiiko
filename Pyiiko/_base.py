"""Shared HTTP session, retry logic, and error handling for iiko API clients."""
from __future__ import annotations

import logging
from time import sleep
from types import TracebackType
from typing import Any, Self
from urllib.parse import urlsplit

import requests
from requests.exceptions import ConnectionError, RequestException, SSLError, Timeout
from urllib3.exceptions import InvalidHeader
from urllib3.util import Retry

from .exceptions import IikoAPIError

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10
_RETRY_DELAYS = (0, 1, 2)
_RETRY_STATUS_CODES = (500, 502, 503, 504)
_MAX_RETRY_AFTER = 60
_RETRY_AFTER_PARSER = Retry()


def _http_retry_delay(response: requests.Response, backoff: int) -> float | None:
    retry_after = response.headers.get("Retry-After")
    delay = None
    if retry_after:
        try:
            delay = _RETRY_AFTER_PARSER.parse_retry_after(retry_after)
        except InvalidHeader:
            pass
    if response.status_code not in _RETRY_STATUS_CODES and (
        delay is None or response.status_code not in Retry.RETRY_AFTER_STATUS_CODES
    ):
        return None
    if delay is not None and delay > _MAX_RETRY_AFTER:
        return None
    return max(backoff, delay or 0)


class BaseIikoClient:
    """Base class for all iiko API clients.

    Provides a shared requests.Session, retries for read-only operations,
    and HTTP errors that omit credentials.

    Supports use as a context manager::

        with IikoServer(ip=..., login=..., password=...) as client:
            data = client.departments()
    """

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()

    def _send(self, method: str, url: str, operation: str, **kwargs: Any) -> requests.Response:
        error: Exception
        try:
            return self._session.request(
                method, url, timeout=self._timeout, allow_redirects=False, **kwargs
            )
        except RequestException as exc:
            error = type(exc)(f"{type(exc).__name__} for {operation}")
        except ValueError:
            error = ValueError(f"Invalid HTTP request or response for {operation}")
        # The original exception can include the query string, headers or body.
        raise error

    def _request(
        self, method: str, path: str, *, retry: bool, **kwargs: Any
    ) -> requests.Response:
        url = f"{self._base_url}/{path.lstrip('/')}"
        operation = f"{method} {urlsplit(path).path}"
        logger.debug("%s", operation)
        for backoff in _RETRY_DELAYS if retry else ():
            delay: float | None = backoff
            try:
                response = self._send(method, url, operation, **kwargs)
            except SSLError:
                raise
            except (Timeout, ConnectionError):
                pass
            else:
                delay = _http_retry_delay(response, backoff)
                if delay is None:
                    break
                response.close()
            if delay:
                sleep(delay)
        else:
            response = self._send(method, url, operation, **kwargs)

        status = response.status_code
        if 300 <= status < 600:
            response.close()
            raise IikoAPIError(f"HTTP {status} for {operation}", status_code=status)
        return response

    def _get(self, path: str, *, retry: bool = True, **kwargs: Any) -> requests.Response:
        return self._request("GET", path, retry=retry, **kwargs)

    def _post(self, path: str, *, retry: bool = False, **kwargs: Any) -> requests.Response:
        return self._request("POST", path, retry=retry, **kwargs)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()
