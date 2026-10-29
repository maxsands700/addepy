# Client conventions

Construct and close clients as described in [configuration](configuration.md).
Namespaces share one authenticated transport. Routes below are relative to its
versioned `base_url`; API requests must remain on the configured HTTPS origin.

## Public client methods

| Method | Result/behavior |
| --- | --- |
| `request(method, endpoint, **kwargs)` | `requests.Response`; accepts `params`, `json`, `data`, `files`, `headers`, `timeout`, `stream`, and `retry`. |
| `iter_pages(endpoint, *, params=None, page_limit=None, max_pages=None, cursor_parameter="page[cursor]")` | Iterator of complete JSON:API documents. |
| `download(endpoint, path, *, chunk_size=65536, overwrite=False, **request_kwargs)` | Streamed GET; returns `Path`. |
| `request_deadline(deadline)` | Context manager bounding requests/retries/refresh by a `time.monotonic()` deadline. |
| `close()` | Close SDK-owned sessions. Context exit calls it. |
| `base_url` | Resolved API base URL. |

```python
with client.request("GET", "/entities/123", params={"fields[entities]": "model_type"}) as response:
    document = response.json()
```

Raw access preserves full server JSON, including unknown attributes, `included`,
`meta`, and `links`. Use it when a wrapper omits an option; supply the complete
wire payload. Resource wrappers construct their own envelopes.

## Return vocabulary

| Reference term | Python value |
| --- | --- |
| resource | Dictionary containing one JSON:API resource, with `data` unwrapped. |
| items | List of resources or endpoint-specific records. |
| document | Complete decoded JSON response. |
| Response | `requests.Response`; `.json()`, `.text`, `.content` for JSON/text/binary. |
| ID | Usually `str`; retain returned composite/UUID identifiers. |
| bytes / Path / None | Binary content / written destination / no returned value. |

Ordinary resource/query helpers already return dictionaries/lists. Call
`.json()` on a Response. Query execute/resume methods return a Response;
portfolio JSON views return a dictionary, non-JSON portfolio views return bytes,
and transaction views return a Response. Exact exceptions appear in resource tables.

## Pagination

- Resource `list_*` helpers usually default to `limit=10000`; `iter_*` helpers
  usually use `limit=None`. `limit` caps total records, `page_limit` sets page size.
  Some nonpaginated helpers have neither argument; consult their signatures.
- Generic default page size: 500, maximum 2000. Fees/schedules, benchmarks/
  strategies, and report lists cap initial pages at 500. Underlying assets and
  payouts use their resource-specific offset helpers.
- `iter_pages` yields full documents; `page_limit=None` leaves the server's page
  size unchanged. `max_pages=0` yields nothing. Positive page sizes are required.
- Returned next links take precedence over metadata cursors; filters omitted
  from next links persist. Repeated coordinates raise `ProtocolError`.
  Explicit `links.next=null` ends iteration. Metadata-only fallback uses
  `meta.page.next_cursor` and the configured `cursor_parameter`.
- Resource iterators with `limit=0` make no request. Negative limits fail.

```python
for entity in client.ownership.entities.iter_entities(model_types=["TRUST"], limit=500):
    print(entity["id"])

for page in client.iter_pages("/fees", params={"include": "fee_schedules"}, page_limit=100):
    print(page.get("included", []))
```

## Downloads and HTTP policy

`download` streams to a temporary file and atomically installs the destination.
The parent directory must exist. Existing paths raise `FileExistsError` unless
`overwrite=True`; interrupted downloads leave no partial destination. File/report
`*_to` wrappers expose overwrite; job `download_job_results` does not.

Read requests retry connection failures and HTTP 429/500/502/503/504 at most twice
by default. `max_retries=0` disables retries. Writes require explicit
`retry=True` and replayable bodies; multipart uploads and file/iterator bodies
are not replayed. Server retry delays exceeding `max_retry_wait` surface errors.
Cross-host download redirects use a separate credential-free session.

Default request timeout: `(10, 60)` seconds. Streaming read timeout measures
inactivity, not total download duration. Job polling has a separate deadline;
see [Jobs](jobs.md).

## Errors

Import exceptions from `addepy`; all SDK errors below inherit `AddePyError`.

| Condition | Exception |
| --- | --- |
| HTTP 400/422 | `ValidationError` |
| HTTP 401 / 403 / 404 / 409 / 410 | `AuthenticationError` / `ForbiddenError` / `NotFoundError` / `ConflictError` / `GoneError` |
| HTTP 429 | `RateLimitError`, with `retry_after` seconds when supplied. |
| Other HTTP error | `AddePyError` |
| Connection / request timeout | `TransportError` / `RequestTimeoutError` (subclass). |
| Malformed expected response/pagination | `ProtocolError` |
| Failed job / polling deadline | `JobError` / `AddePyTimeoutError`; details in [Jobs](jobs.md). |

HTTP errors retain `status_code`, `request_id`, structured `errors`, and
`response`; messages omit response bodies. Test `error.response is not None`
because error Responses are falsy. Local argument validation may raise
`ValueError` or `TypeError`; configuration/file operations may raise filesystem
exceptions. Inspect structured fields rather than parsing error messages.

Implementation: [client.py](../addepy/client.py),
[base.py](../addepy/resources/base.py), [transport.py](../addepy/transport.py),
[exceptions.py](../addepy/exceptions.py).
