# Constituent Attributes

Constituents are investments held by a [composite security](https://developers.addepar.com/docs/composite-securities-limited-access), like an ETF.

Investments that are directly owned by portfolios in your firm will include an Entity ID, while those that are not yet owned directly will not have an Entity ID and will be sourced from market data. We refer to those investments as security master constituents.

With the Constituent Attributes API, you can assign [attribute](https://developers.addepar.com/docs/addepar-attributes-1) values to security master constituents. These attributes are tied to the constituent's ASM ID, which uniquely identifies it in Addepar's security master.

When looking at attribute values, entity-level attributes will take precedence over constituent attributes.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/constituent_attributes",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/constituent_attributes/:id \n \n**POST** \n/v1/constituent_attributes \n \n**PATCH** \n/v1/constituent_attributes/:id \n \n**PATCH** \n/v1/constituent_attributes \n \n**DELETE** \n/v1/constituent_attributes/:id \n \n**DELETE** \n/v1/constituent_attributes",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" is required to retrieve available attributes.",
"5-0": "OAuth Scopes",
"5-1": "`PORTFOLIO`, `TRANSACTIONS`, `TRANSACTIONS_WRITE`, `ENTITIES`, `ENTITIES_WRITE`"
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

All attributes will be returned in successful **GET**, **POST** & **PATCH** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`asm_id`",
"0-1": "The ASM ID to which the attribute value will be assigned. The ASM ID must correspond to a constituent.",
"0-2": "`1234567890`",
"1-0": "`attribute_key`",
"1-1": "The attribute's API field name.",
"1-2": "`asset_class`",
"2-0": "`values`",
"2-1": "The value (or time-varying values) that should be assigned to the constituent's ASM ID.",
"2-2": "`Equity` \n[See how to format values](https://developers.addepar.com/docs/addepar-attributes-1)"
},
"cols": 3,
"rows": 3,
"align": [
"left",
"left",
"left"
]
}
[/block]

## Get a constituent attribute

Retrieves a specific attribute on a specific constituent. You can identify the attribute-constituent pairing by its ID returned in API responses.

**GET** `/v1/constituent_attributes/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/constituent_attributes/1
```

```json Response
HTTP/1.1 200

{
    "data": {
        "id": "1",
        "type": "constituent_attributes",
        "attributes": {
            "asm_id": 123456,
            "values": [
                {
                    "date": null,
                    "value": "Fixed Income",
                    "weight": 1.0
                }
            ],
            "attribute_key": "asset_class"
        },
        "links": {
            "self": "/v1/constituent_attributes/1"
        }
    },
    "included": []
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: The attribute does not exist or you do not have access to it

## Get all constituent attributes

Retrieves all constituent attributes you have permission to access.

**GET** `/v1/constituent_attributes`

```curl Request
GET https://examplefirm.addepar.com/api/v1/constituent_attributes
```

```json Response
HTTP/1.1 200

{
    "data": [
        {
            "id": "1",
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 1001,
                "values": [
                    {
                        "date": null,
                        "value": "Equity",
                        "weight": 1.0
                    }
                ],
                "attribute_key": "_custom_asset_class_123"
            },
            "links": {
                "self": "/v1/constituent_attributes/1"
            }
        },
        {
            "id": "2",
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 2002,
                "values": [
                    {
                        "date": null,
                        "value": "Alternatives",
                        "weight": 1.0
                    }
                ],
                "attribute_key": "_custom_asset_class_123"
            },
            "links": {
                "self": "/v1/constituent_attributes/2"
            }
        },
        {
            "id": "3",
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 3003,
                "values": [
                    {
                        "date": null,
                        "value": "Private Equity",
                        "weight": 1.0
                    }
                ],
                "attribute_key": "_custom_asset_class_123"
            },
            "links": {
                "self": "/v1/constituent_attributes/3"
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

**Optional parameters**

| Filter  | Description                                                   | Example        |
| :------ | :------------------------------------------------------------ | :------------- |
| `asmId` | Returns only the attributes assigned to the specified ASM ID. | `asmId=123456` |

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid filter parameter
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted

## Add an attribute to a constituent

Adds an attribute value to a constituent, and returns the newly-added value.

Include `asm_id`, `attribute_key`, and `values` in the request.

**POST** `/v1/constituent_attributes`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/constituent_attributes

{
    "data": {
        "type": "constituent_attributes",
        "attributes": {
            "asm_id": 123456,
            "attribute_key": "_custom_asset_class_123",
            "values": [
                {
                    "date": null,
                    "value": "Equity"
                },
                {
                    "date": "2024-12-31",
                    "value": "Private Equity"
                }
            ]
        }
    }
}
```

```json Response
HTTP/1.1 201 Created

{
    "data": {
        "id": "11",
        "type": "constituent_attributes",
        "attributes": {
            "asm_id": 123456,
            "values": [
                {
                    "date": null,
                    "value": "Equity",
                    "weight": 1.0
                },
                {
                    "date": "2024-12-31",
                    "value": "Private Equity",
                    "weight": 1.0
                }
            ],
            "attribute_key": "_custom_asset_class_123"
        },
        "links": {
            "self": "/v1/constituent_attributes/11"
        }
    },
    "included": []
}
```

**Response codes:**

- `201 Created`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `409 Conflict`: The "type" was not specified as "constituent_attributes"

## Add multiple attributes to constituents

Adds attribute values to constituents, and returns the newly-added values.

Include `asm_id`, `attribute_key`, and `values` in the request for each constituent attribute.

**POST** `/v1/constituent_attributes`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/constituent_attributes

{
    "data": [
        {
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 123,
                "attribute_key": "_custom_boolean_custom_1_419",
                "values": true
            }
        },
        {
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 123,
                "attribute_key": "_custom_currency_custom_1_421",
                "values": "EUR"
            }
        }
    ]
}
```

```json Response
HTTP/1.1 201 Created

{
    "data": [
        {
            "id": "51",
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 123,
                "values": [
                    {
                        "date": null,
                        "value": true,
                        "weight": 1.0
                    }
                ],
                "attribute_key": "_custom_boolean_custom_1_419"
            },
            "links": {
                "self": "/v1/constituent_attributes/51"
            }
        },
        {
            "id": "52",
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 123,
                "values": [
                    {
                        "date": null,
                        "value": "EUR",
                        "weight": 1.0
                    }
                ],
                "attribute_key": "_custom_currency_custom_1_421"
            },
            "links": {
                "self": "/v1/constituent_attributes/52"
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

**Response codes:**

- `201 Created`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `409 Conflict`: The "type" was not specified as "constituent_attributes"

## Edit a constituent's attribute value

Updates the value of a constituent's specified attribute. You can identify the attribute-constituent pairing by its ID returned in API responses.

Note: For time-varying or weighted attribute values, you must provide the entire attribute history in the request payload.

**PATCH** `/v1/constituent_attributes/:id`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/constituent_attributes/1

{
    "data": {
        "id": "1",
        "type": "constituent_attributes",
        "attributes": {
            "values": [
                {
                    "date": null,
                    "value": "Private Equity",
                    "weight": 1.0
                }
            ]
        }
    }
}
```

```json Response
HTTP/1.1 200

{
    "data": {
        "id": "1",
        "type": "constituent_attributes",
        "attributes": {
            "asm_id": 2012591051,
            "values": [
                {
                    "date": null,
                    "value": "Private Equity",
                    "weight": 1.0
                }
            ],
            "attribute_key": "_custom_asset_class_1665886"
        },
        "links": {
            "self": "/v1/constituent_attributes/1"
        }
    },
    "included": []
}
```

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden `: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: One or more constituent attributes do not exist or you do not have access to it
- `409 Conflict`: The ID in the path doesn't match the ID in the payload
- `409 Conflict`: The "type" was not specified as "constituent_attributes"

## Edit multiple constituent attribute values

Updates the values of multiple constituent attributes.

**PATCH** `/v1/constituent_attributes`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/constituent_attributes

{
    "data": [
        {
            "id": "1",
            "type": "constituent_attributes",
            "attributes": {
                "values": [
                    {
                        "date": null,
                        "value": "Private Equity",
                        "weight": 1.0
                    }
                ]
            }
        },
        {
            "id": "2",
            "type": "constituent_attributes",
            "attributes": {
                "values": [
                    {
                        "date": null,
                        "value": "Private Equity",
                        "weight": 1.0
                    }
                ]
            }
        }
    ]
}
```

```json Response
HTTP/1.1 200

{
    "data": [
        {
            "id": "1",
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 2012591051,
                "values": [
                    {
                        "date": null,
                        "value": "Private Equity",
                        "weight": 1.0
                    }
                ],
                "attribute_key": "_custom_asset_class_1665886"
            },
            "links": {
                "self": "/v1/constituent_attributes/1"
            }
        },
        {
            "id": "2",
            "type": "constituent_attributes",
            "attributes": {
                "asm_id": 2017357863,
                "values": [
                    {
                        "date": null,
                        "value": "Private Equity",
                        "weight": 1.0
                    }
                ],
                "attribute_key": "_custom_asset_class_1665886"
            },
            "links": {
                "self": "/v1/constituent_attributes/2"
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

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden `: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: One or more constituent attributes do not exist or you do not have access to it
- `409 Conflict`: The "type" was not specified as "constituent_attributes"

## Remove an attribute from a constituent

Removes an attribute value from a constituent. You can identify the attribute-constituent pairing by its ID returned in API responses.

**DELETE** `/v1/constituent_attributes/:id`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/constituent_attributes/1
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `403 Forbidden `: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: One or more constituent attributes do not exist or you do not have access to it

## Remove all attributes from a constituent

Removes all attribute values associated with the provided ASM ID.

**DELETE** `/v1/constituent_attributes?asmId=123456`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/constituent_attributes?asmId=123456
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `403 Forbidden `: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: One or more constituent attributes do not exist or you do not have access to it
