# Imported Benchmark Data

Maintain your own custom benchmarks by using imported benchmarks. You can add their daily returns in Addepar, the Import Tool, or via this Imported Benchmark Data API.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/imported_benchmark_data",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/imported_benchmark_data/:id \n \n**PATCH** \n/v1/imported_benchmark_data/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[No](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Benchmark library\"",
"5-0": "OAuth scopes",
"5-1": "`BENCHMARKS_READ` or `BENCHMARKS_WRITE`"
},
"cols": 2,
"rows": 6,
"align": [
"left",
"left"
]
}
[/block]

# Resource overview

Imported benchmark data is described by the below resource object attribute and will appear in successful GET responses.

| Attribute       | Description                                                                              | Example           |
| :-------------- | :--------------------------------------------------------------------------------------- | :---------------- |
| `daily_returns` | A list of date-value JSON objects indicating daily returns for a particular date. Array. | See example below |

# Get daily returns

Returns all the daily returns for an imported benchmark with the given ID.

**GET** `/v1/imported_benchmark_data/:id`

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/imported_benchmark_data/378862
```

```Text RESPONSE
HTTP/1.1 200 Success

{
    "data": {
        "id": "378862",
        "type": "imported_benchmark_data",
        "attributes": {
            "daily_returns": [
                {
                    "date": "2024-01-01",
                    "value": 0.005
                },
                {
                    "date": "2024-01-02",
                    "value": -0.005
                },
                {
                    "date": "2024-01-03",
                    "value": 0.0
                },
                {
                    "date": "2024-01-04",
                    "value": 0.01
                },
                {
                    "date": "2024-01-05",
                    "value": -0.005
                }
            ]
        },
        "links": {
            "self": "/v1/imported_benchmark_data/378862"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success.
- `403 Forbidden`: The currently logged-in user does not have permission to access benchmarks.
- `404 Not Found`: No imported benchmark exists corresponding to the provided ID.

# Update daily returns

Add new daily returns to an existing imported benchmark.

New daily returns will be appended to existing returns. For dates that already have returns, new returns overwrite existing ones.

**PATCH** `/v1/imported_benchmark_data/:id`

**Example**

```Text REQUEST
PATCH https://examplefirm.addepar.com/api/v1/imported_benchmark_data/378862

{
    "data": {
        "id": "378862",
        "type": "imported_benchmark_data",
        "attributes": {
            "daily_returns": [
                {
                    "date": "2021-01-01",
                    "value": 0.005
                },
                {
                    "date": "2021-01-02",
                    "value": -0.005
                },
                {
                    "date": "2021-01-03",
                    "value": 0.0
                },
                {
                    "date": "2021-01-04",
                    "value": 0.01
                },
                {
                    "date": "2021-01-05",
                    "value": -0.005
                }
            ]
        },
        "links": {
            "self": "/v1/imported_benchmark_data/378862"
        }
    },
    "included": []
}
```

```Text RESPONSE
HTTP/1.1 200 Success
```

**Response codes**

- `200 OK`: Success.
- `400 Bad Request`: Invalid request payload.
- `403 Forbidden`: The currently logged-in user does not have permission to update benchmarks.
- `404 Not Found`: No imported benchmark exists corresponding to the provided ID.
- `409 Conflict`: The id field in the request payload does not match the ID in the URL.
