"""Custom exceptions for the Addepy SDK."""
from typing import Any, Optional

import requests


class AddePyError(Exception):
    """Base exception for all AddePy SDK errors."""

    def __init__(
        self, message: str, response: Optional[requests.Response] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.response = response
        self.status_code = response.status_code if response is not None else None
        self.request_id = None
        self.errors: Any = None
        if response is not None:
            self.request_id = response.headers.get("X-Request-ID") or response.headers.get("Request-ID")
            try:
                body = response.json()
                if isinstance(body, dict):
                    self.errors = body.get("errors")
            except ValueError:
                pass


class AuthenticationError(AddePyError):
    """Raised when API authentication fails (401)."""

    pass


class ForbiddenError(AddePyError):
    """Raised when user lacks required permissions (403)."""

    pass


class ConflictError(AddePyError):
    """Raised when action would result in invalid data state (409)."""

    pass


class GoneError(AddePyError):
    """Raised when resource was available but has expired (410)."""

    pass


class RateLimitError(AddePyError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str,
        response: Optional[requests.Response] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        super().__init__(message, response)
        self.retry_after = retry_after


class ValidationError(AddePyError):
    """Raised for invalid request parameters (400, 422)."""

    pass


class NotFoundError(AddePyError):
    """Raised when a resource is not found (404)."""

    pass


class AddePyTimeoutError(AddePyError):
    """Raised when polling times out waiting for job completion."""

    def __init__(
        self, message: str, job_id: str, last_status: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.job_id = job_id
        self.last_status = last_status


class TransportError(AddePyError):
    """A connection failed before an API response was available."""


class RequestTimeoutError(TransportError):
    """A network request exceeded its configured timeout or deadline."""


class ProtocolError(AddePyError):
    """The server response does not satisfy the expected API contract."""


class JobError(AddePyError):
    """A server-side job failed; retains its identifier and structured details."""

    def __init__(self, message: str, job_id: str, status: Optional[str] = None,
                 errors: Any = None, job_data: Any = None,
                 response: Optional[requests.Response] = None) -> None:
        super().__init__(message, response)
        self.job_id = job_id
        self.status = status
        self.errors = errors
        self.job_data = job_data
