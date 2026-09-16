# Investment API contracts

Reviewed September 16, 2026. Offline contract tests validate routes, payloads,
responses, pagination and input preservation; they do not establish live access.

| Resource | SDK coverage | Documentation |
| --- | --- | --- |
| Estimated returns | Entity-filtered list/iterator, composite-ID get, single/bulk upsert, value update, single/entity-wide delete | [Guide](https://developers.addepar.com/docs/estimated-returns) |
| Underlying assets | Get/list/iterator, metric date window, single/bulk create/update/delete | [Guide](https://developers.addepar.com/docs/underlying-assets) |
| Benchmark proxies | Get/list/iterator and single/entity-wide delete | [List](https://developers.addepar.com/reference/listbenchmarkproxies), [get](https://developers.addepar.com/reference/getbenchmarkproxy), [delete](https://developers.addepar.com/reference/deletebenchmarkproxy), [entity-wide delete](https://developers.addepar.com/reference/deletebenchmarkproxies) |
| Model types | Existing type discovery plus single/bulk model type conversion | [Guide](https://developers.addepar.com/docs/model-types) |

Estimated-return POST is an upsert and may return an array even for one input.
The singular SDK method unwraps that response. The list requires an entity filter.

Underlying assets use `/derivatives/underlying_assets` for requests; response
self-links in the guide instead use `/derivatives_underlying_assets`. The SDK
follows the explicit request routes. Pagination uses numeric `page[after]`
offsets; because the documented examples omit pagination links, the iterator
continues until an empty page (or the caller's limit/an explicit terminal link).
Null entries in `metric_values` are preserved to support deleting dated values.

Benchmark proxy read responses have a clear JSON:API contract. The
[create](https://developers.addepar.com/reference/createbenchmarkproxy) and
[update](https://developers.addepar.com/reference/updatebenchmarkproxy) references
instead publish a raw camelCase request schema, with snake_case JSON:API
response examples and no request example. Convenience create/update wrappers
are deferred until Addepar confirms the payload. The public raw request method
can submit a confirmed payload without SDK changes. Proxy list next links may
use `page[cursor]`, which the shared paginator supports.

Model type conversions use `PATCH /entity_types` with resource type
`entity_type_updates`, not an ordinary entity attribute edit. They can remove
attributes unsupported by the target type and are excluded from safe live tests.

Existing `update_benchmarks()` no longer removes IDs from caller dictionaries.
The documented benchmark creation request remains an array with a single object.
Bulk [transaction creation](https://developers.addepar.com/docs/transactions)
also preserves caller relationship IDs. [Historical-price submissions](https://developers.addepar.com/docs/historical-prices)
raise `ProtocolError` if the required asynchronous job ID is missing, instead of
returning `None` as if submission succeeded.

Live validation should use read-only calls for these resources. Write contracts
are exercised offline only, including null metric deletion and entity-wide delete
routes. Production live tests must never execute those writes.

## Legacy ownership and synchronous queries

Representative offline contracts also cover the published
[groups](https://developers.addepar.com/docs/groups),
[group types](https://developers.addepar.com/docs/group-types),
[positions](https://developers.addepar.com/docs/positions), and
[external ID types](https://developers.addepar.com/docs/external-identifier-types)
interfaces. Confirmed existing filter names, member/child-group relationship
methods, bulk arrays, custom/null attribute preservation and response unwrapping.
No ownership route changes were needed. This is representative coverage, not a
claim that every existing method or firm-specific attribute has been verified.

Both `portfolio.analysis.query_raw()` and `portfolio.transactions.query_raw()`
now accept copied parameters, a `data.attributes` envelope, or JSON text. They
preserve unknown fields and external-ID-only scopes and return complete response
metadata. Existing argument helpers delegate to the same normalization without
signature changes. See [Portfolio Query](https://developers.addepar.com/docs/portfolio-query)
and [Transactions Query](https://developers.addepar.com/docs/transactions-query).

The transaction-query guide lists `sortings` in its parameter table but uses
`sorting` in its request example. The argument helper retains its existing
`sorting` field; raw queries preserve whichever field the caller supplies.
Sandbox confirmation is still needed to resolve that documentation conflict.
Saved portfolio views retain their JSON-or-bytes return contract, while saved
transaction views retain `requests.Response` for compatibility.
