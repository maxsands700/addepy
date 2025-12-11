# Benchmarks

Benchmarks are standards against which you can measure performance.

Use the Benchmarks API to get, create, update, and delete benchmarks in Addepar. You can also use the Benchmark Compositions API, Imported Benchmark Data API, and Benchmark Associations Strategies API for other benchmark management.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/benchmarks",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/benchmarks \n/v1/benchmarks/:id \n \n**POST** \n/v1/benchmarks \n \n**PATCH** \n/v1/benchmarks/:id \n \n**DELETE** \n/v1/benchmarks/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "500",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Portfolio Access\" determines the entities that are accessible. \n \n\"Benchmark library\"",
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

# Supported benchmarks

- **Blended** benchmarks are composed of multiple benchmarks, which can either be other blended benchmarks or another benchmark type. Each underlying benchmark is assigned a weight that determines how it contributes to the total return. Example: 50% equity benchmark / 50% fixed income benchmark
- \*\*Imported \*\*benchmarks consist of daily returns provided by a firm because their custom benchmarks aren't available from other sources.
- **Fixed return** benchmarks have a fixed annual return. A 20.00% fixed return benchmark will show 20% annually year-over-year.
- **Security** benchmarks are based on the performance of a specific investment.
- **Portfolio** benchmarks are based on the performance of a specific portfolio.

**Index** benchmarks are provided by vendors and therefore can't be created via the API. You can only update an index benchmark's display name via the API.

# Resource overview

Benchmarks are described by the below resource object attributes. Attributes required for creating benchmarks are noted.

All attributes will be returned in successful GET, POST & PATCH responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`id`",
"0-1": "Identifies a specific benchmark. Number.",
"0-2": "`524`",
"1-0": "`benchmark_type`",
"1-1": "Classification to differentiate benchmarks based on their data source and composition. String. \n \nPossible values are: \n \n- `\"blended\"`\n- `\"imported\"`\n- `\"fixed_return\"`\n- `\"portfolio_benchmark\"`\n- `\"security_benchmark\"`See \"Supported benchmarks\" for details about each type.",
"1-2": "`\"fixed_return\"`",
"2-0": "`rebalance_interval`",
"2-1": "Frequency with which the benchmark is rebalanced. String. \n \nPossible values are: \n \n- `None`: No rebalancing\n- `ONE_DAY`: Daily\n- `ONE_WEEK`: Weekly\n- `ONE_MONTH`: Monthly\n- `THREE_MONTHS`: Quarterly\n- `SIX_MONTHS`: Semi-annually\n- `ONE_YEAR`: AnnuallyOnly required for blended benchmarks.",
"2-2": "`\"THREE_MONTHS\"`",
"3-0": "`fixed_return`",
"3-1": "A fixed-value annual return percentage. Number. \n \nOnly required for fixed return benchmarks.",
"3-2": "`0.15`(represents 15%)",
"4-0": "`is_compounded`",
"4-1": "Indicates whether the fixed annual return is compounded. Boolean. \n \nOnly required for fixed return benchmarks.",
"4-2": "`true`",
"5-0": "`vendor_id`",
"5-1": "Indicates the ID used by the vendor that corresponds to this particular index. This field is immutable. Number. \n \nOnly required for index benchmarks.",
"5-2": "`4118`",
"6-0": "`index_type`",
"6-1": "Type of index. This field is immutable. String. \n \nPossible values are: \n \n- `\"Index Return\"`\n- `\"Index Return (Estimated)\"`\n- `\"Index Return (Preliminary)\"`\n- `\"Total Return\"`\n- `\"Net Return\"`\n- `\"Hedged Return\"`\n- `\"Total Return - MTD\"`Only required for index benchmarks.",
"6-2": "`\"Total Return\"`",
"7-0": "`index_name`",
"7-1": "While the index display name can be updated, this field contains the original name of the index. This field is immutable. String. \n \nOnly required for index benchmarks.",
"7-2": "`\"tr USNTBIROR\"`",
"8-0": "`start_date`",
"8-1": "The earliest date for which there is returns data. String. \n \n\"YYYY-MM-DD\" \n \nOnly required for index benchmarks.",
"8-2": "`2022-12-31`",
"9-0": "`end_date`",
"9-1": "The most recent date for which there is returns data. String. \n \n\"YYYY-MM-DD\" \n \nOnly required for index benchmarks.",
"9-2": "`2024-01-30`",
"10-0": "`benchmark_composition_id`",
"10-1": "Links to the underlying composition of the benchmark. \n \nOnly applies to blended benchmarks.",
"10-2": "`571`",
"11-0": "`entity_id`",
"11-1": "The Entity ID corresponding to an existing entity that will be the basis of the benchmark. \n \nOnly applies to security and portfolio benchmarks. \nFor security benchmarks, this entity must be an investment. \nFor portfolio benchmarks, must be one of the below entity types: \n \n- Household\n- Client\n- Holding Company\n- Trust\n- Fund\n- Holding Account\n- Managed Fund\n- Sleeve",
"11-2": "`14219`"
},
"cols": 3,
"rows": 12,
"align": [
"left",
"left",
"left"
]
}
[/block]

# Create a benchmark

Adds a new benchmark to your firm.

Note that index benchmarks can't be created via the API. If you are looking to add a new index benchmark to your firm's environment, please reach out to your Addepar contact.

**POST** `/v1/benchmarks`

**Required fields for all benchmark types**

- `benchmark_type`
- `name`: The benchmark's display name. This field is required for all types except `fixed_return`.

## Create a blended benchmark

**Required fields**

- `blended`: A JSON object containing a rebalance_interval field
- `rebalance_interval`: Indicates how often the benchmark composition will be rebalanced. Possible values are:
  - `None`: No rebalancing
  - `ONE_DAY`: Daily
  - `ONE_WEEK`: Weekly
  - `ONE_MONTH`: Monthly
  - `THREE_MONTHS`: Quarterly
  - `SIX_MONTHS`: Semi-annually
  - `ONE_YEAR`: Annually

**Other fields**\
`benchmark_composition_id`: This field does not need to be included in POST or PATCH requests and will always be the same as the ID of the benchmark itself. It can be used with the `/v1/benchmark_compositions/:id` endpoint to access the underlying composition of the blended benchmark.

**Example**

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/benchmarks

{
    "data": [
        {
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "blended",
                "name": "blended test",
                "blended": {
                    "rebalance_interval": "one_day"
                }
            }
        }
    ]
}
```

```Text RESPONSE
HTTP/1.1 200 Success

{
    "data": {
        "id": "571",
        "type": "benchmarks",
        "attributes": {
            "blended": {
                "rebalance_interval": "ONE_DAY",
                "benchmark_composition_id": 571
            },
            "benchmark_type": "BLENDED",
            "name": "Default-BB"
        },
        "links": {
            "self": "/v1/benchmarks/571"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success.
- `400 Bad Request`: Invalid request payload.
- `403 Unauthorized`: The current user does not have permission to create/update benchmarks.
- `409 Conflict`: There is already an existing benchmark with the same name.

## Create an imported benchmark

There are no required fields specific to imported benchmarks.

The `/v1/imported_benchmark_data/:id` endpoints are used to retrieve/update the imported returns for an imported benchmark.

**Example**

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/benchmarks

{
    "data": [
        {
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "imported",
                "name": "imported test"
            }
        }
    ]
}
```

## Create a fixed return benchmark

**Required fields**

- `fixed_return`: A JSON object containing the below fields:
  - `fixed_return`: A decimal corresponding to the desired annual rate of return. To create a 5% fixed return benchmark, set this field to 0.05. Up to 17 decimal places are supported.
  - `is_compounded`: A true/false value indicating whether the returns should be compounded.

Note: The name field is not required for fixed return benchmarks. The benchmark name will be based on the `fixed_return` and `is_compounded` fields. For example, if `fixed_return` is `0.05` and `is_compounded` is `true`, then the name will be `5.00 % Compounded`. Providing a value for name will not cause an error, but the name will still follow the above convention.

**Example**

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/benchmarks

{
    "data": [
        {
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "fixed_return",
                "fixed_return": {
                    "fixed_return": 0.15,
                    "is_compounded": true
                },
                "name": "fixed_return test"
            }
        }
    ]
}
```

## Create a portfolio benchmark

**Required fields**

- `portfolio`: A JSON object containing the below field:
  - `entity_id`: The ID of the entity that the benchmark is based on. For portfolio benchmarks, this entity must be one of the below model types:
    - Holding Account
    - Fund
    - Holding Company
    - Managed Fund
    - Client
    - Sleeve
    - Trust

**Example**

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/benchmarks

{
    "data": [
        {
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "portfolio_benchmark",
                "name": "portfolio test",
                "portfolio": {
                    "entity_id": 123
                }
            }
        }
    ]
}
```

## Create a security benchmark

**Required fields**

- `security`: A JSON object with the below field:
  - `entity_id`: The ID of the entity that the benchmark is based on. For security benchmarks, this entity must be one of the below model types:
    - Custom Asset
    - Money Market Fund
    - Bond
    - CMO
    - Certificate of Deposit
    - Closed End Fund
    - Convertible Note
    - ETF
    - ETN
    - Master Limited Partnership
    - Mutual Fund
    - Option
    - Stock
    - REIT
    - Preferred Stock
    - UIT
    - Warrant
    - Forward Contract
    - Digital Asset
    - Historical Segment

**Example**

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/benchmarks

{
    "data": [
        {
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "security_benchmark",
                "name": "security test",
                "security": {
                    "entity_id": 123
                }
            }
        }
    ]
}
```

# Get all benchmarks

Returns a paginated list of all active benchmarks. The default pagination limit is 500.

**GET** `/v1/benchmarks`

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/benchmarks
```

```Text RESPONSE
{
    "data": [
        {
            "id": "421",
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "INDEX",
                "name": "tr USNTBIROR",
                "index": {
                    "vendor": "tr",
                    "vendor_id": "USNTBIROR",
                    "index_type": "INDEX",
                    "index_name": "tr USNTBIROR",
                    "start_date": null,
                    "end_date": null
                }
            },
            "links": {
                "self": "/v1/benchmarks/421"
            }
        },
        {
            "id": "570",
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "INDEX",
                "name": "tr S&P600I (Total Return)",
                "index": {
                    "vendor": "tr",
                    "vendor_id": "S&P600I",
                    "index_type": "TOTAL_RETURN",
                    "index_name": "tr S&P600I",
                    "start_date": null,
                    "end_date": null
                }
            },
            "links": {
                "self": "/v1/benchmarks/570"
            }
        },
        {
            "id": "571",
            "type": "benchmarks",
            "attributes": {
                "blended": {
                    "rebalance_interval": "ONE_DAY",
                    "benchmark_composition_id": 571
                },
                "benchmark_type": "BLENDED",
                "name": "Default-BB"
            },
            "links": {
                "self": "/v1/benchmarks/571"
            }
        },
        {
            "id": "734",
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "IMPORTED",
                "name": "Imported Benchmark 1"
            },
            "links": {
                "self": "/v1/benchmarks/734"
            }
        },
        {
            "id": "735",
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "IMPORTED",
                "name": "Imported Benchmark 2"
            },
            "links": {
                "self": "/v1/benchmarks/735"
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

- `200 OK`: Success

# Get a benchmark

Returns a benchmark with the given ID.

**GET** `/v1/benchmarks/:id`

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/benchmarks/571
```

```Text RESPONSE
{
    "data": {
        "id": "571",
        "type": "benchmarks",
        "attributes": {
            "blended": {
                "rebalance_interval": "ONE_DAY",
                "benchmark_composition_id": 571
            },
            "benchmark_type": "BLENDED",
            "name": "Default-BB"
        },
        "links": {
            "self": "/v1/benchmarks/571"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: No benchmark exists corresponding to the provided ID.

# Update a benchmark

Modifies an existing benchmark.

**PATCH** `/v1/benchmarks/:id`

**Fields that can't be updated**

- `benchmark_type`
- Blended Benchmarks:
  - `benchmark_composition_id`
- Portfolio and Security Benchmarks:
  - `entity_id`
- Index Benchmarks:
  - `vendor`
  - `vendor_id`
  - `index_type`
  - `index_name`
  - `start_date`
  - `end_date`

The only field that can be updated on an index benchmark is name. All its other fields are immutable.

**Example**

```Text REQUEST
PATCH https://examplefirm.addepar.com/api/v1/benchmarks/739

{
    "data": {
        "id": "739",
        "type": "benchmarks",
        "attributes": {
            "benchmark_type": "FIXED_RETURN",
            "name": "15.00 %",
            "fixed_return": {
                "fixed_return": 0.15,
                "is_compounded": false
            }
        }
    }
}
```

```Text RESPONSE
{
    "data": {
        "id": "739",
        "type": "benchmarks",
        "attributes": {
            "benchmark_type": "FIXED_RETURN",
            "name": "new name",
            "fixed_return": {
                "fixed_return": 0.17,
                "is_compounded": false
            }
        },
        "links": {
            "self": "/v1/benchmarks/739"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success
- `400 Bad Request`: Invalid request payload.
- `403 Unauthorized`: The current user does not have permission to update benchmarks.
- `404 Not Found`: No benchmark exists corresponding to the provided ID.
- `409 Conflict`: There is already an existing benchmark with the same name.

# Update multiple benchmarks

Modify multiple existing benchmarks in bulk.

**PATCH** `/v1/benchmarks/:id`

**Example**

```text REQUEST
PATCH https://examplefirm.addepar.com/api/v1/benchmarks

{
    "data": [
        {
            "id": "739",
            "type": "benchmarks",
            "attributes": {
                "name": "name",
                "fixed_return": {
                    "fixed_return": 0.17,
                    "is_compounded": true
                }
            }
        },
        {
            "id": "571",
            "type": "benchmarks",
            "attributes": {
                "blended": {
                    "rebalance_interval": "six_months"
                }
            }
        }
    ]
}
```

```Text RESPONSE
{
    "data": [
        {
            "id": "739",
            "type": "benchmarks",
            "attributes": {
                "benchmark_type": "FIXED_RETURN",
                "name": "17.00 % Compounded",
                "fixed_return": {
                    "fixed_return": 0.17,
                    "is_compounded": true
                }
            },
            "links": {
                "self": "/v1/benchmarks/739"
            }
        },
        {
            "id": "571",
            "type": "benchmarks",
            "attributes": {
                "blended": {
                    "rebalance_interval": "SIX_MONTHS",
                    "benchmark_composition_id": 571
                },
                "benchmark_type": "BLENDED",
                "name": "blended test"
            },
            "links": {
                "self": "/v1/benchmarks/571"
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

- `200 OK`: Success
- `400 Bad Request`: Invalid request payload.
- `403 Unauthorized`: The current user does not have permission to update benchmarks.
- `404 Not Found`: No benchmark exists corresponding to the provided ID.
- `409 Conflict`: There is already an existing benchmark with the same name.

# Delete a benchmark

Deletes a user-created benchmark if it exists. Deleting benchmarks is typically not recommended due to the potential for breaking downstream relationships and usage.

Fixed return and index benchmarks cannot be deleted.

**DELETE** `/v1/benchmarks/:id`

**Example**

```Text REQUEST
DELETE https://examplefirm.addepar.com/api/v1/benchmarks/571
```

```Text RESPONSE
HTTP/1.1 204 No Content
```

**Response codes**

- `204 No Content`: Benchmark was successfully deleted.
- `400 Bad Request`: Attempt to delete a benchmark that cannot be deleted.
- `403 Unauthorized`: The current user does not have permission to delete benchmarks.
- `404 Not Found`: No benchmark exists corresponding to the provided ID.
