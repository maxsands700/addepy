# Target Allocations

Target Allocations are split into two primary components:

- **Allocation Models:** Define the framework for target allocations by specifying the attributes (factors) that can be used.
- **Allocation Templates:** Define specific allocation strategies based on allocation models, including actual target allocations, constraints, and hierarchical values.

You can use the Target Allocations API to create, view, update, and delete allocation models and templates for portfolio management.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/6f9fcf203b9e7fd6a0170c6e70d5537fbcb593821fe2e9d4c43fbcd24652a6e6-Screenshot_2025-09-19_at_11.56.35_AM.png",
"",
""
],
"align": "center"
}
]
}
[/block]

# Allocation Models

[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/allocation_models",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/allocation_models \n/v1/allocation_models/:id \n \n**POST** \n/v1/allocation_models \n \n**PATCH** \n/v1/allocation_models/:id \n \n**DELETE** \n/v1/allocation_models/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "Yes",
"4-0": "Application permissions required",
"4-1": "Access to \"Manage data configuration: Target Allocation\""
},
"cols": 2,
"rows": 5,
"align": [
"left",
"left"
]
}
[/block]

## Resource overview

The Target Allocations API returns a resource object containing the allocation model ID in successful responses.

| Attributes | Description                            | Example |
| :--------- | :------------------------------------- | :------ |
| `id`       | The unique id of the allocation model. | `"123"` |

## Parameters

You can create or update an allocation model by providing the following parameters:
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"h-3": "Validation",
"0-0": "`name`",
"0-1": "The name of the allocation model being created. ",
"0-2": "`\"Balanced Growth Model\"`",
"0-3": "`400 bad request`returned if missing field",
"1-0": "`attribute_ids`",
"1-1": "A list of factor attribute identifiers that define what dimensions can be used in allocation templates created from this model. \n \nCannot be used for `PATCH` because the field is immutable after creation. To change the attributes of an existing allocation model, you must create a new model and delete the old one (if not in use) \n \nUse [/v1/attributes](https://developers.addepar.com/docs/attributes) to get a list of all attributes.",
"1-2": "`[\"asset_class\", \"legal_entity\", \"sector\"]` ",
"1-3": "`400 Bad Request` returned if `attribute_ids` are invalid for `POST`, field exists in a `PATCH` request"
},
"cols": 4,
"rows": 2,
"align": [
"left",
"left",
"left",
"left"
]
}
[/block]

## Get all allocation models

Retrieve all allocation models that the user has permission to view.

**GET** `/v1/allocation_models`

**Example**:

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/allocation_models
```

```json RESPONSE
HTTP/1.1 200

{
  "data": [
    {
      "id": "123",
      "type": "allocation_models",
      "attributes": {
        "name": "Conservative Growth Model",
        "attribute_ids": ["addepar_asset_class", "legal_entity", "sector"]
      },
      "links": {
        "self": "/v1/allocation_models/123"
      }
    },
    {
      "id": "124",
      "type": "allocation_models",
      "attributes": {
        "name": "Aggressive Growth Model",
        "attribute_ids": ["asset_class", "market_cap", "legal_entity", "sector"]
      },
      "links": {
        "self": "/v1/allocation_models/124"
      }
    }
  ],
  "included": [],
  "links": {
    "prev": null,
    "next": "/v1/allocation_models?page[limit]=500&page[after]=124"
  }
}
```

**Response Codes**

- `200 OK`: Success

- `403 Forbidden`: User lacks required permissions.

## Get allocation model by id

Retrieve a specific allocation model by its ID.

**GET** `/v1/allocation_models/:id`

**Example**:

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/allocation_models/123
```

```json RESPONSE
HTTP/1.1 200

{
  "data": {
    "id": "123",
    "type": "allocation_models",
    "attributes": {
      "name": "Conservative Growth Model",
      "attribute_ids": ["asset_class", "legal_entity", "sector"]
    },
    "links": {
      "self": "/v1/allocation_models/123"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success

- `403 Forbidden`: User lacks required permissions.

- `404 Not Found`: No allocation model exists with the specified ID, or the user doesn't have permission to access it.

## Create allocation model

Create a new allocation model with the specified attributes.

**POST** `/v1/allocation_models`

**Example**:

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/allocation_models

{
  "data": {
    "type": "allocation_models",
    "attributes": {
      "name": "Balanced Growth Model",
      "attribute_ids": ["asset_class", "legal_entity", "sector", "market_cap"]
    }
  }
}
```

```json RESPONSE
HTTP/1.1 200

{
  "data": {
    "id": "125",
    "type": "allocation_models",
    "attributes": {
      "name": "Balanced Growth Model",
      "attribute_ids": ["asset_class", "legal_entity", "sector", "market_cap"]
    },
    "links": {
      "self": "/v1/allocation_models/125"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success

- `400 Bad Request`: Request payload is improperly formatted, contains invalid data, includes an id field, or contains unsupported attributes.

- `403 Forbidden`: User lacks the required permission.

## Update allocation model

Update an existing allocation model. This endpoint supports partial updates and preserves existing data where possible.

**PATCH** `/v1/allocation_models/:id`

**Example**:

```Text REQUEST
PATCH https://examplefirm.addepar.com/api/v1/allocation_models/123

{
  "data": {
    "id": "123",
    "type": "allocation_models",
    "attributes": {
      "name": "Updated Conservative Growth Model"
    }
  }
}
```

```json RESPONSE
HTTP/1.1 200

{
  "data": {
    "id": "123",
    "type": "allocation_models",
    "attributes": {
      "name": "Updated Conservative Growth Model",
      "attribute_ids": ["asset_class", "legal_entity", "sector"]
    },
    "links": {
      "self": "/v1/allocation_models/123"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success

- `400 Bad Request`: Request payload is improperly formatted or contains invalid data. i.e. immutable field `attribute_ids`

- `403 Forbidden`: User lacks the required permission.

- `404 Not Found`: No allocation model exists with the specified `id`, or the user doesn't have permission to access it.

- `409 Conflict`: There is a mismatch between the `id` parameter in the URL and the `id` provided in the request payload.

## Delete allocation model

Will delete an existing allocation model.

**DELETE** `/v1/allocation_models/:id`

**Example**:

```Text REQUEST
DELETE https://examplefirm.addepar.com/api/v1/allocation_models/123
```

```json RESPONSE
HTTP/1.1 204
```

**Response Codes**

- `204 No Content`: Success

- `403 Forbidden`: User lacks the required permission, or the allocation model is assigned to clients that the user doesn't have permission to modify.

- `404 Not Found`: No allocation model exists with the specified ID, or the user doesn't have permission to access it.

# Allocation Templates

[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/allocation_templates",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/allocation_templates \n/v1/allocation_templates/:id \n \n**POST** \n/v1/allocation_templates \n \n**PATCH** \n/v1/allocation_templates/:id \n \n**PUT** \n/v1/allocation_templates/:id \n \n**DELETE** \n/v1/allocation_templates/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "Yes",
"4-0": "Application permissions required",
"4-1": "Access to \"Manage data configuration: Target Allocation\""
},
"cols": 2,
"rows": 5,
"align": [
"left",
"left"
]
}
[/block]

## Resource overview

The Target Allocations API returns a resource object containing the allocation template ID in successful responses.

| Attributes | Description                                                                                   | Example                                                                                                                                                                                                                                                                             |
| :--------- | :-------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`       | The unique id of the allocation template.                                                     | `"123"`                                                                                                                                                                                                                                                                             |
| `children` | Nested allocation values based on the attribute hierarchy of the associated allocation model. | ` [        {          "id": 2,          "parent_id": 1,          "attribute_id": "market_cap",          "attribute_value": "LARGE_CAP",          "target_allocation": 40.0,          "min_allocation": 30.0,          "max_allocation": 50.0,          "children": []        }   ]` |

## Parameters

You can create or update an allocation template by providing the following parameters:
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"h-3": "Validation",
"0-0": "`model_id`",
"0-1": "The model associated with the current target allocation. \n \nThis field is immutable. To change the assigned model of an existing target allocation, you must create a new allocation and delete the old one (if not in use)",
"0-2": "`\"123\"`",
"0-3": "`400 bad request`returned if missing field in `POST` and `PUT` requests, field exists in `PATCH` \n \n`404 Not Found` returned if the allocation model does not exist or is not accessible.",
"1-0": "`name`",
"1-1": "The name of the target allocation being created.",
"1-2": "`\"Conservative Growth Template\"`",
"1-3": "`400 bad request`returned if missing field in `POST` and `PUT` requests",
"2-0": "`description`",
"2-1": "An optional field for the description listed under the target allocation.",
"2-2": "`\"A balanced allocation template for conservative growth\"`",
"2-3": "",
"3-0": "`allocation_intervals`",
"3-1": "Allocation distribution for each dimension of the associated allocation model. \n \nOnly `attribute_id`s defined in the corresponding level of the referenced model can be used \n \n`min_allocation` and `max_allocation` are optional bounds. ",
"3-2": "`[  \n        {    \n          \"allocations\": [  \n            {  \n              \"parent_id\": null,  \n              \"attribute_id\": \"asset_class\",  \n              \"attribute_value\": \"BONDS\",  \n              \"target_allocation\": 40.0,  \n              \"min_allocation\": 30.0,  \n              \"max_allocation\": 50.0,  \n              \"children\": [  \n                {  \n                  \"parent_id\": null,  \n                  \"attribute_id\": \"duration\",  \n                  \"attribute_value\": \"SHORT_TERM\",  \n                  \"target_allocation\": 25.0,  \n                  \"min_allocation\": 20.0,  \n                  \"max_allocation\": 30.0,  \n                  \"children\": []  \n                }  \n              ]  \n            }  \n          ]  \n        }  \n      ]`",
"3-3": "`400 bad request` returned if missing field in `POST` and `PUT` requests, empty allocation intervals or allocations, target allocation outside min/max bounds, child target sum exceeding parent target, invalid attribute values for specified attribute IDs, has more than one allocation"
},
"cols": 4,
"rows": 4,
"align": [
"left",
"left",
"left",
"left"
]
}
[/block]

## Get all allocation templates

Retrieve all allocation templates that the user has permission to view.

**GET** `/v1/allocation_templates`

**Example**:

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/allocation_templates
```

```json RESPONSE
HTTP/1.1 200
{
  "data": [
    {
      "id": "123",
      "type": "allocation_templates",
      "attributes": {
        "model_id": 456,
        "name": "Conservative Growth Template",
        "description": "A balanced allocation template for conservative growth",
        "allocation_intervals": [
          {
            "effective_date": "2024-01-01",
            "allocations": [
              {
                "id": 1,
                "parent_id": null,
                "attribute_id": "asset_class",
                "attribute_value": "EQUITY",
                "target_allocation": 60.0,
                "min_allocation": 50.0,
                "max_allocation": 70.0,
                "children": [
                  {
                    "id": 2,
                    "parent_id": 1,
                    "attribute_id": "market_cap",
                    "attribute_value": "LARGE_CAP",
                    "target_allocation": 40.0,
                    "min_allocation": 30.0,
                    "max_allocation": 50.0,
                    "children": []
                  }
                ]
              }
            ]
          }
        ]
      },
      "links": {
        "self": "/v1/allocation_templates/123"
      }
    }
  ],
  "included": [],
  "links": {
    "prev": null,
    "next": "/v1/allocation_templates?page[limit]=500&page[after]=123"
  }
}
```

**Response Codes**

- `200 OK`: Success

- `403 Forbidden`: User lacks required permissions.

## Get allocation template by id

Retrieve a specific allocation template by its ID.

**GET** `/v1/allocation_templates/:id`

**Example**:

```Text REQUEST
GET https://examplefirm.addepar.com/api/v1/allocation_templates/123
```

```json RESPONSE
HTTP/1.1 200

{
  "data": {
    "id": "123",
    "type": "allocation_templates",
    "attributes": {
      "model_id": 456,
      "name": "Conservative Growth Template",
      "description": "A balanced allocation template for conservative growth",
      "allocation_intervals": [
        {
          "effective_date": "2024-01-01",
          "allocations": [
            {
              "id": 1,
              "parent_id": null,
              "attribute_id": "asset_class",
              "attribute_value": "EQUITY",
              "target_allocation": 60.0,
              "min_allocation": 50.0,
              "max_allocation": 70.0,
              "children": [
                {
                  "id": 2,
                  "parent_id": 1,
                  "attribute_id": "market_cap",
                  "attribute_value": "LARGE_CAP",
                  "target_allocation": 40.0,
                  "min_allocation": 30.0,
                  "max_allocation": 50.0,
                  "children": []
                }
              ]
            }
          ]
        }
      ]
    },
    "links": {
      "self": "/v1/allocation_templates/123"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success

- `403 Forbidden`: User lacks required permissions.

- `404 Not Found`: No allocation template exists with the specified ID, or the user doesn't have permission to access it.

## Create allocation template

Create a new allocation template with the specified attributes.

**POST** `/v1/allocation_templates`

**Example**:

```Text REQUEST
POST https://examplefirm.addepar.com/api/v1/allocation_templates

{
  "data": {
    "type": "allocation_templates",
    "attributes": {
      "model_id": 456,
      "name": "Aggressive Growth Template",
      "description": "High-growth allocation strategy",
      "allocation_intervals": [
        {
          "allocations": [
            {
              "parent_id": null,
              "attribute_id": "asset_class",
              "attribute_value": "EQUITY",
              "target_allocation": 80.0,
              "min_allocation": 70.0,
              "max_allocation": 90.0,
              "children": [
                {
                  "parent_id": null,
                  "attribute_id": "market_cap",
                  "attribute_value": "LARGE_CAP",
                  "target_allocation": 50.0,
                  "min_allocation": 40.0,
                  "max_allocation": 60.0,
                  "children": []
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

```json RESPONSE
HTTP/1.1 200

{
  "data": {
    "id": "124",
    "type": "allocation_templates",
    "attributes": {
      "model_id": 456,
      "name": "Aggressive Growth Template",
      "description": "High-growth allocation strategy",
      "allocation_intervals": [
        {
          "effective_date": null,
          "allocations": [
            {
              "id": 3,
              "parent_id": null,
              "attribute_id": "asset_class",
              "attribute_value": "EQUITY",
              "target_allocation": 80.0,
              "min_allocation": 70.0,
              "max_allocation": 90.0,
              "children": [
                {
                  "id": 4,
                  "parent_id": 3,
                  "attribute_id": "market_cap",
                  "attribute_value": "LARGE_CAP",
                  "target_allocation": 50.0,
                  "min_allocation": 40.0,
                  "max_allocation": 60.0,
                  "children": []
                }
              ]
            }
          ]
        }
      ]
    },
    "links": {
      "self": "/v1/allocation_templates/124"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success

- `400 Bad Request`: Request payload is improperly formatted, contains invalid data, includes an id field, or violates validation rules. See Parameters table.

- `403 Forbidden`: User lacks required permissions.

- `404 Not Found`: The specified allocation model does not exist or is not accessible.

## Update allocation template

Update an existing allocation template. This endpoint supports partial updates and preserves existing data where possible. If a field is not provided in the request, the existing value is retained.

**PATCH** `/v1/allocation_templates/:id`

**Example**:

```Text REQUEST
PATCH https://examplefirm.addepar.com/api/v1/allocation_templates/123

{
  "data": {
    "id": "123",
    "type": "allocation_templates",
    "attributes": {
      "name": "Updated Conservative Growth Template",
      "description": "Updated description for conservative growth strategy"
    }
  }
}
```

```json RESPONSE
HTTP/1.1 200

{
  "data": {
    "id": "123",
    "type": "allocation_templates",
    "attributes": {
      "model_id": 456,
      "name": "Updated Conservative Growth Template",
      "description": "Updated description for conservative growth strategy",
      "allocation_intervals": [
        {
          "effective_date": null,
          "allocations": [
            {
              "id": 1,
              "parent_id": null,
              "attribute_id": "asset_class",
              "attribute_value": "EQUITY",
              "target_allocation": 60.0,
              "min_allocation": 50.0,
              "max_allocation": 70.0,
              "children": []
            }
          ]
        }
      ]
    },
    "links": {
      "self": "/v1/allocation_templates/123"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success

- `400 Bad Request`: Request payload is improperly formatted, contains invalid data i.e. immutable field `model_id`, or violates validation rules. See Parameters table.

- `403 Forbidden`: User lacks required permissions.

- `404 Not Found`: No allocation template exists with the specified ID, or the user doesn't have permission to access it.

- `409 Conflict`: There is a mismatch between the id parameter in the URL and the id provided in the request payload.

## Replace allocation template

Completely replace an existing allocation template with the provided data. This endpoint performs a full replacement, not a partial update. Unlike `PATCH`, this operation does not preserve existing data.

**PUT** `/v1/allocation_templates/:id`

**Example**:

```Text REQUEST
PUT https://examplefirm.addepar.com/api/v1/allocation_templates/123

{
  "data": {
    "id": "123",
    "type": "allocation_templates",
    "attributes": {
      "model_id": 456,
      "name": "Completely Replaced Template",
      "description": "This template has been completely replaced",
      "allocation_intervals": [
        {
          "allocations": [
            {
              "parent_id": null,
              "attribute_id": "asset_class",
              "attribute_value": "BONDS",
              "target_allocation": 40.0,
              "min_allocation": 30.0,
              "max_allocation": 50.0,
              "children": [
                {
                  "parent_id": null,
                  "attribute_id": "duration",
                  "attribute_value": "SHORT_TERM",
                  "target_allocation": 25.0,
                  "min_allocation": 20.0,
                  "max_allocation": 30.0,
                  "children": []
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

```json RESPONSE
HTTP/1.1 200

{
  "data": {
    "id": "123",
    "type": "allocation_templates",
    "attributes": {
      "model_id": 456,
      "name": "Completely Replaced Template",
      "description": "This template has been completely replaced",
      "allocation_intervals": [
        {
          "effective_date": null,
          "allocations": [
            {
              "id": 5,
              "parent_id": null,
              "attribute_id": "asset_class",
              "attribute_value": "BONDS",
              "target_allocation": 40.0,
              "min_allocation": 30.0,
              "max_allocation": 50.0,
              "children": [
                {
                  "id": 6,
                  "parent_id": 5,
                  "attribute_id": "duration",
                  "attribute_value": "SHORT_TERM",
                  "target_allocation": 25.0,
                  "min_allocation": 20.0,
                  "max_allocation": 30.0,
                  "children": []
                }
              ]
            }
          ]
        }
      ]
    },
    "links": {
      "self": "/v1/allocation_templates/123"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success

- `400 Bad Request`: Request payload is improperly formatted, contains invalid data, attempts to change the model ID, or violates validation rules. See Parameters table.

- `403 Forbidden`: User lacks required permissions.

- `404 Not Found`: No allocation template exists with the specified ID, or the user doesn't have permission to access it. Or, no allocation model exists with the specified ID, or the user doesn't have permission to access it.

- `409 Conflict`: There is a mismatch between the `id` parameter in the URL and the `id` provided in the request payload.

## Delete allocation template

Delete an existing allocation template.

**DELETE** `/v1/allocation_templates/:id`

**Example**:

```Text REQUEST
DELETE https://examplefirm.addepar.com/api/v1/allocation_templates/123
```

```json RESPONSE
HTTP/1.1 204
```

**Response Codes**

- `204 No Content`: Success

- `403 Forbidden`: User lacks required permissions.

- `404 Not Found`: No allocation template exists with the specified ID, or the user doesn't have permission to access it.
