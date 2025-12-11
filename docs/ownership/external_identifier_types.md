# External ID Types

External ID Types are objects representing each non-Addepar system or application you wish to map to an External ID. Once you’ve created a unique type for each system, use the Entities or Groups API to map them to the appropriate system/application.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"2-0": "Produces",
"3-0": "Pagination",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\".\n\n\"Manage firm settings: Full Access\" for all operations.",
"3-1": "No",
"2-1": "JSON",
"0-1": "/v1/external_id_types",
"1-1": "**GET**\n/v1/external_id_types\n/v1/external_id_types/:id\n\n**POST**\n/v1/entity_types\n\n**PATCH**\n/v1/entity_types/:id\n\n**DELETE**\n/v1/entity_types/:id",
"1-0": "Endpoints",
"5-0": "OAuth Scopes",
"5-1": "**GET**\n`ENTITIES`\n`GROUPS`\n\n**POST**, **PATCH**, and **DELETE**\n`ENTITIES_WRITE`\n`GROUPS_WRITE`"
},
"cols": 2,
"rows": 6
}
[/block]
[block:api-header]
{
"title": "Resource Overview"
}
[/block]

External ID Types are described by the below resource object attributes and will appear in successful **GET**, **POST** & **PATCH** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"1-0": "`display_name`",
"1-1": "Display name of the entity type. String.",
"h-2": "Example",
"1-2": "`\"Salesforce\"`",
"0-0": "`external_id_type_key`",
"0-1": "The ID of the entity ID type. String.",
"0-2": "`\"salesforce\"`"
},
"cols": 3,
"rows": 2
}
[/block]
[block:api-header]
{
"title": "Get All External ID Types"
}
[/block]
Returns a list of all External ID Types.

**GET** `/v1/external_id_types `

**Example:**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/external_id_types",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"data\": [\n {\n \"id\": \"other-external-system\",\n \"type\": \"external_id_types\",\n \"attributes\": {\n \"external_type_key\": \"other-external-system\",\n \"display_name\": \"Other External System\"\n },\n \"links\": {\n \"self\": \"/v1/external_id_types/other-external-system\"\n }\n },\n {\n \"id\": \"randomsystem\",\n \"type\": \"external_id_types\",\n \"attributes\": {\n \"external_type_key\": \"randomsystem\",\n \"display_name\": \"Random External System\"\n },\n \"links\": {\n \"self\": \"/v1/external_id_types/randomsystem\"\n }\n }\n ],\n \"included\": [],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions
  [block:api-header]
  {
  "title": "Get External ID Type By ID"
  }
  [/block]
  Returns an External ID Type corresponding to the given ID.

**GET** `/v1/external_id_types/:id`
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/external_id_types/randomsystem",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"data\": {\n \"id\": \"randomsystem\",\n \"type\": \"external_id_types\",\n \"attributes\": {\n \"external_type_key\": \"randomsystem\",\n \"display_name\": \"Random External System\"\n },\n \"links\": {\n \"self\": \"/v1/external_id_types/randomsystem\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions
- `404 Not Found`: Invalid external ID type
  [block:api-header]
  {
  "title": "Create an External ID Type"
  }
  [/block]
  Adds a new External ID Type to your firm.

**POST** `/v1/external_id_types`
[block:code]
{
"codes": [
{
"code": "POST https://examplefirm.addepar.com/api/v1/external_id_types\n\n{\n \"data\": {\n \"type\": \"external_id_types\",\n \"attributes\": {\n \"external_type_key\": \"randomsystem\",\n \"display_name\": \"Random External System\"\n }\n }\n}",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 201\n\n{\n \"data\": {\n \"id\": \"randomsystem\",\n \"type\": \"external_id_types\",\n \"attributes\": {\n \"external_type_key\": \"randomsystem\",\n \"display_name\": \"Random External System\"\n },\n \"links\": {\n \"self\": \"/v1/external_id_types/randomsystem\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `201 OK`: Success
- `403 Forbidden`: Insufficient application permissions
- `409 Forbidden`: Duplicate `external_type_key`
  [block:api-header]
  {
  "title": "Update an External ID Type"
  }
  [/block]
  Modifies an existing External ID Type.

**PATCH** `/v1/external_id_types/:id`
[block:code]
{
"codes": [
{
"code": "PATCH https://examplefirm.addepar.com/api/v1/external_id_types/randomsystem\n\n{\n \"data\": {\n \"id\": \"randomsystem\",\n \"type\": \"external_id_types\",\n \"attributes\": {\n \"display_name\": \"Known System\"\n }\n }\n}\n",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"data\": {\n \"id\": \"randomsystem\",\n \"type\": \"external_id_types\",\n \"attributes\": {\n \"external_type_key\": \"randomsystem\",\n \"display_name\": \"Known System\"\n },\n \"links\": {\n \"self\": \"/v1/external_id_types/randomsystem\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `201 OK`: Success
- `403 Forbidden`: Insufficient application permissions
- `404 Forbidden`: The external ID type does not exist
  [block:api-header]
  {
  "title": "Delete an External ID Type"
  }
  [/block]
  Deletes an existing External ID Type from your firm.

**DELETE** `/v1/external_id_types/:id`
[block:code]
{
"codes": [
{
"code": "DELETE https://examplefirm.addepar.com/api/v1/external_id_types/randomsystem",
"language": "curl",
"name": "Request"
},
{
"code": "HTTP/1.1 204",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `204 No Content`: Successfully deleted the external ID type
- `400 Bad Request`: The external ID type is associated with an Addepar object
- `403 Forbidden`: Insufficient application permissions
- `404 Forbidden`: The external ID type does not exist
