# Development and diagnostics

## Offline checks

Python 3.10+; CI covers 3.10–3.14. From the repository root:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[dev,dataframe]'
.venv/bin/python -m pytest
.venv/bin/ruff check addepy tests
.venv/bin/python -m build
```

On Windows use `.venv\Scripts\python` and `.venv\Scripts\ruff`.
Tests block network access and clear inherited Addepar variables. Optional reports:

```bash
.venv/bin/python -m pytest --cov=addepy --cov-report=html:test-results/coverage --junitxml=test-results/offline.xml
```

## Live diagnostics

Run explicitly from a host with API access. Credentials come from the named
file; ambient credentials are ignored. Configure the environment in that file.

```bash
python -m addepy.diagnostics --list-checks
python -m addepy.diagnostics --env-file .env.sandbox --read-only
python -m addepy.diagnostics --env-file .env.sandbox --portfolio-query live-queries/portfolio.json --transaction-query live-queries/transactions.json
```

Default checks: current user, entities, portfolio views. Query files submit
exports, validate downloaded results, then discard content. `--read-only`
disables submissions and permits inspection of existing jobs:

```bash
python -m addepy.diagnostics --env-file .env.sandbox --read-only --only portfolio_job --portfolio-job-id YOUR_JOB_ID --job-timeout 1200
```

Transaction equivalent: `--only transaction_job --transaction-job-id YOUR_JOB_ID`.
Resume an existing ID after a timeout. Production/custom hosts require
`--production`; no automatic environment fallback occurs.

| Options | Meaning/default |
| --- | --- |
| `--extended --entity-id ID` | Additional resource reads; entity filter required for proxies/estimated returns. |
| `--only entities,report_schedules` | Select checks; repeatable. |
| `--environment`, `--base-url` | Explicit configuration overrides. |
| `--portfolio-query`, `--transaction-query` | Raw JSON file; mutually exclusive with the corresponding `--*-job-id`. |
| `--job-timeout`, `--poll-interval`, `--request-timeout` | 120 / 5 / 30 seconds. |
| `--max-result-bytes` | Download inspection cap; 10485760 bytes. |
| `--report-dir` | `test-results/live`; timestamped JSON and Markdown. |

Reports include outcomes, HTTP codes, durations, job IDs/status/progress; omit
credentials, query values, and response content. Missing status/progress remains
null unless a valid completed portfolio result establishes completion. Exit codes:
`0` all passed; `1` contract/internal failure; `2` configuration/inconclusive.
Authentication failures and rate limits stop further checks. See
[Jobs](jobs.md) for portfolio completion behavior.

Implementation: [diagnostics.py](../addepy/diagnostics.py),
[offline contracts](../tests/contracts/), [CI](../.github/workflows/tests.yml).
