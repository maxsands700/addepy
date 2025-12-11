# Group Types

Use group types to view client data in the aggregate. By default, Addepar comes with a single built-in group type called Groups.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"2-0": "Produce",
"3-0": "Pagination",
"4-0": "Permissions required",
"4-1": "\"API Access: Create, edit, and delete\"\n\n\"Groups: Manage selected or all groups access\" allows you to retrieve group types.\n\n\"Manage firm settings: Custom group types.\" is required to create, update, or delete group types.",
"3-1": "[No](https://developers.addepar.com/docs/pagination-1)",
"2-1": "JSON",
"0-1": "/v1/group_types",
"1-1": "**GET**\n/v1/group_types/\n/v1/group_types/:id\n\n**POST**\n/v1/group_types\n\n**PATCH**\n/v1/group_types/:id\n\n**DELETE**\n/v1/group_types/:id",
"1-0": "Endpoints",
"5-0": "OAuth Scopes",
"5-1": "`GROUPS` or `GROUPS_WRITE`"
},
"cols": 2,
"rows": 6
}
[/block]
[block:api-header]
{
"title": "Resource overview"
}
[/block]
Group types are described by the below resource object attributes.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"0-0": "`group_type_key`",
"1-0": "`display_name`",
"2-0": "`is_permissioned_resource`",
"0-1": "The ID of the group type. String.",
"1-1": "The user-facing name used to label the group type. String.",
"2-1": "If `true`, users will need access to groups of this type. This is referred to as \"Explicit access\" in Addepar.\n\nIf `false`, users will need to have access to each individual member of a group to access groups of this type. This is referred to as \"Implicit access\" in Addepar. Multiple.",
"h-2": "Example",
"0-2": "`\"GROUPS\"`",
"1-2": "`\"SPECIAL GROUPS\"`",
"2-2": "`true`"
},
"cols": 3,
"rows": 3
}
[/block]
[block:api-header]
{
"title": "Default Group Type"
}
[/block]
By default, firms have one group type, `GROUPS`, that is a permissioned resource. The default group type cannot be changed or deleted.

**Example:**
[block:code]
{
"codes": [
{
"code": "{\n \"data\": {\n \"id\": \"GROUPS\",\n \"type\": \"group_types\",\n \"attributes\": {\n \"is_permissioned_resource\": true,\n \"group_type_key\": \"GROUPS\",\n \"display_name\": \"GROUPS\"\n },\n \"links\": {\n \"self\": \"/v1/group_types/GROUPS\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
[block:api-header]
{
"title": "Get All Group Types"
}
[/block]
Retrieve all group types for the firm.

**GET** `/v1/group_types/`
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/group_types/",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"data\": [\n {\n \"id\": \"HH_GROUPS\",\n \"type\": \"group_types\",\n \"attributes\": {\n \"is_permissioned_resource\": false,\n \"group_type_key\": \"HH_GROUPS\",\n \"display_name\": \"Households\"\n },\n \"links\": {\n \"self\": \"/v1/group_types/HH_GROUPS\"\n }\n },\n {\n \"id\": \"GROUPS\",\n \"type\": \"group_types\",\n \"attributes\": {\n \"is_permissioned_resource\": true,\n \"group_type_key\": \"GROUPS\",\n \"display_name\": \"GROUPS\"\n },\n \"links\": {\n \"self\": \"/v1/group_types/GROUPS\"\n }\n }\n ],\n \"included\": [],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Optional Query Parameters**
[block:parameters]
{
"data": {
"0-0": "`is_permissioned_resource`",
"0-1": "If `true`, users will need access to groups of this type. This is referred to as \"Explicit access\" in Addepar.\n\nIf `false`, users will need to have access to each individual member of a group to access groups of this type. This is referred to as \"Implicit access\" in Addepar. Multiple.",
"0-2": "`is_permissioned_resource=true`",
"h-0": "Parameter",
"h-1": "Description"
},
"cols": 3,
"rows": 1
}
[/block]
**Response Codes:**

- `200 OK`: Success. Returns JSON with all group types.
- `400 Bad Request`: Incorrect API format
  [block:api-header]
  {
  "title": "Get a Group Type By ID"
  }
  [/block]
  Retrieve a group type using a group type key (same as ID).

**GET** `/v1/group_types/:id`
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/group_types/HH_GROUPS",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"meta\": {\n \"exclude_self_link\": false,\n \"link\": null,\n \"pagination_params\": null,\n \"included_params\": null,\n \"filter_params\": null,\n \"fields_param\": null\n },\n \"data\": {\n \"id\": \"HH_GROUPS\",\n \"type\": \"group_types\",\n \"attributes\": {\n \"is_permissioned_resource\": false,\n \"group_type_key\": \"HH_GROUPS\",\n \"display_name\": \"Household groups\"\n },\n \"links\": {\n \"self\": \"/v1/group_types/HH_GROUPS\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success. Returns JSON with the group type.
- `400 Bad Request`: Incorrect API format
- `404 Not Found`: Group type key not found
  [block:api-header]
  {
  "title": "Create a Group Type"
  }
  [/block]
  Create a new group type for your firm.

**POST** `/v1/group_types`
[block:code]
{
"codes": [
{
"code": "POST https://examplefirm.addepar.com/api/v1/group_types\n\n{\n \"data\": {\n \"type\": \"group_types\",\n \"attributes\": {\n \"is_permissioned_resource\": false,\n \"group_type_key\": \"HH_GROUPS\",\n \"display_name\": \"Households\"\n }\n }\n}",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 201\n\n{\n \"data\": {\n \"id\": \"HH_GROUPS\",\n \"type\": \"group_types\",\n \"attributes\": {\n \"is_permissioned_resource\": false,\n \"group_type_key\": \"HH_GROUPS\",\n \"display_name\": \"Households\"\n },\n \"links\": {\n \"self\": \"/v1/group_types/HH_GROUPS\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `201 OK`: Success. Returns JSON with recently created group type.
- `400 Bad Request`: Incorrect API format or missing parameters
- `403 Forbidden`: Lacking admin permission
- `409 Conflict`: Group type key already exists within the firm
  [block:api-header]
  {
  "title": "Update a Group Type by ID"
  }
  [/block]
  Change an existing group type's display name using the group type key (same as ID).

**PATCH** `/v1/group_types/:id`

**Example:**
[block:code]
{
"codes": [
{
"code": "PATCH https://examplefirm.addepar.com/api/v1/group_types/HH_GROUPS\n\n{\n \"data\": {\n \"id\": \"HH_GROUPS\",\n \"type\": \"group_types\",\n \"attributes\": {\n \"display_name\": \"Household groups\"\n }\n }\n}",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"data\": {\n \"id\": \"HH_GROUPS\",\n \"type\": \"group_types\",\n \"attributes\": {\n \"is_permissioned_resource\": false,\n \"group_type_key\": \"HH_GROUPS\",\n \"display_name\": \"Household groups\"\n },\n \"links\": {\n \"self\": \"/v1/group_types/HH_GROUPS\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success. Returns JSON with updated group type.
- `400 Bad Request`: Incorrect API format or missing parameters
- `403 Forbidden`: Lacking admin permission
- `404 Not Found`: Group type key not found
  [block:api-header]
  {
  "title": "Delete a Group Type"
  }
  [/block]
  Delete the group type using the group type key (same as ID).

**DELETE** `/v1/group_types/:id`
[block:code]
{
"codes": [
{
"code": "DELETE https://examplefirm.addepar.com/api/v1/group_types/HH_GROUPS",
"language": "json",
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

- `204 No Content`: Successfully deleted the group
- `400 Bad Request`: Incorrect API format or missing parameters
- `403 Forbidden`: Lacking admin permission \*`404 Not Found`: Group type key not found
