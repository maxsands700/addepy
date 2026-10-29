# AddePy usage reference

Read [configuration](configuration.md) and [client conventions](client.md) first,
then the relevant resource reference. These pages describe the SDK implementation;
SDK signatures and return shapes govern application code.

| Task | Reference | Namespace |
| --- | --- | --- |
| Credentials, environments, OAuth | [Configuration](configuration.md) | `AddePy` |
| Requests, pagination, downloads, errors | [Client](client.md) | `client` |
| Portfolio/transaction asynchronous exports | [Jobs](jobs.md) | `client.portfolio.jobs`, `.transaction_jobs` |
| Views, synchronous queries, transactions, snapshots, investment data | [Portfolio](portfolio.md) | `client.portfolio` |
| Entities, groups, positions, external IDs | [Ownership](ownership.md) | `client.ownership` |
| Fees, schedules, billable portfolios, payouts | [Billing](billing.md) | `client.billing` |
| Users, contacts, files, imports, reports, permissions, audit | [Admin](admin.md) | `client.admin` |
| Tests, packaging, live diagnostics | [Development](development.md) | CLI |

## Conventions

- Examples assume an open `client = AddePy.from_dotenv(".env")`; prefer `with`.
- Resource prefixes are shown per section. Routes are relative to `client.base_url`,
  normally `https://{firm}.addepar.com/api/v1`; `{id}` denotes a supplied identifier.
- JSON:API resources contain `id`, `type`, `attributes`, and optional `relationships`.
  Resource helpers usually unwrap `data`; raw queries/requests retain complete documents.
- Endpoint tables name actual SDK methods. Parameter names are Python names;
  wire names appear in payload notes. Bulk input conventions vary by resource.
- Billing exists only under `client.billing`. Portfolio is exposed through
  `client.portfolio.analysis`; external-ID types through `client.ownership.external_ids`.
- Copied query dictionaries/JSON preserve unknown fields. Portfolio columns are
  attribute objects; transaction columns are strings. Portfolio job completion
  can return a result without a status; use SDK wait/resume helpers.
- Find optional arguments in the linked implementation when extending a call.
  Use `client.request(...)` for operations without a dedicated wrapper.

## Source map

[Client](../addepy/client.py), [configuration](../addepy/configuration.py),
[constants/types](../addepy/constants.py), [errors](../addepy/exceptions.py),
[resources](../addepy/resources/), [offline contracts](../tests/contracts/).
