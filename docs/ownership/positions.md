# Positions

The Positions API can be used to view, create, update, and delete positions in Addepar. Positions are a connection between two entities in our ownership graph.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/positions",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/positions/:id \n/v1/positions \n/v1/positions/:id/owner \n/v1/positions/:id/owned \n/v1/positions/:id/relationships/owner \n/v1/positions/:id/relationships/owned \n \n**POST** \n/v1/positions \n \n**PATCH** \n/v1/positions/:id \n/v1/positions \n \n**DELETE** \n/v1/positions/:id \n/v1/positions",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Portfolio Access\" is required to retrieve, update, and delete positions. \n \n“Transactions: Full permission (view, create, and edit)” is required to create, update and delete positions. \n \n\"Manage Attributes: Only edit certain attribute values or Manage all values and settings” is required to apply, edit, or delete attributes.",
"5-0": "OAuth scopes",
"5-1": "`POSITIONS` or `POSITIONS_WRITE`"
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

Positions are described by the below resource object attributes. Attributes required for creating, updating or deleting Positions are noted. You can assign additional standard and custom attributes to Positions.

All attributes will be returned in successful **GET**, **POST** & **PATCH** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`name`",
"0-1": "Position name. String. \n \nRequired for cash positions. \n \nNames must be different for cash positions that have the same owner and owned entities.",
"0-2": "`\"GOOG\"`",
"1-0": "`incepting_open_position_date`",
"1-1": "Date that ownership was first linked. String. “YYYY-MM-DD” \n \nRequired for Percent Based Assets. \n \nNot applicable for Share Based Assets or Value Based Assets. \n \nWhen linking an entity that directly owns share-based assets, like an account, use a date one day earlier than the first transaction or snapshot. Otherwise, use a historical date like 1900/01/01.",
"1-2": "`“2015-12-31”`",
"2-0": "`incepting_open_position_ownership_percentage`",
"2-1": "Percentage ownership. Number. (Percent, represented as a decimal) \n \nRequired for Percent Based Assets. \n \nNot applicable for Share Based Assets or Value Based Assets.",
"2-2": "`.5`",
"3-0": "`created_at`",
"3-1": "Not editable and cannot be passed in. String.",
"3-2": "`\"2023-07-28T02:24:30Z\"`",
"4-0": "`modified_at`",
"4-1": "Not editable and cannot be passed in. String.",
"4-2": "`\"2023-07-30T10:43:21Z\"`",
"5-0": "Optional attributes",
"5-1": "Additional attributes can be applied to positions.",
"5-2": "[See Addepar Attributes](https://developers.addepar.com/docs/addepar-attributes-1)"
},
"cols": 3,
"rows": 6,
"align": [
"left",
"left",
"left"
]
}
[/block]

## Relationships

| Relationship | Description                                    |
| :----------- | :--------------------------------------------- |
| `owner`      | The entity that holds the position.            |
| `owned`      | The entity that is being held in the position. |

```json Relationships
"relationships":{
        "owner":{
          "links":{
            "self":"/v1/positions/1017641/relationships/owner",
            "related":"/v1/positions/1017641/owner"
          },
          "data":{
            "type":"entities",
            "id":"259825"
          }
        },
        "owned":{
          "links":{
            "self":"/v1/positions/1017641/relationships/owned",
            "related":"/v1/positions/1017641/owned"
          },
          "data":{
            "type":"entities",
            "id":"259837"
          }
        }
      },
      "links":{
        "self":"/v1/positions/1017641"
      }
    }
```

> 📘 Note
>
> There can be more than one open position between the same owner entity and owned entity. However, the positions route only reads or writes to the incepting open position. All **GET** responses include the incepting open position, and all **PATCH** requests modify the incepting open position.

## Get a position

Returns details for the specified position, including inception information and relationships.

**GET** `/v1/positions/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/positions/100
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"100",
    "type":"positions",
    "attributes":{
      "incepting_open_position_date":"2010-01-01",
      "incepting_open_position_ownership_percentage":1.0,
      "created_at":"2023-07-28T02:24:30Z",
      "modified_at":"2023-07-30T10:43:21Z"
    },
    "relationships":{
      "owner":{
        "links":{
          "self":"/v1/positions/100/relationships/owner",
          "related":"/v1/positions/100/owner"
        },
        "data":{
          "type":"entities",
          "id":"1"
        }
      },
      "owned":{
        "links":{
          "self":"/v1/positions/100/relationships/owned",
          "related":"/v1/positions/100/owned"
        },
        "data":{
          "type":"entities",
          "id":"2"
        }
      }
    },
    "links":{
      "self":"/v1/positions/100"
    }
  },
  "included":[

  ]
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned position ID

## Get all positions

Returns details for all positions, including inception information and relationships.

**GET** `/v1/positions`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/positions
```

```json
HTTP/1.1 200

{
  "data":[
    {
      "type":"positions",
      "id":"13",
      "attributes":{
        "name":"Bob",
        "display_name":"Bob",
        "incepting_open_position_date":"2016-12-01",
        "incepting_open_position_value":5,
        "created_at":"2023-07-28T02:24:30Z",
        "modified_at":"2023-07-30T10:43:21Z"
      },
      "relationships":{
        "owner":{
          "links":{
            "self":"/v1/positions/13/relationships/owner",
            "related":"/v1/positions/13/owner"
          },
          "data":{
            "type":"entities",
            "id":"1"
          }
        },
        "owned":{
          "links":{
            "self":"/v1/positions/13/relationships/owned",
            "related":"/v1/positions/13/owned"
          },
          "data":{
            "type":"entities",
            "id":"2"
          }
        }
      },
      "links":{
        "self":"/v1/positions/13"
      }
    },
    {
      "type":"positions",
      "id":"14",
      "attributes":{
        "name":"Bob",
        "display_name":"Bob",
        "incepting_open_position_date":"2016-12-01",
        "incepting_open_position_value":5,
        "created_at":"2023-07-28T02:24:30Z",
        "modified_at":"2023-07-30T10:43:21Z"
      },
      "relationships":{
        "owner":{
          "links":{
            "self":"/v1/positions/13/relationships/owner",
            "related":"/v1/positions/13/owner"
          },
          "data":{
            "type":"entities",
            "id":"1"
          }
        },
        "owned":{
          "links":{
            "self":"/v1/positions/13/relationships/owned",
            "related":"/v1/positions/13/owned"
          },
          "data":{
            "type":"entities",
            "id":"2"
          }
        }
      },
      "links":{
        "self":"/v1/positions/14"
      }
    }
  ]
}
```

**Optional parameters**
[block:parameters]
{
"data": {
"h-0": "Filter",
"h-1": "Description",
"h-2": "Example",
"0-0": "fields[positions]",
"0-1": "Returns only the attributes specified for each position. Ignores spaces. \n \nYou can filter by `fields[positions]=[]` to omit all attributes.",
"0-2": "`fields[positions]=incepting_open_position_date`",
"1-0": "created_before",
"1-1": "Returns all positions created on or before a date, formatted as YYYY-MM-DD.",
"1-2": "`filter[created_before]=\"2023-04-12\"`",
"2-0": "created_after",
"2-1": "Returns all positions created on or after a date, formatted as YYYY-MM-DD.",
"2-2": "`filter[created_after]=\"2023-04-12\"`",
"3-0": "modified_before",
"3-1": "Returns all positions last modified on or before a date, formatted as YYYY-MM-DD.",
"3-2": "`filter[modified_before]=\"2023-04-12\"`",
"4-0": "modified_after",
"4-1": "Returns all positions last modified on or after a date, formatted as YYYY-MM-DD.",
"4-2": "`filter[modified_after]=\"2023-04-12\"`",
"5-0": "owner_model_types",
"5-1": "Returns all positions whose direct owners have a passed-in model type. Ignores spaces.",
"5-2": "`filter[owner_model_types]=PERSON_NODE,TRUST`",
"6-0": "owned_model_types",
"6-1": "Returns all positions whose owned entities have a passed-in model type. Ignores spaces.",
"6-2": "`filter[owned_model_types]=STOCK,BOND`",
"7-0": "owner_entity_id",
"7-1": "Returns all positions whose direct owner has a passed-in entity ID. Ignores spaces.",
"7-2": "`filter[owner_entity_id]=24,26`",
"8-0": "owned_entity_id",
"8-1": "Returns all positions whose owned entity has a passed-in entity ID. Ignores spaces.",
"8-2": "`filter[owned_entity_id]=23,25`"
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

\*\*Response codes: \*\*

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted

## Get position owner entity details

Returns the owner entity.

**GET** `/v1/positions/:id/owner`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/positions/9/owner
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"192",
    "type":"entities",
    "attributes":{
      "currency_factor":"USD",
      "original_name":"Repeated Client",
      "model_type":"PERSON_NODE"
    },
    "links":{
      "self":"/v1/entities/192"
    }
  }
}
```

\*\*Response codes: \*\*

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned entities IDs

## Get position owned entity details

Returns the owned entity.

**GET** `/v1/positions/:id/owned`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/positions/9/owned
```

```json
HTTP/1.1 200

{
  "data":{
    "id":"23",
    "type":"entities",
    "attributes":{
      "currency_factor":"USD",
      "ownership_type":"PERCENT_BASED",
      "original_name":"Trust 1",
      "model_type":"TRUST",
      "is_rolled_up":false,
      "display_name":"Trust 1 Display Name"
    },
    "links":{
      "self":"/v1/entities/23"
    }
  }
}
```

\*\*Response codes: \*\*

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned entities IDs

## Get owner relationship

Returns the relationship of the owner entity.

**GET** `/v1/positions/:id/relationships/owner`

```curl Request
GET https://examplefirm.addepar.com/api/v1/positions/9/relationships/owner
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":192,
    "type":"entities"
  }
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted

## Get owned relationship

Returns the relationship of the owned entity.

GET `/v1/positions/:id/relationships/owned`

```curl Request
GET https://examplefirm.addepar.com/api/v1/positions/9/relationships/owned
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":23,
    "type":"entities"
  }
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted

## Create a position

Creates a new open position.

**POST** `/v1/positions`

**Example:**

In this example, we establish a position between an account (entity 27) and a stock (entity 29) with share-based ownership. This request schema also applies when creating a position for an asset with value-based ownership.

```curl Request
POST https://examplefirm.addepar.com/api/v1/positions

{
  "data":{
    "type":"positions",
    "attributes":{

    },
    "relationships":{
      "owner":{
        "data":{
          "type":"entities",
          "id":"27"
        }
      },
      "owned":{
        "data":{
          "type":"entities",
          "id":"29"
        }
      }
    }
  }
}
```

```json Response
HTTP/1.1 201

{
  "data":{
    "id":"338",
    "type":"positions",
    "relationships":{
      "owner":{
        "links":{
          "self":"/v1/positions/338/relationships/owner",
          "related":"/v1/positions/338/owner"
        },
        "data":{
          "type":"entities",
          "id":"27"
        }
      },
      "owned":{
        "links":{
          "self":"/v1/positions/338/relationships/owned",
          "related":"/v1/positions/338/owned"
        },
        "data":{
          "type":"entities",
          "id":"29"
        }
      }
    },
    "links":{
      "self":"/v1/positions/338"
    }
  },
  "included":[

  ]
}
```

**Example:**

In this example, we establish a position between a person (entity 22) and a trust (entity 23), which has percent-based ownership. The attribute object of the request requires `"incepting_open_position_date"` and `"incepting_open_position_ownership_percentage"` in order to successfully create the position.

```curl Request
POST https://examplefirm.addepar.com/api/v1/positions

{
  "data":{
    "type":"positions",
    "attributes":{
      "incepting_open_position_date":"2001-01-01",
      "incepting_open_position_ownership_percentage":1.0
    },
    "relationships":{
      "owner":{
        "data":{
          "type":"entities",
          "id":"22"
        }
      },
      "owned":{
        "data":{
          "type":"entities",
          "id":"23"
        }
      }
    }
  }
}
```

```json Response
HTTP/1.1 201

{
  "data":{
    "id":"340",
    "type":"positions",
    "attributes":{
      "incepting_open_position_date":"2001-01-01",
      "incepting_open_position_ownership_percentage":1.0
    },
    "relationships":{
      "owner":{
        "links":{
          "self":"/v1/positions/340/relationships/owner",
          "related":"/v1/positions/340/owner"
        },
        "data":{
          "type":"entities",
          "id":"22"
        }
      },
      "owned":{
        "links":{
          "self":"/v1/positions/340/relationships/owned",
          "related":"/v1/positions/340/owned"
        },
        "data":{
          "type":"entities",
          "id":"23"
        }
      }
    },
    "links":{
      "self":"/v1/positions/340"
    }
  },
  "included":[

  ]
}
```

**Response codes:**

- `201 Created`: Successfully created the given position
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned entity ID or attribute
- `409 Conflict`: Incorrect "type"

## Create multiple positions

Creates new open positions.

**POST** `/v1/positions`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/positions

{
  "data":[
    {
      "type":"positions",
      "attributes":{
        "incepting_open_position_date":"2012-12-01",
        "incepting_open_position_ownership_percentage":1.0
      },
      "relationships":{
        "owner":{
          "data":{
            "type":"entities",
            "id":1
          }
        },
        "owned":{
          "data":{
            "type":"entities",
            "id":2
          }
        }
      }
    },
    {
      "type":"positions",
      "attributes":{
        "incepting_open_position_date":"2012-01-01",
        "incepting_open_position_ownership_percentage":1.0
      },
      "relationships ":{
        "owner":{
          "data":{
            "type":"entities",
            "id":3
          }
        },
        "owned":{
          "data":{
            "type":"entities",
            "id":4
          }
        }
      }
    }
  ]
}
```

```json Response
HTTP/1.1 201

{
  "data": [ {
    "type": "positions",
    “id”: “100”,
    "attributes": {
      "incepting_open_position_date": "2012-12-01",
      “incepting_open_position_ownership_percentage”: 1.0
    },
    "relationships ": {
        "owner": {
	“links”: {
		     “self”: “/v1/positions/100/relationships/owner”,
		     “related”: “/v1/positions/100/owner”
		     },
            "data": {
   "type": "entities",
}
      },
        "owned": {
	“links”: {
		     “self”: “/v1/positions/100/relationships/owned”,
		     “related”: “/v1/positions/100/owned”
		     },
            "data": {
    "type": "entities",
    "id": 2
}
      }
    },
	“links”: {
	      “self”: “/v1/positions/100”
	}
       },
  {
    "type": "positions",
    “id”: “200”,
    "attributes": {
      "incepting_open_position_date": "2012-01-01",
      “incepting_open_position_ownership_percentage”: 1.0
    },
    "relationships ": {
        "owner": {
	“links”: {
		     “self”: “/v1/positions/200/relationships/owner”,
		     “related”: “/v1/positions/200/owner”
		     },
            "data": {
    "type": "entities",
    "id": 3
}
      },
        "owned": {
	“links”: {
		     “self”: “/v1/positions/200/relationships/owned”,
		     “related”: “/v1/positions/200/owned”
		     },
            "data": {
    "type": "entities",
    "id": 4
}
   "id": 1
      }
    },
“links”: {
	      “self”: “/v1/positions/200”
	}
       }
   ]
}
```

**Response codes:**

- `201 OK`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned entity ID or attribute
- `409 Conflict`: Incorrect "type"

## Update a position

Updates the specified position.

**PATCH** `/v1/positions/:id`

**Example:**

For a percent-based asset, update the open position date and ownership percentage. The response returns all position level attributes that have been assigned.

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/positions/104

{
  "data":{
    "type":"positions",
    "id":"104",
    "attributes":{
      "incepting_open_position_date":"2010-01-01",
      "incepting_open_position_ownership_percentage":0.2
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"104",
    "type":"positions",
    "attributes":{
      "incepting_open_position_date":"2010-01-01",
      "incepting_open_position_ownership_percentage":0.2,
      "_custom_assett_class_1234":[
        {
          "date":null,
          "value":"cash",
          "weight":1.0
        }
      ],
      "display_name":"Did Both"
    },
    "relationships":{
      "owner":{
        "links":{
          "self":"/v1/positions/104/relationships/owner",
          "related":"/v1/positions/61581171/owner"
        },
        "data":{
          "type":"entities",
          "id":"123"
        }
      },
      "owned":{
        "links":{
          "self":"/v1/positions/104/relationships/owned",
          "related":"/v1/positions/104/owned"
        },
        "data":{
          "type":"entities",
          "id":"456"
        }
      }
    },
    "links":{
      "self":"/v1/positions/104"
    }
  },
  "included":[

  ]
}
```

**Example:**

Updates custom and standard position level attributes.

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/positions/998

{
  "data":{
    "type":"positions",
    "id":"998",
    "attributes":{
      "_custom_balance_sheet_12345":[
        {
          "value":"Below The Line"
        }
      ],
      "display_name":"My Cash Asset"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"998",
    "type":"positions",
    "attributes":{
      "_custom_balance_sheet_12345":[
        {
          "date":null,
          "value":"Below The Line",
          "weight":1.0
        }
      ],
      "display_name":"My Cash Asset"
    },
    "relationships":{
      "owner":{
        "links":{
          "self":"/v1/positions/998/relationships/owner",
          "related":"/v1/positions/998/owner"
        },
        "data":{
          "type":"entities",
          "id":"99"
        }
      },
      "owned":{
        "links":{
          "self":"/v1/positions/998/relationships/owned",
          "related":"/v1/positions/998/owned"
        },
        "data":{
          "type":"entities",
          "id":"100"
        }
      }
    },
    "links":{
      "self":"/v1/positions/998"
    }
  },
  "included":[

  ]
}
```

**Response codes:**

- `200 OK`: Successfully modified the given position
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned position ID
- `409 Conflict`: IDs in the payload and URL do not match, or incorrect "type"

## Update multiple positions

Updates the specified open positions.

**PATCH** `/v1/positions`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/position

{
  "data":[
    {
      "type":"positions",
      "id":"13",
      "attributes":{
        "name":"Bob",
        "display_name":"Bob",
        "incepting_open_position_date":"2016-12-01",
        "incepting_open_position_value":5
      },
      "relationships":{
        "owner":{
          "data":{
            "type":"entities",
            "id":"1"
          }
        },
        "owned":{
          "data":{
            "type":"entities",
            "id":"2"
          }
        }
      }
    },
    {
      "type":"positions",
      "id":"14",
      "attributes":{
        "name":"Bob",
        "display_name":"Bob",
        "incepting_open_position_date":"2016-12-01",
        "incepting_open_position_value":5
      },
      "relationships":{
        "owner":{
          "data":{
            "type":"entities",
            "id":"1"
          }
        },
        "owned":{
          "data":{
            "type":"entities",
            "id":"2"
          }
        }
      }
    }
  ]
}
```

```json Response
HTTP/1.1 200

{
  "data":[
    {
      "type":"positions",
      "id":"13",
      "attributes":{
        "name":"Bob",
        "display_name":"Bob",
        "incepting_open_position_date":"2016-12-01",
        "incepting_open_position_value":5
      },
      "relationships":{
        "owner":{
          "links":{
            "self":"/v1/positions/13/relationships/owner",
            "related":"/v1/positions/13/owner"
          },
          "data":{
            "type":"entities",
            "id":"1"
          }
        },
        "owned":{
          "links":{
            "self":"/v1/positions/13/relationships/owned",
            "related":"/v1/positions/13/owned"
          },
          "data":{
            "type":"entities",
            "id":"2"
          }
        }
      },
      "links":{
        "self":"/v1/positions/13"
      }
    },
    {
      "type":"positions",
      "id":"14",
      "attributes":{
        "name":"Bob",
        "display_name":"Bob",
        "incepting_open_position_date":"2016-12-01",
        "incepting_open_position_value":5
      },
      "relationships":{
        "owner":{
          "links":{
            "self":"/v1/positions/13/relationships/owner",
            "related":"/v1/positions/13/owner"
          },
          "data":{
            "type":"entities",
            "id":"1"
          }
        },
        "owned":{
          "links":{
            "self":"/v1/positions/13/relationships/owned",
            "related":"/v1/positions/13/owned"
          },
          "data":{
            "type":"entities",
            "id":"2"
          }
        }
      },
      "links":{
        "self":"/v1/positions/14"
      }
    }
  ]
}
```

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned position ID
- `409 Conflict`: Incorrect "type"

## Delete a position

Removes a specified position.

**DELETE** `/v1/positions/:id`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/positions/100
```

```json Response
HTTP/1.1 204
```

**Response codes:**

- `204 No Content`: Successfully deleted the position
- `400 Bad Request`: Position is being referenced in transactions
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned position ID
- `409 Conflict`: IDs in the payload and URL do not match, or incorrect type

## Delete multiple positions

Removes the specified positions.

**DELETE** `/v1/positions`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/positions

{
  "data":[
    {
      "type":"positions",
      "id":"13"
    },
    {
      "type":"positions",
      "id":"14"
    }
  ]
}
```

```json Response
HTTP/1.1 204
```

**Response codes:**

- `204 No Content`: Successfully deleted the positions
- `400 Bad Request`: A position is being referenced in transactions
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Nonexistent/non-permissioned position IDs
- `409 Conflict`: Incorrect "type"
