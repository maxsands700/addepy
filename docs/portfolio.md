# Portfolio

Access resources through `client.portfolio`. Paths follow the versioned API
base URL. `resource` means extracted JSON:API `data`; `document` means the complete
JSON response. `list_*` returns a list; `iter_*` yields resources. Collection
options default to `limit=10000` for lists, `limit=None` for iterators, and
`page_limit=500`, unless stated otherwise. See [client conventions](client.md)
and [job exports](jobs.md).

## Analysis: `client.portfolio.analysis`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `list_views()` | GET `/portfolio/views` | List of views; no pagination arguments |
| `get_view(view_id)` | GET `/portfolio/views/{view_id}` | View resource; definition in `attributes.parameters` |
| `get_view_results(view_id, portfolio_id, portfolio_type, start_date, end_date, output_type="JSON")` | GET `/portfolio/views/{view_id}/results` | JSON document; bytes for CSV/TSV/XLSX |
| `query_raw(query)` | POST `/portfolio/query` | Document |
| `query(columns, groupings, portfolio_type, portfolio_id=None, start_date=None, end_date=None, ...)` | POST `/portfolio/query` | Document |

`query_raw` accepts parameter dictionaries, JSON text, or `data.attributes`
envelopes; unknown fields and nested values pass through unchanged. `query`
requires both dates and either `portfolio_id` or
`external_ids=[{"external_type_key": "crm", "external_id": "client-1"}]`.
An empty `portfolio_id=[]` placeholder is accepted with external IDs.
Portfolio types: `ENTITY`, `ENTITY_FUNDS`, `GROUP`, `GROUP_FUNDS`, `FIRM`,
`FIRM_ACCOUNTS`, `FIRM_CLIENTS`, `FIRM_HOUSEHOLDS`, `FIRM_UNVERIFIED_ACCOUNTS`.
Use portfolio ID `1` for `FIRM`. Dates use `YYYY-MM-DD`.

Columns are `{"key": "value", "arguments": {...}}` objects. Groupings accept
those objects or strings; strings become `{"key": ...}`. Optional query keywords:
`filters`, `hide_previous_holdings`, `group_by_historical_values`,
`group_by_multiple_attribute_values`, `look_through_composite_securities`,
`look_through_constituent_holdings`, `display_account_fees`, `external_ids`.
Boolean options default to omission.

```python
result = client.portfolio.analysis.query(
    columns=[{"key": "value"}], groupings=["asset_class"],
    portfolio_type="ENTITY", portfolio_id=entity_id,
    start_date="2026-01-01", end_date="2026-03-31",
)
total = result["data"]["attributes"]["total"]
```

## Transactions: `client.portfolio.transactions`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `get_transaction(transaction_id)` | GET `/transactions/{transaction_id}` | Resource |
| `create_transaction(transaction_type, currency, trade_date, owner_id=None, owned_id=None, ...)` | POST `/transactions` | Resource |
| `create_transactions(transactions)` | POST `/transactions` | List |
| `update_transaction(transaction_id, **attributes)` | PATCH `/transactions/{transaction_id}` | Resource |
| `update_transactions(transactions)` | PATCH `/transactions` | List |
| `delete_transaction(transaction_id)` | DELETE `/transactions/{transaction_id}` | `None` |
| `delete_transactions(transaction_ids)` | DELETE `/transactions` | `None` |
| `get_transaction_owner(transaction_id)` | GET `/transactions/{transaction_id}/owner` | Entity resource |
| `get_transaction_owned(transaction_id)` | GET `/transactions/{transaction_id}/owned` | Entity resource |
| `get_transaction_cash_position(transaction_id)` | GET `/transactions/{transaction_id}/cash_position` | Position resource |
| `get_transaction_new_owner(transaction_id)` | GET `/transactions/{transaction_id}/new_owner` | Entity resource |
| `get_transaction_new_owned(transaction_id)` | GET `/transactions/{transaction_id}/new_owned` | Entity resource |
| `get_transaction_owner_relationship(transaction_id)` | GET `/transactions/{transaction_id}/relationships/owner` | Identifier |
| `get_transaction_owned_relationship(transaction_id)` | GET `/transactions/{transaction_id}/relationships/owned` | Identifier |
| `get_transaction_new_owner_relationship(transaction_id)` | GET `/transactions/{transaction_id}/relationships/new_owner` | Identifier |
| `get_transaction_new_owned_relationship(transaction_id)` | GET `/transactions/{transaction_id}/relationships/new_owned` | Identifier |
| `get_transaction_cash_account_relationship(transaction_id)` | GET `/transactions/{transaction_id}/relationships/cash_account` | Position identifier |
| `get_transaction_files(transaction_id)` | GET `/transactions/{transaction_id}/files` | `visible`, `can_manage_files`, `items` data object |
| `attach_transaction_file(transaction_id, file_id)` | POST `/transactions/{transaction_id}/files` | `None`; associates an existing file |
| `detach_transaction_file(transaction_id, file_id)` | DELETE `/transactions/{transaction_id}/files/{file_id}` | `None`; preserves the file |
| `get_view_results(view_id, portfolio_id, portfolio_type, start_date, end_date, output_type="CSV")` | GET `/transactions/views/{view_id}/results` | `requests.Response`; CSV/TSV/XLSX |
| `query_raw(query)` | POST `/transactions/query` | Document |
| `query_transactions(columns, portfolio_type, portfolio_id=None, start_date=None, end_date=None, ...)` | POST `/transactions/query` | Document with `meta.columns` and record list `data` |

Creation keywords: `amount`, `units`, `cash_position_id`, `new_owner_id`,
`new_owned_id`, plus `**attributes` such as fees, dates, descriptions, and custom
attributes. `owned_id` is required. Omit `owner_id` only for `node_fee` or
`account_fee*` transactions. Destination IDs become relationships, not attributes.
Bulk creation takes flat dictionaries using `type` instead of `transaction_type`;
bulk updates take `{"id": ..., ...attributes}`. Create/update/delete batches
require 1–500 entries. Snapshot/valuation CRUD uses `snapshots`, not this resource.

Query columns are strings, e.g. `["trade_date", "value"]`. Scope and dates follow
Analysis query rules. Optional keywords: `filters`, `sorting`, `limit`,
`external_ids`, `include_online_valuations=False`, `include_unverified=False`,
`include_deleted=False`. Sorting objects use `{"attribute": "trade_date",
"ascending": False}`. Builders emit `sorting`; raw queries preserve either
`sorting` or `sortings`. Use [transaction jobs](jobs.md) for large exports.

## Snapshots: `client.portfolio.snapshots`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `get_snapshot(snapshot_id)` | GET `/snapshots/{snapshot_id}` | Resource |
| `create_snapshot(snapshot_type, currency, trade_date, amount, owner_id, owned_id, ...)` | POST `/snapshots` | Resource; request uses a one-item array |
| `create_snapshots(snapshots)` | POST `/snapshots` | List |
| `update_snapshot(snapshot_id, ...)` | PATCH `/snapshots/{snapshot_id}` | Resource |
| `update_snapshots(snapshots)` | PATCH `/snapshots` | List |
| `delete_snapshot(snapshot_id)` | DELETE `/snapshots/{snapshot_id}` | `None` |
| `delete_snapshots(snapshot_ids)` | DELETE `/snapshots` | `None` |
| `get_snapshot_owner(snapshot_id)` | GET `/snapshots/{snapshot_id}/owner` | Entity resource |
| `get_snapshot_owned(snapshot_id)` | GET `/snapshots/{snapshot_id}/owned` | Entity resource |
| `get_snapshot_position(snapshot_id)` | GET `/snapshots/{snapshot_id}/position` | Position resource |
| `get_snapshot_owner_relationship(snapshot_id)` | GET `/snapshots/{snapshot_id}/relationships/owner` | Identifier |
| `get_snapshot_owned_relationship(snapshot_id)` | GET `/snapshots/{snapshot_id}/relationships/owned` | Identifier |
| `get_snapshot_position_relationship(snapshot_id)` | GET `/snapshots/{snapshot_id}/relationships/position` | Identifier |

Types: `snapshot` or `valuation`. Optional creation keywords: `units`, `comment`,
`price_factor`, `accrued_income_per_unit`, `knowledge_date`. Server asset semantics
determine whether units are required. Keep returned IDs as strings; a knowledge
date can produce IDs such as `123_2026-04-15`.

Bulk creation takes flat dictionaries with the same keys; omitted `snapshot_type`
defaults to `snapshot`. Bulk updates take `id` plus editable attributes.
Single/bulk updates support `amount`, `currency`, `units`, `comment`,
`price_factor`, `accrued_income_per_unit`. Omission preserves a field; explicit
`None` clears it. Dates, type, and relationships are immutable through these
builders. All bulk methods require 1–500 entries.

## Attribute discovery

| Resource | Method | HTTP endpoint | Returns |
| --- | --- | --- | --- |
| `portfolio.arguments` | `list_arguments()` | GET `/arguments` | List |
| `portfolio.arguments` | `get_argument(argument_id)` | GET `/arguments/{argument_id}` | Resource |
| `portfolio.attributes` | `list_attributes(...)`, `iter_attributes(...)` | GET `/attributes` | List / iterator |
| `portfolio.attributes` | `get_attribute(attribute_id)` | GET `/attributes/{attribute_id}` | Resource |
| `portfolio.attributes` | `query_attributes(attribute_keys)` | POST `/attributes/query` | List |
| `portfolio.attributes` | `get_argument_ids(attribute_id)` | GET `/attributes/{attribute_id}/relationships/arguments` | Identifier list |
| `portfolio.attributes` | `get_arguments(attribute_id)` | GET `/attributes/{attribute_id}/arguments` | Resource list |

Attribute collection filters: `category`, `usage`, `output_type`; use the literals
in [constants.py](../addepy/constants.py). Attribute keys may be custom API names.

## Benchmarks: `client.portfolio.benchmarks`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `list_benchmarks(...)`, `iter_benchmarks(...)` | GET `/benchmarks` | List / iterator; page cap 500 |
| `get_benchmark(benchmark_id)` | GET `/benchmarks/{benchmark_id}` | Resource |
| `create_benchmark(benchmark_type, ...)` | POST `/benchmarks` | Resource |
| `update_benchmark(benchmark_id, ...)` | PATCH `/benchmarks/{benchmark_id}` | Resource |
| `update_benchmarks(benchmarks)` | PATCH `/benchmarks` | List |
| `delete_benchmark(benchmark_id)` | DELETE `/benchmarks/{benchmark_id}` | `None` |
| `list_benchmark_compositions(...)`, `iter_benchmark_compositions(...)` | GET `/benchmark_compositions` | List / iterator |
| `get_benchmark_composition(composition_id)` | GET `/benchmark_compositions/{composition_id}` | Resource |
| `update_benchmark_composition(composition_id, intervals)` | PATCH `/benchmark_compositions/{composition_id}` | `None` |
| `get_imported_benchmark_data(benchmark_id)` | GET `/imported_benchmark_data/{benchmark_id}` | Resource |
| `update_imported_benchmark_data(benchmark_id, daily_returns)` | PATCH `/imported_benchmark_data/{benchmark_id}` | `None` |
| `list_benchmark_association_strategies(...)`, `iter_benchmark_association_strategies(...)` | GET `/benchmark_associations_strategies` | List / iterator; page cap 500 |
| `get_benchmark_association_strategy(strategy_id)` | GET `/benchmark_associations_strategies/{strategy_id}` | Resource |
| `create_benchmark_association_strategy(display_name, matching_type, benchmark_associations)` | POST `/benchmark_associations_strategies` | Resource |
| `update_benchmark_association_strategy(strategy_id, ...)` | PATCH `/benchmark_associations_strategies/{strategy_id}` | Resource |
| `delete_benchmark_association_strategy(strategy_id)` | DELETE `/benchmark_associations_strategies/{strategy_id}` | `None` |
| `list_benchmark_proxies(entity_ids=[...], ...)`, `iter_benchmark_proxies(entity_ids=[...], ...)` | GET `/benchmark_proxies` | List / iterator; nonempty entity filter required |
| `get_benchmark_proxy(proxy_id)` | GET `/benchmark_proxies/{proxy_id}` | Resource |
| `delete_benchmark_proxy(proxy_id)` | DELETE `/benchmark_proxies/{proxy_id}` | `None` |
| `delete_entity_benchmark_proxies(entity_id)` | DELETE `/benchmark_proxies/entity/{entity_id}` | `None`; all proxies for that entity |

Creation types and keyword payloads:

| `benchmark_type` | Keywords |
| --- | --- |
| `blended` | `name`, `blended={"rebalance_interval": "THREE_MONTHS"}` |
| `imported` | `name` |
| `fixed_return` | `fixed_return={"fixed_return": 0.05, "is_compounded": True}` |
| `portfolio_benchmark` | `name`, `portfolio={"entity_id": ...}` |
| `security_benchmark` | `name`, `security={"entity_id": ...}` |

Single updates accept `name`, `blended`, `fixed_return`; bulk updates take flat
`id` plus attribute dictionaries. Benchmark type cannot change.
Composition intervals: `[{"date": "2026-01-01", "value":
[{"benchmark_id": 123, "percent": 1.0}]}]`; `value=None` removes that interval.
Daily returns: `[{"date": "2026-01-01", "value": 0.005}]`; supplied dates upsert.
Strategies use `matching_type="PATH"` or `"PDN"` and associations such as
`[{"rules": [{"attribute": "asset_class", "value": "Equity"}],
"benchmarks": [123]}]`. Strategy updates accept `display_name`, `matching_type`,
`benchmark_associations`; omission preserves associations, `[]` clears them.
Proxy IDs combine entity and date. Proxy helpers expose reads/deletes only.

## Estimated returns: `client.portfolio.estimated_returns`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `list_estimated_returns(entity_ids, ...)`, `iter_estimated_returns(entity_ids, ...)` | GET `/estimated_returns` | List / iterator; nonempty entity sequence required |
| `get_estimated_return(estimated_return_id)` | GET `/estimated_returns/{estimated_return_id}` | Resource |
| `create_estimated_return(entity_id, date, return_value)`; alias `upsert_estimated_return` | POST `/estimated_returns` | Resource; upsert by entity/date |
| `create_estimated_returns(estimated_returns)`; alias `upsert_estimated_returns` | POST `/estimated_returns` | List |
| `update_estimated_return(estimated_return_id, return_value)` | PATCH `/estimated_returns/{estimated_return_id}` | Resource |
| `delete_estimated_return(estimated_return_id)` | DELETE `/estimated_returns/{estimated_return_id}` | `None` |
| `delete_entity_estimated_returns(entity_id)` | DELETE `/estimated_returns/entity/{entity_id}` | `None`; all returns for that entity |

IDs look like `123_2026-01-01`. Bulk creation takes attribute dictionaries with
`entity_id`, `date`, `return_value`. Updating changes only the return value.

## Derivatives: `client.portfolio.underlying_assets`

Let `U=/derivatives/underlying_assets`; type is `derivatives_underlying_assets`.

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `list_underlying_assets(...)`, `iter_underlying_assets(...)` | GET `U` | List / iterator; numeric offset pagination |
| `get_underlying_asset(asset_id, ...)` | GET `U/{asset_id}` | Resource |
| `create_underlying_asset(**attributes)` | POST `U` | Resource |
| `create_underlying_assets(assets)` | POST `U` | List |
| `update_underlying_asset(asset_id, **attributes)` | PATCH `U/{asset_id}` | Resource |
| `update_underlying_assets(assets)` | PATCH `U` | List |
| `delete_underlying_asset(asset_id)` | DELETE `U/{asset_id}` | `None` |
| `delete_underlying_assets(asset_ids)` | DELETE `U` | `None` |

Read keywords `metric_date_from` and `metric_date_to` include spot values when
both date bounds are supplied. Create attributes include `entity_name`,
`entity_type`, `underlying_type`, `base_currency`, `financial_graph_node_id`,
`metric_values`. Bulk create takes attribute dictionaries; bulk update takes
flat dictionaries with `id` plus changed attributes. Omitted metrics remain;
`metric_values={"2026-01-01": 100.0}` sets spots; a null value deletes that
date's spot value. Use resource iterators for
this endpoint's numeric offset scheme.

## Historical prices: `client.portfolio.historical_prices`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `get_prices(entity_id, date=None)` | GET `/entities/{entity_id}/prices` | List; `date` keyword-only |
| `create_prices(entity_id, prices)` | POST `/entities/{entity_id}/prices` | Async save ID |
| `delete_price(entity_id, date)` | DELETE `/entities/{entity_id}/prices/{date}` | Async delete ID |

Price entries: `{"date": "2026-01-01", "nodeId": 123, "value": 100.0}`.
POST upserts supplied prices. Missing async IDs raise `ProtocolError`; these
submission IDs are not portfolio-export `jobs` IDs.

## ETF constituents

| Resource | Method | HTTP endpoint | Returns |
| --- | --- | --- | --- |
| `portfolio.composite_securities` | `get_constituent_weight(composite_id, constituent_id, start_date=None, end_date=None)` | GET `/composite_securities/{composite_id}/{constituent_id}` | Resource; date filters keyword-only |
| `portfolio.composite_securities` | `import_constituents(composite_id, date, constituents)` | POST `/composite_securities/import` | Resource |
| `portfolio.composite_securities` | `delete_constituents(composite_id, date)` | DELETE `/composite_securities/{composite_id}/{date}` | `None` |
| `portfolio.constituent_attributes` | `list_constituent_attributes(...)`, `iter_constituent_attributes(...)` | GET `/constituent_attributes` | List / iterator; optional `asm_id` |
| `portfolio.constituent_attributes` | `get_constituent_attribute(attribute_id)` | GET `/constituent_attributes/{attribute_id}` | Resource |
| `portfolio.constituent_attributes` | `create_constituent_attribute(asm_id, attribute_key, values)` | POST `/constituent_attributes` | Resource |
| `portfolio.constituent_attributes` | `create_constituent_attributes(attributes)` | POST `/constituent_attributes` | List |
| `portfolio.constituent_attributes` | `update_constituent_attribute(attribute_id, values)` | PATCH `/constituent_attributes/{attribute_id}` | Resource |
| `portfolio.constituent_attributes` | `update_constituent_attributes(updates)` | PATCH `/constituent_attributes` | List |
| `portfolio.constituent_attributes` | `delete_constituent_attribute(attribute_id)` | DELETE `/constituent_attributes/{attribute_id}` | `None` |
| `portfolio.constituent_attributes` | `delete_constituent_attributes_by_asm(asm_id)` | DELETE `/constituent_attributes?asmId={asm_id}` | `None`; all attributes for that ASM |

Weight entries use `{"entityId": 123, "percentage": 0.42}`. Attribute bulk
creation takes `asm_id`, `attribute_key`, `values`; bulk updates take `id`,
`values`. Values may be scalars or histories such as
`[{"date": None, "value": "Equity", "weight": 1.0}]`. Updating history requires
the complete desired history. Composite weight read keywords become `startDate`
and `endDate`; constituent-attribute filtering uses `asmId`.
