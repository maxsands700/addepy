# Arguments

Arguments are possible settings that can be applied to each instance of an attribute in Addepar. Use the Arguments API in conjunction with the [Attributes API](https://developers.addepar.com/docs/attributes) to discover available attribute arguments for making [Portfolio Query API](https://developers.addepar.com/docs/query) requests.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"2-0": "Produces",
"4-0": "Application Permissions Required",
"5-0": "OAuth Scopes",
"5-1": "`PORTFOLIO`",
"4-1": "\"API Access: Create, edit, and delete\" is required to retrieve available arguments.",
"2-1": "JSON",
"0-1": "/v1/arguments",
"1-1": "**GET**\n/v1/arguments\n/v1/arguments/:id",
"1-0": "Endpoints",
"3-0": "Pagination",
"3-1": "No"
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
Arguments are described by the below resource object attributes and will appear in successful **GET** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`values`",
"1-0": "`default_value`",
"2-0": "`arg_type`",
"2-2": "`\"discrete\"`",
"1-2": "`false`",
"0-2": "`[true, false]`",
"0-1": "Values supported by the argument. [Boolean or String.]",
"2-1": "The argument type which is determined by its output type. String.",
"1-1": "Default argument value. Boolean or String."
},
"cols": 3,
"rows": 3
}
[/block]
[block:api-header]
{
"title": "Get All Arguments"
}
[/block]
Retrieves all attribute arguments supported by the Portfolio Query API.

**GET** `/v1/arguments`

**Example:**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/arguments",
"language": "curl",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"data\": [{\n \"id\": \"adjusted\",\n \"type\": \"arguments\",\n \"attributes\": {\n \"values\": [\n true,\n false\n ],\n \"default_value\": false\n },\n \"links\": {\n \"self\": \"/v1/arguments/adjusted\"\n }\n },\n {\n \"id\": \"cost_basis_type\",\n \"type\": \"arguments\",\n \"attributes\": {\n \"values\": [\n \"ORIGINAL\",\n \"ADJUSTED\",\n \"CALCULATED_ADJUSTED\",\n \"CALCULATED_ADJUSTED_AMORTIZATION_ONLY\",\n \"CALCULATED_ADJUSTED_ACCRETION_ONLY\"\n ],\n \"default_value\": \"ORIGINAL\"\n },\n \"links\": {\n \"self\": \"/v1/arguments/cost_basis_type\"\n }\n },\n {\n \"id\": \"distribution_types\",\n \"type\": \"arguments\",\n \"attributes\": {\n \"values\": [\n \"GENERIC\",\n \"CAP_GAIN\",\n \"LT_CAP_GAIN\",\n \"ST_CAP_GAIN\",\n \"INTEREST_INCOME\",\n \"ORDINARY_INCOME\",\n \"DIVIDEND_INCOME\",\n \"RETURN_OF_CAPITAL\"\n ],\n \"default_value\": \"all\",\n \"arg_type\": \"multi_discrete\"\n },\n \"links\": {\n \"self\": \"/v1/arguments/distribution_types\"\n }\n },\n {\n \"id\": \"currency\",\n \"type\": \"arguments\",\n \"attributes\": {\n \"values\": [\n \"NATIVE_CURRENCY\",\n \"USD\",\n \"EUR\",\n \"GBP\",\n ...,\n \"ZWD\",\n \"ZWL\"\n ],\n \"default_value\": \"USD\",\n \"arg_type\": \"discrete\"\n },\n \"links\": {\n \"self\": \"/v1/arguments/currency\"\n }\n },\n {\n \"id\": \"time_point\",\n \"type\": \"arguments\",\n \"attributes\": {\n \"default_value\": \"CURRENT\",\n \"arg_type\": \"time_point\"\n },\n \"links\": {\n \"self\": \"/v1/arguments/time_point\"\n }\n },\n ],\n \"included\": [],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
  [block:api-header]
  {
  "title": "Get Argument By ID"
  }
  [/block]
  Retrieves the attribute argument with the given ID.

**GET** `/v1/arguments/:id`

**Example:**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/arguments/cost_basis_type",
"language": "curl",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"data\": {\n \"id\": \"cost_basis_type\",\n \"type\": \"arguments\",\n \"attributes\": {\n \"values\": [\n \"ORIGINAL\",\n \"ADJUSTED\",\n \"CALCULATED_ADJUSTED\",\n \"CALCULATED_ADJUSTED_AMORTIZATION_ONLY\",\n \"CALCULATED_ADJUSTED_ACCRETION_ONLY\"\n ],\n \"default_value\": \"ORIGINAL\"\n },\n \"links\": {\n \"self\": \"/v1/arguments/cost_basis_type\"\n }\n },\n \"included\": []\n}",
"language": "json"
}
]
}
[/block]
**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Argument does not exist
