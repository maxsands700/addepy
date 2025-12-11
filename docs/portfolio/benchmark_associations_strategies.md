# Benchmark Associations Strategies

A benchmark associations strategy is a list of benchmark associations that map attribute values to the benchmark(s) that should be applied to entities with those attribute values.

Use the Benchmark Associations Strategies API to manage these strategies. For general benchmark management, use the Benchmarks API.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/benchmark_associations_strategies",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/benchmark_associations_strategies \n/v1/benchmark_associations_strategies/:id \n \n**POST** \n/v1/benchmark_associations_strategies \n \n**PATCH** \n/v1/benchmark_associations_strategies/:id \n \n**DELETE** \n/v1/benchmark_associations_strategies/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "500 strategies",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Benchmark associations\"",
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

Benchmark associations strategies are described by the below properties.
[block:parameters]
{
"data": {
"h-0": "Property",
"h-1": "Description",
"h-2": "Example",
"0-0": "`id`",
"0-1": "Identifies the associations strategy. Number.",
"0-2": "`11`",
"1-0": "`display_name`",
"1-1": "The associations strategy's name that is displayed to the user. Doesn't have to be unique. String.",
"1-2": "`\"Security Benchmarks\"`",
"2-0": "`matching_type`",
"2-1": "Indicates where associations will be applied. \n \nPossible values are: \n \n- `PATH`: Assign benchmarks to all positions matching your association rules. Rolls up to groupings. This is referred to as positions in Addepar.\n- `PDN`: Assign independent benchmarks to specific rows. Doesn't roll up. This is referred to as table rows in Addepar. When using this matching, each association can only have one rule.",
"2-2": "`PATH`",
"3-0": "`benchmark_associations`",
"3-1": "A list of benchmark associations objects, which each consist of `benchmarks` and `rules`. \n \nThe order of the associations in the list will determine the order in which association rules are applied.",
"3-2": "See example below",
"4-0": "`benchmarks`",
"4-1": "A list of existing benchmark IDs to be associated. Portfolio benchmarks can't be used in benchmark associations.",
"4-2": "See example below",
"5-0": "`rules`",
"5-1": "Represents an attribute value that determines which entities will have the benchmark assigned. Consists of `attribute`, `type`, and `value`.",
"5-2": "See example below",
"6-0": "`attribute`",
"6-1": "API field name of the desired attribute. Only \"Word\" attributes and some \"Other\" attributes that have an entity value (more details below) can be used.",
"6-2": "`asset_class`",
"7-0": "`type`",
"7-1": "The attribute's value type. \n \nPossible values types are: \n \n- `WORD`\n- `FINANCIAL_ENTITY`Required for GET requests.",
"7-2": "`WORD`",
"8-0": "`value`",
"8-1": "Attribute value that will be used in the association. \n \nUsually, this is a string. However, \"Other\" attributes with an entity value should provide its Entity ID as either a number or a numeric string.",
"8-2": "`\"Equity\"`"
},
"cols": 3,
"rows": 9,
"align": [
"left",
"left",
"left"
]
}
[/block]

## Using attributes with entity values

In addition to all "Word" attributes, three built-in "Other" attributes have entity values and can be used in benchmark associations:

- `bottom_level_holding_account`: Provide an account's Entity ID as the value.
- `sleeve`: Provide a sleeve's Entity ID as the value.
- `security`: Provide an investment's Entity ID as the value.

If the provided Entity ID belongs to an entity with the incorrect model type for the given attribute, a 400 error will occur.

**Example JSON**

```Text EXAMPLE JSON
{
    "data": {
        "id": "11",
        "type": "benchmark_associations_strategies",
        "attributes": {
            "matching_type": "PATH",
            "benchmark_associations": [
                {
                    "rules": [
                        {
                            "attribute": "security",
                            "value": 200,
                            "type": "FINANCIAL_ENTITY"
                        }
                    ],
                    "benchmarks": [
                        571
                    ]
                }
            ],
            "display_name": "Security Benchmarks"
        },
        "links": {
            "self": "/v1/benchmark_associations_strategies/11"
        }
    },
    "included": []
}
```

# Get all benchmark associations strategies

Returns a paginated list of all active benchmark associations strategies.

**GET** `/v1/benchmark_associations_strategies`

**Optional pagination parameters**

A 500 strategy per page maximum is enforced per request. If there are more than 500, the set will be truncated automatically, and the remaining values linked from the "next" URL in the top-level links object. `"next": /v1/benchmark_associations_strategies?page[limit]=500&page[after]=500`

- `page[limit]`: Number of strategies to be returned. Integer. The maximum result set size is 500.
- `page[after]`: The next page; the returned paginated data must have as its first item the item that is immediately after the cursor in the results list. Integer.

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/benchmark_associations_strategies
```

```Text RESPONSE
HTTP/1.1 200 Success

{
    "data": [
        {
            "id": "2",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [
                    {
                        "rules": [
                            {
                                "attribute": "asset_class",
                                "value": "Equity",
                                "type": "WORD"
                            }
                        ],
                        "benchmarks": [
                            734
                        ]
                    },
                    {
                        "rules": [
                            {
                                "attribute": "sector",
                                "value": "Energy",
                                "type": "WORD"
                            }
                        ],
                        "benchmarks": [
                            735
                        ]
                    }
                ],
                "display_name": "Default Strategy"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/2"
            }
        },
        {
            "id": "3",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PDN",
                "benchmark_associations": [
                    {
                        "rules": [
                            {
                                "attribute": "asset_class",
                                "value": "Derivative",
                                "type": "WORD"
                            }
                        ],
                        "benchmarks": [
                            734
                        ]
                    },
                    {
                        "rules": [
                            {
                                "attribute": "country",
                                "value": "AFG",
                                "type": "WORD"
                            }
                        ],
                        "benchmarks": [
                            559
                        ]
                    }
                ],
                "display_name": "PDN Strategy"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/3"
            }
        },
        {
            "id": "4",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [],
                "display_name": "(ALL) Security Benchmarks"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/4"
            }
        },
        {
            "id": "5",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [],
                "display_name": "(ALL) Security Benchmarks"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/5"
            }
        },
        {
            "id": "6",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [
                    {
                        "rules": [
                            {
                                "attribute": "bottom_level_holding_account",
                                "value": 22,
                                "type": "FINANCIAL_ENTITY"
                            }
                        ],
                        "benchmarks": [
                            571
                        ]
                    }
                ],
                "display_name": "(ALL) Security Benchmarks"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/6"
            }
        },
        {
            "id": "7",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [
                    {
                        "rules": [
                            {
                                "attribute": "bottom_level_holding_account",
                                "value": 22,
                                "type": "FINANCIAL_ENTITY"
                            }
                        ],
                        "benchmarks": [
                            571
                        ]
                    }
                ],
                "display_name": "(ALL) Security Benchmarks"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/7"
            }
        },
        {
            "id": "8",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [
                    {
                        "rules": [
                            {
                                "attribute": "bottom_level_holding_account",
                                "value": 208,
                                "type": "FINANCIAL_ENTITY"
                            }
                        ],
                        "benchmarks": [
                            571
                        ]
                    }
                ],
                "display_name": "(ALL) Security Benchmarks"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/8"
            }
        },
        {
            "id": "9",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [
                    {
                        "rules": [
                            {
                                "attribute": "bottom_level_holding_account",
                                "value": 208,
                                "type": "FINANCIAL_ENTITY"
                            }
                        ],
                        "benchmarks": [
                            571
                        ]
                    }
                ],
                "display_name": "(ALL) Security Benchmarks"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/9"
            }
        },
        {
            "id": "10",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [
                    {
                        "rules": [
                            {
                                "attribute": "security",
                                "value": 213,
                                "type": "FINANCIAL_ENTITY"
                            }
                        ],
                        "benchmarks": [
                            571
                        ]
                    }
                ],
                "display_name": "(ALL) Security Benchmarks"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/10"
            }
        },
        {
            "id": "11",
            "type": "benchmark_associations_strategies",
            "attributes": {
                "matching_type": "PATH",
                "benchmark_associations": [
                    {
                        "rules": [
                            {
                                "attribute": "security",
                                "value": 200,
                                "type": "FINANCIAL_ENTITY"
                            }
                        ],
                        "benchmarks": [
                            571
                        ]
                    }
                ],
                "display_name": "(ALL) Security Benchmarks"
            },
            "links": {
                "self": "/v1/benchmark_associations_strategies/11"
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
- `403 Forbidden`: The currently logged-in user does not have permission to view/edit benchmark associations.

# Get a benchmark associations strategy

Returns a benchmark associations strategy with the given ID.

**GET** `/v1/benchmark_associations_strategies/:id`

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/benchmark_associations_strategies/2
```

```Text RESPONSE
HTTP/1.1 200 Success

{
    "data": {
        "id": "2",
        "type": "benchmark_associations_strategies",
        "attributes": {
            "matching_type": "PATH",
            "benchmark_associations": [
                {
                    "rules": [
                        {
                            "attribute": "asset_class",
                            "value": "Equity",
                            "type": "WORD"
                        }
                    ],
                    "benchmarks": [
                        734
                    ]
                },
                {
                    "rules": [
                        {
                            "attribute": "sector",
                            "value": "Energy",
                            "type": "WORD"
                        }
                    ],
                    "benchmarks": [
                        735
                    ]
                }
            ],
            "display_name": "Default Strategy"
        },
        "links": {
            "self": "/v1/benchmark_associations_strategies/2"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success.
- `403 Forbidden`: The currently logged-in user does not have permission to view/edit benchmark associations.
- `404 Not Found`: The provided ID does not exist.

# Create a benchmark associations strategy

Adds a new benchmark associations strategy to your firm. Only one strategy can be created per request.

**POST** `/v1/benchmark_associations_strategies`

**Example**

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/benchmark_associations_strategies

{
    "data": {
        "type": "benchmark_associations_strategies",
        "attributes": {
            "matching_type": "PATH",
            "benchmark_associations": [
                {
                    "rules": [
                        {
                            "attribute": "asset_class",
                            "value": "Equity"
                        }
                    ],
                    "benchmarks": [
                        571
                    ]
                }
            ],
            "display_name": "Equity Strategy"
        }
    }
}
```

```Text RESPONSE
HTTP/1.1 201 Created

{
    "data": {
        "id": "18",
        "type": "benchmark_associations_strategies",
        "attributes": {
            "matching_type": "PATH",
            "benchmark_associations": [
                {
                    "rules": [
                        {
                            "attribute": "asset_class",
                            "value": "Equity",
                            "type": "WORD"
                        }
                    ],
                    "benchmarks": [
                        571
                    ]
                }
            ],
            "display_name": "Equity Strategy"
        },
        "links": {
            "self": "/v1/benchmark_associations_strategies/18"
        }
    },
    "included": []
}
```

**Response codes**

- `201 Created`: Success.
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: The currently logged-in user does not have permission to view/edit benchmark associations.

# Update a benchmark associations strategy

Modifies an existing benchmark associations strategy.

**PATCH** /`v1/benchmark_associations_strategies/:id`

To update the `matching_type` and/or `display_name` of the strategy without changing the underlying associations, omit the `benchmark_associations` field from the request. This will preserve all existing associations.

When you include the `benchmark_associations`, newly provided associations will overwrite all existing associations. To append new associations to the existing list, run a `GET /v1/benchmark_associations_strategies/:id` request first and modify the payload as desired.

**Example**

```Text REQUEST
PATCH https://examplefirm.addepar.com/api/v1/benchmark_associations_strategies/18

{
    "data": {
        "id": "18",
        "type": "benchmark_associations_strategies",
        "attributes": {
            "matching_type": "PATH",
            "benchmark_associations": null,
            "display_name": "Equity Strategy"
        }
    }
}
```

```Text RESPONSE
HTTP/1.1 200 Success

{
    "data": {
        "id": "18",
        "type": "benchmark_associations_strategies",
        "attributes": {
            "matching_type": "PATH",
            "benchmark_associations": [],
            "display_name": "Equity Strategy"
        },
        "links": {
            "self": "/v1/benchmark_associations_strategies/18"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success.
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: The currently logged-in user does not have permission to view/edit benchmark associations.
- `404 Not Found`: The provided ID does not exist.
- `409 Conflict`: The id field in the request payload does not match the ID in the URL.

# Delete a benchmark associations strategy

Deletes an existing benchmark associations strategy if it exists.

**DELETE** `/v1/benchmark_associations_strategies/:id`

**Example**

```Text REQUEST
DELETE https://examplefirm.addepar.com/api/v1/benchmark_associations_strategies/18
```

```Text RESPONSE
HTTP/1.1 204 No Content
```

**Response codes**

- `204 No Content`: Success.
- `403 Forbidden`: The currently logged-in user does not have permission to view/edit benchmark associations.
- `404 Not Found`: The provided ID does not exist.
