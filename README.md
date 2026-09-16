# AddePy

Unofficial Python SDK for the [Addepar API](https://developers.addepar.com/docs/welcome). Python 3.10+.

AddePy provides resource wrappers, raw portfolio/transaction queries, resumable export jobs, pagination, and streaming downloads. Version 0.6 adds billing, payout, report schedule, estimated return, derivative underlying asset, and model-type operations. See the [API coverage and verification notes](docs/API_COVERAGE.md).

**Install**

```bash
pip install addepy
# Optional pandas support:
pip install 'addepy[dataframe]'
```

For this checkout, including the test suite:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
python -m pytest
```

The pytest suite runs entirely offline and blocks network connections. To verify a firm from your work computer, follow [TESTING.md](TESTING.md). No live Addepar compatibility is claimed from mocked tests alone.

**Configure a client**

Choose the configuration source explicitly:

- `AddePy(...)` uses only the settings passed to its constructor.
- `AddePy.from_env(...)` reads the process's `ADDEPAR_*` environment variables.
- `AddePy.from_dotenv(...)` reads one `.env` file.

For a local project, copy [.env.example](.env.example) to a private `.env` at your consuming Git repository's root and fill in your credentials. This repository ignores `.env`; add it to your application's `.gitignore` too.

```python
from addepy import AddePy

with AddePy.from_dotenv() as client:
    entities = client.ownership.entities.list_entities(limit=10)
```

With no path, `from_dotenv()` starts at the current working directory and finds the nearest ancestor containing a `.git` directory or file, including worktrees. It reads only that repository's root `.env`. A missing repository or root file raises an error; nested `.env` files and files above the repository are not searched. Use `AddePy.from_dotenv(".env.sandbox")` for another file; explicit relative paths resolve from the current working directory, and relative or absolute paths also work outside Git repositories.

Both factories accept keyword overrides. They do not merge file settings with process variables, interpolate values, or modify the process environment. An explicit authentication option replaces all authentication loaded from the source; overriding a key pair requires both `key_id` and `key_secret`.

`ADDEPAR_API_KEY` is the existing **base64-encoded `key_id:key_secret` pair**, optionally prefixed with `Basic `. OAuth uses `ADDEPAR_ACCESS_TOKEN` instead. The detailed [authentication guide](https://developers.addepar.com/docs/basic-authentication) documents both mechanisms.

The factories also recognize `ADDEPAR_KEY_ID`/`ADDEPAR_KEY_SECRET`, `ADDEPAR_FIRM_NAME`, `ADDEPAR_FIRM_ID`, `ADDEPAR_ENVIRONMENT`, and `ADDEPAR_BASE_URL`. The environment defaults to `production` when omitted; the example file selects `sandbox`.

For explicit configuration:

```python
client = AddePy(
    firm_name="yourfirm",
    firm_id="12345",
    key_id="your-key-id",
    key_secret="your-key-secret",
    environment="sandbox",  # production, development, or sandbox
)
```

Use `base_url="https://yourfirm.sandbox.addepar.com/api/v1"` for an explicit API base. The constructor has no file or environment fallback, and `load_env` has been removed. A custom `requests.Session` can be supplied as `session=`; the caller owns its lifecycle.

**Run copied raw queries**

Copy the query JSON from Addepar into a private file. Both job resources accept JSON strings or dictionaries, either direct query parameters or the exported `{"data": {"attributes": {...}}}` envelope. Query fields and values pass through unchanged; the SDK creates the job envelope and never modifies your input.

```python
from pathlib import Path
from addepy import AddePy

with AddePy.from_dotenv() as client:
    portfolio = Path("live-queries/portfolio.json").read_text(encoding="utf-8")
    transactions = Path("live-queries/transactions.json").read_text(encoding="utf-8")

    portfolio_result = client.portfolio.jobs.execute_job(portfolio).json()
    transaction_result = client.portfolio.transaction_jobs.execute_job(transactions).json()
```

Argument helpers (`create_query_job`, `create_view_job`) remain available. `execute_portfolio_query` and `execute_portfolio_query_job` are aliases for portfolio `execute_job`. Transaction `execute_query_job` remains the argument helper; transaction `execute_job` accepts a raw query.

For long-running jobs, keep the ID and download to a file:

```python
with AddePy.from_dotenv() as client:
    query = Path("live-queries/portfolio.json").read_text(encoding="utf-8")
    job_id = client.portfolio.jobs.create_job(query)
    client.portfolio.jobs.wait_for_job(job_id, timeout=1200)
    client.portfolio.jobs.download_job_results(job_id, "portfolio.json")

# After a local timeout or process restart, reuse the saved ID:
with AddePy.from_dotenv() as client:
    response = client.portfolio.jobs.resume_job(job_id)
```

The same methods exist on `transaction_jobs`. Local timeouts leave server jobs running. `JobError` carries `job_id`, `status`, `errors`, and `job_data`; `AddePyTimeoutError` carries `job_id` and `last_status`. Downloads stream to an atomic file and preserve existing files. Addepar [job results expire after 24 hours](https://developers.addepar.com/docs/jobs).

Portfolio jobs also accept `batch=True`, an explicit opt-in to [Addepar's beta batched computation](https://developers.addepar.com/docs/batched-jobs). Attribute and view restrictions apply; see [API notes](docs/API_COVERAGE.md) for the documented job-type ambiguity.

**Navigate resources and results**

| Namespace | Examples |
| --- | --- |
| `client.portfolio` | `analysis`, `jobs`, `transaction_jobs`, `transactions`, `snapshots`, `benchmarks`, `historical_prices`, `estimated_returns`, `underlying_assets` |
| `client.ownership` | `entities`, `groups`, `positions`, `external_ids` |
| `client.admin` | `users`, `roles`, `teams`, `contacts`, `files`, `reports`, `report_schedules`, `import_tool`, `fees`, `fee_schedules`, `billable_portfolios`, `payout_recipients`, `payout_rules` |

Most singular resource methods return a resource dictionary; list methods return lists. Job downloads return `requests.Response`, and streamed download helpers return `Path`. Method docstrings describe endpoint-specific exceptions to these conventions.

```python
for entity in client.ownership.entities.iter_entities():
    process(entity)

# Preserve included resources, links, and metadata:
for page in client.iter_pages("/entities", page_limit=100):
    process_page(page)

# Raw endpoint access for new fields or APIs:
response = client.request("GET", "/entities", params={"page[limit]": 1})
```

`list_*` methods generally cap results at 10,000; `iter_*` methods can traverse all pages lazily. Prefer explicit limits for exploratory calls.

**Import CSV or a DataFrame**

```python
from pathlib import Path

result = client.admin.import_tool.execute_import(
    Path("attributes.csv"), "ATTRIBUTES", is_dry_run=True,
)
print(result["digests"], result["warnings"], result["errors"])
```

Imports accept CSV text, bytes, a `Path`, a readable file, or a pandas DataFrame. A string means CSV contents, so use `Path` for filenames. Dry runs and warning review are the defaults; committing an import requires `is_dry_run=False`. Import operations are excluded from the live verification suite.

**OAuth refresh and request policy**

```python
from addepy import AddePy, OAuthTokenProvider

with OAuthTokenProvider(
    token_url="https://api.addepar.com/public/oauth2/token",
    client_id="your-client-id",
    client_secret="your-client-secret",
    refresh_token="your-refresh-token",
    on_token_update=save_tokens_to_your_secret_store,
) as tokens:
    with AddePy(firm_name="yourfirm", firm_id="12345", token_provider=tokens) as client:
        entities = client.ownership.entities.list_entities(limit=10)
```

Register and authorize the OAuth application separately. The provider uses returned `expires_in` values and can persist rotated refresh tokens through the callback. Use the appropriate [OAuth token URL for your environment](https://developers.addepar.com/docs/oauth).

Requests use connection/read timeouts and up to two retries for transient **read** failures. Writes are not retried automatically. Addepar's retry delay is respected; delays beyond `max_retry_wait` raise the original error instead of retrying early. `max_retries=0` disables retries. `retry=True` on a raw write is an explicit caller decision and cannot replay streaming bodies.

Polling deadlines also constrain built-in OAuth refresh, request timeouts, and retry sleeps. Arbitrary token-provider callbacks manage their own blocking behavior; streaming read timeouts are inactivity limits, not a total transfer deadline. Cross-host download redirects do not carry API credentials, firm headers, cookies, or client certificates.

Exceptions retain `status_code`, `request_id`, `errors`, and `response` where available. Exception messages omit raw response bodies. See [MIGRATION.md](MIGRATION.md) for behavior changes and [TESTING.md](TESTING.md) for verification.
