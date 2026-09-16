"""Public SDK client; resource namespaces share one configurable transport."""

import base64
import os
from pathlib import Path
import re
import tempfile
from typing import TYPE_CHECKING, Any, Callable, Optional

import requests
from dotenv import load_dotenv

from ._version import __version__
from .constants import DEFAULT_CONTENT_TYPE, DEFAULT_REQUEST_TIMEOUT
from .exceptions import RequestTimeoutError, TransportError
from .transport import Transport, raise_api_error

if TYPE_CHECKING:
    from .resources.admin import AdminNamespace
    from .resources.ownership import OwnershipNamespace
    from .resources.portfolio import PortfolioNamespace


class AddePy:
    """Addepar client with Basic or OAuth authentication.

    ``api_key`` remains the base64-encoded key:secret pair used by earlier
    releases. Alternatively pass ``key_id``/``key_secret``, ``access_token``, or
    a callable ``token_provider``. Explicit credentials override environment
    credentials. Injected sessions belong to the caller and are not closed.
    ``load_env=False`` skips .env loading; it still permits environment variables.
    """

    def __init__(
        self,
        firm_name: Optional[str] = None,
        firm_id: Optional[str] = None,
        api_key: Optional[str] = None,
        load_env: bool = True,
        *,
        key_id: Optional[str] = None,
        key_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        token_provider: Optional[Callable[[], str]] = None,
        environment: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Any = DEFAULT_REQUEST_TIMEOUT,
        max_retries: int = 2,
        max_retry_wait: float = 60,
        session: Optional[requests.Session] = None,
        download_session: Optional[requests.Session] = None,
    ) -> None:
        if load_env:
            load_dotenv()
        self._firm_name = firm_name or os.getenv("ADDEPAR_FIRM_NAME")
        self._firm_id = str(firm_id or os.getenv("ADDEPAR_FIRM_ID") or "")
        self.environment = environment or os.getenv("ADDEPAR_ENVIRONMENT", "production")
        suffixes = {
            "production": "addepar.com",
            "development": "clientdev.addepar.com",
            "sandbox": "sandbox.addepar.com",
        }
        if self.environment not in suffixes:
            raise ValueError("environment must be production, development, or sandbox")
        self._base_url = base_url or os.getenv("ADDEPAR_BASE_URL")
        if not self._base_url:
            if not self._firm_name or not re.fullmatch(
                r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?", self._firm_name
            ):
                raise ValueError("Provide a valid firm_name or explicit base_url")
            self._base_url = (
                f"https://{self._firm_name}.{suffixes[self.environment]}/api/v1"
            )
        if not self._firm_id:
            raise ValueError("Missing firm_id/ADDEPAR_FIRM_ID")

        explicit_auth = any(
            v is not None
            for v in (api_key, key_id, key_secret, access_token, token_provider)
        )
        if not explicit_auth:
            access_token = os.getenv("ADDEPAR_ACCESS_TOKEN")
            if not access_token:
                api_key = os.getenv("ADDEPAR_API_KEY")
        if (key_id is None) != (key_secret is None):
            raise ValueError("key_id and key_secret must be supplied together")
        if (
            sum(
                (
                    api_key is not None,
                    key_id is not None,
                    access_token is not None,
                    token_provider is not None,
                )
            )
            != 1
        ):
            raise ValueError(
                "Supply exactly one authentication method: api_key, key pair, access_token, or token_provider"
            )
        headers = {
            "Accept": DEFAULT_CONTENT_TYPE,
            "Content-Type": DEFAULT_CONTENT_TYPE,
            "Addepar-Firm": self._firm_id,
            "User-Agent": f"addepy/{__version__}",
        }
        if key_id is not None:
            api_key = base64.b64encode(f"{key_id}:{key_secret}".encode()).decode(
                "ascii"
            )
        if api_key is not None:
            api_key = api_key.removeprefix("Basic ").strip()
            if not api_key:
                raise ValueError("api_key cannot be empty")
            headers["Authorization"] = f"Basic {api_key}"
        if access_token is not None:
            access_token = access_token.removeprefix("Bearer ").strip()
            if not access_token:
                raise ValueError("access_token cannot be empty")
            headers["Authorization"] = f"Bearer {access_token}"
        self._transport = Transport(
            base_url=self._base_url,
            headers=headers,
            timeout=timeout,
            max_retries=max_retries,
            max_retry_wait=max_retry_wait,
            session=session,
            token_provider=token_provider,
            download_session=download_session,
        )
        self._session = self._transport.session
        self._portfolio: Optional["PortfolioNamespace"] = None
        self._admin: Optional["AdminNamespace"] = None
        self._ownership: Optional["OwnershipNamespace"] = None

    @property
    def base_url(self) -> str:
        return self._transport.base_url

    @property
    def portfolio(self) -> "PortfolioNamespace":
        if self._portfolio is None:
            from .resources.portfolio import PortfolioNamespace

            self._portfolio = PortfolioNamespace(self)
        return self._portfolio

    @property
    def admin(self) -> "AdminNamespace":
        if self._admin is None:
            from .resources.admin import AdminNamespace

            self._admin = AdminNamespace(self)
        return self._admin

    @property
    def ownership(self) -> "OwnershipNamespace":
        if self._ownership is None:
            from .resources.ownership import OwnershipNamespace

            self._ownership = OwnershipNamespace(self)
        return self._ownership

    def request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        """Make a raw API request, retaining response and unknown JSON fields.

        Read requests retry transient failures by default. Writes require an
        explicit ``retry=True``; callers must ensure replay is safe. Per-call
        ``timeout``, ``headers``, ``params``, ``json``, and ``stream`` are accepted.
        """
        return self._transport.request(method, endpoint, **kwargs)

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request(method, endpoint, **kwargs)

    def request_deadline(self, deadline: float) -> Any:
        return self._transport.request_deadline(deadline)

    def iter_pages(self, endpoint: str, **kwargs: Any) -> Any:
        """Iterate complete JSON:API pages, including included, links and meta."""
        from .resources.base import BaseResource

        return BaseResource(self).iter_pages(endpoint, **kwargs)

    def download(
        self,
        endpoint: str,
        path: Any,
        *,
        chunk_size: int = 65536,
        overwrite: bool = False,
        **request_kwargs: Any,
    ) -> Path:
        """Stream to an atomic file; failures never leave partial results.

        Caller chooses the filename. Existing files are preserved unless
        ``overwrite=True``. Cross-host GET redirects use a credential-free session.
        """
        target = Path(path)
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if target.exists() and not overwrite:
            raise FileExistsError(target)
        request_kwargs["stream"] = True
        response = self.request("GET", endpoint, **request_kwargs)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=target.parent, prefix=f".{target.name}.", delete=False
            ) as handle:
                temporary = Path(handle.name)
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        handle.write(chunk)
            if overwrite:
                os.replace(temporary, target)
            else:
                # Linking protects against concurrent destination creation too.
                os.link(temporary, target)
            return target
        except requests.RequestException as exc:
            error = (
                RequestTimeoutError
                if isinstance(exc, requests.Timeout)
                else TransportError
            )
            raise error("Download interrupted before completion") from exc
        finally:
            response.close()
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def _handle_error_response(self, response: requests.Response) -> None:
        raise_api_error(response)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> "AddePy":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


# Older resource annotations used this name; keep downstream imports valid.
AddeparClient = AddePy
