# Roles

Roles represent standard sets of permissions available to your firm. Use the Roles API to view your firm's roles, and add or remove the users assigned to each role.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/240c83a-Roles.png",
"Roles.png",
3104,
2024,
"#e7e8e8"
]
}
]
}
[/block]
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"2-0": "Produces",
"3-0": "Pagination",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\"\n\n\"Manage firm settings: Users and permissions\" for all operations.",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"2-1": "JSON",
"0-1": "/v1/roles",
"1-1": "**GET**\n/v1/roles/:id\n/v1/roles\n/v1/roles/:id/relationships/assigned_users\n/v1/roles/:id/assigned_users\n\n**POST**\n/v1/roles/:id/relationships/assigned_users\n\n**PATCH**\n/v1/roles/:id/relationships/assigned_users\n\n**DELETE**\n/v1/roles/:id/relationships/assigned_users",
"1-0": "Endpoints",
"5-0": "OAuth Scopes",
"5-1": "**GET** \n`USERS` and `USERS_WRITE`\n\n**POST**, **PATCH**, and **DELETE**\n`USERS_WRITE`"
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
The attributes below will always appear in **GET**, **POST**, and **PATCH** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`name`",
"0-1": "The name of the role. String.",
"0-2": "`\"Platform Team\"`"
},
"cols": 3,
"rows": 1
}
[/block]
[block:api-header]
{
"title": "Relationships"
}
[/block]
[block:parameters]
{
"data": {
"0-0": "`assigned_users`",
"0-1": "Users assigned to the role.",
"0-2": "\"members\": {\n \"data\": [\n { \"type\": \"entities\", \"id\": \"22\" },\n { \"type\": \"entities\", \"id\": \"24\" },\n { \"type\": \"entities\", \"id\": \"117\" }\n ]\n }",
"h-0": "Relationship",
"h-1": "Description",
"h-2": "Example"
},
"cols": 2,
"rows": 1
}
[/block]
[block:code]
{
"codes": [
{
"code": "\"relationships\":{\n \"assigned_users\":{\n \"links\":{\n \"self\":\"/v1/roles/455914/relationships/assigned_users\",\n \"related\":\"/v1/roles/455914/assigned_users\"\n },\n \"data\":[\n {\n \"type\":\"users\",\n \"id\":\"621500\"\n }\n ]\n }\n}",
"language": "json",
"name": "Relationships"
}
]
}
[/block]
[block:callout]
{
"type": "info",
"title": "Note",
"body": "Creation, deletion, and modification of roles are done from within the application. Roles must be created in the application before the API can be used to update its members."
}
[/block]
[block:api-header]
{
"title": "Get a Role"
}
[/block]
Returns the details for a specific role.

**GET** `/v1/roles/:id`

**Example:**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/roles/80",
"language": "curl",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n \n{\n \"data\": {\n \"id\": \"80\",\n \"type\": \"roles\",\n \"attributes\": {\n \"name\": \"Advisor Role”\n },\n \"relationships\": {\n \"assigned_users\": {\n \"links\": {\n \"self\": \"/v1/roles/80/relationships/assigned_users\",\n \"related\": \"/v1/roles/80/assigned_users\"\n },\n \"data\": [\n { \n \"type\": \"users\",\n \"id\": \"101\"\n }\n ]\n }\n },\n \"links\": {\n \"self\": \"/v1/roles/80\"\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Responses**

- `200 OK`: Success
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not found`: No role exists with the provided ID in the firm
  [block:api-header]
  {
  "title": "Get All Roles"
  }
  [/block]
  Returns a list of all roles at the firm.

**GET** `/v1/roles`

**Example:**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/roles",
"language": "curl",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n \n{\n \"data\": {\n \"id\": \"80\",\n \"type\": \"roles\",\n \"attributes\": {\n \"name\": \"Advisor Role”\n },\n \"relationships\": {\n \"assigned_users\": {\n \"links\": {\n \"self\": \"/v1/roles/80/relationships/assigned_users\",\n \"related\": \"/v1/roles/80/assigned_users\"\n },\n \"data\": [\n { \n \"type\": \"users\",\n \"id\": \"101\"\n }\n ]\n }\n },\n \"links\": {\n \"self\": \"/v1/roles/80\"\n }\n },\n \"data\": {\n \"id\": \"90\",\n \"type\": \"roles\",\n \"attributes\": {\n \"name\": \"Administrator Role”\n },\n \"relationships\": {\n \"assigned_users\": {\n \"links\": {\n \"self\": \"/v1/roles/90/relationships/assigned_users\",\n \"related\": \"/v1/roles/90/assigned_users\"\n },\n \"data\": [\n {\n \"type\": \"users\",\n \"id\": \"102\"\n }\n ]\n }\n },\n \"links\": {\n \"self\": \"/v1/roles/90\"\n }\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: User lacks sufficient application permissions
  [block:api-header]
  {
  "title": "Get a Role's Users"
  }
  [/block]
  Returns a list of IDs for all users assigned to a specific role.

**GET** `/v1/roles/:id/relationships/assigned_users`

**Example:**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.com.addepar.com/api/v1/roles/80/relationships/assigned_users",
"language": "curl",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n \n{\n \"data\": [\n {\n \"id\": \"2000\",\n \"type\": \"users\"\n }\n ]\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid relationship queried
- `400 Bad Request`: Include parameter not supported
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned role ID
  [block:api-header]
  {
  "title": "Get a Role's User Details"
  }
  [/block]
  Returns details about the users assigned to a specific role.

**GET** `/v1/roles/:id/assigned_users`

**Example:**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/roles/80/assigned_users",
"language": "curl",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n \n{\n \"id\": \"2000\",\n \"type\": \"users\",\n \"attributes\": {\n \"email\": \"user2@addepar.com\",\n \"first_name\": \"Jane\",\n \"last_name\": \"Smith\",\n \"login_method\": \"email_password\",\n \"two_factor_auth_enabled\": true,\n \"admin_access\": false,\n \"all_data_access\": false,\n \"external_user_id\": \"A67890\"\n },\n \"relationships\": {\n \"permissioned_entities\": {\n \"links\": {\n \"self\": \"/v1/users/2000/relationships/permissioned_entities\",\n \"related\": \"/v1/users/2000/permissioned_entities\"\n },\n \"data\": [\n {\n \"type\": \"entities\",\n \"id\": 10000\n },\n {\n \"type\": \"entities\",\n \"id\": 10001\n }\n ]\n },\n \"assigned_role\": {\n \"links\": {\n \"self\": \"/v1/users/2000/relationships/assigned_role\",\n \"related\": \"/v1/users/2000/assigned_role\"\n },\n \"data\": [\n {\n \"type\": \"roles\",\n \"id\": \"80\"\n }\n ]\n },\n \"permissioned_groups\": {\n \"links\": {\n \"self\": \"/v1/users/2000/relationships/permissioned_groups\",\n \"related\": \"/v1/users/2000/permissioned_groups\"\n },\n \"data\": [\n {\n \"type\": \"entities\",\n \"id\": 20000\n },\n {\n \"type\": \"entities\",\n \"id\": 20001\n }\n ]\n }\n },\n \"links\": {\n \"self\": \"/v1/users/2000\"\n }\n }\n ],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid relationship queried
- `400 Bad Request`: Include parameter not supported
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned role ID
  [block:api-header]
  {
  "title": "Assign Users to a Role"
  }
  [/block]
  If a user is already assigned to a role, calling this endpoint will overwrite the role, and assign the user a new role.

**POST** `/v1/roles/:id/relationships/assigned_users`

**Example:**
[block:code]
{
"codes": [
{
"code": "POST https://examplefirm.addepar.com/api/v1/roles/90/relationships/assigned_users\n \n{\n \"data\": [\n {\n \"id\": \"2000\",\n \"type\": \"users\"\n }\n ]\n}",
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

- `204 No Content`: Success
- `400 Bad Request`: Nonexistent/non-permissioned user/attribute ID
- `404 Not Found`: Nonexistent/non-permissioned role ID
  [block:api-header]
  {
  "title": "Update Users Assigned to a Role"
  }
  [/block]
  Updates the specified users assigned to a role.

**PATCH** `/v1/roles/:id/relationships/assigned_users`

**Example:**
[block:code]
{
"codes": [
{
"code": "PATCH https://examplefirm.addepar.com/api/v1/roles/80/relationships/assigned_users\n \n{\n \"data\": [\n {\n \"id\": \"2000\",\n \"type\": \"users\"\n }\n ]\n}",
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

- `204 No Content`: Success
- `400 Bad Request`: Nonexistent/non-permissioned user/attribute ID
- `404 Not Found`: Nonexistent/non-permissioned user ID
  [block:api-header]
  {
  "title": "Remove Users from a Role"
  }
  [/block]
  Removes a specified user from a role.

**DELETE** `/v1/roles/:id/relationships/assigned_users`

**Example:**
[block:code]
{
"codes": [
{
"code": "DELETE https://examplefirm.addepar.com/api/v1/roles/80/relationships/assigned_users\n \n{\n \"data\": [\n {\n \"id\": \"2000\",\n \"type\": \"users\"\n }\n ]\n}",
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
**Responses:**

- `204 No Content`: Success
- `400 Bad Request`: Failed to provide an id or tried to delete a role that cannot be deleted
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not found`: No role exists with the provided id in the firm
