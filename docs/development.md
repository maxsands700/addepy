# Development

## Local checks

From the repository root, using Python 3.10+:

```bash
python -m venv .venv
```

Activate with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\Activate.ps1` in Windows PowerShell, then:

```bash
python -m pip install -e '.[dev,dataframe]'
python -m pytest
ruff check addepy tests
python -m build
```

Tests block network access and clear inherited Addepar settings. CI runs tests, lint, and packaging on Python 3.10–3.14. To capture coverage or machine-readable results:

```bash
python -m pytest --cov=addepy --cov-report=html:test-results/coverage --junitxml=test-results/offline.xml
```

## Live diagnostics

From a computer with Addepar API access, configure a private credential file as described in [configuration](configuration.md). For sandbox, copy [`.env.example`](../.env.example) to `.env.sandbox`, set `ADDEPAR_ENVIRONMENT=sandbox`, and enter that environment's credentials.

```bash
python -m addepy.diagnostics --env-file .env.sandbox --read-only
```

This checks the current user, entities, and portfolio views. To verify both query flows, save small working queries under the ignored `live-queries/` directory:

```bash
python -m addepy.diagnostics --env-file .env.sandbox --portfolio-query live-queries/portfolio.json --transaction-query live-queries/transactions.json --job-timeout 1200
```

Queries create temporary exports. Diagnostics permit reads and those export submissions, with no business-data writes. They download and validate the results, then discard the contents. `--read-only` disables submissions but permits checking existing jobs:

```bash
python -m addepy.diagnostics --env-file .env.sandbox --read-only --only portfolio_job --portfolio-job-id YOUR_JOB_ID --job-timeout 1200
```

For transactions, use `--only transaction_job --transaction-job-id YOUR_JOB_ID`. Resume the existing ID after a timeout instead of submitting again. See [portfolio completion behavior](jobs.md#portfolio-completion-behavior) for the live response without a status field.

For production, use a file with production settings and pass both `--env-file .env.production --production`. Custom API hosts also require `--production`; there is no fallback between environments. The credential file must be explicit, and ambient credentials are ignored.

Useful options:

| Option | Purpose |
| --- | --- |
| `--list-checks` | List available checks without making requests. |
| `--extended --entity-id YOUR_ENTITY_ID` | Include additional read endpoints; estimated returns need the entity filter. |
| `--only entities,report_schedules` | Select checks by name. |
| `--job-timeout 1200` | Polling deadline per job; default is 120 seconds. |
| `--poll-interval 5` | Seconds between polls; default is 5. |
| `--request-timeout 30` | Request timeout; default is 30 seconds. |
| `--max-result-bytes 10485760` | Download inspection limit; default is 10 MiB. |
| `--report-dir test-results/live` | Report directory; shown here with its default. |

## Reports

Each run writes timestamped JSON and Markdown reports. They contain outcomes, HTTP codes, durations, and job IDs/status/progress; they omit credentials, query values, and response data. Status remains `null` until captured or inferred from a valid completed portfolio result; missing progress remains `null`. A `Completed` job can still fail result validation.

| Outcome | Next step |
| --- | --- |
| `pass` | The selected check succeeded. |
| `contract_failure`, `internal_error` | Inspect the query and SDK behavior. |
| `auth_blocked`, `permission_blocked` | Check credentials or access. |
| `unavailable`, `network_error` | Check the resource ID, expiry, endpoint, or connection. |
| `rate_limited` | Retry after the server's rate limit clears. |
| `missing_input`, `skipped`, `incomplete` | Supply inputs, adjust limits, or resume the job. |
| `policy_blocked`, `config_error` | Correct the runner's configuration. |

Exit codes are `0` for all selected checks passed, `1` for contract/internal failures, and `2` for configuration or inconclusive checks. Authentication failures and rate limits stop further checks. Reports and queries are Git-ignored. When reporting an issue, include the reports, `git rev-parse HEAD`, Python version, and operating system.
