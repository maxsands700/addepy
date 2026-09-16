"""HTTP policy shared by every SDK resource."""

from contextlib import contextmanager
from contextvars import ContextVar
from collections.abc import Iterator as IteratorABC
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import math
import random
import time
from typing import Any, Callable, Iterator, Optional
from urllib.parse import urljoin, urlparse

import requests
from requests.adapters import TimeoutSauce

from .auth import OAuthTokenProvider
from .exceptions import (
    AddePyError,
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    GoneError,
    NotFoundError,
    ProtocolError,
    RateLimitError,
    RequestTimeoutError,
    TransportError,
    ValidationError,
)


class _HeaderAuth(requests.auth.AuthBase):
    """Keep explicitly configured SDK headers ahead of session/netrc credentials."""

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        return request


def retry_after(response: requests.Response) -> Optional[float]:
    """Read Addepar's delay, or the standard seconds/HTTP-date header."""
    value = response.headers.get("X-RateLimit-Retry-After") or response.headers.get(
        "Retry-After"
    )
    if value is None:
        return None
    try:
        seconds = float(value)
        return max(0.0, seconds) if math.isfinite(seconds) else None
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            return max(0.0, (date - datetime.now(timezone.utc)).total_seconds())
        except (ValueError, TypeError, OverflowError):
            return None


def raise_api_error(response: requests.Response) -> None:
    """Expose diagnostic data without copying potentially sensitive bodies into logs."""
    status = response.status_code
    message = f"Addepar returned HTTP {status}"
    if status == 429:
        raise RateLimitError(message, response, retry_after=retry_after(response))
    error_class = {
        400: ValidationError,
        401: AuthenticationError,
        403: ForbiddenError,
        404: NotFoundError,
        409: ConflictError,
        410: GoneError,
        422: ValidationError,
    }.get(status, AddePyError)
    raise error_class(message, response)


class Transport:
    def __init__(
        self,
        *,
        base_url: str,
        headers: dict[str, str],
        timeout: Any,
        max_retries: int,
        max_retry_wait: float,
        session: Optional[requests.Session] = None,
        token_provider: Optional[Callable[[], str]] = None,
        download_session: Optional[requests.Session] = None,
    ) -> None:
        parsed = urlparse(base_url)
        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError(
                "base_url must be an HTTPS API URL without credentials, query, or fragment"
            )
        if max_retries < 0 or max_retry_wait < 0:
            raise ValueError("Retry limits must be nonnegative")
        self.base_url = base_url.rstrip("/")
        self._origin = (parsed.scheme, parsed.hostname, parsed.port or 443)
        self.headers = dict(headers)
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_retry_wait = max_retry_wait
        self.session = session if session is not None else requests.Session()
        self._owns_session = session is None
        self._download_session = download_session
        self._owns_download_session = download_session is None
        self._token_provider = token_provider
        self._deadline: ContextVar[Optional[float]] = ContextVar(
            "addepy_deadline", default=None
        )

    @contextmanager
    def request_deadline(self, deadline: float) -> Iterator[None]:
        current = self._deadline.get()
        token = self._deadline.set(
            min(current, deadline) if current is not None else deadline
        )
        try:
            yield
        finally:
            self._deadline.reset(token)

    def resolve_url(self, endpoint: str) -> str:
        parsed = urlparse(endpoint)
        if parsed.scheme or parsed.netloc:
            self._validate_url(endpoint, same_origin=True)
            return endpoint
        root = urlparse(self.base_url)
        if endpoint.startswith("/api/v1/") or endpoint == "/api/v1":
            url = f"{root.scheme}://{root.netloc}{endpoint}"
        elif endpoint.startswith("/v1/") or endpoint == "/v1":
            prefix = (
                self.base_url[:-3]
                if self.base_url.endswith("/v1")
                else self.base_url + "/"
            )
            url = prefix.rstrip("/") + endpoint
        else:
            url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        self._validate_url(url, same_origin=True)
        return url

    def _validate_url(self, url: str, *, same_origin: bool) -> None:
        parsed = urlparse(url)
        origin = (parsed.scheme, parsed.hostname, parsed.port or 443)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.fragment
            or (same_origin and origin != self._origin)
        ):
            raise ValueError(
                "API URLs must use HTTPS and the configured host; redirects cannot include credentials"
            )

    def _timeout(self, configured: Any) -> Any:
        values = (
            configured if isinstance(configured, tuple) else (configured, configured)
        )
        if len(values) != 2 or any(
            not isinstance(v, (int, float)) or v <= 0 or not math.isfinite(v)
            for v in values
        ):
            raise ValueError(
                "timeout must be positive seconds or a (connect, read) pair"
            )
        deadline = self._deadline.get()
        if deadline is None:
            return configured
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RequestTimeoutError("Request deadline exceeded")
        return TimeoutSauce(
            total=remaining,
            connect=min(values[0], remaining),
            read=min(values[1], remaining),
        )

    def _send(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Follow redirects explicitly; never send API headers to storage hosts."""
        follow = kwargs.pop("allow_redirects", True)
        timeout = kwargs.pop("timeout", self.timeout)
        external = False
        for _ in range(11):
            current = dict(kwargs)
            session = self.session
            if external:
                if self._download_session is None:
                    self._download_session = requests.Session()
                    self._download_session.trust_env = False
                session = self._download_session
                # Prepare independently of the session: Session.request() would
                # merge its auth, headers and cookies back into the request.
                prepared = requests.Request(
                    method,
                    url,
                    headers={
                        "Accept": "*/*",
                        "User-Agent": self.headers.get("User-Agent", "addepy"),
                    },
                ).prepare()
                response = session.send(
                    prepared,
                    timeout=self._timeout(timeout),
                    allow_redirects=False,
                    stream=kwargs.get("stream", False),
                    verify=kwargs.get("verify", True),
                    cert=None,
                    proxies={},
                )
            else:
                current.setdefault("auth", _HeaderAuth())
                response = session.request(
                    method,
                    url,
                    timeout=self._timeout(timeout),
                    allow_redirects=False,
                    **current,
                )
            if not follow or response.status_code not in (301, 302, 303, 307, 308):
                return response
            location = response.headers.get("Location")
            if not location:
                response.close()
                raise ProtocolError("Redirect response is missing Location", response)
            next_url = urljoin(url, location)
            try:
                self._validate_url(next_url, same_origin=False)
            except ValueError:
                response.close()
                raise
            parsed = urlparse(next_url)
            new_external = (
                parsed.scheme,
                parsed.hostname,
                parsed.port or 443,
            ) != self._origin
            # Never replay a write to a redirect target. A 303 explicitly becomes GET.
            if method not in ("GET", "HEAD") and response.status_code != 303:
                response.close()
                raise ProtocolError(
                    "Refusing to replay a write request across a redirect", response
                )
            if response.status_code == 303:
                method = "GET"
                kwargs.pop("json", None)
                kwargs.pop("data", None)
                kwargs.pop("files", None)
                kwargs["headers"] = {
                    k: v
                    for k, v in kwargs.get("headers", {}).items()
                    if k.lower()
                    not in ("content-type", "content-length", "transfer-encoding")
                }
            response.close()
            kwargs.pop("params", None)
            url = next_url
            external = external or new_external
        raise ProtocolError("Too many HTTP redirects")

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        retry: Optional[bool] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        method = method.upper()
        url = self.resolve_url(endpoint)
        # Stream bodies cannot be replayed safely even when retry=True.
        replayable = (
            not hasattr(kwargs.get("data"), "read")
            and not isinstance(kwargs.get("data"), IteratorABC)
            and "files" not in kwargs
        )
        can_retry = (
            method in ("GET", "HEAD", "OPTIONS") if retry is None else retry
        ) and replayable
        request_headers = dict(self.headers)
        request_headers.update(headers or {})
        for attempt in range(self.max_retries + 1):
            if self._token_provider is not None:
                if isinstance(self._token_provider, OAuthTokenProvider):
                    token = self._token_provider.get_token(
                        deadline=self._deadline.get()
                    )
                else:
                    token = self._token_provider()
                if not isinstance(token, str) or not token:
                    raise AuthenticationError(
                        "Token provider returned an empty or invalid token"
                    )
                request_headers["Authorization"] = f"Bearer {token}"
            response = None
            try:
                response = self._send(method, url, headers=request_headers, **kwargs)
            except requests.RequestException as exc:
                if not can_retry or attempt >= self.max_retries:
                    error = (
                        RequestTimeoutError
                        if isinstance(exc, requests.Timeout)
                        else TransportError
                    )
                    raise error(
                        f"{method} request failed ({type(exc).__name__})"
                    ) from exc
            else:
                if response.status_code < 400:
                    return response
                if (
                    not can_retry
                    or attempt >= self.max_retries
                    or response.status_code not in (429, 500, 502, 503, 504)
                ):
                    raise_api_error(response)
            delay = retry_after(response) if response is not None else None
            if delay is None:
                delay = (2**attempt) + random.uniform(0, 0.25)
            remaining = (
                None
                if self._deadline.get() is None
                else self._deadline.get() - time.monotonic()
            )
            if delay > self.max_retry_wait or (
                remaining is not None and delay >= remaining
            ):
                if response is not None:
                    raise_api_error(response)
                raise TransportError("Retry delay exceeds the configured wait budget")
            if response is not None:
                response.close()
            time.sleep(delay)
        raise TransportError("Request retry budget exhausted")

    def close(self) -> None:
        if self._owns_session:
            self.session.close()
        if self._owns_download_session and self._download_session is not None:
            self._download_session.close()
