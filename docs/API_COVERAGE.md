# API coverage and verification

Reviewed against [Addepar's guides and API Explorer](https://developers.addepar.com/docs/welcome) on September 16, 2026. Offline tests assert documented methods, paths, payloads, representative responses, pagination, and SDK behavior. They cannot establish that a specific firm exposes an endpoint or that conflicting examples match the deployed API.

| Area | Implemented in this release | Offline coverage |
| --- | --- | --- |
| Transport/authentication | Basic key pairs and encoded credentials, OAuth bearer/refresh provider, production/development/sandbox URLs, public raw requests, bounded read retries, structured errors, credential-free cross-host downloads | [Transport](../tests/unit/test_transport.py), [OAuth/imports](../tests/unit/test_auth_imports.py) |
| Pagination and polling | Returned next links, both cursor spellings, metadata cursors, returned offset coordinates, full page access, bounded monotonic polling | [Pagination/polling](../tests/unit/test_pagination_polling.py) |
| Portfolio/transaction jobs | Raw JSON strings/dictionaries, optional builders, wait/resume/cancel, JSON/file downloads, beta portfolio batch header | [Lifecycle](../tests/unit/test_jobs.py), [job contracts](../tests/contracts/test_jobs.py) |
| Billing/payouts | Fees and schedules, PUT replacements, recipients/rules, billable portfolio reads/bulk operations/associations | [Admin contracts](../tests/contracts/test_admin_resources.py), [detailed notes](../API_NOTES_ADMIN.md) |
| Reporting/files | Schedule CRUD/execution relationships, raw execution requests, generation brand option, streaming downloads, shared upload transport | [Admin contracts](../tests/contracts/test_admin_resources.py) |
| Investment data | Estimated returns, derivative underlying assets, benchmark proxy reads/deletes, model-type conversion | [Investment contracts](../tests/contracts/test_investment_resources.py), [detailed notes](../API_NOTES_INVESTMENT.md) |
| Existing ownership and synchronous queries | Representative group/position/external-ID relationship and bulk contracts; raw portfolio/transaction synchronous queries; input preservation fixes | [Ownership/query contracts](../tests/contracts/test_legacy_queries_ownership.py), [legacy portfolio regressions](../tests/contracts/test_legacy_portfolio_contracts.py) |
| Imports | CSV text/bytes/files/Path and optional DataFrame adapter, existing dry-run default | [OAuth/imports tests](../tests/unit/test_auth_imports.py) |

Existing resources remain available; the table identifies reviewed additions and representative regression coverage, not exhaustive validation of every resource method. The live diagnostic report identifies exactly which checks ran. Business-data writes are exercised only with mocked requests, including in sandbox; this suite does not establish live write compatibility.

**Known documentation conflicts**

- The [welcome page](https://developers.addepar.com/docs/welcome) simplifies authentication to bearer tokens, while [Access & Authentication](https://developers.addepar.com/docs/basic-authentication) documents Basic API keys and OAuth separately. Both are supported. OAuth lifetime descriptions also differ, so refresh follows actual `expires_in` values.
- The [pagination guide](https://developers.addepar.com/docs/pagination-1) uses `page[after]`; several API Explorer schemas use `page[cursor]`. Follow returned links; billing and payout metadata/offset schemes have dedicated support.
- The [transaction job guide](https://developers.addepar.com/docs/transaction-jobs) lists `sortings` but its request example uses `sorting`. Argument helpers retain the existing `sorting` spelling; raw queries preserve either spelling supplied by the user.
- The [standard jobs guide](https://developers.addepar.com/docs/jobs) uses `PORTFOLIO_QUERY`, while [batched jobs](https://developers.addepar.com/docs/batched-jobs) also names `portfolio_query_results`. `batch=True` adds the documented header without rewriting the standard job type. `job_type=` permits an explicit verified override.
- Contrary to the documented portfolio job status contract, a user confirmed on an Addepar-connected work computer that `GET /jobs/{id}` can return completed portfolio results (`meta`, `data`, `included`, and `data.attributes.total` with `columns`/`children`) without `data.attributes.status`. Portfolio polling recognizes a valid result structure as completion and preserves the original document. An explicit status takes precedence; arbitrary missing-status responses and transaction jobs remain strict. This compatibility case is covered with synthetic regression fixtures based on that observation.
- [Report schedule execution](https://developers.addepar.com/reference/createreportscheduleexecute) has an incomplete request schema. `execute_schedule(id, payload)` forwards a complete caller-supplied JSON:API document. The live suite does not execute schedules.
- Benchmark proxy [create](https://developers.addepar.com/reference/createbenchmarkproxy)/[update](https://developers.addepar.com/reference/updatebenchmarkproxy) references publish camelCase request schemas alongside snake_case JSON:API responses without a usable request example. Dedicated write helpers are deferred; `client.request()` can submit a firm-confirmed payload.

**Deferred dedicated wrappers**

The proposal's later-stage pricing datasets/source strategies, transaction datasets, data timelines, personas, and API-version convenience wrapper remain outside this release. Their reference contracts need further confirmation; use `client.request()` for a confirmed operation. The SDK does not invent schemas for them. The [proposal](../REVAMP_PROPOSAL.md) links the individual reference pages.

Run [the live suite](../TESTING.md) from the authorized work computer to resolve deployment-specific compatibility. A 403 or hidden 404 is inconclusive about the request contract; it is never recorded as a pass. Use a small copied query and a narrow date range for export checks.
