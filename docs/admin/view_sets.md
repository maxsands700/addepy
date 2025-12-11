# View Sets

View sets are groups of views that determine what contacts see in the Client Portal. You can use the View Sets API to manage and assign these sets to contacts.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/16939b499a69e4d169bec5e7b1e4092e1d4941119802380a50a5a1e4866aaeb3-Screenshot_2024-12-10_at_12.39.03_PM.png",
null,
null
],
"align": "center"
}
]
}
[/block]

<br />
[block:parameters]
{
  "data": {
    "h-0": "",
    "h-1": "",
    "0-0": "Base Route",
    "0-1": "/v1/view_sets",
    "1-0": "Endpoints",
    "1-1": "**GET**  \n/v1/view_sets/:id  \n/v1/view_sets",
    "2-0": "Produces",
    "2-1": "JSON",
    "3-0": "Pagination",
    "3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
    "4-0": "Application Permissions Required",
    "4-1": "\"API Access: Create, edit, and delete\"  \n  \n\"Full Access\" for all operations.",
    "5-0": "OAuth Scopes",
    "5-1": "**GET**  \n`USERS_READ`"
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

View sets contain the below attributes. Required attributes are noted in the description.

All attributes will be returned in successful **GET** responses containing the view sets resource.

| Attribute | Description                                                                      | Example           |
| :-------- | :------------------------------------------------------------------------------- | :---------------- |
| `name`    | The view set's name. String.                                                     | `"Firm View Set"` |
| `views`   | A list of objects representing the views in a set. See below for object details. | See below.        |

### View objects

| Attribute | Description                                                | Example              |
| :-------- | :--------------------------------------------------------- | :------------------- |
| `id`      | The view’s unique identifier. String.                      | `"16"`               |
| `name`    | The view’s name. String.                                   | `"Benchmarks"`       |
| `type`    | The type of view, such as Analysis or Transaction. String. | `"TRANSACTION_TYPE"` |

<br />

## Get a view set

Retrieves details for a specific view set.

**GET** `/v1/view_sets/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/view_sets/2000
```

```json Response
HTTP/1.1 200

{
    "data":{
        "id":"2000",
        "type":"view_sets",
        "attributes":{
            "name":"Firm View Set",
            "views": [
                {
                    "id": "16",
                    "name": "Benchmarks",
                    "type": "TRANSACTION_TYPE"
                }
            ],
        },
        "links": {
            "self": "/v1/view_sets/2000"
        }
    }
}
```

**Response codes**

- `200 OK`: Success
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: View set not found

## Get all view sets

Retrieves details for all view sets.

**GET** `/v1/view_sets`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/view_sets
```

```json Response
HTTP/1.1 200

{
    "data":[
      {
        "id":"2000",
        "type":"view_sets",
        "attributes":{
            "name":"Firm View Set",
            "views": [
                {
                    "id": "16",
                    "name": "Benchmarks",
                    "type": "TRANSACTION_TYPE"
                }
            ],
        },
        "links": {
            "self": "/v1/view_sets/2000"
        }
      }
    ]
}
```

**Response codes**

- `200 OK`: Success
- `403 Forbidden`: You need full access permissions to perform this action
