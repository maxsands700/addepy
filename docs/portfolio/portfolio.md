# Portfolio

The Portfolio API makes it easy to extract data for a specific portfolio based on a saved analysis view in Addepar or direct query.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/1cad978-Analysis.png",
"Analysis.png",
3104,
2024,
"#e4e6e6"
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
"5-0": "OAuth Scopes",
"5-1": "`PORTFOLIO`",
"3-1": "No",
"2-1": "JSON, CSV (views only), TSV (views only), or XLSX (views only)",
"0-1": "/v1/portfolio",
"1-1": "**GET**\n/v1/portfolio/views\n/v1/portfolio/views/:id\n/v1/portfolio/views/:view-id/results\n\n**POST**\n/v1/portfolio/query",
"1-0": "Endpoints",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\"\n\n\"Analysis firm and team views: View only\" is required to extract view data."
},
"cols": 2,
"rows": 6
}
[/block]
[block:callout]
{
"type": "success",
"title": "",
"body": "For large-scale data queries, Addepar recommends using the Jobs API in conjunction with Portfolio API. Because the Portfolio API retrieves data for entire portfolios, the server's responses can be large and may result in timeouts. You can help avoid timeouts by using the Jobs API to make asynchronous requests to Portfolio API, check the status of a job, and download a job's results."
}
[/block]
[block:api-header]
{
"title": "Comparing View vs. Query APIs"
}
[/block]
The below table highlights the main differences between the Portfolio Query and View APIs.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "View",
"h-2": "Query",
"1-0": "Request Structure",
"2-0": "Portability",
"3-0": "Batching",
"4-0": "Attribute Coverage",
"5-0": "Supported formats",
"6-0": "Asynchronous",
"1-1": "Relies on view in application.",
"1-2": "Query is constructed dynamically in API request.",
"2-1": "Views must be created for each firm.",
"2-2": "Requests can be used across multiple firms.",
"3-1": "Cannot batch requests.",
"3-2": "Batches multiple clients/entities in one request.",
"4-1": "All attributes are covered.",
"4-2": "Most attributes are covered.",
"5-1": "JSON, CSV, TSV, XLS.",
"5-2": "JSON only.",
"6-1": "Supported.",
"6-2": "Supported.",
"0-0": "Use Cases",
"0-1": "- Exporting a static portfolio view for offline analysis in Excel.\n- Running static exports to data warehouse.",
"0-2": "- Dynamic access to portfolio data.\n- Portable requests across different firms for standardized integrations."
},
"cols": 3,
"rows": 7
}
[/block]
[block:api-header]
{
"title": "Get a list of portfolio views"
}
[/block]
Get a complete list of views for portfolios you have access to. Responses include a Portfolio Query API request.

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
- 404 Not Found: Missing public_portfolio_view_api feature flag.
