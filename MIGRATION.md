# Migrating to AddePy 0.6

Existing namespaces and public job helpers remain available. The release adds capabilities and tightens incorrect behavior; no wholesale client rewrite is needed in calling applications.

| Area | Action or behavior change |
| --- | --- |
| pandas | Install `addepy[dataframe]` if your application uses pandas. Core CSV/file imports work without it. |
| Raw transaction jobs | Use `client.portfolio.transaction_jobs.execute_job(raw_query)` or `create_job(raw_query)`. Existing argument-based `execute_query_job(...)` remains available. |
| Portfolio method names | `execute_job`, `execute_portfolio_query`, and `execute_portfolio_query_job` are supported aliases. The former README's missing method now exists. |
| Job failures | Missing status raises `JobError`; it no longer defaults to success. Documented `Error` states now terminate polling. Catch `JobError` for structured server failure details. |
| Polling | Status is checked immediately. Waiting uses a monotonic deadline, including SDK-managed requests/retries and OAuth refresh. Invalid/zero polling intervals and timeouts raise `ValueError`. Local timeouts do not cancel remote jobs. |
| Network failures | Requests connection/timeout failures become `TransportError`/`RequestTimeoutError`, with the original exception as their cause. |
| HTTP errors | `status_code` is populated for failures. Exception text omits the response body; use `.errors` or `.response` explicitly when diagnosing locally. |
| Retries | GET/HEAD/OPTIONS retry transient failures up to twice by default. Set `max_retries=0` for former one-attempt behavior. Writes still require explicit opt-in to retry. |
| Pagination | Next links/cursors are followed according to endpoint behavior. Zero item limits make no request; malformed pages and repeated cursors raise rather than silently truncate or loop. |
| Historical prices | A submission missing its documented async job ID raises `ProtocolError`; previously it could return `None`. |
| Bulk payloads | Transaction and benchmark helpers no longer remove fields from caller dictionaries. |
| Imports | Existing `import_dataframe=` arguments still work. They also accept CSV text/bytes, `Path`, and readable files. Use `Path("file.csv")` for a filename; plain strings are CSV contents. |
| Sessions and URLs | Use public `client.request()` instead of reaching into `_session`. Injected sessions remain caller-owned. Explicit URLs must use HTTPS; pagination cannot redirect the initial API request to another host. |
| Streaming downloads | New `*_to` and `download_job_results` methods write atomically and refuse existing destinations. Old response/byte-returning methods remain available. |

`ADDEPAR_API_KEY` still means Basic credentials. Use `access_token=`/`ADDEPAR_ACCESS_TOKEN` or `OAuthTokenProvider` for OAuth. Do not reinterpret an existing API key as a bearer token based on the welcome page; see the [detailed authentication guide](https://developers.addepar.com/docs/basic-authentication).

New billing replacement methods are explicitly named `replace_*` because the API uses PUT. Provide the full desired attributes/relationships; this is different from a partial PATCH. Method docstrings and [API notes](docs/API_COVERAGE.md) describe resource-specific payloads and return values.
