# View List

Get a complete list of views for portfolios you have access. Then, easily use a view ID to see view details or get the request body to quickly query the view.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/47f0d3b-Lists_of_views_in_Addepar.png",
"47f0d3b-Lists_of_views_in_Addepar.png",
3104,
2024,
"#000000"
]
}
]
}
[/block]
[block:api-header]
{
"title": "Resource Overview"
}
[/block]
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`share_type`",
"1-0": "`display_name`",
"1-2": "`false`",
"0-2": "`PERSONAL`",
"0-1": "The share type of the view. String.\nSupported values:\n-`PERSONAL`\n-`FIRM`\n-`TEAM`\n-`PORTAL`\n-`PORTAL_TEAM`",
"1-1": "Default argument value. Boolean or String.",
"2-0": "`parameters`",
"2-1": "Returns a request body for the Portfolio Query API. List of objects. [See parameters.](https://developers.addepar.com/docs/portfolio-query#parameters)",
"2-2": "`[{\"key\": \"time_weighted_return\"}]`"
},
"cols": 3,
"rows": 3
}
[/block]
[block:api-header]
{
"title": "Get a List of Portfolio Views"
}
[/block]
Get a complete list of views for portfolios you have access to. Then, use View IDs to quickly see view details or get a portfolio query request body.

**GET** `/v1/portfolio/views`
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/api/v1/portfolio/views",
"language": "json",
"name": "Request"
},
{
"code": "200 OK: Success\n\n{\n \"data\": [\n {\n \"id\": \"19\",\n \"type\": \"portfolio_views\",\n \"attributes\": {\n \"share_type\": \"PERSONAL\",\n \"display_name\": \"AdvancedTable\"\n },\n \"links\": {\n \"self\": \"/v1/portfolio_views/19\"\n }\n },\n {\n \"id\": \"2\",\n \"type\": \"portfolio_views\",\n \"attributes\": {\n \"share_type\": \"FIRM\",\n \"display_name\": \"owner1\"\n },\n \"links\": {\n \"self\": \"/v1/portfolio_views/2\"\n }\n },\n {\n \"id\": \"4\",\n \"type\": \"portfolio_views\",\n \"attributes\": {\n \"share_type\": \"PORTAL\",\n \"display_name\": \"TOTAL RETURN VIEW\"\n },\n \"links\": {\n \"self\": \"/v1/portfolio_views/4\"\n }\n }\n ],\n \"included\": [],\n \"links\": {\n \"next\": null\n }\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Responses**

- 200 OK: Success
- 404 Not Found: User lacks API permission or has not granted the appropriate scope
  [block:api-header]
  {
  "title": "Get a Portfolio View Query Request Body by ID"
  }
  [/block]
  Returns a complete request body to quickly query on a portfolio view.

**GET** `/v1/portfolio/views/:id`

**Example:**
[block:code]
{
"codes": [
{
"code": "GET https://examplefirm.addepar.com/v1/portfolio/views/:id",
"language": "json",
"name": "Request"
},
{
"code": "HTTP/1.1 200\n\n{\n \"data\": {\n \"id\": \"2\",\n \"type\": \"portfolio_views\",\n \"attributes\": {\n \"share_type\": \"FIRM\",\n \"parameters\": {\n \"columns\": [\n {\n \"key\": \"value\",\n \"arguments\": {\n \"adjusted\": false,\n \"time_point\": \"current\",\n \"accrued\": \"all\",\n \"currency\": \"USD\"\n }\n }\n ],\n \"groupings\": [\n {\n \"key\": \"ownership\"\n },\n {\n \"key\": \"asset_class\"\n },\n {\n \"key\": \"security\"\n }\n ],\n \"filters\": [],\n \"hide_previous_holdings\": false,\n \"group_by_historical_values\": false,\n \"group_by_multiple_attribute_values\": false,\n \"look_through_composite_securities\": false,\n \"display_account_fees\": false\n },\n \"display_name\": \"owner1\"\n },\n \"links\": {\n \"self\": \"/v1/portfolio_views/2\"\n }\n },\n \"included\": []\n}",
"language": "json",
"name": "Response"
}
]
}
[/block]
**Responses**

- 200 OK: Success
- 404 Not Found: User lacks API permission or has not granted the appropriate scope
