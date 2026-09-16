# Query jobs

Portfolio and transaction resources share the same workflow:

| Method | Result |
| --- | --- |
| `create_job(query)` | Submits once and returns a job ID string. |
| `get_job_status(job_id)` | Original JSON document from the status endpoint. |
| `wait_for_job(job_id)` | Waits and returns the successful status or completed portfolio result document. |
| `get_job_results(job_id)` | Downloads results as a `requests.Response`. |
| `resume_job(job_id)` | Waits, then downloads as a `requests.Response`; no new submission. |
| `execute_job(query)` | Creates, waits, and downloads as a `requests.Response`. |
| `download_job_results(job_id, path)` | Streams results to a new file and returns its `Path`; call after waiting. |

Use `client.portfolio.jobs` for portfolios and `client.portfolio.transaction_jobs` for transactions. The [README](../README.md) shows both complete examples.

## Query inputs

Pass a dictionary or JSON text with either direct query parameters or Addepar's exported `data.attributes` envelope:

```python
query = {
    "data": {
        "attributes": {
            "portfolio_type": "entity",
            "portfolio_id": [12345],
            "start_date": "2026-01-01",
            "end_date": "2026-03-31",
            "columns": [{"key": "value"}],
            "groupings": [],
        }
    }
}
```

Use a portfolio you can access. Transaction query columns are strings such as `"trade_date"` and `"value"`. Copying a working query from Addepar is the simplest way to retain its options.

The SDK preserves raw fields and values and constructs the job submission envelope. Do not wrap the query in `job_type` / `parameters`. Argument-based `create_query_job(...)` helpers remain available; transaction `execute_query_job(...)` is also an argument helper, not a raw-query method.

## Long-running jobs and file downloads

Keep the ID so a later process can resume the same job:

```python
from pathlib import Path
from addepy import AddePy, AddePyTimeoutError

query = Path("portfolio-query.json").read_text(encoding="utf-8")

with AddePy.from_dotenv(".env") as client:
    jobs = client.portfolio.jobs
    job_id = jobs.create_job(query)
    print("Save this job ID:", job_id)
    try:
        jobs.wait_for_job(job_id, timeout=1200)
    except AddePyTimeoutError:
        print("Still waiting; resume this ID later:", job_id)
    else:
        jobs.download_job_results(job_id, "portfolio-result.json")
```

Resume with `client.portfolio.jobs.resume_job(saved_job_id, timeout=1200).json()`, or wait again and then call `download_job_results` for a streamed file. Transaction jobs use the same methods. Output directories must exist; file helpers preserve existing files and never leave partial output at the destination.

`JobError` exposes `job_id`, `status`, `errors`, and `job_data`. `AddePyTimeoutError` exposes `job_id` and `last_status`; a local timeout does not cancel the remote job. Retrieve results before they expire. `cancel_job(job_id)` is an explicit cancellation/archive operation.

Polling checks immediately, then uses `initial_wait=30`, `max_wait=300`, `backoff_factor=1.5`, and `timeout=1200` seconds by default. Pass these keyword arguments to wait/resume/execute helpers to change them. The wait timeout applies to polling; it is not a total deadline for submission and downloading.

## Portfolio completion behavior

The live API can return portfolio results (`meta`, `data`, `included`, and `data.attributes.total` with columns/children) directly from `GET /jobs/{id}` without a status field. This differs from the online job-status documentation. The SDK recognizes that result structure as completion; an absent status alone is insufficient. Explicit statuses take precedence. Transaction jobs still require a status.

`get_job_status` and `wait_for_job` preserve the returned document. Execute/resume helpers still download the result, so callers continue receiving a `requests.Response`. Use `.json()` for JSON, `.text` for CSV/TSV, and `.content` for binary exports.

## Saved views and batch computation

`create_view_job(...)` submits a saved-view export; `execute_view_job(...)` also waits and downloads. Portfolio views support JSON, CSV, TSV, and XLSX; transaction views support CSV, TSV, and XLSX. Method docstrings list their arguments.

Portfolio query and view helpers accept `batch=True` to opt into beta batch computation, which has view and attribute restrictions. Raw portfolio `create_job` / `execute_job` also accept `job_type=` for a firm-specific override; the default is `PORTFOLIO_QUERY`. The SDK does not rewrite copied query options or enable batch mode automatically.
