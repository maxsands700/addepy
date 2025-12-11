# Snapshots

Snapshots are used to record the value of a share-based or percent-based asset on a single day. Valuations, on the other hand, are used to record the value of value-based assets like real estate, hedge funds, private equity, venture capital, and private funds.

Use the Snapshots API to get, create, update, and delete snapshots and valuations in Addepar. You can use the [View API](https://developers.addepar.com/docs/transactions-view) to extract existing saved views and [Query API](https://developers.addepar.com/docs/transaction-query) to retrieve snapshot and valuation data.

![](https://files.readme.io/fe2536f-updated_snapshots.png "fe2536f-updated_snapshots.png")
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/snapshots",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/snapshots/:id \n/v1/snapshots/:id/owner \n/v1/snapshots/:id/relationships/owner \n/v1/snapshots/:id/owned \n/v1/snapshots/:id/relationships/owned \n/v1/snapshots/:id/position \n/v1/snapshots/:id/relationships/position \n \n**POST** \n/v1/snapshots \n \n**PATCH** \n/v1/snapshots/:id \n/v1/snapshots \n \n**DELETE** \n/v1/snapshots \n/v1/snapshots/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[No](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Portfolio Access\" determines the entities that are accessible.",
"5-0": "OAuth scopes",
"5-1": "`TRANSACTIONS` or `TRANSACTIONS_WRITE`"
},
"cols": 2,
"rows": 6,
"align": [
"left",
"left"
]
}
[/block]

## Resource overview

Snapshots and valuations are described by the below resource object attributes.

All attributes will be returned in successful **GET** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`type`",
"0-1": "Either \"snapshot\" or \"valuation\". String.",
"0-2": "`\"snapshot\"`",
"1-0": "`currency `",
"1-1": "Three-letter currency code, representing the snapshot or valuation's currency. String.",
"1-2": "`\"USD\"`",
"2-0": "`trade_date `",
"2-1": "The date the snapshot or valuation occurred. String. \n \n\"YYYY-MM-DD \"",
"2-2": "`\"2023-01-25\"`",
"3-0": "`units`",
"3-1": "The number of shares of a security. Number. \n \nOnly required for snapshots on share-based assets.",
"3-2": "`24.48`",
"4-0": "`amount`",
"4-1": "Default value of the snapshot or valuation. Number.",
"4-2": "`1000`",
"5-0": "`created_at`",
"5-1": "Not editable and cannot be passed in. String.",
"5-2": "`\"2023-07-28T02:24:30Z\"`",
"6-0": "`modified_at`",
"6-1": "Not editable and cannot be passed in. String.",
"6-2": "`\"2023-07-30T10:43:21Z\"`",
"7-0": "Optional Attributes",
"7-1": "Additional attributes can be applied to snapshots and valuations. Multiple. \n \nSee \"Optional Snapshot and Valuation Attributes\" below.",
"7-2": "` \"comment\": After 2022 acquisition\"`"
},
"cols": 3,
"rows": 8,
"align": [
"left",
"left",
"left"
]
}
[/block]

\*\* Optional snapshot and valuation attributes\*\*
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"0-0": "`price_factor`",
"0-1": "A multiplier affecting a security's total value. Note that this is called \"Principal Factor\" in Addepar. Number. \n \nOnly applies to bond snapshots.",
"1-0": "`accrued_income_per_unit`",
"1-1": "Accrued income that the custodian may calculate and provide per-unit. Note that **isn't the position's total** accrued income. Number.",
"2-0": "`comment`",
"2-1": "Describes the snapshot or valuation, with a max length of 4,000 characters. String."
},
"cols": 2,
"rows": 3,
"align": [
"left",
"left"
]
}
[/block]

## Relationship overview

| Relationship | Description                                                  |
| :----------- | :----------------------------------------------------------- |
| `owner`      | The ID of the owning entity of the snapshot or valuation.    |
| `owned`      | The ID of the owned entity of the snapshot or valuation.     |
| `position`   | The ID of the position between the owner and owned entities. |

```json Relationships
"relationships": {
      "owner": {
        "links": {
          "self": "/v1/snapshots/1079/relationships/owner",
          "related": "/v1/snapshots/1079/owner"
        },
        "data": {
          "type": "entities",
          "id": "124"
        }
      },
      "position": {
        "links": {
          "self": "/v1/snapshots/1079/relationships/position",
          "related": "/v1/snapshots/1234/position"
        },
        "data": {
          "type": "positions",
          "id": "128"
        }
      },
      "owned": {
        "links": {
          "self": "/v1/snapshots/1079/relationships/owned",
          "related": "/v1/snapshots/1079/owned"
        }
      }
    }
```

## Get a snapshot

Returns a snapshot or valuation with the given ID.

\*\*GET \*\* `/v1/snapshots/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/snapshots/37483253353524
```

```json Response
HTTP/1.1 200 Success

{
    "data": {
        "id": "37483253353524",
        "type": "snapshots",
        "attributes": {
          	"created_at":"2023-07-28T02:24:30Z",
            "amount": -1000000.0,
            "currency": "USD",
            "comment": "",
            "units": 1000.0,
            "type": "snapshot",
            "trade_date": "2023-05-31",
            "modified_at":"2023-07-30T10:43:21Z"
        },
        "relationships": {
            "owner": {
                "links": {
                    "self": "/v1/snapshots/37483253353524/relationships/owner",
                    "related": "/v1/snapshots/37483253353524/owner"
                },
                "data": {
                    "type": "entities",
                    "id": "7644"
                }
            },
            "owned": {
                "links": {
                    "self": "/v1/snapshots/37483253353524/relationships/owned",
                    "related": "/v1/snapshots/37483253353524/owned"
                },
                "data": {
                    "type": "entities",
                    "id": "54"
                }
            },
            "position": {
                "links": {
                    "self": "/v1/snapshots/37483253353524/relationships/position",
                    "related": "/v1/snapshots/37483253353524/position"
                },
                "data": {
                    "type": "positions",
                    "id": "17454"
                }
            }
        },
        "links": {
            "self": "/v1/snapshots/37483253353524"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned snapshot or valuation

## Get snapshot owner entity

Returns the owner entity of the snapshot or valuation.

**GET** `/v1/snapshots/:id/owner`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/37483253353524/owner
```

```json Response
HTTP/1.1 200 Success

{
  "data": {
    "id": "7644",
    "type": "entities",
    "attributes": {
      "last_verified_date": "2023-01-31",
      "currency_factor": "USD",
      "is_archived": false,
      "online_status": "OFFLINE",
      "ownership_type": "PERCENT_BASED",
      "original_name": "Test Account",
      "model_type": "FINANCIAL_ACCOUNT",
      "is_rolled_up": false,
      "wrapper": false
    },
    "links": {
      "self": "/v1/entities/7644"
    }
  },
  "included": []
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned snapshot or valuation
- `404 Not Found`: Nonexistent/non-permissioned entity

## Get snapshot owner relationship

Returns the relationship of the owner entity.

\*\*GET \*\* `/v1/snapshots/:id/relationships/owner`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/snapshots/37483253353524/relationships/owned
```

```json Response
HTTP/1.1 200 Success

{
  "data": {
    "id": 7644,
    "type": "entities"
  }
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned snapshot or valuation

## Get snapshot owned entity

Returns the owned entity of the snapshot or valuation.

\*\*GET \*\* `/v1/snapshots/:id/owned`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/snapshots/37483253353524/owned
```

```json Response
HTTP/1.1 200 Success

{
  "data": {
    "id": "54",
    "type": "entities",
    "attributes": {
      "currency_factor": "EUR",
      "is_archived": false,
      "ownership_type": "SHARE_BASED",
      "original_name": "Convertible Note 3",
      "model_type": "CONVERTIBLE_NOTE",
      "created_at": "2014-08-07T23:37:18Z",
      "modified_at": "2017-09-14T23:06:08Z"
    },
    "links": {
      "self": "/v1/entities/54"
    }
  },
  "included": []
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned snapshot or valuation
- `404 Not Found`: Nonexistent/non-permissioned entity

## Get snapshot owned relationship

Returns the relationship of the owned entity.

\*\*GET \*\* `/v1/snapshots/:id/relationships/owned`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/snapshots/37483253353524/relationships/owned
```

```json Response
HTTP/1.1 200 Success

{
  "data": {
    "id": 54,
    "type": "entities"
  }
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned snapshot or valuation

## Get snapshot position

Returns the snapshot or valuation's position with the given ID.

\*\*GET \*\* `/v1/snapshots/:id/cash_position`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/snapshots/37483253353524/position
```

```json Response
HTTP/1.1 200 Success

{
    "data": {
        "id": "17454",
        "type": "positions",
        "relationships": {
            "owner": {
                "links": {
                    "self": "/v1/positions/17454/relationships/owner",
                    "related": "/v1/positions/17454/owner"
                },
                "data": {
                    "type": "entities",
                    "id": "7644"
                }
            },
            "owned": {
                "links": {
                    "self": "/v1/positions/17454/relationships/owned",
                    "related": "/v1/positions/17454/owned"
                },
                "data": {
                    "type": "entities",
                    "id": "54"
                }
            }
        },
        "links": {
            "self": "/v1/positions/17454"
        }
    },
    "included": []
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned snapshot or valuation
- `404 Not Found`: Nonexistent/non-permissioned entity

## Get snapshot position relationship

Returns the snapshot or valuation's position relationship.

\*\*GET \*\* `/v1/snapshots/:id/relationships/position`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/snapshots/3748325335352/relationships/position
```

```json Response
HTTP/1.1 200 Success

{
  "data": {
    "id": 17454,
    "type": "positions"
  }
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned snapshot or valuation

## Create a snapshot

Adds a new snapshot or valuation to your firm. One request can create up to 500.

**POST**`/v1/snapshots`

**Required fields**

- `type`
- `currency`
- `trade_date`
- `amount`
- `units` required for snapshots, but not valuations

The following fields should be omitted from the object in the payload, since they will be generated when we save the object:

- `id`
- `vendor_id`
- `created_at`
- `modified_at`

**Optional fields**

See "Optional Snapshot and Valuation Attributes" above.

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/snapshots

{
  "data": [
    {
      "type": "snapshots",
      "attributes": {
        "amount": 1000.00,
        "currency": "USD",
        "comment": "This is a comment",
        "units": 10.0,
        "type": "snapshot",
        "trade_date": "2023-01-31"
      },
      "relationships": {
        "owner": {
          "data": {
            "type": "entities",
            "id": "22"
          }
        },
        "owned": {
          "data": {
            "type": "entities",
            "id": "34"
          }
        }
      }
    },
    {
      "type": "snapshots",
      "attributes": {
        "amount": 1000.00,
        "currency": "USD",
        "comment": "This is a comment",
        "units": 10.0,
        "type": "snapshot",
        "trade_date": "2023-02-01"
      },
      "relationships": {
        "owner": {
          "data": {
            "type": "entities",
            "id": "22"
          }
        },
        "owned": {
          "data": {
            "type": "entities",
            "id": "34"
          }
        }
      }
    }
  ]
}
```

```json Response
HTTP/1.1 200 Success

{
    "data": [
        {
            "id": "344671144892",
            "type": "snapshots",
            "attributes": {
                "amount": 1000.0,
                "created_at": "2023-08-22T18:29:05Z",
                "currency": "USD",
                "comment": "This is a comment",
                "units": 10.0,
                "type": "snapshot",
                "modified_at": "2023-08-22T18:29:05Z",
                "trade_date": "2023-01-31"
            },
            "relationships": {
                "owner": {
                    "links": {
                        "self": "/v1/snapshots/344671144892/relationships/owner",
                        "related": "/v1/snapshots/344671144892/owner"
                    },
                    "data": {
                        "type": "entities",
                        "id": "22"
                    }
                },
                "owned": {
                    "links": {
                        "self": "/v1/snapshots/344671144892/relationships/owned",
                        "related": "/v1/snapshots/344671144892/owned"
                    },
                    "data": {
                        "type": "entities",
                        "id": "34"
                    }
                },
                "position": {
                    "links": {
                        "self": "/v1/snapshots/344671144892/relationships/position",
                        "related": "/v1/snapshots/344671144892/position"
                    },
                    "data": {
                        "type": "positions",
                        "id": "160"
                    }
                }
            },
            "links": {
                "self": "/v1/snapshots/344671144892"
            }
        }
    ]
}
```

**Response codes**

- `201 Created`: Success. Snapshot created and returns snapshot JSON
- `400 Bad Request`: If a required field is missing
- `400 Bad Request`: Non-supported type. Supported types are SNAPSHOT or VALUATION
- `400 Bad Request`: If the snapshot fails to validate
- `403 Forbidden`: If the user does not have write access for transactions

## Edit a snapshot

Modifies an existing snapshot or valuation.

**PATCH** `/v1/snapshots/:id`

The following attribute fields cannot be updated:

- `vendor_id`
- `created_at`
- `modified_at`
- `type`
- `trade_date` This will change the snapshot ID, so this update cannot be made via API.

The following relationship fields cannot be updated:

- `owner`
- `owned`
- `position`

To remove an attribute field from a snapshot, set value to null.

**Example:**

This example removes a comment from a snapshot.

```Text Request
PATCH /v1/snapshots/:id

{
  "data": {
    "id": "344671144892",
    "type": "snapshots",
    "attributes": {
      "amount": 1000,
      "currency": "USD",
      "comment": null,
      "trade_date": "2023-01-31"
    }
  }
}
```

```Text Response
HTTP/1.1 200 Success
```

**Response codes**

- `200 OK`: Successfully modified the snapshot
- `400 Bad Request`: Invalid payload
- `400 Bad Request`: If the snapshot fails to validate
- `403 Forbidden`: If the user does not have write access for transactions
- `404 Not Found`: Nonexistent/non-permissioned transaction or snapshot

## Edit multiple snapshots

Modifies existing snapshots or valuations. One request can edit up to 500.

**PATCH** `/v1/snapshots`

The following attribute fields cannot be updated:

- `vendor_id`
- `created_at`
- `modified_at`
- `type`
- `trade_date` This will change the snapshot ID, so this update cannot be made via API

The following relationship fields can not be updated:

- `owner`
- `owned`
- `position`

To remove an attribute field from a snapshot, set value to null.

**Example:**

This example removes a comment from multiple snapshots.

```Text Request
PATCH /v1/snapshots

{
  "data": [
    {
      "id": "344671144892",
      "type": "snapshots",
      "attributes": {
        "comment": null
      }
    },
    {
      "id": "344671144893",
      "type": "snapshots",
      "attributes": {
        "comment": null
      }
    }
  ]
}
```

```Text Response
{
    "data": [
        {
            "id": "344671144892",
            "type": "snapshots",
            "attributes": {
                "amount": 1000.0,
                "created_at": "2023-08-23T03:05:03Z",
                "currency": "USD",
                "comment": "",
                "units": 10.0,
                "type": "snapshot",
                "modified_at": "2023-08-23T03:05:03Z",
                "trade_date": "2023-01-31"
            },
            "relationships": {
                "owner": {
                    "links": {
                        "self": "/v1/snapshots/344671144892/relationships/owner",
                        "related": "/v1/snapshots/344671144892/owner"
                    },
                    "data": {
                        "type": "entities",
                        "id": "22"
                    }
                },
                "owned": {
                    "links": {
                        "self": "/v1/snapshots/344671144892/relationships/owned",
                        "related": "/v1/snapshots/344671144892/owned"
                    },
                    "data": {
                        "type": "entities",
                        "id": "34"
                    }
                },
                "position": {
                    "links": {
                        "self": "/v1/snapshots/344671144892/relationships/position",
                        "related": "/v1/snapshots/344671144892/position"
                    },
                    "data": {
                        "type": "positions",
                        "id": "160"
                    }
                }
            },
            "links": {
                "self": "/v1/snapshots/344671144892"
            }
        },
        {
            "id": "344671144893",
            "type": "snapshots",
            "attributes": {
                "amount": 1000.0,
                "created_at": "2023-08-23T03:05:03Z",
                "currency": "USD",
                "comment": "",
                "units": 10.0,
                "type": "snapshot",
                "modified_at": "2023-08-23T03:05:03Z",
                "trade_date": "2023-02-01"
            },
            "relationships": {
                "owner": {
                    "links": {
                        "self": "/v1/snapshots/344671144893/relationships/owner",
                        "related": "/v1/snapshots/344671144893/owner"
                    },
                    "data": {
                        "type": "entities",
                        "id": "22"
                    }
                },
                "owned": {
                    "links": {
                        "self": "/v1/snapshots/344671144893/relationships/owned",
                        "related": "/v1/snapshots/344671144893/owned"
                    },
                    "data": {
                        "type": "entities",
                        "id": "34"
                    }
                },
                "position": {
                    "links": {
                        "self": "/v1/snapshots/344671144893/relationships/position",
                        "related": "/v1/snapshots/344671144893/position"
                    },
                    "data": {
                        "type": "positions",
                        "id": "160"
                    }
                }
            },
            "links": {
                "self": "/v1/snapshots/344671144893"
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

- `200 OK`: Successfully modified the snapshots
- `400 Bad Request`: Invalid payload
- `400 Bad Request`: If the snapshot fails to validate
- `403 Forbidden`: If the user does not have write access for transactions
- `404 Not Found`: Nonexistent/non-permissioned snapshot

## Delete a snapshot

Deletes an existing snapshot or valuation if it exists.

**DELETE** `v1/snapshots/:id`

```Text Request
DELETE https://examplefirm.addepar.com/api/v1/snapshots/1968
```

```Text Response
HTTP/1.1 204 No Content
```

**Response codes**

- `204 No Content`: Successfully deleted the snapshot
- `403 Forbidden`: If the user does not have permission to delete the snapshot
- `404 Not Found`: Nonexistent/non-permissioned snapshot ID

## Delete multiple snapshots

Deletes existing snapshots or valuations. One request can delete up to 500.

\*\*DELETE \*\* `/v1/snapshots`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/snapshots

{
   "data":[
      {
         "id":"344671144892",
         "type":"snapshots",
      },
      {
         "id":"344671144893",
         "type":"snapshots",
      }
   ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes**

- `204 No Content`: Successfully deleted the snapshots
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: If the user does not have permission to delete the snapshots
- `404 Not Found`: Nonexistent/non-permissioned snapshot IDs
- `409 Conflict` : Incorrect "type"
