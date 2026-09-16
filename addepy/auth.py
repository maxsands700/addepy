"""OAuth refresh support, independent of the resource API transport."""

import threading
import time
import math
from typing import Any, Callable, Optional
from urllib.parse import urlparse

import requests
from requests.adapters import TimeoutSauce

from .exceptions import AuthenticationError, RequestTimeoutError, TransportError


class OAuthTokenProvider:
    """Callable bearer-token provider that refreshes using returned ``expires_in``.

    Register/authorize the OAuth application separately, then provide its refresh
    token. ``on_token_update`` can persist rotated tokens in your secrets store.
    The caller owns any injected session and this provider's lifecycle.
    """

    def __init__(
        self,
        *,
        token_url: str,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        access_token: Optional[str] = None,
        expires_in: float = 0,
        timeout: float = 30,
        session: Optional[requests.Session] = None,
        on_token_update: Optional[Callable[[dict[str, Any]], None]] = None,
    ) -> None:
        parsed = urlparse(token_url)
        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or parsed.username
            or parsed.password
            or parsed.fragment
        ):
            raise ValueError(
                "token_url must be an HTTPS URL without embedded credentials"
            )
        if timeout <= 0 or not all((client_id, client_secret, refresh_token)):
            raise ValueError("OAuth credentials and a positive timeout are required")
        self.token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._access_token = access_token
        self._expires_at = time.monotonic() + expires_in
        self._timeout = timeout
        self._session = session if session is not None else requests.Session()
        self._owns_session = session is None
        self._on_token_update = on_token_update
        self._lock = threading.Lock()

    def __call__(self) -> str:
        return self.get_token()

    def get_token(self, *, deadline: Optional[float] = None) -> str:
        """Get a token within an optional monotonic transport/polling deadline."""
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            raise RequestTimeoutError("OAuth refresh deadline exceeded")
        acquired = (
            self._lock.acquire()
            if remaining is None
            else self._lock.acquire(timeout=remaining)
        )
        if not acquired:
            raise RequestTimeoutError("OAuth refresh lock deadline exceeded")
        try:
            if self._access_token and time.monotonic() < self._expires_at:
                return self._access_token
            timeout: Any = self._timeout
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise RequestTimeoutError("OAuth refresh deadline exceeded")
                timeout = TimeoutSauce(
                    total=remaining,
                    connect=min(self._timeout, remaining),
                    read=min(self._timeout, remaining),
                )
            try:
                response = self._session.post(
                    self.token_url,
                    data={
                        "grant_type": "refresh_token",
                        "client_id": self._client_id,
                        "client_secret": self._client_secret,
                        "refresh_token": self._refresh_token,
                    },
                    headers={"Accept": "application/json"},
                    timeout=timeout,
                    allow_redirects=False,
                )
            except requests.RequestException as exc:
                error = (
                    RequestTimeoutError
                    if isinstance(exc, requests.Timeout)
                    else TransportError
                )
                raise error("OAuth token refresh connection failed") from exc
            try:
                if not 200 <= response.status_code < 300:
                    raise AuthenticationError("OAuth token refresh failed", response)
                try:
                    tokens = response.json()
                    token = tokens["access_token"]
                    lifetime = float(tokens["expires_in"])
                    if (
                        not isinstance(token, str)
                        or not token
                        or lifetime <= 0
                        or not math.isfinite(lifetime)
                    ):
                        raise ValueError("Invalid token response")
                except (ValueError, TypeError, KeyError) as exc:
                    raise AuthenticationError(
                        "OAuth response needs access_token and positive expires_in",
                        response,
                    ) from exc
                self._access_token = token
                self._refresh_token = tokens.get("refresh_token") or self._refresh_token
                # A proportional margin also supports short-lived test/server tokens.
                self._expires_at = time.monotonic() + lifetime - min(30, lifetime * 0.1)
                if self._on_token_update is not None:
                    self._on_token_update(dict(tokens))
                return token
            finally:
                response.close()
        finally:
            self._lock.release()

    def close(self) -> None:
        if self._owns_session:
            self._session.close()

    def __enter__(self) -> "OAuthTokenProvider":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
