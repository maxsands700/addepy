# Testing AddePy

Run the offline suite on any computer. Run live compatibility checks only from a computer with authorized Addepar access. Live checks exercise public SDK methods; they do not create, edit, or delete business data. Portfolio and transaction query jobs are permitted by default when you supply query files, because they create temporary exports rather than changing portfolio data.

**1. Set up this checkout on the work computer**

Copy the source checkout or the provided source archive to the work computer; no Git push is needed. Use Python 3.10 or later:

```bash
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\Activate.ps1` in Windows PowerShell. If activation is restricted, run `.venv\Scripts\python.exe` directly in the commands below.

```bash
python -m pip install -e '.[dev]'
python -m pytest --junitxml=test-results/offline.xml
```

This suite blocks network connections and clears inherited Addepar settings. It tests SDK behavior and documented request/response contracts using synthetic data, including writes. It never loads your real credentials or calls Addepar. Optional DataFrame integration tests run after `python -m pip install '.[dataframe]'`; without pandas, that test is explicitly skipped.

For coverage and static checks:

```bash
python -m pytest --cov=addepy --cov-report=html:test-results/coverage
ruff check addepy tests
```

**2. Configure sandbox access**

Copy `.env.example` to `.env.sandbox` and replace the placeholders:

```dotenv
ADDEPAR_ENVIRONMENT=sandbox
ADDEPAR_FIRM_NAME=yourfirm
ADDEPAR_FIRM_ID=12345
ADDEPAR_API_KEY=your_base64_encoded_key_id_and_secret
```

The sandbox must actually be provisioned for your firm; changing a URL does not create one. A development environment can instead use `ADDEPAR_ENVIRONMENT=development`. You can specify a complete `ADDEPAR_BASE_URL` ending in `/api/v1` (or `/v1` for the global API). See [Addepar's environment URLs](https://developers.addepar.com/docs/urls).

Choose exactly one credential method: `ADDEPAR_API_KEY`, `ADDEPAR_ACCESS_TOKEN` (OAuth), or the pair `ADDEPAR_KEY_ID`/`ADDEPAR_KEY_SECRET`. The live command reads only the explicit credential file, disables variable interpolation, and does not use ambient credentials or `.netrc`. Tokens can expire during a run; use fresh credentials when retrying an authentication-blocked check.

Diagnostics always require `--env-file`; SDK factory defaults do not apply. Relative paths resolve from the current working directory, so the command also works in an extracted source archive without Git metadata. Application code can read the same file with `AddePy.from_dotenv(".env.sandbox")`. No-argument `AddePy.from_dotenv()` instead requires a consuming Git repository and its root `.env`; `AddePy.from_env()` reads process variables, and `AddePy(...)` uses only explicit arguments.

```bash
python -m addepy.diagnostics --env-file .env.sandbox
```

This runs a small smoke suite: current user, one entity, and available portfolio views. It does not automatically submit a query without a supplied query file. It prints outcomes and creates timestamped JSON and Markdown reports under `test-results/live/`.

**3. Verify both raw query workflows**

Create an ignored `live-queries/` directory. Copy a small portfolio query and a small transaction query from Addepar into `portfolio.json` and `transactions.json`. Use a portfolio you can access and a narrow date range; the SDK preserves your copied fields. Supply either direct parameters or the exported `data.attributes` envelope, not a full job submission envelope.

```bash
python -m addepy.diagnostics --env-file .env.sandbox --portfolio-query live-queries/portfolio.json --transaction-query live-queries/transactions.json --job-timeout 1200
```

The suite submits each query once, polls for completion, downloads its JSON result, checks its structure, and discards its contents. It retains job IDs for troubleshooting and resumption. It never cancels jobs, changes data, imports records, generates client reports, or publishes documents. It does not test saved-view file exports or beta batch computation automatically.

If a job exceeds the wait deadline, resume the existing job instead of submitting again:

```bash
python -m addepy.diagnostics --env-file .env.sandbox --only portfolio_job --portfolio-job-id YOUR_JOB_ID --job-timeout 1200
```

Transaction jobs use `--only transaction_job --transaction-job-id YOUR_JOB_ID`. Results expire according to Addepar's retention policy. `--read-only` prevents all job submissions while allowing an existing job to be inspected.

**4. Check additional endpoints or use production**

```bash
python -m addepy.diagnostics --list-checks
python -m addepy.diagnostics --env-file .env.sandbox --extended --entity-id YOUR_ENTITY_ID
python -m addepy.diagnostics --env-file .env.sandbox --only entities,report_schedules,fee_schedules
```

Extended checks read additional resources with small limits where their endpoints support them. Estimated returns require `--entity-id`; without it, the check is marked `missing_input`. Feature access and permissions vary by firm. Use `--only` to avoid spending request budget on irrelevant endpoints.

If sandbox is unavailable, create a separate `.env.production` with actual production settings and use:

```bash
python -m addepy.diagnostics --env-file .env.production --production --portfolio-query live-queries/portfolio.json --transaction-query live-queries/transactions.json
```

`--production` is required based on the actual host, even if a configuration file incorrectly labels a production URL as sandbox. There is no automatic fallback from sandbox to production. The same request guard applies in both environments: only reads and the exact two query-job POST routes/types are allowed. Imports, PATCH/PUT/DELETE, billing writes, report execution, and publication are blocked. Cross-host result downloads cannot carry API credentials or cookies.

**5. Interpret the report**

| Outcome | Meaning and next step |
| --- | --- |
| `pass` | The specific SDK call and inspected response structure worked. This is not certification of every field or endpoint. |
| `contract_failure` | Request/response/job behavior failed the check. Confirm the copied query is valid in Addepar, then compare the linked documentation and SDK contract. |
| `auth_blocked` | Credentials failed or expired. Fix authentication; the endpoint remains unverified. |
| `permission_blocked` | The user/app lacks access. Check firm permissions/scopes; this does not establish an SDK defect. |
| `unavailable` | The resource may be hidden, unsupported, expired, or the server unavailable. Check feature access and the supplied IDs. |
| `rate_limited` | Wait for capacity before retrying. Remaining checks stop after authentication failures or rate limits. |
| `network_error` | Check work-computer network/TLS access and timeouts. |
| `missing_input`, `skipped`, `incomplete` | No compatibility conclusion. Supply the input, enable the check, increase its limit, or resume its job. |
| `policy_blocked`, `config_error`, `internal_error` | Correct configuration or investigate the SDK guard/runner. A blocked request was not sent. |

Exit codes: **0** means all selected checks passed; **1** means a contract/internal failure; **2** means configuration or inconclusive/blocked checks. Permission failures and skips never count as passes. Empty collections only verify the collection envelope, not populated item behavior.

The default job wait is 120 seconds; `--job-timeout` increases it. `--poll-interval` defaults to 5 seconds, and `--request-timeout` to 30 seconds. Result inspection is capped at 10 MiB by default; use a smaller query or increase `--max-result-bytes`. Live checks disable automatic retries and stop after rate limiting instead of consuming more quota.

Reports contain check names, documentation links, outcomes, HTTP status where available, durations, and export job IDs/status/progress. They omit credentials, query values, firm identifiers, and response data. `test-results/`, `.env*` credential files, and `live-queries/` are ignored by Git. Review any additional diagnostics you capture before sharing them.

Bring back the Markdown/JSON reports and the local Git commit ID (`git rev-parse HEAD`), or the commit suffix in the source archive filename. Those reports identify what worked, what failed, and what could not be tested. Write compatibility and the [documented API ambiguities](docs/API_COVERAGE.md) still require separate confirmation; the safe live suite deliberately does not exercise business-data writes.
