# Resources and data

Create a client as shown in the [README](../README.md). Resource methods live
under three namespaces; use their method docstrings for individual parameters.

| Namespace | Resources |
| --- | --- |
| `client.portfolio` | `analysis`, `jobs`, `transaction_jobs`, `transactions`, `snapshots`, `attributes`, `arguments`, `benchmarks`, `historical_prices`, `estimated_returns`, `underlying_assets`, `composite_securities`, `constituent_attributes` |
| `client.ownership` | `entities`, `groups`, `positions`, `external_ids` |
| `client.admin` | `users`, `roles`, `teams`, `contacts`, `files`, `reports`, `report_schedules`, `import_tool`, `audit`, `client_portal`, `view_sets`, `target_allocations`, `fees`, `fee_schedules`, `billable_portfolios`, `payout_recipients`, `payout_rules` |

## Results and pagination

Most singular methods return a resource dictionary (`id`, `type`, `attributes`,
and possibly `relationships`); plural methods return lists. Most delete and
relationship mutations return `None`. Query jobs return `requests.Response` for
downloads; file download helpers return `Path`. See [Jobs](jobs.md).

List methods generally default to at most 10,000 results. Iterators fetch pages
lazily and can traverse all results; `limit` caps total records and `page_limit`
controls the requested page size.

```python
from addepy import AddePy

with AddePy.from_dotenv(".env") as client:
    for entity in client.ownership.entities.iter_entities(limit=500):
        print(entity["id"])

    # Full pages preserve included resources, links, and metadata.
    for page in client.iter_pages("/entities", page_limit=100, max_pages=2):
        print(page.get("meta", {}))

    # Raw access returns requests.Response, with SDK authentication and errors.
    document = client.request(
        "GET", "/entities", params={"page[limit]": 1}
    ).json()
```

Use resource iterators for payouts and underlying assets: they handle these
endpoints' different offset schemes. The general paginator follows returned next
links and metadata cursors, preserving filters and rejecting repeated pages.

## Synchronous queries and files

`client.portfolio.analysis.query_raw(query)` and
`client.portfolio.transactions.query_raw(query)` accept dictionaries or JSON text,
either direct query parameters or a `data.attributes` envelope. They return the
full JSON document, including metadata. Unknown fields and external-ID scopes
pass through unchanged. Use [query jobs](jobs.md) for larger exports.

Transaction argument helpers use `sorting`; raw queries preserve the caller's
spelling, including `sortings`. Do not rename a working copied query's fields.

Saved-view return types differ: `analysis.get_view_results()` returns a dictionary
for JSON and bytes for other formats; `transactions.get_view_results()` returns
`requests.Response` (default CSV). Read `.text` for CSV/TSV or `.content` for XLSX.

`client.admin.files.download_file_to(id, path)` and
`download_archived_file_to(id, path)` stream files to disk. Generated report ZIPs
use `client.admin.reports.download_zipped_file_to(job_id, path)`. These return
`Path`, preserve existing files unless `overwrite=True`, and leave no partial
destination on failure. Their counterparts without `_to` return bytes.

## CSV and DataFrame imports

```python
from pathlib import Path
from addepy import AddePy

with AddePy.from_dotenv(".env") as client:
    result = client.admin.import_tool.execute_import(
        Path("attributes.csv"), "ATTRIBUTES", is_dry_run=True
    )
    print(result["digests"], result["warnings"], result["errors"])
```

Inputs can be CSV text, bytes, a `Path`, a readable file, or a pandas DataFrame.
A string is CSV **content**, so use `Path` for filenames. DataFrames serialize
without their index; install `pip install 'addepy[dataframe]'` for pandas support.

Imports default to `is_dry_run=True` and `ignore_warnings=False`. Review the
returned errors and warnings; set `is_dry_run=False` to submit an actual import.
For separate submission and tracking, `create_import()` returns an ID;
`get_import_status(id)` returns a status string and `get_import_results(id)`
returns the same `digests`/`warnings`/`errors` dictionary.

## Billing and payouts

`replace_fee`, `replace_fee_schedule`, their bulk variants, and payout
`replace_*` methods perform **full PUT replacement**. Supply every attribute and
relationship you intend to retain. These are not partial PATCH updates.
`fee_schedules.replace_fees(schedule_id, fee_ids)` replaces all fee associations;
`remove_fees(schedule_id)` removes all of them.

Bulk payload conventions are endpoint-specific:

| Operation | Input items |
| --- | --- |
| Fee, fee schedule, and payout bulk creation | JSON:API resources with `attributes` and optional `relationships`; `type` may be omitted |
| Fee and fee schedule bulk replacement | Complete JSON:API resources, including `id` |
| Billable portfolio bulk creation | Attribute dictionaries with `schedule_id` and exactly one of `entity_id` or `group_id` |
| Estimated return and underlying asset bulk creation | Attribute dictionaries |
| Underlying asset bulk update | Flat dictionaries with `id` and attributes to change |

Fee schedule resources carry fee IDs under
`relationships.fees.data = [{"type": "fees", "id": "..."}]`; singular helpers
accept `fee_ids` directly. Singular billing methods unwrap a one-item response
array into a dictionary. `create_billable_portfolio()` instead returns a string
ID; its plural counterpart returns a resource list.

Billable portfolio `update_fee_schedules()` takes a mapping of
`{billable_portfolio_id: schedule_id}`. Bulk schedule reassignment and archive
accept at most 500 portfolios and require the corresponding firm feature.
Archiving stops future billing; assigning a fee schedule can restore a portfolio.

Payout list/iterator methods accept `search`; rules also accept `recipient_ids`.
They handle plain `offset`/`limit` pagination and retain returned item shapes.
Supply recipient IDs inside payout-rule splits, rather than expanded recipients.

## Reports and schedules

Report generation takes portfolios as
`{"portfolio_type": "entity" or "group", "portfolio_id": "..."}`.
`create_report_generation_job()` returns a job resource; `brand_id` is a team ID,
and `label` is a list of label IDs. Publishing and notifications are controlled
separately through `portal_publishing` and `contact_notification`.

Schedule methods use `/report_schedule` with resource type `report_schedules`.
`create_schedule(attributes)` accepts an attribute dictionary;
`update_schedule(id, attributes)` patches only supplied values, including explicit
`None`. Listing accepts API query names verbatim in `params`. Scheduled dates and
times follow the firm's timezone.

`execute_schedule(id, payload)` requires the complete JSON:API request document
for your execution options and returns the complete response document.
`list_executions(id)` returns relationship identifiers, not expanded jobs.

## Investment data

Estimated return listing requires a nonempty `entity_ids` sequence. Individual
IDs combine entity and date, such as `"123_2024-01-15"`. Creation is an upsert of
the entity/date pair; `upsert_estimated_return(s)` aliases make that intent
explicit. Updating an existing return changes only its value.

Underlying assets use `/derivatives/underlying_assets` with resource type
`derivatives_underlying_assets`. Supply both `metric_date_from` and
`metric_date_to` in `YYYY-MM-DD` format to include spot values. Updates preserve
omitted metrics; a `None` metric value deletes that date's spot value.

Benchmark proxy methods live under `client.portfolio.benchmarks` and support
reads and deletes. Proxy IDs also combine entity and date. For operations without
a dedicated wrapper, use `client.request()` with your API payload.
`delete_entity_estimated_returns()` and `delete_entity_benchmark_proxies()` remove
all records of that kind for an entity.

Model conversion uses `client.ownership.entities.change_model_type(id, type)` or
`change_model_types([{"id": "...", "new_model_type": "etf"}])`. Use API model
names from `list_entity_types()`. Conversion uses the dedicated `/entity_types`
route and can remove attributes unsupported by the target model type.
