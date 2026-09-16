**AddePy revamp proposal — September 16, 2026**

Recommend evolving the existing `portfolio`, `ownership`, and `admin` namespaces, with shared infrastructure underneath. The SDK already covers substantial ground; the priorities are reliable query workflows, API correctness, and targeted coverage expansion. Reviewed the repository against Addepar's current guides and API Explorer.

**Raw queries remain a core interface.** Both portfolio and transaction jobs should accept copied query JSON as a dictionary or JSON string, including Addepar's `data.attributes` envelope. Preserve every query field, avoid modifying the caller's input, and wrap it for the appropriate job endpoint. Keep optional argument-based helpers and both submit-only and submit/wait/download workflows. Portfolio already supports raw dictionaries; transaction jobs need equivalent support. This preserves the convenient [Addepar query export workflow](https://developers.addepar.com/docs/portfolio-query-builder).

Recommended changes, in priority order:

1. **Fix correctness and establish contract tests.** Missing portfolio job status currently defaults to success; HTTP exceptions lose their status codes; README examples reference nonexistent methods. Fix these alongside request/response fixtures covering raw queries, pagination, job failures, and downloads. Add CI, working examples, and consistent package/version metadata so future endpoint additions remain dependable.

2. **Separate transport, endpoint wrappers, and workflow helpers.** Keep resource methods thin; share authentication, requests, pagination, errors, and polling. Add an injectable HTTP session, configurable timeouts, and a public raw-request escape hatch. This reduces duplication and lets users access new API fields before dedicated wrappers exist.

3. **Improve authentication and request reliability.** Retain Basic API-key authentication; add OAuth token/refresh support and explicit environment URLs. Use bounded retries that honor Addepar's rate-limit headers, with write retries explicitly controlled to avoid duplicate submissions. Preserve structured errors and response metadata for diagnosis. See [authentication](https://developers.addepar.com/docs/basic-authentication), [OAuth](https://developers.addepar.com/docs/oauth), [environments](https://developers.addepar.com/docs/urls), and [rate limits](https://developers.addepar.com/docs/rate-limiting-1).

4. **Unify job handling and large-result access.** Provide consistent wait, resume-by-ID, cancel, and download helpers, with deadlines and endpoint-specific failure states. Follow server-provided pagination links/cursors under each endpoint's contract; retain lazy iterators and expose page metadata. Stream large exports to files, with explicit JSON/file result handling. This supports long-running workflows without restarting jobs or loading everything into memory. See [portfolio jobs](https://developers.addepar.com/docs/jobs), [transaction jobs](https://developers.addepar.com/docs/transaction-jobs), and [pagination](https://developers.addepar.com/docs/pagination-1).

5. **Keep data handling lightweight and flexible.** Make pandas an optional extra for DataFrame imports/exports; support CSV and file inputs in the core package. Add useful type hints while retaining raw JSON and unknown fields, especially for firm-specific attributes and copied queries.

Expand endpoint coverage in this order. These are gaps in this SDK, not claims that every endpoint was recently released:

| Priority | Add or complete | Why |
| --- | --- | --- |
| First | Opt-in [batched portfolio jobs](https://developers.addepar.com/docs/batched-jobs), using the existing jobs endpoint and batch header; label beta restrictions. | Faster large-portfolio extraction while retaining raw queries. |
| Next | [Report schedules](https://developers.addepar.com/docs/report-schedules), execution, and execution history. | Complete recurring reporting alongside existing report generation/downloads. |
| Next | [Fees](https://developers.addepar.com/docs/fee-rules), [fee schedules](https://developers.addepar.com/docs/fee-schedules), [payout recipients](https://developers.addepar.com/docs/payout-recipients)/[rules](https://developers.addepar.com/docs/payout-rules), and remaining [billable portfolio](https://developers.addepar.com/docs/billing) operations. | Complete billing setup and maintenance beyond today's limited wrapper. |
| Next | [Estimated returns](https://developers.addepar.com/docs/estimated-returns), [benchmark proxies](https://developers.addepar.com/reference/listbenchmarkproxies), and [derivative underlying assets](https://developers.addepar.com/docs/underlying-assets). | Fill investment-data gaps alongside existing benchmark and pricing resources. |
| Later | [Pricing datasets](https://developers.addepar.com/reference/listpricingdatasets)/[source strategies](https://developers.addepar.com/reference/listpricingsourcesstrategies), [transaction datasets](https://developers.addepar.com/reference/listtransactiondatasets), [data timelines](https://developers.addepar.com/reference/listdatatimelines), and [personas](https://developers.addepar.com/reference/listpersonas). | Broaden data and access administration once firm availability and sparse reference contracts are verified. |

Use the published API descriptions to track coverage and detect changes. Some documentation conflicts—for example, [the welcome page](https://developers.addepar.com/docs/welcome) and the detailed authentication/pagination guides—need sandbox verification before enforcing strict schemas or generating wrappers wholesale. Preserve existing public methods through compatibility aliases when standardizing names.
