"""Custom exceptions for the Addepy SDK."""
from typing import Optional

import requests


class AddeparError(Exception):
    """Base exception for all Addepar API errors."""

    def __init__(
        self, message: str, response: Optional[requests.Response] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.response = response
        self.status_code = response.status_code if response else None


class AuthenticationError(AddeparError):
    """Raised when API authentication fails (401)."""

    pass


class RateLimitError(AddeparError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str,
        response: Optional[requests.Response] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        super().__init__(message, response)
        self.retry_after = retry_after


class ValidationError(AddeparError):
    """Raised for invalid request parameters (400, 422)."""

    pass


class NotFoundError(AddeparError):
    """Raised when a resource is not found (404)."""

    pass


class AddeparTimeoutError(AddeparError):
    """Raised when polling times out waiting for job completion."""

    def __init__(
        self, message: str, job_id: str, last_status: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.job_id = job_id
        self.last_status = last_status
