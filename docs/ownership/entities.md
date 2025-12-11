# Entities

Entities are any asset within a portfolio, like a trust, holding account, or investment. Clients and households are also entities. Use the Entities API to create and delete entities in Addepar, and retrieve and update entity details.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/entities",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/entities/:id \n/v1/entities \n \n**POST** \n/v1/entities/ \n \n**PATCH** \n/v1/entities/:id \n/v1/entities \n \n**DELETE** \n/v1/entities/:id \n/v1/entities",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Portfolio Access\" is required to retrieve, update, and delete entities. \n \nNo specific portfolio access is required to create entities. \n \n\"Manage Attributes: Only edit certain attribute values or Manage all values and settings” is required to apply, edit, or delete attributes.",
"5-0": "OAuth scopes",
"5-1": "`ENTITIES` or `ENTITIES_WRITE`"
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

Entities are described by the below resource object attributes. Attributes required for creating, updating or deleting entities are noted. You can assign additional standard and custom attributes to entities.

All attributes will be returned in successful **GET**, **POST** & **PATCH** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Type",
"h-2": "Example",
"0-0": "`original_name`",
"0-1": "Name of the entity. String.",
"0-2": "`\"Smith Trust\"`",
"1-0": "`model_type`",
"1-1": "Describes the type of entity. String.",
"1-2": "`\"TRUST\"`",
"2-0": "`ownership_type`",
"2-1": "Not editable and cannot be passed in, though a value will be returned for all non-client entities. String. \nSupported values: \n \n- `PERCENT_BASED`\n- `SHARE_BASED`\n- `VALUE_BASED`",
"2-2": "`\"PERCENT_BASED\"`",
"3-0": "`currency_factor`",
"3-1": "Required but only applicable for non-client entities. String.",
"3-2": "`\"USD\"`",
"4-0": "`underlying_type`",
"4-1": "Required but only applicable for forward and futures contract entities. String. \nSupported values: \n \n- `INTEREST_RATE`\n- `CURRENCY`\n- `COMMODITY`\n- `SECURITY`\n- `INDEX`",
"4-2": "`CURRENCY`",
"5-0": "`delivery_price`",
"5-1": "Required for forward contract entities. String.",
"5-2": "`{\n   \"value\": 100.5\n   \"currency\": \"USD\"\n}`",
"6-0": "`created_at`",
"6-1": "Not editable and cannot be passed in. String.",
"6-2": "`\"2023-07-28T02:24:30Z\"`",
"7-0": "`modified_at`",
"7-1": "Not editable and cannot be passed in. String.",
"7-2": "`\"2023-07-30T10:43:21Z\"`",
"8-0": "Optional attributes",
"8-1": "Additional attributes can be applied to entities. String.",
"8-2": "[See Addepar Attributes](https://developers.addepar.com/docs/addepar-attributes-1)"
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

## Get an entity

Retrieves all attributes for a specific entity.

**GET** `/v1/entities/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/entities/1000002
```

```json Response
HTTP/1.1 200

{
  "data": {
    "id": "1000002",
    "type": "entities",
    "attributes": {
      "created_at": "2023-07-28T02:24:30Z"
      "currency_factor": "USD",
      "original_name": "X092849032",
      "ownership_type": "PERCENT_BASED",
      "display_name": "Citco",
      "model_type": "FINANCIAL_ACCOUNT",
      "is_rolled_up": false
      "modified_at": "2023-07-30T10:43:21Z"
    },
    "links": {
      "self": "/v1/entities/1000002"
    }
  }
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: The entity does not exist or you do not have access to it

## Get all entities

Retrieves the full list of all entities you have permission to access, as well as all attributes for each entity.

**GET** `/v1/entities`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/entities
```

```json Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "1000001",
      "type": "entities",
      "attributes": {
        "created_at": "2023-07-28T02:24:30Z",
        "model_type": "PERSON_NODE",
        "original_name": "Adam Smith",
        "modified_at": "2023-07-30T10:43:21Z"

      },
      "links": {
        "self": "/v1/entities/1000001"
      }
    },
    {
      "id": "1000002",
      "type": "entities",
      "attributes": {
        "created_at": "2023-07-28T02:24:30Z"
        "currency_factor": "USD",
        "display_name": "Citco",
        "is_rolled_up": false,
        "model_type": "FINANCIAL_ACCOUNT",
        "original_name": "X092849032",
        "ownership_type": "PERCENT_BASED",
        "modified_at": "2023-07-30T10:43:21Z"
      },
      "links": {
        "self": "/v1/entities/1000002"
      }
    },
    {
      "id": "1000003",
      "type": "entities",
      "attributes": {
        "created_at": "2023-07-28T02:24:30Z",
        "currency_factor": "USD",
        "model_type": "TRUST",
        "original_name": "Adam Irrevocable Trust",
        "ownership_type": "PERCENT_BASED",
        "modified_at": "2023-07-30T10:43:21Z",
        "_custom_firm_id_ABC123": [
           {
              "date": null,
              "value": "ABC123",
              "weight": 1.0
           }
         ]
      },
      "links": {
        "self": "/v1/entities/1000003"
      }
    }
  ],
  "links": {
    "next": null
  }
}
```

**Optional parameters**
[block:parameters]
{
"data": {
"h-0": "Filter",
"h-1": "Description",
"h-2": "Example",
"0-0": "model_types \n(or entity_types)",
"0-1": "Returns only the model type(s) specified. Ignores spaces. \n \nYou can't combine model type and linking status filters. \n \nWhile \"model_types\" is the most accurate term, we also support \"entity_types\" for historical compatibility. The filters work the same way.",
"0-2": "`filter[model_types]=TRUST,FINANCIAL_ACCOUNT`",
"1-0": "linking_status=linked",
"1-1": "Returns all online accounts that are linked to an owner.",
"1-2": "`filter[linking_status]=linked`",
"2-0": "linking_status=unlinked",
"2-1": "Returns all online accounts that are not linked to an owner.",
"2-2": "`filter[linking_status]=unlinked`",
"3-0": "created_before",
"3-1": "Returns all entities created on or before a date, formatted as YYYY-MM-DD.",
"3-2": "`filter[created_before]=\"2023-04-12\"`",
"4-0": "created_after",
"4-1": "Returns all entities created on or after a date, formatted as YYYY-MM-DD.",
"4-2": "`filter[created_after]=\"2023-04-12\"`",
"5-0": "modified_before",
"5-1": "Returns all entities last modified on or before a date, formatted as YYYY-MM-DD.",
"5-2": "`filter[modified_before]=\"2023-04-12\"`",
"6-0": "modified_after",
"6-1": "Returns all entities last modified on or after a date, formatted as YYYY-MM-DD.",
"6-2": "`filter[modified_after]=\"2023-04-12\"`",
"7-0": "ids",
"7-1": "Returns all entities matching the entity IDs specified",
"7-2": "`filter[ids]=1,2,3`",
"8-0": "fields[entities]",
"8-1": "Returns only the attributes specified for each entity. Ignores spaces. \n \nYou can filter by `fields[entities]=[]` to omit all attributes.",
"8-2": "`fields[entities]=model_type,ownership_type`"
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

> ℹ️ Performance tip
>
> To speed up responses, filter to get only these attributes or fewer: `fields[entities]=created_at,currency_factor_model_type,modified_at,original_name,ownership_type`

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid filter parameters
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted

## Create an entity

Adds a new entity to your firm.

Attributes `original_name`, `model_type` and `currency_factor` must be included.

Returns all attributes of the new entity.

**POST** `/v1/entities/`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/entities

{
  "data":{
    "type":"entities",
    "attributes":{
      "original_name":"New entity",
      "currency_factor":"USD",
      "model_type":"PERSON_NODE"
    }
  }
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":{
      "id":"1111",
      "type":"entities",
      "attributes":{
         "model_type":"PERSON_NODE",
         "original_name":"Adam Smith",
         "currency_factor":"USD"
      },
      "links":{
         "self":"/v1/entities/1111"
      }
   }
}
```

**Optional parameters**
[block:parameters]
{
"data": {
"h-0": "Filter",
"h-1": "Description",
"h-2": "Example",
"0-0": "allow_new_investment_types",
"0-1": "If you want to give an investment a new investment type that your firm has never used before, set this to true. \n \nInvestment type is a custom label for something unique that an available model type doesn’t describe. \n \nDefaults to false if not set.",
"0-2": "`allow_new_investment_types=true` \n \nThen, pass in a new investment type: \n`\"investment_type\":\"BOAT\"`"
},
"cols": 3,
"rows": 1,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Response codes:**

- `201 Created`: Success
- `400 Bad Request`: Invalid payload or type of entities (model_type) cannot be created
- `403 Forbidden `: Insufficient application permissions or appropriate scope not granted
- `409 Conflict`: The "type" was not specified as "entities"

## Create multiple entities

Adds new entities to your firm.

Attributes `original_name`, `model_type` and `currency_factor` must be included.

Returns all attributes for each new entity.

**POST** `/v1/entities/`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/entities

{
  "data":[
    {
      "type":"entities",
      "attributes":{
        "model_type":"PERSON_NODE",
        "original_name":"Adam Smith",
        "currency_factor":"USD"
      }
    },
    {
      "type":"entities",
      "attributes":{
        "currency_factor":"USD",
        "model_type":"TRUST",
        "original_name":"Smith Trust"
      }
    }
  ]
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":[
      {
         "id":"1111",
         "type":"entities",
         "attributes":{
            "model_type":"PERSON_NODE",
            "original_name":"Adam Smith",
            "currency_factor":"USD"
         },
         "links":{
            "self":"/v1/entities/1111"
         }
      },
      {
         "id":"1112",
         "type":"entities",
         "attributes":{
            "currency_factor":"USD",
            "model_type":"TRUST",
            "original_name":"Smith Trust",
            "ownership_type":"PERCENT_BASED"
         },
         "links":{
            "self":"/v1/entities/1112"
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
"0-0": "allow_new_investment_types",
"0-1": "If you want to give an investment a new investment type that your firm has never used before, set this to true. \n \nInvestment type is a custom label for something unique that an available model type doesn’t describe. \n \nDefaults to false if not set.",
"0-2": "`allow_new_investment_types=true` \n \nThen, pass in a new investment type: \n`\"investment_type\":\"BOAT\"`"
},
"cols": 3,
"rows": 1,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Response codes:**

- `201 Created`: Success
- `400 Bad Request`: Invalid payload or one or more types of entities (model_type) cannot be created
- `403 Forbidden `: Insufficient application permissions or appropriate scope not granted
- `409 Conflict `: The "type" for one or more entities was not specified as "entities"

## Edit an entity

Adds, modifies, or deletes the attributes or custom attributes of an existing entity.

Returns all attributes of the updated entity.

**PATCH** `/v1/entities/:id`

**Example:**

This example is for Addepar's standard attributes. See [Addepar attributes](https://developers.addepar.com/docs/addepar-attributes-1) for a custom attribute example.

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/entities/1111

{
  "data":{
    "id":"1111",
    "type":"entities",
    "attributes":{
      "original_name":"Adam T. Smith"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "data": {
	"id": "1111",
       "type": "entities",
       "attributes": {
          "model_type": "PERSON_NODE",
          "original_name": "Adam T. Smith"
    },
      "links": {
        "self": "/v1/entities/1111"
     }
  }
}
```

**Optional parameters**
[block:parameters]
{
"data": {
"h-0": "Filter",
"h-1": "Description",
"h-2": "Example",
"0-0": "allow_new_investment_types",
"0-1": "If you want to give an investment a new investment type that your firm has never used before, set this to true. \n \nInvestment type is a custom label for something unique that an available model type doesn’t describe. \n \nDefaults to false if not set.",
"0-2": "`allow_new_investment_types=true` \n \nThen, pass in a new investment type: \n`\"investment_type\":\"BOAT\"`"
},
"cols": 3,
"rows": 1,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload or the type of entity (model_type) cannot be updated
- `403 Forbidden `: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: One or more entities do not exist or you do not have access to it
- `409 Conflict`: The ID in the path doesn't match the ID in the payload
- `409 Conflict`: The "type" was not specified as "entities"

## Edit multiple entities

Adds, modifies, or deletes attributes of existing entities. Returns all attributes of the updated entities. In the example, the two entity names are being updated from `“Adam Smith”` and `“Smith Family Trust”` as seen in the POST example above, to `“Adam T. Smith”` and `“The Smith Family Trust”` respectively.

Model types not supported:

- `Digital Asset (DIGITAL_ASSET)`

**PATCH** `/v1/entities`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/entities

{
  "data":[
    {
      "id":"1111",
      "type":"entities",
      "attributes":{
        "original_name":"Adam T. Smith"
      }
    },
    {
      "id":"1112",
      "type":"entities",
      "attributes":{
        "original_name":"The Smith Family Trust"
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
    "id": "1111",
    "type": "entities",
    "attributes": {
       "model_type": "PERSON_NODE",
       "original_name": "Adam T. Smith"
    },
    "links": {
             "self": "/v1/entities/1111"
    }
},
{
    "id": "1112",
    "type": "entities",
    "attributes": {
       "currency_factor": "USD",
       "model_type": "TRUST",
       "original_name": "The Smith Family Trust",
       "ownership_type": "PERCENT_BASED"
    },
    "links": {
       "self": "/v1/entities/1112"
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
"0-0": "allow_new_investment_types",
"0-1": "If you want to give an investment a new investment type that your firm has never used before, set this to true. \n \nInvestment type is a custom label for something unique that an available model type doesn’t describe. \n \nDefaults to false if not set.",
"0-2": "`allow_new_investment_types=true` \n \nThen, pass in a new investment type: \n`\"investment_type\":\"BOAT\"`"
},
"cols": 3,
"rows": 1,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload or one or more types of entities (model_type) cannot be updated
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: One or more entities do not exist or you do not have access to them
- `409 Conflict`: The "type" for one or more entities was not specified as "entities"

## Delete an entity

Deletes an existing entity from your firm. An entity cannot be deleted if it holds other entities. For example, you cannot delete a holding company if it owns a security.

**DELETE** `/v1/entities/:id`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/entities/1111
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload, or the entity is referenced by positions/affiliations
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: The entity does not exist or you do not have access to it
- `409 Conflict `: The "type" was not specified as "entities"

## Delete multiple entities

Deletes multiple existing entities from your firm. An entity cannot be deleted if it holds other entities. For example, you cannot delete a holding company if it owns a security.

Model types not supported:

- `Digital Asset (DIGITAL_ASSET)`

**DELETE** `/v1/entities`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/entities

{
  "data":[
    {
      "id":1111,
      "type":"entities"
    },
    {
      "id":1112,
      "type":"entities"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload, or one or more entities are referenced by positions/affiliations
- `403 Forbidden `: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: One or more entities do not exist or you do not have access to them
- `409 Conflict `: The "type" for one or more entities was not specified as "entities"
