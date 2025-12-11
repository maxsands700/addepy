# Response Codes

`__MAGIC_BLOCK_0__`
The Addepar API returns HTTP response codes to clarify the status of each API request.
[block:parameters]
{
"data": {
"h-0": "Status Code",
"h-1": "Title",
"h-2": "Request Type",
"0-0": "200",
"1-0": "201",
"2-0": "202",
"3-0": "204",
"4-0": "303",
"0-1": "OK",
"0-2": "Successful **GET** or **PATCH** request",
"1-1": "Created",
"2-1": "Accepted",
"3-1": "No Content",
"4-1": "See Other",
"1-2": "Successful **POST** request",
"2-2": "Successful **POST** request to jobs route",
"3-2": "Successful **DELETE** request\n\nSuccessful **POST**, **PATCH**, or **DELETE** to a relationships sub-route",
"4-2": "Completed asynchronous job. Follow the link in the \"Location\" header to retrieve the results."
},
"cols": 3,
"rows": 5
}
[/block]
[block:api-header]
{
"title": "Unsuccessful Request Codes"
}
[/block]
A failed request to the Addepar API will result in one of the following status codes. Please review the "detail" field in the error response for additional information about a particular failed request.
[block:parameters]
{
"data": {
"h-0": "Status Code",
"h-1": "Title",
"h-2": "Reason",
"h-3": "Troubleshooting",
"0-0": "400",
"0-1": "Bad Request",
"0-2": "Improperly formatted query parameters or payload",
"0-3": "Check the fields indicated in the error response.",
"1-1": "Unauthorized",
"1-2": "Failed authentication",
"1-0": "401",
"2-0": "403",
"3-0": "404",
"4-0": "405",
"5-0": "409",
"6-0": "410",
"7-0": "415",
"8-0": "429",
"9-0": "500",
"2-1": "Forbidden",
"3-1": "Not Found",
"4-1": "Method Not Allowed",
"5-1": "Conflict",
"6-1": "Gone",
"7-1": "Unsupported Media Type",
"8-1": "Too Many Requests",
"9-1": "Internal Server Error",
"2-2": "User lacks required permission(s)",
"3-2": "Incorrect URL or ID",
"4-2": "Unsupported HTTP method",
"5-2": "Action would result in an invalid data state",
"6-2": "The resource was available but has expired",
"7-2": "Invalid Content-Type header",
"8-2": "Request rate limit has been exceeded",
"9-2": "An unexpected error occurred",
"1-3": "Check the API key, secret, and \"Addepar-Firm\" header.",
"2-3": "Check that the user has API permission and Application Permissions or has authorized the required OAuth scope required for the particular URL.",
"3-3": "Check that the ID is correct and the user has permission to access it.",
"4-3": "Generally only **GET**, **POST**, **PATCH**, and **DELETE** are supported.",
"5-3": "Check that the \"type\" field matches that of the URL.",
"6-3": "Try making another request to the Jobs API",
"7-3": "Attach \"Content-Type\" header \"application/vnd.api+json\".",
"8-3": "Check the \"X-RateLimit-Retry-After\" header for the number of seconds until the next request can be made.",
"9-3": "Please contact Support if you see this."
},
"cols": 4,
"rows": 10
}
[/block]
