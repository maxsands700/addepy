# Rate Limiting

To ensure a reliable service quality for all our clients, the Addepar API enforces rate limiting on API requests.

Rate limiting is implemented at the firm level and is counted over a 24-hour window for all authenticated calls.

- Maximum number of requests in a 15-minute window is 50
- Maximum number of requests in 24-hour window is 1000
- Maximum runtime per request is 60 sec

If the API request breaches a limit, the request will be rejected with the `429 Too Many Requests` response code. The response will also contain `X-RateLimit-Retry-After` header to indicate how long an API client should wait (in seconds) before making another request. If the API request takes longer than 60 seconds, the request will be canceled with `400 Bad Request`.
[block:callout]
{
"type": "info",
"body": "To request an increase in rate limits, contact Addepar Support and provide context around the use case for your request. To contact Support, login to your Addepar account, click the question mark icon located on the Global Navigation bar, and click Contact Support. From there, fill in the form fields and click Send."
}
[/block]
