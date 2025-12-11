# Billable Portfolios

A billable portfolio is a portfolio that is associated with a specific fee schedule. A billable portfolio can be a household, client, legal entity, or group. Use the Billable Portfolios API to add new portfolios, edit their fee schedules, archive portfolios, and restore archived portfolios.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/f2cbb17af0f739744885bb35007b64011b8dfddd69f32403847ad1b88f0c7e4a-Active_billable_portfolios.png",
"",
""
],
"align": "center"
}
]
}
[/block]
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/billable_portfolios",
"1-0": "Endpoints",
"1-1": "**POST** \n/v1/billable_portfolios \n \n**PATCH** \n/v1/billable_portfolios/:id/relationships/fee_schedules \n \n**DELETE** \n/v1/billable_portfolios/:id/relationships/fee_schedules",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "No",
"4-0": "Application permissions required",
"4-1": "\"Run and manage bills, include fee adjustment and payment tracking\" or \"Full access to Billing and billing data\"",
"5-0": "OAuth scopes",
"5-1": "`BILLING_WRITE`"
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

Arguments are described by the below resource object attributes and will appear in successful **POST** responses.

| Attribute | Description                                    | Example        |
| :-------- | :--------------------------------------------- | :------------- |
| `id`      | The billable portfolio's ID. List of integers. | `[1234, 5678]` |

## Parameters

| Parameter     | Description                                                                                                                 | Example |
| :------------ | :-------------------------------------------------------------------------------------------------------------------------- | :------ |
| `entity_id`   | The ID of the entity that is a billable portfolio. You can only use either `entity_id` or `group_id` per request, not both. | `1234`  |
| `group_id`    | The ID of the group that is a billable portfolio. You can only use either `entity_id` or `group_id` per request, not both.  | `4567`  |
| `schedule_id` | The ID of the associated fee schedule.                                                                                      | \`9101  |

## Relationships

| Relationship    | Description                            |
| :-------------- | :------------------------------------- |
| `fee_schedules` | The billable portfolio's fee schedule. |

## Add a billable portfolio

Set up a group or entity for billing with a specified fee schedule.

**POST** `/v1/billable_portfolios`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/billable_portfolios

{
  “data”: {
    “type”: “create_billable_portfolio”,
    “attributes”: {
      “group_id”: 1,
      “schedule_id”: 2
    }
  }
}
```

```json Response
HTTP/1.1 200

{
    “id”: 1234
}
```

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/billable_portfolios

{
  “data”: {
    “type”: “create_billable_portfolio”,
    “attributes”: {
      “entity_id”: 1,
      “schedule_id”: 2
    }
  }
}
```

```json Response
HTTP/1.1 200

{
    “id”: 1234
}
```

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Failed during validation
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Argument does not exist

## Update a fee schedule or restore a billable portfolio

Update a billable portfolio's fee schedule to a different one. You can also restore an archived billable portfolio by adding a fee schedule to it.

**PATCH** `/v1/billable_portfolios/:id/relationships/fee_schedules`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/billable_portfolios/2/relationships/fee_schedules

{
  “data”: {
  	"id": 3,
    “type”: “fee_schedules”
  }
}
```

```json Response
HTTP/1.1 200
```

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Failed during validation
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Billable portfolio or fee schedule does not exist.

## Archive a billable portfolio

Archive a billable portfolio when you no longer want to bill on it. None of its previous bills will change.

**DELETE** `/v1/billable_portfolios/:id/relationships/fee_schedules`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/billable_portfolios/2/relationships/fee_schedules
```

```json Response
HTTP/1.1 200
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Billable portfolio does not exist.
- `409 Conflict`: Billable portfolio is already archived.
