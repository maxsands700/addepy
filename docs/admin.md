# Admin endpoints

Access resources through `client.admin.<resource>`. Paths below are relative to
the configured API base (`.../api/v1`). `id` denotes the resource ID; method
arguments are positional unless shown as `name=...`. Helpers construct JSON:API
envelopes; pass Python arguments, not an outer `data` object, except where stated.
Resource returns are dictionaries; linkage returns contain `id`/`type` only.
See [client conventions](client.md) for pagination, errors, and downloads.

## Audit — `audit`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `get_audit_entry(id)` | GET `/audit_trail/{id}` | Resource |
| `query_login_attempts(start_date=None, end_date=None, ...)` | POST `/audit_trail`, `object_type="login_attempt"` | List, all pages |
| `query_attribute_changes(start_date=None, end_date=None, ...)` | POST `/audit_trail`, `object_type="attribute"` | List, all pages |
| `query_transaction_changes(start_date=None, end_date=None, ...)` | POST `/audit_trail`, `object_type="transaction"` | List, all pages |
| `query_permission_changes(start_date=None, end_date=None, ...)` | POST `/audit_trail`, `object_type="permission"` | List, all pages |

All queries accept `actions`, `user_type`, `users`, `page_limit=500`.
Actions: `["Add", "Modify", "Remove"]`; login attempts support `Add`. User types:
`firmusers`, `addeparusers`, `anyone`, `custom`; supply `users=[id, ...]` for
`custom`. Dates accept `YYYY-MM-DD` or timezone-qualified timestamps. Omitted
dates use server defaults: neither means today; one date supplies both bounds.
Report-change history has no API wrapper because the API does not expose it.

## Client Portal — `client_portal`

`publish_files(files_id, portal_publishing, contact_notification,
publish_override_contact_ids=None)` → POST `/portal/publish_files` → result list.
`files_id` is a list of integer file IDs, up to 500 per API request. Publishing:
`do_not_publish`, `use_contact_preference`, `publish`; notifications:
`do_not_notify`, `use_contact_preference`, `notify`. SDK uppercases both values.
Override contacts are integer IDs. HTTP 200 can contain partial failures: inspect
each result's `publish_status`, `notify_status`, and `error`.

## Contacts — `contacts`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `get_contact(id)` | GET `/contacts/{id}` | Resource |
| `list_contacts(...)`, `iter_contacts(...)` | GET `/contacts` | List / iterator |
| `create_contact(first_name, last_name, ...)` | POST `/contacts` | Resource |
| `update_contact(id, ...)` | PATCH `/contacts/{id}` | Resource |
| `delete_contact(id)` | DELETE `/contacts/{id}` | `None` |

Create/update optional keywords: `title`, `suffix`, `login_email`,
`external_user_id`, `birthday`, `employer`, `occupation`, `ssn`,
`mailing_addresses`, `emails`, `phone_numbers`, `family_members`,
`default_affiliation`; update also accepts `first_name`, `last_name`.
`None` omits a field. Nested input shapes:

```python
emails=[{"email": "person@example.com", "email_type": "WORK"}]
phone_numbers=[{"number": "+12125550123", "phone_type": "CELL"}]
mailing_addresses=[{"street": "1 Main St", "city": "New York", "state": "NY", "zip": "10001"}]
family_members=[{"first_name": "Sam", "last_name": "Lee", "relationship": "Spouse"}]
default_affiliation={"entity_id": "123", "group_id": None}
```

Affiliation methods receive `contact_id` first, then the specified ID list.
Relationship writes return `None`; getters return linkage lists or a nullable
single identifier.

| Methods | Verbs, in method order | Endpoint suffix after `/contacts/{contact_id}` |
| --- | --- | --- |
| `get_entity_affiliations`, `add_entity_affiliations`, `replace_entity_affiliations`, `remove_entity_affiliations` | GET, POST, PATCH, DELETE | `/relationships/entity_affiliations`; writes take `entity_ids` |
| `get_group_affiliations`, `add_group_affiliations`, `replace_group_affiliations`, `remove_group_affiliations` | GET, POST, PATCH, DELETE | `/relationships/group_affiliations`; writes take `group_ids` |
| `get_default_view_set`, `set_default_view_set`, `remove_default_view_set` | GET, POST, DELETE | `/relationships/default_view_set`; setter takes `view_set_id` |
| `get_team`, `replace_team`, `remove_team` | GET, PATCH, DELETE | `/relationships/team`; replacement takes `team_id` |
| `invite_to_portal` | POST | `/invite` |
| `restore_portal_access`, `revoke_portal_access` | PATCH, PATCH | `/restore`, `/revoke` |
| `exempt_from_2fa`, `require_2fa` | PATCH, PATCH | `/exempt_two_factor_authentication`, `/require_two_factor_authentication` |
| `enable_sso`, `disable_sso` | PATCH, PATCH | `/enable_saml`, `/disable_saml`; enable takes `saml_user_id` |

Portal/security methods receive `contact_id` and return `None`. Use these methods
for read-only contact fields such as portal access and SAML settings.

## Files — `files`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `get_file(id, ...)` | GET `/files/{id}` | Resource |
| `list_files(...)`, `iter_files(...)` | GET `/files` | List / iterator |
| `upload_file(file_data, name, ...)` | POST `/files`, multipart | Resource |
| `update_file(id, name=None, parent_folder_id=None)` | PATCH `/files/{id}` | Resource |
| `delete_file(id)` | DELETE `/files/{id}` | `None` |
| `download_file(id)`, `download_file_to(id, path, overwrite=False)` | GET `/files/{id}/download` | Bytes / `Path` |
| `get_archived_file(id)` | GET `/archive/files/{id}` | Resource |
| `list_archived_files(...)`, `iter_archived_files(...)` | GET `/archive/files` | List / iterator |
| `download_archived_file(id)`, `download_archived_file_to(id, path, overwrite=False)` | GET `/archive/files/{id}/download` | Bytes / `Path` |

`get_file` and both collection families accept `created_after`, `created_before`,
`entity_id`, `group_id`, `included_objects`, `parent_folder_id`; collections also
accept pagination arguments. Dates are ISO 8601. Included objects:
`FILES_ONLY`, `FOLDERS_ONLY`, `FILES_AND_FOLDERS`. Query keys use
`filter[files][<name>]`: `createdAfter`, `createdBefore`, `entityId`, `groupId`,
`includedObjects`, `parentFolderId`.
The API gives `entity_id` precedence when both entity/group filters are supplied.

Upload accepts bytes or a **string local pathname** (`str(path)` for `Path`).
`name` includes the extension. Optional `parent_folder_id` / `file_path` locate
the **remote folder**; `entity_ids`, `group_ids` create associations. The SDK
builds multipart `file` and JSON `metadata` parts.

| Methods | Verbs, in method order | Endpoint suffix after `/files/{file_id}` |
| --- | --- | --- |
| `get_associated_entities`, `add_associated_entities`, `replace_associated_entities`, `remove_associated_entities` | GET, POST, PATCH, DELETE | `/relationships/associated_entities`; writes take `entity_ids` |
| `get_associated_groups`, `add_associated_groups`, `replace_associated_groups`, `remove_associated_groups` | GET, POST, PATCH, DELETE | `/relationships/associated_groups`; writes take `group_ids` |

Association getters return linkage lists; writes return `None`.

## Import Tool — `import_tool`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `create_import(import_dataframe, import_type, is_dry_run=True, ignore_warnings=False)` | POST `/imports`; DELETE for `DELETE_TRANSACTIONS` | Import ID string |
| `get_import_status(import_id)` | GET `/imports/{import_id}` | Status string |
| `get_import_results(import_id)` | GET `/import_results/{import_id}` | `{digests, warnings, errors}` |
| `execute_import(import_dataframe, import_type, ...)` | Create → poll → results | `{digests, warnings, errors}` |

Import data: CSV text, UTF-8 bytes, `Path`, readable file, or DataFrame. A string
is CSV content; use `Path` for filenames. DataFrames serialize without their
index and require the optional `dataframe` install extra. Requests send
`Content-Type: text/plain`, `Accept: application/json`; import options are query
parameters. Types are uppercased; unknown values are rejected locally.

Accepted types: `ATTRIBUTES`, `BENCHMARKS`, `BENCHMARK_ASSOCIATIONS`,
`BENCHMARK_PROXIES`, `CONSTITUENT_ATTRIBUTES`, `CONSTITUENTS`, `CONTACTS`,
`COST_BASIS`, `DELETE_TRANSACTIONS`, `ESTIMATED_RETURNS`, `GROUPS`,
`HISTORICAL_PRICES`, `MANAGE_INVESTMENTS`, `MANAGE_OWNERSHIP`, `MANUAL_ADJUSTMENTS`,
`POSITION_VALUATIONS`, `SUMMARY_DATA`, `TARGET_ALLOCATIONS`,
`TOTAL_OUTSTANDING_SHARES`, `TRANSACTIONS`, `VALUES_AND_FLOWS`.

```python
from pathlib import Path

result = client.admin.import_tool.execute_import(Path("attributes.csv"), "ATTRIBUTES")
print(result["digests"], result["warnings"], result["errors"])
```

`is_dry_run=False` submits changes. `execute_import` also accepts
`initial_wait=30`, `max_wait=300`, `backoff_factor=1.5`, `timeout=1200`.
It returns reviewable warning/error results; `VALIDATION_FAILED` or
`IMPORT_FAILED` raises `AddePyError`. Keep the ID from `create_import` for manual
status/results retrieval; execution does not provide a separate resume helper.

## Reports — `reports`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `list_reports(...)`, `iter_reports(...)` | GET `/reports` | List / iterator |
| `create_report_generation_job(report_id, portfolios, start_date, end_date, ...)` | POST `/report_generation_job` | Job resource |
| `get_generated_report(job_id)` | GET `/generated_reports/{job_id}` | Resource with status |
| `list_generated_reports(...)`, `iter_generated_reports(...)` | GET `/generated_reports` | List / iterator |
| `get_report_creator(job_id)` | GET `/generated_reports/{job_id}/creator` | User resource |
| `get_zipped_file(job_id)` | GET `/generated_reports/{job_id}/zipped_file` | File metadata resource |
| `download_zipped_file(job_id)`, `download_zipped_file_to(job_id, path, overwrite=False)` | GET `/generated_reports/{job_id}/zipped_file/download` | Bytes / `Path` |

Report-list filters: `created_after`, `created_before`, `modified_after`,
`modified_before`, `name`, `entity_id`, `group_id`; pagination includes
`page_after` and `page_limit` capped at 500. Generated-report filters:
`completed_after`, `completed_before`, `status`, `entity_id`, `group_id`;
`page_size=50` uses zero-based `page[number]`. `status` accepts comma-separated
`FINISHED`, `ERROR`, `CANCELED`. Poll generated reports explicitly; there is no
report-generation wait helper.

```python
job = client.admin.reports.create_report_generation_job(
    report_id="42", portfolios=[{"portfolio_type": "entity", "portfolio_id": "22"}],
    start_date="2026-01-01", end_date="2026-03-31",
)
generated = client.admin.reports.get_generated_report(job["id"])
print(generated["attributes"]["status"])
```

Portfolio types are `entity` / `group`. Optional generation arguments:
`portal_publishing` (`PUBLISH`, `DO_NOT_PUBLISH`, `USE_CONTACT_PREFERENCE`),
`contact_notification` (`NOTIFY`, `DO_NOT_NOTIFY`, `USE_CONTACT_PREFERENCE`),
`label=[integer_id, ...]`, `brand_id` (team ID). Values pass through unchanged.

## Report schedules — `report_schedules`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `get_schedule(id)` | GET `/report_schedule/{id}` | Resource |
| `list_schedules(...)`, `iter_schedules(...)` | GET `/report_schedule` | List / iterator |
| `create_schedule(attributes)` | POST `/report_schedule` | Resource |
| `update_schedule(id, attributes)` | PATCH `/report_schedule/{id}` | Resource |
| `delete_schedule(id)` | DELETE `/report_schedule/{id}` | `None` |
| `execute_schedule(id, payload)` | POST `/report_schedule/{id}/execute` | Complete JSON document |
| `list_executions(id, ...)`, `iter_executions(id, ...)` | GET `/report_schedule/{id}/relationships/executions` | Linkage list / iterator |

Route is singular; resource type is `report_schedules`. Creation attributes
include `report_id`, `portfolio_id`, `frequency`, `start_date`, `time`, plus
API options. Dictionaries pass through; update preserves explicit nulls.
Listing accepts raw query names through `params`. Execution requires a complete
JSON:API `payload`; the SDK does not invent execution attributes/type. Schedule
dates/times use the firm's timezone. Execution getters return identifiers,
not expanded job resources.

## Roles — `roles`

| Methods | Verbs, in method order | HTTP endpoint / result |
| --- | --- | --- |
| `get_role(id)` | GET | `/roles/{id}` → resource |
| `list_roles(...)`, `iter_roles(...)` | GET | `/roles` → list / iterator |
| `get_assigned_users(id)` | GET | `/roles/{id}/relationships/assigned_users` → linkage list |
| `get_assigned_user_details(id, ...)`, `iter_assigned_user_details(id, ...)` | GET | `/roles/{id}/assigned_users` → expanded user list / iterator |
| `assign_users(id, user_ids)`, `replace_assigned_users(id, user_ids)`, `remove_users(id, user_ids)` | POST, PATCH, DELETE | `/roles/{id}/relationships/assigned_users` → `None` |

## Teams — `teams`

| Methods | Verbs, in method order | HTTP endpoint / result |
| --- | --- | --- |
| `get_team(id)` | GET | `/teams/{id}` → resource |
| `list_teams(...)`, `iter_teams(...)` | GET | `/teams` → list / iterator; optional `ids="1,2"` |
| `create_team(name, member_ids=None)` | POST | `/teams` → resource |
| `update_team(id, name=None, member_ids=None)` | PATCH | `/teams/{id}` → resource |
| `delete_team(id)` | DELETE | `/teams/{id}` → `None` |
| `get_members(id)` | GET | `/teams/{id}/relationships/members` → linkage list |
| `add_members(id, user_ids)`, `replace_members(id, user_ids)`, `remove_members(id, user_ids)` | POST, PATCH, DELETE | `/teams/{id}/relationships/members` → `None` |

`member_ids` are user IDs; supplied lists replace membership on create/update.

## Users — `users`

| Methods | Verbs, in method order | HTTP endpoint / result |
| --- | --- | --- |
| `get_user(id)`, `get_current_user()` | GET, GET | `/users/{id}`, `/users/me` → resource |
| `list_users(...)`, `iter_users(...)` | GET | `/users` → list / iterator |
| `create_user(email, login_method="email_password", ...)` | POST | `/users` → resource |
| `update_user(id, ...)`, `delete_user(id)` | PATCH, DELETE | `/users/{id}` → resource / `None` |
| `get_users_by_email(emails)` | POST | `/users/email_query` → list; wraps `email_ids` |
| `get_users_by_external_id(external_ids)` | POST | `/users/external_user_id_query` → list; wraps `external_user_ids` |
| `get_user_assigned_role(id)`, `update_user_role(id, role_id)` | GET, PATCH | `/users/{id}/relationships/assigned_role` → nullable linkage / `None` |
| `get_permissioned_entities(id)`, `add_permissioned_entities(id, entity_ids)`, `remove_permissioned_entities(id, entity_ids)` | GET, POST, DELETE | `/users/{id}/relationships/permissioned_entities` → linkage list / `None` / `None` |
| `get_permissioned_groups(id)`, `add_permissioned_groups(id, group_ids)`, `remove_permissioned_groups(id, group_ids)` | GET, POST, DELETE | `/users/{id}/relationships/permissioned_groups` → linkage list / `None` / `None` |

Create/update optional keywords: `first_name`, `last_name`, `admin_access`,
`all_data_access`, `external_user_id`. Creation also accepts `saml_user_id`,
required with `login_method="saml"`; access flags default false. Update does not
change email/login method/SAML ID. Explicit false updates revoke the
corresponding access flag. Role assignment uses `update_user_role`.

## Target allocations — `target_allocations`

| Methods | Verbs, in method order | HTTP endpoint / result |
| --- | --- | --- |
| `get_allocation_model(id)` | GET | `/allocation_models/{id}` → resource |
| `list_allocation_models(...)`, `iter_allocation_models(...)` | GET | `/allocation_models` → list / iterator |
| `create_allocation_model(name, attribute_ids)` | POST | `/allocation_models` → resource |
| `update_allocation_model(id, name)`, `delete_allocation_model(id)` | PATCH, DELETE | `/allocation_models/{id}` → resource / `None` |
| `get_allocation_template(id)` | GET | `/allocation_templates/{id}` → resource |
| `list_allocation_templates(...)`, `iter_allocation_templates(...)` | GET | `/allocation_templates` → list / iterator |
| `create_allocation_template(model_id, name, allocation_intervals, description=None)` | POST | `/allocation_templates` → resource |
| `update_allocation_template(id, name=None, description=None, allocation_intervals=None)` | PATCH | `/allocation_templates/{id}` → resource |
| `replace_allocation_template(id, model_id, name, allocation_intervals, description=None)` | PUT | `/allocation_templates/{id}` → resource; full replacement |
| `delete_allocation_template(id)` | DELETE | `/allocation_templates/{id}` → `None` |

Model `attribute_ids` and template `model_id` are immutable. Deleting a model
also deletes its templates. Intervals are lists of dictionaries containing
`allocations`; allocation nodes contain `parent_id`, `attribute_id`,
`attribute_value`, `target_allocation`, optional `min_allocation` /
`max_allocation`, and `children`. Named `None` arguments are omitted; use raw
requests if an API operation requires explicit nulls unsupported by the helper.

## View sets — `view_sets`

`get_view_set(id)` → GET `/view_sets/{id}` → resource.
`list_view_sets(...)`, `iter_view_sets(...)` → GET `/view_sets` → list / iterator.
