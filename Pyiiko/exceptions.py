"""Custom exceptions for pyiiko."""
from __future__ import annotations


class IikoError(Exception):
    """Base exception for all pyiiko errors."""


class IikoAuthError(IikoError):
    """Raised when authentication fails (bad credentials, expired token)."""


class IikoAPIError(IikoError):
    """Raised when the server returns an HTTP error response."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
