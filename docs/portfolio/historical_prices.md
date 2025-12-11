# Historical Prices

Historical prices represent the price of a share-based investment on a specific date. They're usually created for assets that were held before you used Addepar.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/entities/:id/prices",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/entities/:id/prices \n \n**POST** \n/v1/entities/:id/prices \n \n**DELETE** \n/v1/entities/:id/prices/:date",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Application permissions required",
"3-1": "\"API Access: Create, edit, and delete\"",
"4-0": "OAuth scopes",
"4-1": "**GET** \n`HISTORICAL_PRICES_READ` \n \n**POST** and **DELETE** \n`HISTORICAL_PRICES_WRITE`"
},
"cols": 2,
"rows": 5,
"align": [
"left",
"left"
]
}
[/block]

# Resource overview

Historical prices are described by the below attributes.

| Attribute | Description                                                                         | Example        |
| :-------- | :---------------------------------------------------------------------------------- | :------------- |
| `date`    | The date for which the price is recorded, in `YYYY-MM-DD` format. String. Required. | `"2025-01-25"` |
| `source`  | The price data's source. For historical prices, this is always `GLOBAL`. String.    | `"GLOBAL"`     |
| `value`   | The numerical value of the price on the specified date. Number. Required.           | `101.0`        |
| `nodeId`  | The investment's Entity ID that the price is for. Number. Required.                 | `60`           |

# Get historical prices

Returns an entity's historical prices.

**GET** `/v1/entities/:id/prices`

- `date`: The date to retrieve a price for, in `YYYY-MM-DD` format. If omitted, all of the entity's historical prices will be returned (optional).

**Example**

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/entities/60/prices
```

```Text RESPONSE
HTTP/1.1 200 OK

{
    "data": [
        {
            "id": "60_2012-06-29",
            "type": "historical_prices",
            "attributes": {
                "date": "2012-06-29",
                "source": "GLOBAL",
                "value": 101.0,
                "nodeId": 60
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
- `403 Forbidden`: Lacking necessary permissions
- `404 Not Found`: Entity ID is nonexistent or not permissioned, or no price was found for the specified date

# Create or update historical prices

Creates or updates historical prices for a given entity. This operation is asynchronous and returns the background job's ID.

**POST** `/v1/entities/:id/prices`

**Example**

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/entities/60/prices

{
    "data": [
        {
            "type":"historical_prices",
            "attributes":{
                "date": "2012-06-29",
                "nodeId": 60,
                "value": 101.0
            }
        }
    ]
}
```

```Text RESPONSE
HTTP/1.1 200 OK

{
    "async_price_save_id": 10
}
```

**Response codes**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload or creating more prices than the limit
- `403 Forbidden`: Lacking the required permissions to write prices
- `404 Not Found`: Entity ID is nonexistent or not permissioned

# Delete historical prices

Deletes an entity's historical price on a specific date. This operation is asynchronous and returns the background job's ID.

**DELETE** `/v1/entities/:id/prices/:date`

- `date`: The date of the price to be deleted, in `YYYY-MM-DD` format **(required)**.

**Example**

```Text REQUEST
DELETE https://examplefirm.addepar.com/api/v1/entities/60/prices/2012-06-29
```

```Text RESPONSE
HTTP/1.1 200 OK

{
    "async_price_delete_id": 10
}
```

**Response codes**

- `200 OK`: Successfully submitted the job to delete prices
- `400 Bad Request`: The date query parameter is missing
- `403 Forbidden`: Lacking the required permissions to write prices
- `404 Not Found`: Entity ID is nonexistent or not permissioned
