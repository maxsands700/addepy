# Model Types

Get characteristics of available entities, including their associated attributes, attributes required for creation, and which attributes are editable. Use this API alongside the Entities API to discover, create, and edit entities more easily.

We generally use the term "model type" for a kind of entity. However, this API was written to use "entity type". They mean the same thing. This API provides model type information.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/entity_types",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/entity_types \n/v1/entity_types/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "No",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" is required to retrieve available model types.",
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

Types are described by the below resource object attributes and will appear in successful **GET** responses.

| Attribute           | Description                              | Example                   |
| :------------------ | :--------------------------------------- | :------------------------ |
| `display_name`      | Display name of the model type. String.  | `"Person"`                |
| `category`          | Category for the model type. String.     | `"Security"`              |
| `ownership_type`    | The model type's ownership type. String. | `"share_based"`           |
| `entity_attributes` | Attribute properties. Object.            | See model type attributes |

**Model type attributes**
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`key`",
"0-1": "The attribute's name. String.",
"0-2": "`\"currency_factor\"`",
"1-0": "`required`",
"1-1": "Specifies if attribute is required for entity creation or modification. Boolean.",
"1-2": "`true`",
"2-0": "`writability`",
"2-1": "Indicates whether attribute can be modified. String. \n \n- `MUTABLE`: Can be edited with permission.\n- `IMMUTABLE`: Cannot be set or modified.\n- `FINAL`: Can be set upon entity creation but cannot be modified.\n- `RESTRICTED_FOR_ONLINE`: Requires \"edit online data\" permissions to modify.",
"2-2": "`\"MUTABLE\"`"
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

## Supported model types

| Name                                                                      | API display name             | Ownership type             |
| :------------------------------------------------------------------------ | :--------------------------- | :------------------------- |
| Household                                                                 | `household`                  | Percent-based              |
| Client                                                                    | `person_node`                | Percent-based              |
| Prospect                                                                  | `prospect`                   | Percent-based              |
| Managed fund                                                              | `managed_partnership`        | Share-based or value-based |
| Holding company                                                           | `holding_company`            | Percent-based              |
| Manager                                                                   | `manager`                    | Percent-based              |
| Private fund                                                              | `fund`                       | Value-based                |
| Trust                                                                     | `trust`                      | Percent-based              |
| Vehicle                                                                   | `vehicle`                    | Percent-based              |
| Holding Account                                                           | `financial_account`          | Percent-based              |
| Sleeve                                                                    | `sleeve`                     | Percent-based              |
| Annuity                                                                   | `annuity`                    | Value-based                |
| Art\*                                                                     | `art`                        | Share-based or value-based |
| Bond                                                                      | `bond`                       | Share-based                |
| Car\*                                                                     | `car`                        | Share-based or value-based |
| Certificate of deposit                                                    | `certificate_of_deposit`     | Share-based                |
| Closed end fund                                                           | `closed_end_fund`            | Share-based                |
| CMO                                                                       | `cmo`                        | Share-based                |
| Collectible\*                                                             | `collectible`                | Share-based or value-based |
| Convertible note                                                          | `convertible_note`           | Share-based                |
| Custom asset, or any other custom investment type that's not in this list | `generic_asset`              | Any                        |
| Currency                                                                  | `cash`                       | Share-based                |
| Digital asset                                                             | `digital_asset`              | Share-based                |
| ETF                                                                       | `etf`                        | Share-based                |
| ETN                                                                       | `etn`                        | Share-based                |
| Forward contract                                                          | `forward_contract`           | Share-based                |
| Futures contract                                                          | `futures_contract`           | Share-based                |
| Hedge fund\*                                                              | `hedge_fund`                 | Share-based or value-based |
| Historical segment                                                        | `historical_segment`         | Value-based                |
| Loan                                                                      | `loan`                       | Value-based                |
| Master limited partnership                                                | `master_limited_partnership` | Share-based                |
| Money market fund                                                         | `money_market_fund`          | Share-based                |
| Mutual fund                                                               | `mutual_fund`                | Share-based                |
| Option                                                                    | `option`                     | Share-based                |
| Preferred stock                                                           | `preferred_stock`            | Share-based                |
| Private equity fund\*                                                     | `private_equity_fund`        | Share-based or value-based |
| Private investment\*                                                      | `private_investment`         | Share-based or value-based |
| Promissory note\*                                                         | `promissory_note`            | Share-based or value-based |
| Real estate\*                                                             | `real_estate`                | Share-based or value-based |
| REIT                                                                      | `reit`                       | Share-based                |
| Stock                                                                     | `stock`                      | Share-based                |
| Structured product                                                        | `structured_product`         | Share-based                |
| UIT                                                                       | `uit`                        | Share-based                |
| Unknown security                                                          | `unknown_security`           | Share-based                |
| Venture capital\*                                                         | `venture_capital`            | Share-based or value-based |
| Warrant                                                                   | `warrant`                    | Share-based                |

\*This model type is currently only available to firms that started using Addepar on or after September 12, 2025.

## Get all model types

Returns a list of all model types.

**GET** `/v1/entity_types`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/entity_types
```

```json Response
HTTP/1.1 200

{
    "data": [
      {
        "id": "person_node",
        "type": "entity_types",
        "attributes": {
          "entity_attributes": [
            {
              "key": "currency_factor",
              "required": true,
              "writability": "MUTABLE"
            },
            {
              "key": "original_name",
              "required": false,
              "writability": "MUTABLE"
            },
            {
              "key": "display_name",
              "required": false,
              "writability": "MUTABLE"
            }
          ],
          "display_name": "Person",
        },
        "links": {
          "self": "/v1/entity_types/person_node"
        }
      },
      {
        "id": "stock",
        "type": "entity_types",
        "attributes": {
          "ownership_type": "share_based",
          "entity_attributes": [
            {
              "key": "currency_factor",
              "required": true,
              "writability": "IMMUTABLE"
            },
            {
              "key": "original_name",
              "required": true,
              "writability": "IMMUTABLE"
            },
            {
              "key": "ownership_type",
              "required": true,
              "writability": "IMMUTABLE"
            },
            {
              "key": "ticker_symbol",
              "required": false,
              "writability": "IMMUTABLE"
            },
            {
              "key": "display_name",
              "required": false,
              "writability": "MUTABLE"
            },
            {
              "key": "cusip",
              "required": false,
              "writability": "IMMUTABLE"
            },
            {
              "key": "isin",
              "required": false,
              "writability": "IMMUTABLE"
            },
            {
              "key": "sedol",
              "required": false,
              "writability": "IMMUTABLE"
            },
            {
              "key": "secid_id",
              "required": false,
              "writability": "IMMUTABLE"
            },
            {
              "key": "secid_element_type",
              "required": false,
              "writability": "IMMUTABLE"
            },
            {
              "key": "secid_verification_state",
              "required": false,
              "writability": "IMMUTABLE"
            }
          ],
          "category": "Security",
          "display_name": "Stock",
        },
        "links": {
          "self": "/v1/entity_types/stock"
        }
      }
    ],
    "included": [],
    "links": {
        "next": null
    }
}
```

**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted

## Get a model type

Returns details about a specified model type.

**GET** `/v1/entity_types/:id`

```curl Request
GET https://examplefirm.addepar.com/api/v1/entity_types/bond
```

```json Response
HTTP/1.1 200

{
  "data": {
    "id": "bond",
    "type": "entity_types",
    "attributes": {
      "ownership_type": "share_based",
      "entity_attributes": [
        {
          "key": "currency_factor",
          "required": true,
          "writability": "MUTABLE"
        },
        {
          "key": "original_name",
          "required": true,
          "writability": "IMMUTABLE"
        },
        {
          "key": "ownership_type",
          "required": true,
          "writability": "IMMUTABLE"
        },
        {
          "key": "display_name",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "cusip",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "isin",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "sedol",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "bond_type",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "coupon_rate",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "coupon_type",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "bond_frequency",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "original_principal_per_share",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "issue_date",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "dated_date",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "accrual_start_date",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "first_payment_date",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "last_payment_date",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "maturity_date",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "day_count_convention",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "call_info",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "is_prerefunded",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "secid_id",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "secid_element_type",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "secid_verification_state",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "coupon_cap",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "coupon_floor",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "reset_frequency",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "first_variable_coupon_date",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "floating_index",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "floating_spread",
          "required": false,
          "writability": "IMMUTABLE"
        },
        {
          "key": "actual_security_type",
          "required": false,
          "writability": "IMMUTABLE"
        }
      ],
      "category": "Security",
      "display_name": "Bond",
    },
    "links": {
      "self": "/v1/entity_types/bond"
    }
  },
  "included": []
}
```

**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: Invalid model type
