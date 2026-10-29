# Export jobs

Use `client.portfolio.jobs` for portfolios;
`client.portfolio.transaction_jobs` for transactions. Tables use `J` for
`/jobs` or `/transaction_jobs`. Paths follow the versioned API base URL.

## Raw queries

`create_job(query_dict)` and `execute_job(query_dict)` accept parameter mappings,
JSON object text, or exported `data.attributes` envelopes. The SDK copies query
fields and values without rewriting unknown options or external IDs. Pass query
parameters, not an outer `job_type` / `parameters` object; the SDK builds that
submission envelope.

```python
from pathlib import Path
from addepy import AddePy

query = Path("portfolio-query.json").read_text(encoding="utf-8")
with AddePy.from_dotenv(".env") as client:
    with client.portfolio.jobs.execute_job(query) as response:
        result = response.json()
```

Portfolio columns are objects such as `{"key": "value"}`; transaction columns
are strings such as `"trade_date"`. Reuse known working exported queries.
Portfolio JSON contains `data.attributes.total`; transaction JSON contains
record list `data` and `meta.columns`.

## Shared methods and endpoints

| Method | HTTP operation | Returns |
| --- | --- | --- |
| `create_job(query_dict)` | POST `J` | Job ID string |
| `execute_job(query_dict, ...)` | Create, wait, download | `requests.Response` |
| `get_job_status(job_id)` | GET `J/{job_id}` | Original document |
| `wait_for_job(job_id, ...)` | Poll GET `J/{job_id}` | Successful status or completed portfolio result document |
| `get_job_results(job_id, stream=False)` | GET `J/{job_id}/download` | `requests.Response` |
| `download_job_results(job_id, path)` | Stream GET `J/{job_id}/download` | `Path`; call after waiting |
| `resume_job(job_id, ...)` | Wait, download; no submission | `requests.Response` |
| `list_jobs(limit=10000, page_limit=500)` | GET `J` | List of job resources |
| `iter_jobs(limit=None, page_limit=500)` | Paginated GET `J` | Resource iterator |
| `get_job_creator(job_id)` | GET `J/{job_id}/creator` | User resource |
| `get_job_creator_relationship(job_id)` | GET `J/{job_id}/relationships/creator` | User identifier |
| `cancel_job(job_id)` | DELETE `J/{job_id}` | `None`; cancels or archives completed results |

Responses: `.json()` for JSON, `.text` for CSV/TSV, `.content` for XLSX. Close
streamed responses. Disk downloads require an existing parent directory,
preserve existing files, and leave no partial destination. Job results expire
24 hours after creation.

## Portfolio builders and aliases

Prefix: `client.portfolio.jobs`. All submissions POST `/jobs`.

| Method | Arguments / behavior |
| --- | --- |
| `create_job(query_dict, *, batch=False, job_type=None)` | Raw query; default job type `PORTFOLIO_QUERY` |
| `create_query_job(portfolio_type, portfolio_id, start_date, end_date, columns, groupings, *, filters=None, hide_previous_holdings=False, batch=False)` | Argument builder; returns ID |
| `create_view_job(view_id, portfolio_type, portfolio_id, start_date, end_date, output_type="JSON", *, batch=False)` | Saved-view job; returns ID |
| `execute_job(query_dict, *, batch=False, job_type=None, ...)` | Raw query; returns response |
| `execute_view_job(view_id, portfolio_type, portfolio_id, start_date, end_date, output_type="JSON", *, batch=False, ...)` | Saved view; returns response |
| `execute_portfolio_query_job`, `execute_portfolio_query` | Aliases of raw `execute_job`; neither is an argument builder |
| `execute_portfolio_view` | Alias of `execute_view_job` |

Portfolio job column/grouping entries are dictionaries. The query builder
requires a portfolio ID; use raw queries for external-ID scopes. View formats:
JSON/CSV/TSV/XLSX. View job type is `portfolio_view_results`; builder portfolio
types and view output types are lowercased. Raw query casing is preserved.
`batch=True` adds only `Addepar-Compute-Type: BATCH`; compatible views/attributes
are required. Batch mode is opt-in. No `execute_query_job` method exists here.

## Transaction builders and aliases

Prefix: `client.portfolio.transaction_jobs`. All submissions POST
`/transaction_jobs`; query job type is `transaction_query`, view job type
`transaction_view_results`.

| Method | Arguments / behavior |
| --- | --- |
| `create_query_job(columns, portfolio_type, portfolio_id=None, start_date=None, end_date=None, ...)` | Argument builder; returns ID |
| `execute_query_job(columns, portfolio_type, portfolio_id=None, start_date=None, end_date=None, ...)` | Argument builder; returns response |
| `create_view_job(view_id, portfolio_id, portfolio_type, start_date, end_date, output_type="CSV")` | Saved view; returns ID |
| `execute_view_job(view_id, portfolio_id, portfolio_type, start_date, end_date, output_type="CSV", ...)` | Saved view; returns response |
| `execute_transaction_query`, `execute_transaction_query_job` | Aliases of raw `execute_job`; do not pass builder arguments |

Query builders require both dates and one scope: `portfolio_id` or
`external_ids=[{"external_type_key": "crm", "external_id": "client-1"}]`.
An empty `portfolio_id=[]` placeholder is accepted with external IDs. Optional
query keywords: `filters=None`, `sorting=None`, `limit=None`, `external_ids=None`,
`include_online_valuations=False`, `include_unverified=False`,
`include_deleted=False`. Columns are strings. Builders lowercase
`portfolio_type` and emit `sorting`; raw queries preserve either `sorting` or
`sortings`. View formats are CSV/TSV/XLSX; query jobs return JSON.

## Waiting, failures, and resumption

Wait/resume/execute methods accept keyword-only polling options:
`initial_wait=30`, `max_wait=300`, `backoff_factor=1.5`, `timeout=1200` seconds.
The first check is immediate; subsequent checks use capped exponential backoff.
The timeout bounds polling requests, retries, and OAuth refresh, excluding
initial submission and final download.

```python
from addepy import AddePyTimeoutError

jobs = client.portfolio.jobs
job_id = jobs.create_job(query)  # Save this ID before waiting.
try:
    with jobs.resume_job(job_id, timeout=1200) as response:
        result = response.json()
except AddePyTimeoutError:
    print(job_id)  # Resume this ID later; do not submit again.
```

A local timeout does not cancel the server job. `AddePyTimeoutError` provides
`job_id` and diagnostic `last_status`; `JobError` provides `job_id`, `status`,
`errors`, and `job_data`. Explicit failed/canceled states stop polling; unknown
nonempty states continue until completion, failure, or timeout.

Portfolio status GETs may return completed results without a status field.
The SDK recognizes a non-job result with `data.attributes.total.columns` as a
dictionary or `.children` as a list. Missing status alone is insufficient;
malformed/error documents fail, and explicit statuses take precedence.
Transaction jobs require a status. Wait returns the original document;
execute/resume still download and return a response even if status GET already
contained the completed portfolio result. Preserve this working behavior.
