# Audit

Audit logs track changes to attribute values, transactions, reports, and user roles and permissions. Each entry in a log represents an addition, modification, or deletion.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/3b94b0e-updated_audit_log.png",
"3b94b0e-updated_audit_log.png",
3104,
1948,
"#000000",
null,
"651191a8950ad700250157e6"
],
"caption": ""
}
]
}
[/block]
Audit logs can be downloaded directly in the application, or you can use the Audit API to retrieve the information.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"2-0": "Produces",
"3-0": "Pagination",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" and \"Manage firm settings: Audit logs\"",
"3-1": "Yes",
"2-1": "JSON",
"0-1": "/v1/audit_trail",
"1-1": "**GET**\n/v1/audit_trail/:id\n\n**POST**\n/v1/audit_trail",
"1-0": "Endpoints",
"5-0": "OAuth Scopes",
"5-1": "`AUDIT_TRAIL`"
},
"cols": 2,
"rows": 6
}
[/block]
[block:html]
{
"html": "<div><br></br></div>\n\n<style></style>"
}
[/block]
[block:api-header]
{
"title": "See login attempts"
}
[/block]
**POST** `/v1/audit_trail`

Retrieves a list of attempts by each user to sign into the application, Help Center, or Client Portal using Addepar credentials, SSO, or two-factor authentication.

**Example**
[block:code]
{
"codes": [
{
"code": "POST https://examplefirm.addepar.com/api/v1/audit_trail\n\n{\n \"data\": {\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"object_type\": \"login_attempt\",\n \"start_date\": \"2021-03-26\",\n \"end_date\": \"2021-03-30\"\n }\n }\n}",
"language": "json",
"name": "Request"
},
{
"code": "{\n \"data\": [\n {\n \"id\": \"AXhvvXcZjFzsG3PMeBgm\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"performed_by_user_id\": \"993434\",\n \"action\": \"login_attempt\",\n \"source\": \"Manual\",\n \"timestamp\": \"2021-03-26T18:13:11.059332Z\",\n \"status\": \"successful\"\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXhvvXcZjFzsG3PMeBgm\"\n }\n }\n ],\n \"included\": [],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Request objects**
[block:parameters]
{
"data": {
"0-0": "`object_type`",
"h-0": "Request Object",
"h-1": "Description",
"h-2": "Example",
"0-2": "`login_attempt`",
"0-1": "Required. Type of audit log you're retrieving. \n\nValid input:\n`login_attempt`",
"1-0": "`start_date`",
"2-0": "`end_date`",
"1-2": "`2021-03-26`",
"1-1": "Required. First date of the time period you want to audit.\n\nValid formats:\n`YYYY-MM-DD` Example: 2021-01-01. Timezone is assumed to be UTC.\n `YYYY-MM-DDThh:mm:ss` followed by a timezone. Example 1: 2021-01-01T00:00:00Z timezone is UTC as specified by \"Z\". Example 2: 2021-01-01T00:00:00-05:00 timezone is EST as specified by offset -05:00.\n\nIf both `start_date` and `end_date` are missing, the time period will be today only. If one of them is missing, it will be set to equal the other one.\n\nYou must specify both `start_date` and `end_date` if you want to use the `YYYY-MM-DDThh:mm:ss` format.",
"2-1": "Required. Last date of the time period you want to audit.\n\nValid formats:\n`YYYY-MM-DD` Example: 2021-01-01. Timezone is assumed to be UTC.\n `YYYY-MM-DDThh:mm:ss` followed by a timezone. Example 1: 2021-01-01T00:00:00Z timezone is UTC as specified by \"Z\". Example 2: 2021-01-01T00:00:00-05:00 timezone is EST as specified by offset -05:00.\n\nIf both `start_date` and `end_date` are missing, the time period will be today only. If one of them is missing, it will be set to equal the other one.\n\nYou must specify both `start_date` and `end_date` if you want to use the `YYYY-MM-DDThh:mm:ss` format.",
"2-2": "`2021-03-30`",
"3-0": "`actions`",
"3-1": "Operation performed. \n\nValid input: \n`Add` \n\nIf missing or empty, all actions will be included.",
"4-0": "`user_type `",
"4-1": "Valid inputs:\n`firmusers` includes users at your firms\n`addeparusers` includes Addepar employees\n`anyone` includes all firm users and Addepar employees\n`custom` allows you to specify certain `users`",
"5-0": "`users`",
"5-1": "List of IDs for the specific users you want to query. If `user_type: custom` but no users are specified, then all firm users will be included."
},
"cols": 2,
"rows": 6
}
[/block]
**Response objects**
[block:parameters]
{
"data": {
"2-0": "`source`",
"2-1": "`Manual` indicates that the action was performed manually in the application. `Import` indicates the action was performed using the Import Tool.",
"2-2": "`Manual`",
"h-0": "Response Object",
"h-1": "Description",
"h-2": "Example",
"0-0": "`action`",
"0-1": "Operation performed.",
"0-2": "`login_attempt`",
"4-0": "`timestamp`",
"4-1": "Date and time the attempt was made ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format) based on your firm's timezone.",
"4-2": "`2021-03-26T18:13:11.059332Z`",
"3-0": "`status`",
"3-1": "Indicates whether the attempt was successful.\n\nOutputs for attempts using Addepar credentials:\n `locked_out`\n`password_incorrect`\n`successful`\n`username_invalid`\n\nOutputs for attempts using SSO:\n`sso_successful`\n`sso_token_incorrect`\n\nOutputs for attempts using two-factor authentication:\n` two_factor_code_incorrect```\n `two_factor_successful` \n````two_factor_username_invalid `",
"1-0": "`performed_by_user_id`",
"1-1": "User ID of the person who attempted to sign in."
},
"cols": 2,
"rows": 5
}
[/block]
**Response codes:**

- 200 OK: Success
- 403 Forbidden: User does not have permission to see audit trails
  [block:api-header]
  {
  "title": "See changes to attribute values"
  }
  [/block]
  **POST** /v1/audit_trail

Retrieves a list user changes to attribute values applied at the asset- and position-level. You have the option to specify which actions you want to query.

**Example**
[block:code]
{
"codes": [
{
"code": "POST https://examplefirm.addepar.com/api/v1/audit_trail\n\n{\n \"data\": {\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"object_type\": \"attribute\",\n \"start_date\": \"2021-02-01\",\n \"end_date\": \"2021-02-02\",\n \"actions\": [\"Add\"]\n }\n }\n}",
"language": "json",
"name": "Request"
},
{
"code": "{\n \"data\": [\n {\n \"id\": \"AXdjWf3wBGo8qwhMY-GY\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"entity_type\": \"FINANCIAL_ACCOUNT\",\n \"entity_name\": \"Ami Smith IRA\",\n \"performed_by_user_id\": \"429647\",\n \"action\": \"add_entity_attribute\",\n \"attribute_name\": \"displayName\",\n \"old_value\": {},\n \"source\": \"Manual\",\n \"object_id\": 1521518,\n \"new_value\": {\n \"value\": \"Ami Smith IRA\"\n },\n \"timestamp\": \"2021-02-02T15:26:18.093818Z\"\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXdjWf3wBGo8qwhMY-GY\"\n }\n },\n {\n \"id\": \"AXVWDBrDBGo8qwhMU1Qq\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"performed_by_user_id\": \"489308\",\n \"owner_id\": 9172603,\n \"action\": \"add_position_attribute\",\n \"attribute_name\": \"Position name\",\n \"old_value\": {},\n \"source\": \"Manual\",\n \"object_id\": 67285723,\n \"owned_id\": 9172604,\n \"new_value\": {},\n \"timestamp\": \"2020-02-02T15:20:35.254635Z\"\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXVWDBrDBGo8qwhMU1Qq\"\n }\n },\n \"included\": [],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Request objects**
[block:parameters]
{
"data": {
"0-0": "`object_type`",
"1-0": "`start_date`",
"2-0": "`end_date`",
"3-0": "`actions`",
"3-1": "Operation performed. \n\nValid inputs: \n`Add` \n`Modify` \n`Remove`\n\nIf missing or empty, all actions will be included.",
"1-1": "Required. First date of the time period you want to audit.\n\nValid formats:\n`YYYY-MM-DD` Example: 2021-01-01. Timezone is assumed to be UTC.\n `YYYY-MM-DDThh:mm:ss` followed by a timezone. Example 1: 2021-01-01T00:00:00Z timezone is UTC as specified by \"Z\". Example 2: 2021-01-01T00:00:00-05:00 timezone is EST as specified by offset -05:00.\n\nIf both `start_date` and `end_date` are missing, the time period will be today only. If one of them is missing, it will be set to equal the other one.\n\nYou must specify both `start_date` and `end_date` if you want to use the `YYYY-MM-DDThh:mm:ss` format.",
"2-1": "Required. Last date of the time period you want to audit.\n\nValid formats:\n`YYYY-MM-DD` Example: 2021-01-01. Timezone is assumed to be UTC.\n `YYYY-MM-DDThh:mm:ss` followed by a timezone. Example 1: 2021-01-01T00:00:00Z timezone is UTC as specified by \"Z\". Example 2: 2021-01-01T00:00:00-05:00 timezone is EST as specified by offset -05:00.\n\nIf both `start_date` and `end_date` are missing, the time period will be today only. If one of them is missing, it will be set to equal the other one.\n\nYou must specify both `start_date` and `end_date` if you want to use the `YYYY-MM-DDThh:mm:ss` format.",
"0-1": "Required. Type of audit log you're retrieving. \n\nValid input: \n`attribute`",
"h-0": "Request Object",
"h-1": "Description",
"h-2": "Example",
"1-2": "",
"4-0": "`user_type `",
"5-0": "`users`",
"4-1": "Valid inputs:\n`firmusers` includes users at your firms\n`addeparusers` includes Addepar employees\n`anyone` includes all firm users and Addepar employees\n`custom` allows you to specify certain `users`",
"5-1": "List of IDs for the specific users you want to query. If `user_type: custom` but no users are specified, then all firm users will be included."
},
"cols": 2,
"rows": 6
}
[/block]
**Response objects**
[block:parameters]
{
"data": {
"15-0": "`timestamp`",
"15-1": "Date and time the change was made ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format) based on your firm's timezone.",
"15-2": "`2020-08-14T21:25:52.739226Z`",
"3-0": "`entity_type`",
"7-0": "`owned_id`",
"14-0": "`source`",
"14-1": "`Manual` indicates that the action was performed manually in the application. `Import` indicates the action was performed using the Import Tool.",
"14-2": "`Manual`",
"3-1": "Type of entity. Only applicable for changes to attributes at the entity-level.",
"7-1": "Unique identifier of the asset where the attribute is applied. Only applicable for changes to attributes at the position-level.",
"3-2": "`FINANCIAL_ACCOUNT`",
"7-2": "`Abc Def LP`",
"h-0": "Response Object",
"h-1": "Description",
"h-2": "Example",
"9-0": "`owned_type`",
"10-0": "`owner_id`",
"11-0": "`owner_name`",
"12-0": "`owner_type`",
"10-1": "Unique identifier of the entity that directly owns the asset where the attribute is applied. Only applicable for changes to attributes at the position-level.",
"9-1": "Type of entity where the attribute is applied. Only applicable for changes to attributes at the position-level.",
"11-1": "Name of the entity that directly owns the asset where the attribute is applied. Only applicable for changes to attributes at the position-level.",
"12-1": "Name of the entity that directly owns the asset where the attribute is applied. Only applicable for changes to attributes at the position-level.",
"13-0": "`performed_by_user_id`",
"13-1": "User ID of the person who made the change.",
"0-0": "`action`",
"0-1": "Operation performed. \n\nOutputs for changes to attributes applied at the entity-level:\n`add_entity_attribute`\n`modify_entity_attribute`\n`remove_entity_attribute`\n\nOutputs for changes to attributes applied at the position-level:\n`add_position_attribute`\n`modify_position_attribute`\n`remove_position_attribute`",
"1-0": "`attribute_name`",
"1-1": "Name of the attribute.",
"2-0": "`entity_name`",
"2-1": "Name of the entity. Only applicable for changes to attributes at the entity-level.",
"8-0": "`owned_name`",
"8-1": "Name of the asset where the attribute is applied. Only applicable for changes to attributes at the position-level.",
"5-0": "`object_id`",
"5-1": "Attribute's unique identifier.",
"6-0": "`old_value`",
"6-1": "Value before the change was made. Empty for add_entity_attribute and add_position_attribute actions.",
"4-0": "`new_value`",
"4-1": "Value after the change was made. Empty for remove_entity_attribute and remove_position_attribute actions."
},
"cols": 2,
"rows": 16
}
[/block]
**Response codes:**

- 200 OK: Success
- 403 Forbidden: User does not have permission to see audit trails
  [block:api-header]
  {
  "title": "See changes to transactions, snapshots, and valuations"
  }
  [/block]
  **POST** /v1/audit_trail

Retrieves a list user changes to transactions, snapshots, and valuations. You have the option to specify which actions you want to query.

**Example**
[block:code]
{
"codes": [
{
"code": "POST https://examplefirm.addepar.com/api/v1/audit_trail\n\n{\n \"data\": {\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"object_type\": \"transaction\",\n \"start_date\": \"2021-03-15\",\n \"end_date\": \"2021-04-30\",\n \"actions\": [\"Modify\"]\n }\n }\n}",
"language": "json",
"name": "Request"
},
{
"code": "{\n \"data\": [\n {\n \"id\": \"AXkTzXRPIxTCzqh13ZoS\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"transaction_id\": \"1050036245\",\n \"performed_by_user_id\": \"568215\",\n \"action\": \"modify_transaction\",\n \"old_value\": {\n \"values\": {\n \"base\": 5000000.0\n },\n \"units\": {\n \"cash\": 5000000.0\n }\n },\n \"source\": \"Manual\",\n \"new_value\": {\n \"values\": {\n \"base\": 5100000.0\n },\n \"units\": {\n \"cash\": 5100000.0\n }\n },\n \"timestamp\": \"2021-04-27T14:48:22.329990Z\"\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXkTzXRPIxTCzqh13ZoS\"\n }\n },\n {\n \"id\": \"AXMlgAy1adBDjZjM5RMX\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"performed_by_user_id\": \"589138\",\n \"action\": \"modify_snapshot\",\n \"old_value\": {\n \"entities\": {\n \"owner_id\": 3433411,\n \"owned_id\": 3433415\n },\n \"values\": {\n \"base\": 397831.61\n },\n \"comment\": \"\"\n },\n \"source\": \"Manual\",\n \"new_value\": {\n \"entities\": {\n \"owner_id\": 3433411,\n \"owned_id\": 3433415\n },\n \"values\": {\n \"base\": 397832.61\n },\n \"comment\": \"Test Edit\"\n },\n \"timestamp\": \"2020-04-27T19:00:15.668508Z\"\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXMlgAy1adBDjZjM5RMX\"\n }\n },\n {\n \"id\": \"AXkTzmpFIxTCzqh13ZoT\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"performed_by_user_id\": \"568215\",\n \"action\": \"modify_valuation\",\n \"old_value\": {\n \"entities\": {\n \"owner_id\": 1304930,\n \"owned_id\": 3444734\n },\n \"values\": {\n \"base\": 8000002.0\n }\n },\n \"source\": \"Manual\",\n \"new_value\": {\n \"entities\": {\n \"owner_id\": 1304930,\n \"owned_id\": 3444734\n },\n \"values\": {\n \"base\": 8000003.0\n }\n },\n \"timestamp\": \"2021-04-27T14:49:25.311221Z\"\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXkTzmpFIxTCzqh13ZoT\"\n }\n }\n ],\n \"included\": [],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Request objects**
[block:parameters]
{
"data": {
"h-0": "Request Object",
"h-1": "Description",
"0-0": "`object_type`",
"1-0": "`start_date`",
"2-0": "`end_date`",
"3-0": "`actions`",
"2-1": "Required. Last date of the time period you want to audit.\n\nValid formats:\n`YYYY-MM-DD` Example: 2021-01-01. Timezone is assumed to be UTC.\n `YYYY-MM-DDThh:mm:ss` followed by a timezone. Example 1: 2021-01-01T00:00:00Z timezone is UTC as specified by \"Z\". Example 2: 2021-01-01T00:00:00-05:00 timezone is EST as specified by offset -05:00.\n\nIf both `start_date` and `end_date` are missing, the time period will be today only. If one of them is missing, it will be set to equal the other one.\n\nYou must specify both `start_date` and `end_date` if you want to use the `YYYY-MM-DDThh:mm:ss` format.",
"1-1": "Required. First date of the time period you want to audit.\n\nValid formats:\n`YYYY-MM-DD` Example: 2021-01-01. Timezone is assumed to be UTC.\n `YYYY-MM-DDThh:mm:ss` followed by a timezone. Example 1: 2021-01-01T00:00:00Z timezone is UTC as specified by \"Z\". Example 2: 2021-01-01T00:00:00-05:00 timezone is EST as specified by offset -05:00.\n\nIf both `start_date` and `end_date` are missing, the time period will be today only. If one of them is missing, it will be set to equal the other one.\n\nYou must specify both `start_date` and `end_date` if you want to use the `YYYY-MM-DDThh:mm:ss` format.",
"0-1": "Required. Type of audit log you're retrieving. \n\nValid input: \n`transaction`",
"3-1": "Operation performed. \n\nValid inputs: \n`Add` \n`Modify` \n`Remove`\n\nIf missing or empty, all actions will be included.",
"4-0": "`user_type `",
"5-0": "`users`",
"4-1": "Valid inputs:\n`firmusers` includes users at your firms\n`addeparusers` includes Addepar employees\n`anyone` includes all firm users and Addepar employees\n`custom` allows you to specify certain `users`",
"5-1": "List of IDs for the specific users you want to query. If `user_type: custom` but no users are specified, then all firm users will be included."
},
"cols": 2,
"rows": 6
}
[/block]
**Response objects**
[block:parameters]
{
"data": {
"5-0": "`timestamp`",
"5-1": "Date and time the change was made ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format) based on your firm's timezone.",
"5-2": "`2021-04-27T14:48:22.329990Z`",
"h-0": "Response Object",
"h-1": "Description",
"h-2": "Example",
"1-0": "`new_value`",
"1-2": "`modify_transaction`",
"1-1": "Value after the change was made. Empty for the following actions:\n`remove_transaction`\n`remove_snapshot`\n`remove_valuation`",
"2-0": "`old_value`",
"2-1": "Value before the change was made. Empty for the following actions:\n`add_transaction`\n`add_snapshot`\n`add_valuation`",
"2-2": "values:base is `5000000.0 `\n\nunits: cash is `5000000.0 `",
"3-0": "`performed_by_user_id`",
"3-1": "User ID of the person who made the change.",
"3-2": "`Manual`",
"0-0": "`action`",
"0-1": "Operation performed. \n\nOutputs for changes to transactions:\n`add_transaction`\n`modify_transaction`\n`remove_transaction`\n\nOutputs for changes to snapshots:\n`add_snapshot`\n`modify_snapshot`\n`remove_snapshot`\n\nOutputs for changes to valuations:\n`add_valuation`\n`modify_valuation`\n`remove_valuation`",
"4-0": "`source`",
"4-1": "`Manual` indicates that the action was performed manually in the application. `Import` indicates the action was performed using the Import Tool.",
"6-0": "`transaction_id`",
"6-1": "Unique identifier of the transaction. Only applicable for changes to transactions, not snapshots or valuations."
},
"cols": 2,
"rows": 7
}
[/block]
**Response codes:**

- 200 OK: Success
- 403 Forbidden: User does not have permission to see audit trails
  [block:api-header]
  {
  "title": "See changes to reports"
  }
  [/block]
  The Audit API is not currently available to retrieve changes to reports. You must use pull these audit logs directly from the application.
  [block:api-header]
  {
  "title": "See changes to roles and permissions"
  }
  [/block]
  **POST** /v1/audit_trail

Retrieves a list user changes to roles and user permissions.

**Example**
[block:code]
{
"codes": [
{
"code": "POST https://examplefirm.addepar.com/api/v1/audit_trail\n\n{\n \"data\": {\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"object_type\": \"permission\",\n \"start_date\": \"2021-03-15\",\n \"end_date\": \"2021-03-30\"\n }\n }\n}",
"language": "json",
"name": "Request"
},
{
"code": "{\n \"data\": [\n {\n \"id\": \"AXg0eEfajFzsG3PMdPKT\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"user_email\": \"user@addepar.com\",\n \"user_id\": 826728,\n \"user_name\": \"Addepar User\",\n \"action\": \"remove_user_permissions\",\n \"old_value\": {\n \"user_role\": \"FULL_ACCESS\"\n },\n \"source\": \"Manual\",\n \"new_value\": {},\n \"timestamp\": \"2021-03-15T06:00:01.241144Z\"\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXg0eEfajFzsG3PMdPKT\"\n }\n },\n {\n \"id\": \"AXUOmW0sBGo8qwhMUyVP\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"role_id\": 400103,\n \"performed_by_user_id\": \"627858\",\n \"action\": \"modify_role\",\n \"old_value\": {},\n \"source\": \"Manual\",\n \"new_value\": {},\n \"timestamp\": \"2020-03-15T18:22:17.387804Z\"\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXUOmW0sBGo8qwhMUyVP\"\n }\n },\n \"included\": [],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Request objects**
[block:parameters]
{
"data": {
"h-0": "Request Object",
"h-1": "Description",
"0-0": "`object_type`",
"1-0": "`start_date`",
"2-0": "`end_date`",
"0-1": "Required. Type of audit log you're retrieving. \n\nValid input: \n`permission`",
"1-1": "Required. First date of the time period you want to audit.\n\nValid formats:\n`YYYY-MM-DD` Example: 2021-01-01. Timezone is assumed to be UTC.\n `YYYY-MM-DDThh:mm:ss` followed by a timezone. Example 1: 2021-01-01T00:00:00Z timezone is UTC as specified by \"Z\". Example 2: 2021-01-01T00:00:00-05:00 timezone is EST as specified by offset -05:00.\n\nIf both `start_date` and `end_date` are missing, the time period will be today only. If one of them is missing, it will be set to equal the other one.\n\nYou must specify both `start_date` and `end_date` if you want to use the `YYYY-MM-DDThh:mm:ss` format.",
"2-1": "Required. Last date of the time period you want to audit.\n\nValid formats:\n`YYYY-MM-DD` Example: 2021-01-01. Timezone is assumed to be UTC.\n `YYYY-MM-DDThh:mm:ss` followed by a timezone. Example 1: 2021-01-01T00:00:00Z timezone is UTC as specified by \"Z\". Example 2: 2021-01-01T00:00:00-05:00 timezone is EST as specified by offset -05:00.\n\nIf both `start_date` and `end_date` are missing, the time period will be today only. If one of them is missing, it will be set to equal the other one.\n\nYou must specify both `start_date` and `end_date` if you want to use the `YYYY-MM-DDThh:mm:ss` format.",
"3-1": "Operation performed. \n\nValid inputs: \n`Add`\n`Modify` \n`Remove`\n\nIf missing or empty, all actions will be included.",
"3-0": "`action`",
"4-0": "`user_type `",
"5-0": "`users`",
"4-1": "Valid inputs:\n`firmusers` includes users at your firms\n`addeparusers` includes Addepar employees\n`anyone` includes all firm users and Addepar employees\n`custom` allows you to specify certain `users`",
"5-1": "List of IDs for the specific users you want to query. If `user_type: custom` but no users are specified, then all firm users will be included."
},
"cols": 2,
"rows": 6
}
[/block]
**Response objects**
[block:parameters]
{
"data": {
"0-0": "`action`",
"0-1": "Operation performed.",
"0-2": "`remove_user_permissions`",
"1-0": "`new_value`",
"5-0": "`timestamp`",
"5-1": "Date and time the change was made ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format) based on your firm's timezone.",
"5-2": "`2020-08-14T21:25:52.739226Z`",
"h-0": "Response Object",
"h-1": "Description",
"h-2": "Example",
"1-1": "Value after the change was made.",
"6-0": "`user_email`",
"6-1": "Email address of the user.",
"7-0": "`user_id`",
"7-1": "User ID of the user.",
"8-0": "`user_name`",
"8-1": "Name of the user.",
"3-0": "`performed_by_user_id`",
"3-1": "User ID of the person who made the change.",
"4-0": "`source`",
"4-1": "`Manual` indicates that the action was performed manually in the application. `Import` indicates the action was performed using the Import Tool.",
"2-0": "`old_value`",
"2-1": "Value before the change was made."
},
"cols": 2,
"rows": 9
}
[/block]
**Response codes:**

- 200 OK: Success
- 403 Forbidden: User does not have permission to see audit trails
  [block:api-header]
  {
  "title": "Get details about a specific Audit Log Entry ID"
  }
  [/block]
  **GET** `/v1/audit_trail/:id`

Retrieves details about a specific user action. Use the endpoints listed above to get the entry ID.

**Example**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/audit_trail/AXifSBFEeYH1_Q0j5iiH",
"language": "json",
"name": "Request"
},
{
"code": "{\n \"data\": {\n {\n \"id\": \"AXifSBFEeYH1_Q0j5iiH\",\n \"type\": \"audit_trail\",\n \"attributes\": {\n \"transaction_id\": \"150170\",\n \"performed_by_user_id\": \"3254\",\n \"vendor_id\": \"5f44be6d-9cb9-48cb-8cf0-3e7c9c2689d0\",\n \"action\": \"add_transaction\",\n \"old_value\": {},\n \"source\": \"Manual\",\n \"type\": \"TRANSFER_IN\",\n \"new_value\": {\n \"date\": \"2021-04-04\",\n \"settlement_date\": \"2021-04-02\",\n \"entities\": {\n \"owner_id\": 1101,\n \"owned_id\": 1104\n },\n \"values\": {\n \"base\": 100.0\n },\n \"currency\": \"USD\",\n \"units\": {\n \"base\": 1.0\n },\n \"affects_value\": false,\n \"affects_cost_basis\": false,\n \"affects_unfunded\": false\n },\n \"timestamp\": \"2021-04-04T23:46:43.622124Z\",\n \"is_reversal\": false\n },\n \"links\": {\n \"self\": \"/v1/audit_trail/AXifSBFEeYH1_Q0j5iiH\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response codes**

- 200 OK: Success
- 403 Forbidden: User does not have permission to see the audit trail
- 404 Not Found: No audit trail found or non-permissioned audit trail ID
