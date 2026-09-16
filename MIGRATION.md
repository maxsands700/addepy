# Migrating to AddePy 0.6

This is a self-contained migration guide for applications using AddePy 0.2–0.5.
Give the entire file to an LLM together with your application repository. Most
resource calls remain compatible; the required change is choosing an explicit
configuration source. Preserve existing business behavior while applying the
changes below.

## Instructions for a migration agent

1. Find every `AddePy` construction, client wrapper, dependency declaration,
   dotenv loader, environment setting, SDK exception handler, and mocked client.
   Include scripts, notebooks, tests, CI, and deployment configuration.
2. Determine where each entry point currently gets its configuration. Apply the
   matching configuration recipe below; do not guess a new environment or firm.
   Preserve application-level dotenv loading if other code depends on it.
3. Keep existing public resource methods and return-value handling unless this
   guide identifies a required change. Optional new helpers are not mandatory
   rewrites. Never turn a synchronous query into an export job automatically.
4. Preserve every query field and value: IDs and their types, dates, filters,
   grouping and column arguments, external IDs, sorting, unknown options, and
   output format. Preserve import dry-run/warning flags, notification settings,
   overwrite behavior, and all create/update/delete side effects.
5. Update error handling, polling, test doubles, and dependency files for the
   behavior changes below. Run the application's offline tests; add focused
   coverage for changed configuration and result handling. Do not submit live
   writes or rerun timed-out jobs as part of refactoring.
6. Report changed entry points, chosen configuration sources, checks run, and
   any unresolved application-specific assumptions. Do not invent credentials,
   queries, endpoint aliases, or new business behavior to fill a gap.

## Dependencies

Use Python 3.10+ and update the existing dependency declaration and lockfile to
AddePy 0.6. For example:

```bash
python -m pip install 'addepy>=0.6,<0.7'
```

pandas is no longer installed by the core SDK. Applications that use DataFrames
must retain their own pandas dependency or use `addepy[dataframe]>=0.6,<0.7`.
`requests` and `python-dotenv` remain core dependencies.

## Select the configuration source explicitly

Previously `AddePy()` called `load_dotenv()` and filled missing arguments from
process variables. Process variables generally took precedence over file values.
Even `AddePy(load_env=False)` still read process variables.

Now `AddePy(...)` reads only its arguments. `load_env` is removed, including the
old fourth positional argument. The first three positional arguments remain
`firm_name`, `firm_id`, and `api_key`; all additional options are keyword-only.

| Existing configuration intent | Replacement |
| --- | --- |
| All settings supplied explicitly | Keep `AddePy(firm_name=..., firm_id=..., api_key=...)`; remove `load_env`. |
| Process variables, including an existing application-managed dotenv loader | `AddePy.from_env(...)` |
| One credential file supplies all settings | `AddePy.from_dotenv("path/to/.env", ...)` |
| Consuming Git repository's root `.env` | `AddePy.from_dotenv(...)` with no path |
| Explicit arguments plus missing settings from a source | Pass the existing arguments as factory overrides. |
| File defaults plus process overrides | Preserve an explicit merge in application code, as shown below. |

Before:

```python
from addepy import AddePy

client = AddePy(load_env=False, firm_id="123")
```

After, retaining process variables and the firm override:

```python
from addepy import AddePy

client = AddePy.from_env(firm_id="123")
```

For a file-only application, create its credential file and load it directly:

```dotenv
ADDEPAR_FIRM_NAME=yourfirm
ADDEPAR_FIRM_ID=123
ADDEPAR_API_KEY=BASE64_ENCODED_KEY_ID_COLON_KEY_SECRET
ADDEPAR_ENVIRONMENT=production
```

```python
from addepy import AddePy

with AddePy.from_dotenv(".env") as client:
    user = client.admin.users.get_current_user()
```

File paths are relative to the working directory unless absolute. No-argument
`from_dotenv()` searches upward from the working directory for the nearest Git
root, including worktrees, and reads only that root's `.env`. It does not use a
nested `.env` or search beyond that root. Missing repositories/files raise
`FileNotFoundError`. An explicit file path works outside Git repositories.

Factories never merge file/process settings, interpolate `${VARIABLE}` values,
or mutate `os.environ`. If the application relies on the old merge, interpolation,
or environment mutation, keep that behavior explicitly in its startup code:

```python
from dotenv import load_dotenv
from addepy import AddePy

load_dotenv(".env", override=False)  # Use the application's existing file path.
client = AddePy.from_env()          # Existing process values retain precedence.
```

Do not replace an established dotenv path with implicit discovery. Do not remove
an existing loader used by other libraries. Factory overrides win, including
explicit `None` values; avoid passing `None` when you intend to inherit a source
value. Explicit empty credentials now fail instead of falling back to the source.

These are the supported factory variables; other client options are keywords:

| Variable | Client keyword |
| --- | --- |
| `ADDEPAR_FIRM_NAME` | `firm_name` |
| `ADDEPAR_FIRM_ID` | `firm_id` |
| `ADDEPAR_ENVIRONMENT` | `environment` |
| `ADDEPAR_BASE_URL` | `base_url` |
| `ADDEPAR_API_KEY` | `api_key` |
| `ADDEPAR_KEY_ID`, `ADDEPAR_KEY_SECRET` | `key_id`, `key_secret` |
| `ADDEPAR_ACCESS_TOKEN` | `access_token` |

`environment` defaults to `production`; supported values are `production`,
`sandbox`, and `development`. Generated URLs are respectively
`https://{firm}.addepar.com/api/v1`, `https://{firm}.sandbox.addepar.com/api/v1`,
and `https://{firm}.clientdev.addepar.com/api/v1`. An explicit `base_url` replaces
the generated URL and allows omitting `firm_name`; `firm_id` is still required.

## Preserve the authentication method

`api_key` / `ADDEPAR_API_KEY` still means the **base64-encoded `key_id:key_secret`
pair**, optionally prefixed with `Basic `. Keep existing encoded values unchanged;
do not encode them again or interpret them as OAuth bearer tokens.

Alternatively supply `key_id` and `key_secret` together; the SDK encodes them.
OAuth uses `access_token` / `ADDEPAR_ACCESS_TOKEN`, or a callable `token_provider`
returning a bearer token. `OAuthTokenProvider` is exported from `addepy` for
refresh-token workflows; introducing OAuth is not required for this migration.

Configure exactly one of: encoded API key, key pair, access token, token provider.
Conflicting methods or an incomplete key pair raise `ValueError`. A factory
authentication override replaces the entire source authentication group. For
example, `AddePy.from_env(key_id=..., key_secret=...)` replaces any source token or
API key; supplying only `key_id` does not inherit the source `key_secret`.

## Queries and jobs

Namespaces remain `client.portfolio`, `client.ownership`, and `client.admin`.
Existing CRUD, import, view, and argument-based query calls remain available.
Method return types have not been changed into a universal result wrapper.

| Existing call | Current call / migration action |
| --- | --- |
| `portfolio.jobs.execute_portfolio_query_job(query_dict)` | Supported unchanged; `execute_job(query_dict)` is the common name. |
| `portfolio.jobs.execute_portfolio_query(query_dict)` from older README examples | Now a supported alias of `execute_job`. |
| `portfolio.jobs.create_job(query_dict)` | Supported; additionally accepts raw parameters or JSON text. |
| `portfolio.jobs.create_query_job(...)` | Supported argument builder; still returns a job ID. |
| `portfolio.jobs.execute_view_job(...)` | Supported; `execute_portfolio_view(...)` is an alias. |
| `portfolio.transaction_jobs.execute_query_job(...)` | Supported argument builder. Do not pass a raw query dictionary as its first argument. |
| `portfolio.transaction_jobs.create_query_job(...)` | Supported argument builder; still returns a job ID. |
| `portfolio.transaction_jobs.create_view_job(...)` / `execute_view_job(...)` | Supported saved-view exports. |
| `portfolio.analysis.query(...)` | Supported synchronous argument builder; `query_raw(query)` accepts copied JSON. |
| `portfolio.transactions.query_transactions(...)` | Supported synchronous argument builder; `query_raw(query)` accepts copied JSON. |

Both job resources now share `create_job(query_dict)`, `execute_job(query_dict)`,
`get_job_status(job_id)`, `wait_for_job(job_id)`, `get_job_results(job_id)`,
`resume_job(job_id)`, `download_job_results(job_id, path)`, `iter_jobs`, `list_jobs`,
and `cancel_job`. Transaction aliases `execute_transaction_query` and
`execute_transaction_query_job` also execute raw query JSON.

Raw input can be a mapping or JSON object string containing either query
parameters directly or `{"data": {"attributes": { ...parameters... }}}`.
The SDK copies those parameters, preserving unknown fields and nested values;
it does not mutate the input. Pass query parameters, not a job submission
envelope containing `job_type` and `parameters`. A filename is not JSON input;
read it first. Keep existing argument builders when their behavior is desired:
they normalize some values, such as job portfolio-type casing and a transaction
builder's string portfolio ID into a list; raw methods preserve values as given.

For copied queries, the complete flow is:

```python
from pathlib import Path
from addepy import AddePy

portfolio_query = Path("portfolio-query.json").read_text(encoding="utf-8")
transaction_query = Path("transaction-query.json").read_text(encoding="utf-8")

with AddePy.from_dotenv(".env") as client:
    with client.portfolio.jobs.execute_job(portfolio_query, timeout=1200) as response:
        portfolio_result = response.json()
    with client.portfolio.transaction_jobs.execute_job(
        transaction_query, timeout=1200
    ) as response:
        transaction_result = response.json()
```

Before/after for a portfolio caller, using its existing `query_dict`:

```python
# Before; this method remains supported.
result = client.portfolio.jobs.execute_portfolio_query_job(query_dict).json()

# Optional common spelling, with identical return handling.
result = client.portfolio.jobs.execute_job(query_dict).json()
```

`execute_job`, `execute_*_job`, `resume_job`, and `get_job_results` return a
`requests.Response`: call `.json()` for JSON, `.text` for CSV/TSV, and `.content`
for XLSX. Synchronous `query`/`query_transactions`/`query_raw` methods already
return a dictionary; do not add `.json()` to them. Portfolio saved views support
JSON/CSV/TSV/XLSX and default to JSON. Transaction saved views support CSV/TSV/XLSX
and default to CSV; transaction query jobs return JSON.

Synchronous saved views retain their distinct return types:
`portfolio.analysis.get_view_results(...)` returns a dictionary for JSON and
bytes for CSV/TSV/XLSX; `portfolio.transactions.get_view_results(...)` returns
`requests.Response`. Preserve existing parsing; do not add `.json()` or `.content`
to a portfolio view result that is already a dictionary or bytes.

Retain existing result parsing. A portfolio JSON result has a tree under
`result["data"]["attributes"]["total"]`, with columns and nested children.
A transaction JSON query result has a list of records under `result["data"]`
and column metadata under `result["meta"]["columns"]`. Preserve any `included`
and other metadata the application uses. Neither result is automatically a
DataFrame. Ordinary resource helpers that return a resource object or list still
do so; do not blindly add or remove a `data` index across the application.

### Completion and resuming existing jobs

`get_job_status()` returns the server's dictionary without normalization.
`wait_for_job()` returns the successful status document **or completed portfolio
result**, not a response object and not a status string.

The live portfolio API can return a completed result from `GET /jobs/{id}` without
`data.attributes.status`, contrary to the online job documentation. The SDK
recognizes a result whose `data.attributes.total` contains a columns dictionary
or children list, excluding error/job envelopes. Explicit statuses take
precedence. Other missing/empty statuses raise `JobError`; transaction jobs still
require a status. Explicit failures such as `Error` stop polling; unknown nonempty
states keep polling until a known terminal state or timeout. Replace custom loops
using `.get("status", "Completed")` or
requiring a status on every portfolio response with `wait_for_job`/`resume_job`.
Do not reintroduce blanket “missing status means success” logic.

`resume_job` waits and downloads without creating a new job. The download still
occurs when the portfolio status endpoint itself returned the completed result.
To retain the job ID before waiting:

```python
from addepy import AddePy, AddePyTimeoutError

with AddePy.from_dotenv(".env") as client:
    jobs = client.portfolio.jobs  # Or client.portfolio.transaction_jobs.
    job_id = jobs.create_job(query_dict)  # Existing query; submit exactly once.
    try:
        with jobs.resume_job(job_id, timeout=1200) as response:
            result = response.json()
    except AddePyTimeoutError as error:
        print("Resume this existing job later:", error.job_id)
        raise
```

Use `resume_job(saved_job_id, timeout=1200)` on a later run; do not call
`execute_job` again merely because waiting timed out. A local timeout does not
cancel the remote job. `cancel_job` explicitly requests cancellation or archives
completed results. Preserve existing cancellation behavior.

Polling checks immediately, then waits `initial_wait` seconds, increasing by
`backoff_factor` up to `max_wait`. Defaults are 30, 1.5, 300, and a 1200-second
polling timeout. Intervals and timeout must be finite and positive; the backoff
factor must be finite and at least 1. The monotonic polling deadline includes
SDK-managed requests, retries, and OAuth refresh during polling. It does not cover
initial submission or the subsequent download. `AddePyTimeoutError.last_status`
is diagnostic text and may contain a serialized document; do not parse it as a
status enum or log it as guaranteed sanitized output.

`batch=True` is optional for portfolio jobs and is not enabled by migration.
Keep the default unless the application's views and attributes support batched
computation. Raw transaction `sorting`/`sortings` spelling is preserved; do not
rename fields based solely on inconsistent online examples.

## Errors, retries, and transport

Existing HTTP exception classes and `AddePyError` catches still work. Update
handlers that previously expected underlying Requests exceptions or parsed
exception text:

| Situation | Current behavior |
| --- | --- |
| Connection failure | `TransportError`, with the original exception in `__cause__`. |
| Request timeout | `RequestTimeoutError`, a subclass of `TransportError`. |
| Polling deadline | `AddePyTimeoutError` with `job_id` and diagnostic `last_status`. |
| Failed/canceled export job or invalid status document | `JobError` with `job_id`, `status`, `errors`, and `job_data` when available. |
| Malformed pagination / missing historical-price async ID | `ProtocolError`. |
| HTTP error | Existing typed exception with `status_code`, `request_id`, `errors`, and `response` when available. |

All these SDK exceptions inherit `AddePyError`; configuration/argument mistakes
can instead raise `ValueError`, `TypeError`, or `FileNotFoundError`. Replace
`except requests.Timeout` around SDK calls with `except RequestTimeoutError`, and
`except requests.RequestException` with appropriate SDK exceptions. Keep Requests
handlers for direct Requests calls. HTTP exception messages no longer include
response bodies; use structured fields instead of string parsing. Test response
presence with `error.response is not None` (error HTTP responses are falsy).

The HTTP timeout defaults to `(10, 60)` seconds for connect/read. Set
`timeout=(connect_seconds, read_seconds)` on the constructor/factory, or override
it on `client.request`. This is separate from the polling timeout above.

GET/HEAD/OPTIONS retry connection failures and HTTP 429/500/502/503/504 up to twice
by default. `max_retries=0` preserves one-attempt behavior, which is useful when
the application already owns retries. `max_retry_wait` defaults to 60 seconds;
longer server retry delays are surfaced as errors rather than slept through.
Writes do not retry by default. Do not add write retries during migration;
`client.request(..., retry=True)` requires replay-safe application semantics, and
file/stream uploads cannot be replayed automatically.

Replace direct `_session` calls with public
`client.request(method, endpoint, json=..., params=..., headers=...)` so SDK
authentication, timeout, retry, and error handling apply. Pass `session=` for
connection customization or test doubles, and `base_url=` instead of assigning
private attributes. `_request` remains a compatibility alias. Explicit API URLs
must use HTTPS on the configured origin; pagination cannot send credentials to
another host. Cross-host download redirects use a separate credential-free session.
Injected sessions remain caller-owned, including `download_session`; context
managers close sessions created by the SDK.

## Imports, collections, and downloads

- `admin.import_tool.create_import` and `execute_import` retain the
  `import_dataframe=` argument, even when the value is CSV text/bytes, `Path`, or
  a readable file. Existing DataFrames still work with pandas installed. Use
  `Path("transactions.csv")` for a filename: a plain string is CSV content.
  `create_import` returns an ID; `execute_import` returns a dictionary containing
  `digests`, `warnings`, and `errors`. Preserve `is_dry_run` (default `True`) and
  `ignore_warnings` (default `False`) exactly.
- Transaction bulk creation and benchmark bulk updates no longer remove keys
  from caller dictionaries. Remove reliance on that mutation; do not change the
  submitted payloads. Historical-price submissions missing a job ID now raise
  `ProtocolError` instead of returning `None`.
- Existing `iter_*`/`list_*` collection methods remain. Older releases fetched all
  pages for calls such as `list_entities()` and `list_jobs()`; many current
  `list_*` helpers cap results at 10,000 by default. `page_limit` controls page
  size, not this total cap. Where the application needs a complete collection,
  use `list(resource.iter_*(...))`, preserving all filters, for example
  `list(client.ownership.entities.iter_entities())`. Retain intentional explicit
  total limits. Zero item limits make no request;
  negative limits, malformed collections, and repeated pagination coordinates
  raise errors instead of silently truncating or looping.
- `client.iter_pages(endpoint, params=...)` yields full JSON:API page dictionaries
  including `data`, `included`, `links`, and `meta`; it is distinct from resource
  iterators yielding individual resource objects. Preserve that distinction in
  wrappers and mocks.
- Existing byte/response downloads remain supported. Optional
  `download_job_results(job_id, path)`, `files.download_file_to`,
  `files.download_archived_file_to`, and `reports.download_zipped_file_to` stream
  to atomic files and return `Path`. The parent directory must already exist.
  They refuse existing destinations by default; do not substitute them for
  overwriting code without preserving its intended behavior. File/report `_to`
  helpers and `client.download` accept `overwrite=True`; `download_job_results`
  does not. With `get_job_results(stream=True)`, the caller must read and close
  the response.

New resources are additive; they do not require rewriting existing CRUD calls.
For code specifically changing an entity's model type, use
`ownership.entities.change_model_type(entity_id, new_model_type)` or
`change_model_types([{"id": ..., "new_model_type": ...}])`, not an ordinary
attribute update. `get_entity_type(...)["attributes"]["entity_attributes"]` is
an array, despite older docstrings describing a dictionary. New billing
`replace_*` methods use PUT with complete desired attributes/relationships;
do not substitute them for partial PATCH updates.

## Completion checklist

- Every client has an intentional source, firm, environment, and exactly one
  authentication method. No `load_env` arguments or unintended source merges
  remain. Secrets and real query/results files are not committed.
- Existing public calls still use the correct argument and return shapes.
  Portfolio completion works with both a status document and a completed result;
  malformed responses and explicit job errors remain failures.
- Queries, imports, output formats, write side effects, retry policy, and file
  overwrite behavior are preserved. Timed-out jobs retain their IDs for resuming.
- Dependency/lockfiles and mocks reflect optional pandas, explicit factories,
  immediate polling, and SDK exceptions. Offline application tests pass.
