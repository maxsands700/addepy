"""Python SDK for Addepar. See README.md for setup and query examples."""

import logging

from .client import AddePy
from .auth import OAuthTokenProvider
from ._version import __version__
from .exceptions import (
    AddePyError,
    AddePyTimeoutError,
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    GoneError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    JobError,
    ProtocolError,
    TransportError,
    RequestTimeoutError,
)

# Create logger for the package
logger = logging.getLogger("addepy")
logger.addHandler(logging.NullHandler())  # Prevent "no handler" warnings

__all__ = [
    "AddePy",
    "OAuthTokenProvider",
    "__version__",
    "JobError",
    "ProtocolError",
    "TransportError",
    "RequestTimeoutError",
    "AddePyError",
    "AddePyTimeoutError",
    "AuthenticationError",
    "ConflictError",
    "ForbiddenError",
    "GoneError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
]
