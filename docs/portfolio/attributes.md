# Attributes

Attributes are qualitative and quantitative details you can use to organize and analyze data in Addepar. Use the Attributes API to discover the Addepar attributes available to your firm.

Read more about Addepar attributes [here](https://developers.addepar.com/docs/addepar-attributes-1).
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"0-1": "/v1/attributes",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/attributes \n/v1/attributes/:id \n/v1/attributes/:id/relationships/arguments \n/v1/attributes/:id/arguments \n \n**POST** \n/v1/attributes/query",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" is required to retrieve available attributes.",
"5-0": "OAuth Scopes",
"5-1": "`PORTFOLIO`"
},
"cols": 2,
"rows": 6,
"align": [
"left",
"left"
]
}
[/block]

## Resource Overview

Attributes are described by the below resource object attributes and will appear in successful **GET** & **POST** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`output_type`",
"0-1": "The output type of the attribute. String.",
"0-2": "`\"Percent\"`",
"1-0": "`usage`",
"1-1": "Applicability of attribute. [String.]. See \"Usage\" below.",
"1-2": "`[\"groupings\", \"columns\"]`",
"2-0": "`display_name`",
"2-1": "Display name of the attribute. String.",
"2-2": "`\"TWR\"`",
"3-0": "`category`",
"3-1": "Usage category for the attribute. String.",
"3-2": "`\"Performance Metrics\"`",
"4-0": "`created_at`",
"4-1": "Not editable and can't be passed in. String. \n \n*Note: creation dates are unreliable for attributes modified before September 22, 2023. Previously, a bug updated both `created_at` and `modified_at` when editing an attribute.*",
"4-2": "`\"2023-07-28T02:24:30Z\"`",
"5-0": "`modified_at`",
"5-1": "Not editable and can't be passed in. String.",
"5-2": "`\"2023-07-30T10:43:21Z\"`"
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

**Usage**

| Usage                        | Description                                                                                                                                                    |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`                    | Can be used in portfolio columns.                                                                                                                              |
| `groupings`                  | Can be used in portfolio groupings.                                                                                                                            |
| `filters`                    | Can be used to portfolio filters.                                                                                                                              |
| `position_custom_attributes` | Can be applied at the position level and will appear under additional attributes in the application.                                                           |
| `entity_custom_attributes`   | Can be applied at the entity level and will appear under additional attributes in the application. These can also be applied to groups unless otherwise noted. |
| `entity_attributes`          | Can be applied at the entity level and will appear under the entities' attributes in the application.                                                          |

## Relationships

| Relationship | Description                                                             |
| :----------- | :---------------------------------------------------------------------- |
| `arguments`  | Possible settings that can be applied to each instance of an attribute. |

```json Relationships
"relationships": {
        "arguments": {
          "links": {
            "self": "/v1/attributes/value/relationships/arguments",
            "related": "/v1/attributes/value/arguments"
          },
          "data": [{
              "type": "arguments",
              "id": "time_point"
            },{
              "type": "arguments",
              "id": "adjusted"
            },
            {
              "type": "arguments",
              "id": "accrued"
            },
            {
              "type": "arguments",
              "id": "currency"
            }
          ]
        }
      }
```

## Get All Attributes

Retrieves all attributes available to the user.

**GET** `v1/attributes`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/attributes
```

```json Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "time_weighted_return",
      "type": "attributes",
      "attributes": {
        "output_type": "Percent",
        "usage": [
          "groupings",
          "columns",
          "filters"
        ],
        "display_name": "TWR",
        "category": "Performance Metrics",
        "created_at": "2023-07-28T02:24:30Z",
        "modified_at": "2023-07-30T10:43:21Z"
      },
      "relationships": {
        "arguments": {
          "links": {
            "self": "/v1/attributes/time_weighted_return/relationships/arguments",
            "related": "/v1/attributes/time_weighted_return/arguments"
          },
          "data": [{
              "type": "arguments",
              "id": "period"
            },
            {
              "type": "arguments",
              "id": "bucketed"
            },
            {
              "type": "arguments",
              "id": "adjusted"
            },
            {
              "type": "arguments",
              "id": "accrued"
            },
            {
              "type": "arguments",
              "id": "currency"
            },
            {
              "type": "arguments",
              "id": "annualized_default_false"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/attributes/time_weighted_return"
      }
    },
    {
      "id": "value",
      "type": "attributes",
      "attributes": {
        "output_type": "Number",
        "usage": [
          "groupings",
          "columns",
          "filters"
        ],
        "display_name": "Value",
        "category": "Holding Details",
        "created_at": "2023-07-28T02:24:30Z",
        "modified_at": "2023-07-30T10:43:21Z"
      },
      "relationships": {
        "arguments": {
          "links": {
            "self": "/v1/attributes/value/relationships/arguments",
            "related": "/v1/attributes/value/arguments"
          },
          "data": [{
              "type": "arguments",
              "id": "time_point"
            },{
              "type": "arguments",
              "id": "adjusted"
            },
            {
              "type": "arguments",
              "id": "accrued"
            },
            {
              "type": "arguments",
              "id": "currency"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/attributes/value"
      }
    },
    {
      "id": "_custom_boolean_custom_1_419",
      "type": "attributes",
      "attributes": {
        "output_type": "Boolean",
        "usage": [
          "entity_custom_attributes",
          "groupings",
          "columns",
          "position_custom_attributes",
          "filters"
        ],
        "display_name": "Boolean Custom 1",
        "category": "Custom",
        "created_at": "2023-07-28T02:24:30Z",
        "modified_at": "2023-07-30T10:43:21Z"
      },
      "relationships": {
        "arguments": {
          "links": {
            "self": "/v1/attributes/_custom_boolean_custom_1_419/relationships/arguments",
            "related": "/v1/attributes/_custom_boolean_custom_1_419/arguments"
          },
          "data": []
        }
      },
      "links": {
        "self": "/v1/attributes/_custom_boolean_custom_1_419"
      }
    }
  ],
  "included": [],
  "links": {
    "next": null
  }
}
```

**Optional Query Parameters:**

- `filter[category]`: `Cash Flows`, `Security Details`, `Holding Details`, etc.
- `filter[usage]`: One of `columns`, `groupings`, `filters`, `positon_custom_attributes`,`entity_custom_attributes`,`entity_attributes`.
- `filter[output_type]`: One of `Word`, `Boolean`, `Percent, Date`, `Currency`, `List`, `Number`.

**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Get Attribute By ID

Retrieves the attribute with the given ID.

**GET** `/v1/attributes/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/attributes/time_weighted_return
```

```json Response
HTTP/1.1 200

{
  "data": {
    "id": "time_weighted_return",
    "type": "attributes",
    "attributes": {
      "output_type": "Percent",
      "usage": [
        "groupings",
        "columns"
      ],
      "display_name": "TWR",
      "category": "Performance Metrics",
      "created_at": "2023-07-28T02:24:30Z",
      "modified_at": "2023-07-30T10:43:21Z"
    },
    "relationships": {
      "arguments": {
        "links": {
          "self": "/v1/attributes/time_weighted_return/relationships/arguments",
          "related": "/v1/attributes/time_weighted_return/arguments"
        },
        "data": [{
            "type": "arguments",
            "id": "period"
          },
          {
            "type": "arguments",
            "id": "excluded_fee_types"
          },
          {
            "type": "arguments",
            "id": "bucketed"
          },
          {
            "type": "arguments",
            "id": "adjusted"
          },
          {
            "type": "arguments",
            "id": "accrued"
          },
          {
            "type": "arguments",
            "id": "currency"
          },
          {
            "type": "arguments",
            "id": "annualized_default_false"
          }
        ]
      }
    },
    "links": {
      "self": "/v1/attributes/time_weighted_return"
    }
  },
  "included": []
}
```

**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope
- `404 Not Found`: Attribute does not exist

## Query By Multiple Attribute Keys

Retrieves all attributes with matching attribute keys.

**POST** /v1/attributes/query

```curl Request
POST https://examplefirm.addepar.com/api/v1/attributes/query

{
  "data" : {
    "type" : "attribute_search",
    "attributes" : {
      "attribute_keys" : [
        "account_fees",
        "account_number",
        "_custom_automatic_conversion_minimum_amount_406"
      ]
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "data" : [
    {
      "id" : "account_fees",
      "type" : "attributes",
      "attributes" : {
        "output_type" : "Word",
        "spec_id" : 222,
        "usage" : [
          "filters"
        ],
        "created_at" : "2014-08-07T22:13:37Z",
        "display_name" : "Account Fees",
        "category" : "Cash Flows",
        "modified_at" : "2014-08-07T22:13:37Z"
      },
      "relationships" : {
        "arguments" : {
          "links" : {
            "self" : "/v1/attributes/account_fees/relationships/arguments",
            "related" : "/v1/attributes/account_fees/arguments"
          },
          "data" : []
        }
      },
      "links" : {
        "self" : "/v1/attributes/account_fees"
      }
    },
    {
      "id" : "account_number",
      "type" : "attributes",
      "attributes" : {
        "output_type" : "Word",
        "spec_id" : 223,
        "usage" : [
          "entity_attributes",
          "filters"
        ],
        "created_at" : "2014-08-07T22:13:37Z",
        "display_name" : "Account Number",
        "category" : "Account Details",
        "modified_at" : "2014-08-07T22:13:37Z"
      },
      "relationships" : {
        "arguments" : {
          "links" : {
            "self" : "/v1/attributes/account_number/relationships/arguments",
            "related" : "/v1/attributes/account_number/arguments"
          },
          "data" : []
        }
      },
      "links" : {
        "self" : "/v1/attributes/account_number"
      }
    },
    {
      "id" : "_custom_automatic_conversion_minimum_amount_406",
      "type" : "attributes",
      "attributes" : {
        "output_type" : "Number",
        "spec_id" : 406,
        "usage" : [
          "entity_custom_attributes",
          "groupings",
          "columns",
          "position_custom_attributes",
          "filters"
        ],
        "created_at" : "2014-08-07T23:39:06Z",
        "display_name" : "Automatic Conversion Minimum Amount",
        "category" : "Uncategorized",
        "modified_at" : "2014-08-07T23:39:06Z"
      },
      "relationships" : {
        "arguments" : {
          "links" : {
            "self" : "/v1/attributes/_custom_automatic_conversion_minimum_amount_406/relationships/arguments",
            "related" : "/v1/attributes/_custom_automatic_conversion_minimum_amount_406/arguments"
          },
          "data" : []
        }
      },
      "links" : {
        "self" : "/v1/attributes/_custom_automatic_conversion_minimum_amount_406"
      }
    }
  ],
  "included" : [],
  "links" : {
    "prev" : null,
    "next" : null
  }
}
```

**Response Codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Get Arguments For Attribute

Retrieves the list of argument ids associated with the given attribute ID.

**GET** `v1/attributes/:id/relationships/arguments`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/attributes/time_weighted_return/relationships/arguments
```

```json Response
HTTP/1.1 200

{
  "data": [{
      "id": "period",
      "type": "arguments"
    },
    {
      "id": "excluded_fee_types",
      "type": "arguments"
    },
    {
      "id": "bucketed",
      "type": "arguments"
    },
    {
      "id": "adjusted",
      "type": "arguments"
    },
    {
      "id": "accrued",
      "type": "arguments"
    },
    {
      "id": "currency",
      "type": "arguments"
    },
    {
      "id": "annualized_default_false",
      "type": "arguments"
    }
  ]
}
```

**Responses:**

- `200 OK`: Success
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope
- `404 Not Found`: Attribute does not exist

## Get Argument Objects For Attribute

Retrieves the list of arguments associated with the given attribute ID.

**GET** `/v1/attributes/:id/arguments`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/attributes/cost_basis/arguments
```

```json Response
HTTP/1.1 200

{
    "data": [
        {
            "id": "cost_basis_type",
            "type": "arguments",
            "attributes": {
                "values": [
                    "ORIGINAL",
                    "ADJUSTED",
                    "CALCULATED_ADJUSTED",
                    "CALCULATED_ADJUSTED_AMORTIZATION_ONLY",
                    "CALCULATED_ADJUSTED_ACCRETION_ONLY"
                ],
                "default_value": "ORIGINAL",
                "arg_type": "discrete"
            },
            "links": {
                "self": "/v1/arguments/cost_basis_type"
            }
        },
        {
            "id": "currency",
            "type": "arguments",
            "attributes": {
                "values": [
                    "NATIVE_CURRENCY",
                    "REF_CURRENCY",
                    "USD",
                    "EUR",
                    "GBP",
                    "AED",
                    "AFN",
                    "ALL",
                    "AMD",
                    "ANG",
                    "AOA",
                    "ARS",
                    "ATS",
                    "AUD",
                    "AWG",
                    "AZN",
                    "BAM",
                    "BBD",
                    "BDT",
                    "BEF",
                    "BGN",
                    "BHD",
                    "BIF",
                    "BMD",
                    "BND",
                    "BOB",
                    "BOV",
                    "BRL",
                    "BSD",
                    "BTC",
                    "BTN",
                    "BWP",
                    "BYN",
                    "BYR",
                    "BZD",
                    "CAD",
                    "CDF",
                    "CHF",
                    "CLF",
                    "CLP",
                    "CNH",
                    "CNY",
                    "COP",
                    "CRC",
                    "CUC",
                    "CUP",
                    "CYP",
                    "CVE",
                    "CZK",
                    "DEM",
                    "DJF",
                    "DKK",
                    "DOP",
                    "DZD",
                    "EEK",
                    "EGP",
                    "ERN",
                    "ESP",
                    "ETB",
                    "ETH",
                    "FIM",
                    "FJD",
                    "FRF",
                    "GEL",
                    "GGP",
                    "GHC",
                    "GHS",
                    "GIP",
                    "GMD",
                    "GNF",
                    "GRD",
                    "GTQ",
                    "GYD",
                    "HKD",
                    "HNL",
                    "HRK",
                    "HTG",
                    "HUF",
                    "IDR",
                    "IEP",
                    "ILS",
                    "IMP",
                    "INR",
                    "IQD",
                    "IRR",
                    "ISK",
                    "ITL",
                    "JEP",
                    "JMD",
                    "JOD",
                    "JPY",
                    "KES",
                    "KGS",
                    "KHR",
                    "KMF",
                    "KPW",
                    "KRW",
                    "KWD",
                    "KYD",
                    "KZT",
                    "LAK",
                    "LBP",
                    "LKR",
                    "LRD",
                    "LSL",
                    "LTC",
                    "LTL",
                    "LVL",
                    "LUF",
                    "LYD",
                    "MAD",
                    "MDL",
                    "MGA",
                    "MKD",
                    "MMK",
                    "MNT",
                    "MOP",
                    "MRO",
                    "MRU",
                    "MTL",
                    "MUR",
                    "MVQ",
                    "MVR",
                    "MWK",
                    "MXN",
                    "MXP",
                    "MXV",
                    "MYR",
                    "MZN",
                    "NAD",
                    "NGN",
                    "NIO",
                    "NLG",
                    "NOK",
                    "NPR",
                    "NZD",
                    "OMR",
                    "PAB",
                    "PEN",
                    "PGK",
                    "PHP",
                    "PKR",
                    "PLN",
                    "PTE",
                    "PYG",
                    "QAR",
                    "RON",
                    "RSD",
                    "RUB",
                    "RWF",
                    "SAR",
                    "SBD",
                    "SCR",
                    "SDG",
                    "SEK",
                    "SGD",
                    "SHP",
                    "SIT",
                    "SKK",
                    "SLL",
                    "SOS",
                    "SRD",
                    "STD",
                    "SVC",
                    "SYP",
                    "SZL",
                    "THB",
                    "TJS",
                    "TMT",
                    "TND",
                    "TOP",
                    "TRL",
                    "TRY",
                    "TTD",
                    "TVD",
                    "TWD",
                    "TZS",
                    "UAH",
                    "UGX",
                    "UYI",
                    "UYU",
                    "UZS",
                    "VEB",
                    "VEF",
                    "VND",
                    "VUV",
                    "WST",
                    "XAU",
                    "XCD",
                    "XEU",
                    "XOF",
                    "XRP",
                    "XPF",
                    "YER",
                    "YUD",
                    "ZAR",
                    "ZMK",
                    "ZMW",
                    "ZWD",
                    "ZWL"
                ],
                "default_value": null,
                "arg_type": "discrete"
            },
            "links": {
                "self": "/v1/arguments/currency"
            }
        },
        {
            "id": "excluding_fees",
            "type": "arguments",
            "attributes": {
                "values": [
                    true,
                    false
                ],
                "default_value": false,
                "arg_type": "boolean"
            },
            "links": {
                "self": "/v1/arguments/excluding_fees"
            }
        },
        {
            "id": "rollups_ignore_dashes",
            "type": "arguments",
            "attributes": {
                "values": [
                    true,
                    false
                ],
                "default_value": false,
                "arg_type": "boolean"
            },
            "links": {
                "self": "/v1/arguments/rollups_ignore_dashes"
            }
        },
        {
            "id": "time_point",
            "type": "arguments",
            "attributes": {
                "default_value": "current",
                "arg_type": "time_point"
            },
            "links": {
                "self": "/v1/arguments/time_point"
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
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope
- `404 Not Found`: Attribute does not exist
