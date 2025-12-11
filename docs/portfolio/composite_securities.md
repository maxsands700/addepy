# Composite Securities

Composite securities are investments made up of underlying "constituent" securities. Common examples of composite securities are ETFs, mutual funds, and benchmarks.

You can track underlying constituent data in Addepar to deepen your analysis of composite securities. Use the Composite Securities API to get, create, and delete constituent weights in Addepar. You can also use the [Constituent Attributes API](https://developers.addepar.com/docs/constituent-attributes) to manage attribute values on constituents.

Addepar currently only supports constituent data for ETFs. We plan to expand this functionality to more investments over time.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/composite_securities",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/composite_securities/:id/:constituentId \n \n**POST** \n/v1/composite_securities/import \n \n**DELETE** \n/v1/composite_securities/:id/:date",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\"",
"5-0": "OAuth scopes",
"5-1": "**GET** \n`COMPOSITE_SECURITIES_READ` \n \n**POST** and **DELETE** \n`COMPOSITE_SECURITIES_WRITE`"
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

Composite securities are described by the below attributes. Required attributes are noted in the description.

| Attribute      | Description                                                                                                                     | Example        |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `date`         | The date of the composite security’s constituent weights. String. Required.                                                     | `"2024-01-01"` |
| `constituents` | A list of objects forming the composite security’s constituents for the specified date. See below for object details. Required. | See below.     |

## Constituent object

The constituent object represents a constituent security and its weighting in the composite security on a particular date.

| Attribute    | Description                                                                     | Example |
| :----------- | :------------------------------------------------------------------------------ | :------ |
| `entityId`   | The constituent security entity, identified by its Entity ID. Number. Required. | `199`   |
| `percentage` | The constituent security's weight. Number. Required.                            | `0.42`  |

# Get constituent weight

Returns a constituent's weight data from within a composite security. Only one constituent can be retrieved per request. If you don't provide a start date or end date, all weights will be returned.

**GET** `/v1/composite_securities/:id/:constituentId`

- `startDate`: The start date for the constituent data (optional)
- `endDate`: The end date for the constituent data (optional)

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/composite_securities/58/199&startDate=2024-01-01
```

```Text RESPONSE
HTTP/1.1 200

{
    "data": {
        "id": "58",
        "type": "constituent_values",
        "attributes": {
            "values": [
                {
                    "2024-01-01": 0.42
                },
                {
                    "2024-01-02": 0.45
                }
            ]
        }
    },
    "included": []
}
```

**Response codes**

- `200 Success`: Success
- `400 Bad Request`: Invalid query parameters
- `400 Bad Request`: Composite Security ID or Constituent ID do not refer to valid entities
- `404 Not Found`: Composite Security ID or Constituent ID not found

# Create constituent weight

Adds new constituent weight data to a composite security on a specific date.

**POST** `/v1/composite_securities/import`

**Example**

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/composite_securities/import

{
  "data": {
    "type": "composite_security",
    "id": "58",
    "attributes":{
      "date": "2024-01-01",
      "constituents": [
        {
          "entityId": 199,
          "percentage": 0.42
        },
        {
          "entityId": 200,
          "percentage": 0.58
        }
      ]
    }
  }
}
```

```Text RESPONSE
HTTP/1.1 200

{
    "data": {
        "id": "58",
        "type": "composite_security",
        "attributes": {
            "date": "2024-01-01",
            "constituents": [
                {
                    "entityId": 199,
                    "percentage": 0.42
                },
                {
                    "entityId": 200,
                    "percentage": 0.58
                }
            ]
        }
    },
    "included": []
}
```

**Response codes**

- `201 Created`: Created
- `400 Bad Request`: Composite Security ID is found in the constituent list
- `400 Bad Request`: Composite Security ID or Constituent ID do not refer to valid entities
- `400 Bad Request`: Duplicate Constituent ID

# Delete constituent weight

Removes all constituent weight data from a composite security on a specific date.

**DELETE** `/v1/composite_securities/:id/:date`

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/composite_securities/58/2024-01-01
```

```Text RESPONSE
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Deleted
