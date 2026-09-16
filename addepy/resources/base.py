"""HTTP helpers, bounded polling, and JSON:API pagination."""

from contextlib import nullcontext
import json
import math
import time
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, Optional, TypeVar
from urllib.parse import parse_qsl, urlsplit, urlunsplit

import requests

from ..constants import (
    DEFAULT_BACKOFF_FACTOR, DEFAULT_INITIAL_WAIT, DEFAULT_MAX_WAIT,
    DEFAULT_PAGE_LIMIT, DEFAULT_TIMEOUT, MAX_PAGE_LIMIT,
)
from ..exceptions import AddePyTimeoutError, ProtocolError, RequestTimeoutError

if TYPE_CHECKING:
    from ..client import AddePy

T = TypeVar("T")


class BaseResource:
    def __init__(self, client: "AddePy") -> None:
        self._client = client

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        return self._client._request("GET", endpoint, params=params, **kwargs)

    def _post(self, endpoint: str, json: Any = None, data: Any = None,
              params: Any = None, headers: Any = None, **kwargs: Any) -> requests.Response:
        return self._client._request("POST", endpoint, json=json, data=data, params=params, headers=headers, **kwargs)

    def _patch(self, endpoint: str, json: Any = None, **kwargs: Any) -> requests.Response:
        return self._client._request("PATCH", endpoint, json=json, **kwargs)

    def _put(self, endpoint: str, json: Any = None, **kwargs: Any) -> requests.Response:
        return self._client._request("PUT", endpoint, json=json, **kwargs)

    def _delete(self, endpoint: str, json: Any = None, data: Any = None,
                params: Any = None, headers: Any = None, **kwargs: Any) -> requests.Response:
        return self._client._request("DELETE", endpoint, json=json, data=data, params=params, headers=headers, **kwargs)

    def _poll_until_complete(self, job_id: str, check_status_fn: Callable[[str], T],
                             is_complete_fn: Callable[[T], bool], *,
                             initial_wait: float = DEFAULT_INITIAL_WAIT,
                             max_wait: float = DEFAULT_MAX_WAIT,
                             backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
                             timeout: float = DEFAULT_TIMEOUT, job_type: str = "job") -> T:
        """Check immediately, then poll within a monotonic deadline.

        The same deadline limits transport retries and request timeouts. A slow
        server's completed response arriving after the deadline is a timeout too.
        """
        if any(not math.isfinite(v) or v <= 0 for v in (initial_wait, max_wait, timeout)) or not math.isfinite(backoff_factor) or backoff_factor < 1:
            raise ValueError("Polling intervals/timeout must be positive; backoff_factor must be >= 1")
        deadline = time.monotonic() + timeout
        wait_time = min(initial_wait, max_wait)
        last_status: Optional[T] = None

        def timed_out() -> AddePyTimeoutError:
            return AddePyTimeoutError(
                f"{job_type.capitalize()} {job_id} did not complete within {timeout} seconds",
                job_id=job_id, last_status=str(last_status) if last_status is not None else None,
            )

        deadline_factory = getattr(self._client, "request_deadline", None)
        context = deadline_factory(deadline) if deadline_factory is not None else nullcontext()
        with context:
            while True:
                if time.monotonic() >= deadline:
                    raise timed_out()
                try:
                    last_status = check_status_fn(job_id)
                except RequestTimeoutError as exc:
                    if time.monotonic() >= deadline:
                        raise timed_out() from exc
                    raise
                if time.monotonic() >= deadline:
                    raise timed_out()
                if is_complete_fn(last_status):
                    return last_status
                time.sleep(min(wait_time, max(0, deadline - time.monotonic())))
                wait_time = min(wait_time * backoff_factor, max_wait)

    def iter_pages(self, endpoint: str, *, params: Optional[Dict[str, Any]] = None,
                   page_limit: Optional[int] = None, max_pages: Optional[int] = None,
                   cursor_parameter: str = "page[cursor]") -> Generator[Dict[str, Any], None, None]:
        """Yield full response documents, following server links or metadata cursors.

        Explicit next links take precedence. Their query parameters replace the
        current pagination coordinates while preserving filters omitted by the
        server. Repeated links/cursors raise ProtocolError instead of looping.
        ``cursor_parameter`` controls metadata-only cursors (e.g. billable
        portfolios); links retain their exact documented cursor spelling.
        """
        if page_limit is not None and page_limit <= 0:
            raise ValueError("page_limit must be positive")
        if max_pages is not None and max_pages < 0:
            raise ValueError("max_pages cannot be negative")
        if max_pages == 0:
            return
        current_endpoint = endpoint
        request_params = dict(params or {})
        if page_limit is not None:
            request_params["page[limit]"] = min(page_limit, MAX_PAGE_LIMIT)
        seen: set[str] = set()
        pages = 0
        while True:
            fingerprint = current_endpoint + json.dumps(request_params, sort_keys=True, default=str)
            if fingerprint in seen:
                raise ProtocolError("Pagination returned a repeated next page")
            seen.add(fingerprint)
            response = self._get(current_endpoint, params=request_params)
            try:
                document = response.json()
            except ValueError as exc:
                raise ProtocolError("Expected a JSON:API page", response) from exc
            if not isinstance(document, dict) or "data" not in document:
                raise ProtocolError("Expected a JSON:API page containing data", response)
            yield document
            pages += 1
            if max_pages is not None and pages >= max_pages:
                return
            links = document.get("links") or {}
            next_link = links.get("next") if isinstance(links, dict) else None
            if isinstance(next_link, dict):
                next_link = next_link.get("href")
            if next_link:
                if not isinstance(next_link, str):
                    raise ProtocolError("Pagination next link must be a URL")
                parsed = urlsplit(next_link)
                # A query-only link is relative to the current resource.
                if parsed.path or parsed.netloc:
                    current_endpoint = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
                next_params: dict[str, Any] = {}
                for key, value in parse_qsl(parsed.query, keep_blank_values=True):
                    if key in next_params:
                        previous = next_params[key]
                        next_params[key] = previous + [value] if isinstance(previous, list) else [previous, value]
                    else:
                        next_params[key] = value
                # Do not retain a stale cursor/offset when the server changes it.
                request_params = {k: v for k, v in request_params.items()
                                  if k not in ("page[after]", "page[cursor]", "page[number]", "page[offset]", "cursor", "offset")}
                request_params.update(next_params)
                continue
            # Explicit links.next=null declares the end, even if old metadata remains.
            if isinstance(links, dict) and "next" in links:
                return
            meta = document.get("meta") or {}
            page = meta.get("page") or {} if isinstance(meta, dict) else {}
            cursor = page.get("next_cursor") if isinstance(page, dict) else None
            if cursor is None or cursor == "":
                return
            request_params[cursor_parameter] = cursor

    def _items(self, pages: Any, max_items: Optional[int]) -> Generator[Dict[str, Any], None, None]:
        if max_items is not None and max_items < 0:
            raise ValueError("max_items cannot be negative")
        if max_items == 0:
            return
        count = 0
        for page in pages:
            items = page["data"]
            if not isinstance(items, list):
                raise ProtocolError("Expected a collection with data as an array")
            for item in items:
                if not isinstance(item, dict):
                    raise ProtocolError("Expected resource objects in data array")
                yield item
                count += 1
                if max_items is not None and count >= max_items:
                    return

    def _paginate(self, endpoint: str, *, params: Optional[Dict[str, Any]] = None,
                  page_limit: int = DEFAULT_PAGE_LIMIT, max_items: Optional[int] = None,
                  cursor_parameter: str = "page[cursor]") -> Generator[Dict[str, Any], None, None]:
        return self._items(self.iter_pages(endpoint, params=params, page_limit=page_limit,
                                          cursor_parameter=cursor_parameter), max_items)

    def _paginate_offset(self, endpoint: str, *, params: Optional[Dict[str, Any]] = None,
                         page_size: int = 50, max_items: Optional[int] = None) -> Generator[Dict[str, Any], None, None]:
        if page_size <= 0:
            raise ValueError("page_size must be positive")
        request_params = dict(params or {})
        request_params.update({"page[size]": page_size, "page[number]": 0})
        return self._items(self.iter_pages(endpoint, params=request_params), max_items)
