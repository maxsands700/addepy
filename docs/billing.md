# Billing

Use `client.billing`; billing resources are absent from `client.admin`.
Routes below are relative to the configured API base. See [client conventions](client.md).

## Fees — `client.billing.fees`

| SDK call | HTTP route | Result |
| --- | --- | --- |
| `get_fee(fee_id, include=None, full_document=False)` | GET `/fees/{id}` | Resource; full document when requested |
| `list_fees(...)`, `iter_fees(...)` | GET `/fees` | List / resource iterator |
| `iter_fee_pages(...)` | GET `/fees` | Full-document iterator |
| `create_fee(attributes, relationships=None)` | POST `/fees` | Resource |
| `create_fees(fees)` | POST `/fees` | List |
| `replace_fee(fee_id, attributes, relationships=None)` | PUT `/fees/{id}` | Resource |
| `replace_fees(fees)` | PUT `/fees` | List |
| `delete_fee(fee_id)` | DELETE `/fees/{id}` | `None` |
| `delete_fees(fee_ids)` | DELETE `/fees` | `None` |
| `get_fee_schedules(fee_id)` | GET `/fees/{id}/fee_schedules` | Expanded schedule list |
| `get_fee_schedule_relationships(fee_id)` | GET `/fees/{id}/relationships/fee_schedules` | Schedule identifier list |

Read options: `include="fee_schedules"`; collections accept `limit` and
`page_limit` (max 500). Page iterators accept `max_pages`, not an item limit.
Item/list helpers omit top-level `included`; use full documents for expansions.

Single creation accepts an attribute dictionary and submits a one-item array.
Bulk creation/replacement accepts JSON:API resources: `{"attributes": {...}}`,
with `id` required for replacement; `type="fees"` may be omitted. Both require
1–500 items. PUT replaces the complete fee. `rate_asset_valuation` is edit-only;
`relationships.fee_schedules` is read-only. Manage assignments through schedules.
Other attributes and relationship keys pass through.

```python
document = client.billing.fees.get_fee(
    fee_id, include="fee_schedules", full_document=True
)
schedules = document.get("included", [])
```

## Fee schedules — `client.billing.fee_schedules`

| SDK call | HTTP route | Result |
| --- | --- | --- |
| `get_fee_schedule(schedule_id, include=None, full_document=False)` | GET `/fee_schedules/{id}` | Resource / full document |
| `list_fee_schedules(...)`, `iter_fee_schedules(...)` | GET `/fee_schedules` | List / resource iterator |
| `iter_fee_schedule_pages(...)` | GET `/fee_schedules` | Full-document iterator |
| `create_fee_schedule(attributes, fee_ids)` | POST `/fee_schedules` | Resource |
| `create_fee_schedules(schedules)` | POST `/fee_schedules` | List |
| `replace_fee_schedule(schedule_id, attributes, fee_ids)` | PUT `/fee_schedules/{id}` | Resource |
| `replace_fee_schedules(schedules)` | PUT `/fee_schedules` | List |
| `delete_fee_schedule(schedule_id)` | DELETE `/fee_schedules/{id}` | `None` |
| `delete_fee_schedules(schedule_ids)` | DELETE `/fee_schedules` | `None` |
| `get_fees(schedule_id)` | GET `/fee_schedules/{id}/fees` | Expanded fee list |
| `get_fee_relationships(schedule_id)` | GET `/fee_schedules/{id}/relationships/fees` | Fee identifier list |
| `add_fees(schedule_id, fee_ids)` | POST `/fee_schedules/{id}/relationships/fees` | `None` |
| `replace_fees(schedule_id, fee_ids)` | PUT `/fee_schedules/{id}/relationships/fees` | `None` |
| `remove_fees(schedule_id)` | DELETE `/fee_schedules/{id}/relationships/fees` | `None`; removes all associations |

Reads mirror fee options with `include="fees"`; page size max 500.
Creation submits an array; singular helpers build the envelope. Create/replace
requires at least one fee. Complete flat-fee and schedule creation:

```python
billing = client.billing
fee = billing.fees.create_fee({
    "name": "Annual management fee",
    "fee_structure": "FLAT",
    "scaling": "EVEN",
    "margin_handling_method": "USE_VALUE",
    "asset_valuation": {
        "method": "ON_BILL_DATE",
        "adjustment_type": "NONE",
        "accrual_type": "NONE",
    },
    "flat_fee_amount": 2500.0,
    "flat_fee_apply_to": "DIRECT_OWNER",
})
schedule_attributes = {
    "name": "Quarterly USD",
    "currency": "USD",
    "interval": "QUARTERLY",
    "billing_period_cycle_start_month": 1,
    "timing": "IN_ARREARS",
    "rounding": "NONE",
}
schedule = billing.fee_schedules.create_fee_schedule(
    schedule_attributes, fee_ids=[fee["id"]]
)
```

Bulk items contain `attributes` plus
`relationships.fees.data=[{"type": "fees", "id": fee_id}]`.
`type="fee_schedules"` may be omitted; replacement additionally requires `id`.
Supply all retained attributes and fees on PUT. Empty `add_fees` and
`replace_fees` fail locally; use `remove_fees` to clear associations.

## Billable portfolios — `client.billing.billable_portfolios`

| SDK call | HTTP route | Result |
| --- | --- | --- |
| `get_billable_portfolio(portfolio_id)` | GET `/billable_portfolios/{id}` | Resource |
| `list_billable_portfolios(...)`, `iter_billable_portfolios(...)` | GET `/billable_portfolios` | List / resource iterator |
| `create_billable_portfolio(schedule_id, entity_id=..., group_id=..., payout_rule_id=None)` | POST `/billable_portfolios` | ID string |
| `create_billable_portfolios(portfolios)` | POST `/billable_portfolios` | List |
| `update_fee_schedule(billable_portfolio_id, fee_schedule_id)` | PATCH `/billable_portfolios/{id}/relationships/fee_schedules` | `None` |
| `update_fee_schedules(schedules)` | PATCH `/billable_portfolios/relationships/fee_schedules` | `None` |
| `archive_billable_portfolio(billable_portfolio_id)` | DELETE `/billable_portfolios/{id}/relationships/fee_schedules` | `None` |
| `archive_billable_portfolios(portfolio_ids)` | DELETE `/billable_portfolios/relationships/fee_schedules` | `None` |
| `update_payout_rule(portfolio_id, rule_id)` | PATCH `/billable_portfolios/{id}/relationships/payout_rule` | `None` |
| `remove_payout_rule(portfolio_id)` | DELETE `/billable_portfolios/{id}/relationships/payout_rule` | `None` |

Creation requires `schedule_id` and exactly one of `entity_id` / `group_id`.
Bulk input is attribute dictionaries, not JSON:API resources:
`[{"schedule_id": "2", "entity_id": "1", "payout_rule_id": "3"}]`.
Bulk reassignment takes `{portfolio_id: schedule_id}`; reassignment/archive
accept 1–500 portfolios and require the firm feature. Assigning a schedule can
restore an archived portfolio. Lists/iterators accept `limit`, `page_limit`.

## Payouts

Recipients use `client.billing.payout_recipients`; rules use
`client.billing.payout_rules`.

| SDK call | HTTP route | Result |
| --- | --- | --- |
| `get_payout_recipient(recipient_id)` | GET `/billing/payout/recipients/{id}` | Resource |
| `list_payout_recipients(...)`, `iter_payout_recipients(...)` | GET `/billing/payout/recipients` | List / resource iterator |
| `create_payout_recipient(attributes)` | POST `/billing/payout/recipients` | Resource |
| `create_payout_recipients(recipients)` | POST `/billing/payout/recipients` | List |
| `replace_payout_recipient(recipient_id, attributes)` | PUT `/billing/payout/recipients/{id}` | Resource |
| `delete_payout_recipient(recipient_id)` | DELETE `/billing/payout/recipients/{id}` | `None` |
| `delete_payout_recipients(recipient_ids)` | DELETE `/billing/payout/recipients` | `None` |
| `get_payout_rule(rule_id)` | GET `/billing/payout/rules/{id}` | Resource |
| `list_payout_rules(...)`, `iter_payout_rules(...)` | GET `/billing/payout/rules` | List / resource iterator |
| `create_payout_rule(attributes)` | POST `/billing/payout/rules` | Resource |
| `create_payout_rules(rules)` | POST `/billing/payout/rules` | List |
| `replace_payout_rule(rule_id, attributes)` | PUT `/billing/payout/rules/{id}` | Resource |
| `delete_payout_rule(rule_id)` | DELETE `/billing/payout/rules/{id}` | `None` |
| `delete_payout_rules(rule_ids)` | DELETE `/billing/payout/rules` | `None` |

Collections accept `search`, `limit`, `page_limit`; rules also accept
`recipient_ids=[...]`. These wrappers handle plain `offset`/`limit` pagination.
Single writes take attributes; bulk creation takes resource dictionaries with
`attributes` and optional `type` (`payout_recipient` / `payout_rule`). PUT replaces
all attributes. Recipient PUT omits body `id`; rule PUT includes it. Bulk delete
helpers take ID lists. Single responses unwrap one-item arrays when needed.

Rule splits contain recipient IDs, not expanded recipient resources:

```python
rule = client.billing.payout_rules.create_payout_rule({
    "name": "Advisor split",
    "splits": [{"recipient": {"id": recipient_id},
                "distribution_type": "PERCENTAGE", "distribution_amount": 100.0,
                "children": []}],
})
```

Source: [fees/schedules](../addepy/resources/billing/fees.py),
[billable portfolios](../addepy/resources/billing/billable_portfolios.py),
[payouts](../addepy/resources/billing/payouts.py).
