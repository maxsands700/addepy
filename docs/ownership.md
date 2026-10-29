# Ownership

Use `client.ownership`. Routes are relative to the configured API base.
See [client conventions](client.md) for resource returns and pagination.

Entity/group/position collection helpers accept `limit`, `page_limit`, and
`created_before`, `created_after`, `modified_before`, `modified_after`
(`YYYY-MM-DD`). Type collections do not paginate.

## Entities — `client.ownership.entities`

| SDK call | HTTP route | Result |
| --- | --- | --- |
| `get_entity(entity_id)` | GET `/entities/{id}` | Resource |
| `list_entities(...)`, `iter_entities(...)` | GET `/entities` | List / resource iterator |
| `create_entity(original_name, model_type, currency_factor=None, **attributes)` | POST `/entities` | Resource |
| `create_entities(entities, allow_new_investment_types=False)` | POST `/entities` | List |
| `update_entity(entity_id, allow_new_investment_types=False, **attributes)` | PATCH `/entities/{id}` | Resource |
| `update_entities(entities, allow_new_investment_types=False)` | PATCH `/entities` | List |
| `delete_entity(entity_id)` | DELETE `/entities/{id}` | `None` |
| `delete_entities(entity_ids)` | DELETE `/entities` | `None` |
| `get_entity_type(type_id)` | GET `/entity_types/{id}` | Model-type resource |
| `list_entity_types()` | GET `/entity_types` | List |
| `change_model_type(entity_id, new_model_type)` | PATCH `/entity_types` | Update resource |
| `change_model_types(updates)` | PATCH `/entity_types` | Update-resource list |

Additional collection options: `model_types=[...]`, `linking_status="linked"`
or `"unlinked"`, `ids=[...]`, `fields=[...]`; `fields=[]` omits attributes.
Model-type and linking-status filters cannot be combined on the API.

Creation accepts `underlying_type`, `delivery_price`, and
`allow_new_investment_types=False` as keyword options. Currency is required for
non-client entities; forwards/futures require their model-specific fields.
`get_entity_type(type_id)["attributes"]["entity_attributes"]` is an array of
attribute definitions; type IDs use API names such as `bond` or `etf`.

Bulk creation takes flat attribute dictionaries. Bulk updates take flat
`{"id": ..., attribute: value}` dictionaries, not nested `attributes`:

```python
entities = client.ownership.entities
created = entities.create_entities([
    {"original_name": "Example Trust", "model_type": "TRUST", "currency_factor": "USD"}
])
entities.update_entities([{"id": created[0]["id"], "display_name": "Trust"}])
```

Change model types through `change_model_type(s)`, not ordinary attribute PATCH.
Bulk input: `[{"id": "123", "new_model_type": "etf"}]`. Conversion may remove
attributes unsupported by the target model.

Standard/custom attributes pass through. Time-varying values use the Addepar
attribute structure; external IDs are attributes named `external_id_{key}`:

```python
entities.update_entity(
    entity_id,
    external_id_salesforce="crm-123",
    _custom_status_123=[{"date": None, "value": "Active", "weight": 1.0}],
)
```

## Groups — `client.ownership.groups`

| SDK call | HTTP route | Result |
| --- | --- | --- |
| `get_group(group_id)` | GET `/groups/{id}` | Resource |
| `list_groups(...)`, `iter_groups(...)` | GET `/groups` | List / resource iterator |
| `create_group(name, group_type_id="GROUPS", member_ids=None, attributes=None)` | POST `/groups` | Resource |
| `create_groups(groups)` | POST `/groups` | List |
| `update_group(group_id, name=None, attributes=None)` | PATCH `/groups/{id}` | Resource |
| `update_groups(groups)` | PATCH `/groups` | List |
| `delete_group(group_id)` | DELETE `/groups/{id}` | `None` |
| `delete_groups(group_ids)` | DELETE `/groups` | `None` |
| `search_groups(display_names=None, group_types=None, external_ids=None)` | POST `/groups/query` | Matching resource list |
| `get_members(group_id)` | GET `/groups/{id}/relationships/members` | Entity identifier list |
| `get_member_details(group_id, ...)`, `iter_member_details(group_id, ...)` | GET `/groups/{id}/members` | Expanded entity list / iterator |
| `add_members(group_id, entity_ids)` | POST `/groups/{id}/relationships/members` | `None` |
| `replace_members(group_id, entity_ids)` | PATCH `/groups/{id}/relationships/members` | `None`; replaces all members |
| `remove_members(group_id, entity_ids)` | DELETE `/groups/{id}/relationships/members` | `None`; removes selected members |
| `get_child_groups(group_id, ...)`, `iter_child_groups(group_id, ...)` | GET `/groups/{id}/child_groups` | Expanded group list / iterator |
| `add_child_groups(group_id, child_group_ids)` | POST `/groups/{id}/relationships/child_groups` | `None` |
| `replace_child_groups(group_id, child_group_ids)` | PATCH `/groups/{id}/relationships/child_groups` | `None`; replaces all child groups |
| `get_group_type(group_type_id)` | GET `/group_types/{id}` | Resource |
| `list_group_types(is_permissioned_resource=None)` | GET `/group_types` | List |
| `create_group_type(group_type_key, display_name, is_permissioned_resource=True)` | POST `/group_types` | Resource |
| `update_group_type(group_type_id, display_name=None)` | PATCH `/group_types/{id}` | Resource |
| `delete_group_type(group_type_id)` | DELETE `/group_types/{id}` | `None` |

Collection `group_types` and `ids` filters are comma-separated strings;
`search_groups` uses lists. Search external IDs use
`{"external_id_type": "salesforce", "external_id": "crm-123"}`; query APIs use
`external_type_key` instead. Supply at least one search criterion.

Bulk creation items: `{"name": ..., "group_type_id": "GROUPS", "member_ids": [...],
"attributes": {...}}`. Bulk updates: `{"id": ..., "name": ..., "attributes": {...},
"member_ids": [...], "child_group_ids": [...]}`. Custom attributes remain nested
under `attributes`; empty membership lists explicitly replace associations.
Single `update_group` edits attributes only; use relationship methods for members.
Member-detail/child-group list and iterator helpers accept `limit`, `page_limit`.
The built-in `GROUPS` type cannot be edited/deleted.

## Positions — `client.ownership.positions`

| SDK call | HTTP route | Result |
| --- | --- | --- |
| `get_position(position_id)` | GET `/positions/{id}` | Resource |
| `list_positions(...)`, `iter_positions(...)` | GET `/positions` | List / resource iterator |
| `create_position(owner_id, owned_id, **attributes)` | POST `/positions` | Resource |
| `create_positions(positions)` | POST `/positions` | List |
| `update_position(position_id, **attributes)` | PATCH `/positions/{id}` | Resource |
| `update_positions(positions)` | PATCH `/positions` | List |
| `delete_position(position_id)` | DELETE `/positions/{id}` | `None` |
| `delete_positions(position_ids)` | DELETE `/positions` | `None` |
| `get_position_owner(position_id)` | GET `/positions/{id}/owner` | Expanded entity |
| `get_position_owned(position_id)` | GET `/positions/{id}/owned` | Expanded entity |
| `get_position_owner_relationship(position_id)` | GET `/positions/{id}/relationships/owner` | Entity identifier |
| `get_position_owned_relationship(position_id)` | GET `/positions/{id}/relationships/owned` | Entity identifier |

Additional collection filters: `fields`, `owner_model_types`,
`owned_model_types`, `owner_entity_id`, `owned_entity_id`; each takes a list.
`fields=[]` omits attributes. Single creation accepts `name`,
`incepting_open_position_date`, `incepting_open_position_ownership_percentage`,
and custom attribute keywords. Percent-based ownership uses decimal fractions
(`0.5` = 50%); cash positions require a unique name per owner/owned pair.

Bulk creation items require `owner_id`, `owned_id`; known creation fields stay
at the top level, extra attributes go inside `attributes`. Bulk updates instead
take flat `{"id": ..., attribute: value}` dictionaries. Updates edit the
incepting open position; use snapshots/transactions for subsequent balances/flows.

```python
client.ownership.positions.create_positions([{
    "owner_id": owner_id, "owned_id": asset_id,
    "incepting_open_position_date": "2026-01-01",
    "incepting_open_position_ownership_percentage": 0.5,
    "attributes": {"_custom_status_123": [{"value": "Open"}]},
}])
```

## External ID types — `client.ownership.external_ids`

| SDK call | HTTP route | Result |
| --- | --- | --- |
| `get_external_id_type(external_id_type_id)` | GET `/external_id_types/{key}` | Resource |
| `list_external_id_types()` | GET `/external_id_types` | List |
| `create_external_id_type(external_type_key, display_name)` | POST `/external_id_types` | Resource |
| `update_external_id_type(external_id_type_id, display_name)` | PATCH `/external_id_types/{key}` | Resource |
| `delete_external_id_type(external_id_type_id)` | DELETE `/external_id_types/{key}` | `None` |

The type's key is its ID. Create the type, assign `external_id_{key}` on an entity
or group, then query using the matching external-ID dictionary. This resource
manages type definitions, not individual entity/group mappings.

Source: [entities](../addepy/resources/ownership/entities.py),
[groups](../addepy/resources/ownership/groups.py),
[positions](../addepy/resources/ownership/positions.py),
[external ID types](../addepy/resources/ownership/external_ids.py).
