# Benchmark Compositions

A benchmark composition is a list of weighted benchmarks. Every benchmark composition is linked to one blended benchmark, as it represents the composition for that benchmark. A composition may contain multiple intervals, allowing the value of a benchmark composition to change over time.

Use the Benchmark Compositions API to retrieve or update benchmark compositions. To manage a blended benchmark as a whole, use the Benchmarks API.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/benchmark_compositions",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/benchmark_compositions \n/v1/benchmark_compositions/id \n \n**PATCH** \n/v1/benchmark_compositions/id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "500",
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

[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`date`",
"0-1": "Date the interval started. At least one interval must have a date of `null`, representing the initial value. If there are multiple intervals with the same date, they will be aggregated into a single interval. String. \n \n\"YYYY-MM-DD\" \n \nDate is required for every interval.",
"0-2": "`\"2023-31-12\"`",
"1-0": "`value`",
"1-1": "Field that lists benchmark exposure objects. Object. \n \nValue is required for every interval.",
"1-2": "See examples below",
"2-0": "`benchmark_id`",
"2-1": "Identifies the benchmark composition. A benchmark composition has the same ID as the blended benchmark it's associated with. A benchmark can only appear once in an interval. Portfolio benchmarks aren't allowed in blended benchmarks. Number. \n \nBenchmark ID is required for every value.",
"2-2": "`571`",
"3-0": "`percent`",
"3-1": "Value's portion of a composition. The sum of percents in a benchmark composition don't need to add up to 100%. Percents can also be negative, which represents inverse exposure. \n \nPercent is required for every value.",
"3-2": "`0.1`"
},
"cols": 3,
"rows": 4,
"align": [
"left",
"left",
"left"
]
}
[/block]

# Get all benchmark compositions

Returns a paginated list of all active benchmark compositions. The default pagination limit is 500.

**GET** `/v1/benchmark_compositions`

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/benchmark_compositions
```

```Text RESPONSE
HTTP/1.1 200 Success

{
    "data": [
        {
            "id": "571",
            "type": "benchmark_compositions",
            "attributes": {
                "intervals": [
                    {
                        "date": null,
                        "value": [
                            {
                                "benchmark_id": 421,
                                "percent": 0.5
                            },
                            {
                                "benchmark_id": 734,
                                "percent": 0.5
                            },
                            {
                                "benchmark_id": 735,
                                "percent": 0.5
                            }
                        ],
                        "weight": 1.0
                    }
                ]
            },
            "links": {
                "self": "/v1/benchmark_compositions/571"
            }
        },
        {
            "id": "736",
            "type": "benchmark_compositions",
            "attributes": {
                "intervals": [
                    {
                        "date": null,
                        "value": [
                            {
                                "benchmark_id": 421,
                                "percent": 0.5
                            },
                            {
                                "benchmark_id": 734,
                                "percent": 0.5
                            }
                        ],
                        "weight": 1.0
                    }
                ]
            },
            "links": {
                "self": "/v1/benchmark_compositions/736"
            }
        }
    ],
    "included": [],
    "links": {
        "prev": null,
        "next": null
    }
}
```

**Response codes**

- `200 OK`: Success.

# Get a benchmark composition

Returns a benchmark composition with the given ID.

**GET** `/v1/benchmark_compositions/id`

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/benchmark_compositions/571
```

```Text RESPONSE
HTTP/1.1 200 Success

{
    "data": {
        "id": "571",
        "type": "benchmark_compositions",
        "attributes": {
            "intervals": [
                {
                    "date": null,
                    "value": [
                        {
                            "benchmark_id": 734,
                            "percent": 0.5
                        },
                        {
                            "benchmark_id": 421,
                            "percent": 0.5
                        }
                    ],
                    "weight": 1.0
                }
            ]
        },
        "links": {
            "self": "/v1/benchmark_compositions/571"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: The provided ID does not correspond to an existing blended benchmark.

# Update a benchmark composition

Modifies the underlying composition of an existing blended benchmark.

**PATCH** `/v1/benchmark_compositions/id`

**Important notes**

- These requests preserve existing data where possible. If the request payload includes an interval with the same date as an existing interval, the existing interval will be overwritten.
- The same benchmark can't be included more than once in a given interval.
- Every valid benchmark composition must include an interval with `"date": null`, which corresponds to the initial value of the composition.
- To remove an existing interval from a composition, users must explicitly set the value field to `null`. As an example, to remove an existing interval that begins on 12/31/2020, the payload must include:

```Text NULL VALUE
{
    "date": "2020-12-31",
    "value": null
}
```

- If the request includes multiple interval JSONs with the same date, they will be concatenated into a single interval in the response. For example, a request may contain two intervals for 12/31/2020, as shown below:

```Text TWO INTERVALS WITH THE SAME DATE
{
"intervals": [
    {
        "date": "2020-12-31",
        "value": [
            {
                "benchmark_id": 123,
                "percent": 0.5
            }
        ]
    },
    {
        "date": "2020-12-31",
        "value": [
            {
                "benchmark_id": 456,
                "percent": 0.5
            }
        ]
    }
]
}
```

These would be joined into a single interval:

```Text JOINED INTO A SINGLE INTERVAL
{
    "date": null,
    "value": [
        {
            "benchmark_id": 456,
            "percent": 0.5
        },
        {
            "benchmark_id": 123,
            "percent": 0.5
        }
    ]
}
```

**Example**

```Text REQUEST
PATCH https://examplefirm.addepar.com/api/v1/benchmark_compositions

{
    "data": {
        "id": "736",
        "type": "benchmark_compositions",
        "attributes": {
            "intervals": [
                {
                    "date": null,
                    "value": [
                        {
                            "benchmark_id": 734,
                            "percent": 0.5
                        },
                        {
                            "benchmark_id": 421,
                            "percent": 0.5
                        },
                        {
                            "benchmark_id": 735,
                            "percent": 0.5
                        },
                        {
                            "benchmark_id": 571,
                            "percent": 0.5
                        }
                    ]
                },
                {
                    "date": "2020-12-31",
                    "value": null
                }
            ]
        }
    }
}
```

```Text RESPONSE
HTTP/1.1 200 Success
```

**Response codes**

- `200 OK`: The composition was updated successfully.
- `400 Bad Request`: Request payload is improperly formatted or contains invalid data.
- `403 Forbidden`: The current user does not have permission to update benchmarks.
- `404 Not Found`: The provided ID does not correspond to an existing blended benchmark.
- `409 Conflict`: There is a mismatch between the id parameter in the URL and the id provided in the request payload.
