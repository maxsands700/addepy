# Query

The Transactions Query API allows clients to query for transactions based on dates and attributes, providing a way for partners and clients to get transaction data back into their data warehouses.

![](https://files.readme.io/f45e4a0-Edit_transactions_table.png "Edit transactions table.png")
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"0-1": "/v1/transactions/query",
"1-0": "Endpoints",
"1-1": "**POST** \n/v1/transactions/query",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "No",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Transaction firm view: View only\" and \"Transactions: View-only\" to extract view data.",
"5-0": "OAuth Scopes",
"5-1": "`TRANSACTIONS` OR `TRANSACTIONS_WRITE`"
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

The resource object will return attributes specified by columns in successful **_POST_** requests for the Transactions Query API. A meta-object will also be returned in the response detailing the columns used in the query.

## Parameters

**Required Parameters:**
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "`column`",
"0-1": "List of column attribute keys. [String].",
"0-2": "`[\"trade_date\", \"security\"]`",
"1-0": "`start_date`",
"1-1": "The start date of the time period of transaction data. String. \n \n\"YYYY-MM-DD\"",
"1-2": "`\"2021-09-05\"`",
"2-0": "`end_date`",
"2-1": "The end date of the time period of transaction data. String. \n \n\"YYYY-MM-DD\"",
"2-2": "`\"2021-09-06\"`",
"3-0": "`portfolio_type`",
"3-1": "The type of portfolio. String. \n \nSupported Values: \n \n- `ENTITY`\n- `ENTITY_FUNDS`\n- `GROUP`\n- `GROUP_FUNDS`\n- `FIRM`\n- `FIRM_ACCOUNTS`\n- `FIRM_CLIENTS`\n- `FIRM_HOUSEHOLDS`\n- `FIRM_UNVERIFIED_ACCOUNTS`",
"3-2": "`\"ENTITY\"`",
"4-0": "`portfolio_id` or `external_ids` See below.",
"4-1": "The ID of a portfolio configured in Addepar. Number or [Number]. \n \nA portfolio can be either an entity (i.e. a client, account, legal entity etc.) or a group of entities. \n \nIf the portfolio_type is `FIRM`, the portfolio_id must be 1.",
"4-2": "`7` \n \n`[22, 24]`",
"5-0": "`external_ids`",
"5-1": "External id of the entity/group being queried for. Array of Objects.",
"5-2": "`[{\n  \"external_type_key\": \"salesforce\",\n  \"external_id\": \"salesforce_external_id\"\n}]`"
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

<details><summary>Transaction Columns</summary>
<p>

| Column                         | Appears in Addepar As          |
| :----------------------------- | :----------------------------- |
| `account_number`               | Account #                      |
| `accrued_income`               | Snapshot Accrued Income        |
| `are_tax_lots_ignored`         | Are Custodian Tax Lots Ignored |
| `asset_class`                  | Asset Class                    |
| `cash_account`                 | Paid to(from)                  |
| `client`                       | Client                         |
| `comments`                     | Comments                       |
| `context`                      | Context                        |
| `currency`                     | Currency                       |
| `cusip`                        | CUSIP                          |
| `data_source`                  | Data Source                    |
| `data_type`                    | Summary Data Level             |
| `description`                  | Description                    |
| `direct_owner_id`              | Direct Owner Entity ID         |
| `edited_online_data`           | Edited Online Data             |
| `associated_hidden_positions`  | Associated Hidden Position(s)  |
| `entity_id`                    | Entity ID                      |
| `ex_date`                      | Ex-Date                        |
| `fees`                         | Fees                           |
| `fund`                         | Fund                           |
| `affected_by_hidden_positions` | Affected by Hidden Position(s) |
| `has_tax_lots`                 | Has Tax Lots                   |
| `has_wash_sale`                | Has Wash Sale                  |
| `is_verified`                  | Is Verified                    |
| `direct_owner`                 | Direct Owner                   |
| `id`                           | ID                             |
| `isin`                         | ISIN                           |
| `limited_partner`              | Limited Partner                |
| `other_affected_assets`        | Other Affected Assets          |
| `ownership_type`               | Ownership Type                 |
| `account_name`                 | Account Name                   |
| `position`                     | Position                       |
| `position_id`                  | Position ID                    |
| `posted_date`                  | Posted Date                    |
| `price_factor`                 | Price Factor                   |
| `price_per_share`              | Price Per Share                |
| `recallable_amount`            | Recallable Amount              |
| `security`                     | Security                       |
| `model_type`                   | Security Model Type            |
| `sedol`                        | SEDOL                          |
| `grouping_configuration`       | Grouping Configuration         |
| `tag`                          | TAG                            |
| `ticker_symbol`                | Ticker Symbol                  |
| `trade_date`                   | Trade Date                     |
| `settlement_date`              | Settlement Date                |
| `snapshot_units`               | Snapshot Units                 |
| `summary`                      | Summary                        |
| `transaction_units`            | Transaction Units              |
| `type`                         | Type                           |
| `units`                        | Units                          |
| `units_changed`                | Units Changed                  |
| `value`                        | Value                          |
| `vendor_id`                    | Vendor ID                      |
| `affects_adjusted_value`       | Affects Adjusted Value         |
| `affects_cost_basis`           | Affects Cost Basis             |
| `affects_paid_in_capital`      | Affects Paid-in Capital        |
| `affects_unfunded_commitments` | Affects Unfunded Commitments   |
| `general_fee`                  | General Fee                    |
| `external_brokerage_fee`       | External Broker Fee            |
| `internal_brokerage_fee`       | Internal Broker Fee            |
| `other_government_tax`         | Other Government Tax           |
| `counterparty_fee`             | Counterparty Fee               |
| `entry_exit_fee`               | Entry and Exit Fee             |
| `foreign_fee`                  | Foreign Fee                    |
| `matching_fee`                 | Matching/Confirmation Fee      |
| `market_fee`                   | Market Fee                     |
| `market_tax`                   | Market Tax                     |
| `other_fee`                    | Other Fee                      |
| `stamp_tax`                    | Stamp Duty                     |
| `stock_exchange_tax`           | Stock Exchange Tax             |
| `stock_exchange_fee`           | Stock Exchange Fee             |
| `turnover_fee`                 | Turnover Fee                   |
| `value_added_tax`              | Value Added Tax (VAT)          |
| `withholding_tax`              | Withholding Tax                |
| `last_edit_by`                 | Last Edited By                 |
| `last_edit_date`               | Last Edited Date               |
| `modified_date`                | Modified Date                  |
| `general_distribution`         | General Distribution           |
| `return_of_capital`            | Return of Capital              |
| `long_term_capital_gain`       | Long-Term Capital Gain         |
| `short_term_capital_gain`      | Short-Term Capital Gain        |
| `unknown_capital_gain`         | Unknown Capital Gain           |
| `interest_income`              | Interest Income                |
| `ordinary_income`              | Ordinary Income                |
| `dividend_income`              | Dividend Income                |
| `total_distribution`           | Total Distribution             |
| `created_date`                 | Created Date                   |

</p>
</details>

## Query Transactions Data

Returns transaction data based on the given query parameters.

**POST** `/v1/transactions/query`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions/query

{
  "data": {
    "type": "transaction_query",
    "attributes": {
      "columns": ["direct_owner", "security", "value", "trade_date"],
      "portfolio_type": "GROUP",
      "portfolio_id": 7,
      "start_date": "2021-02-01",
      "end_date": "2021-03-01",
      "include_online_valuations": false,
      "include_unverified": false,
      "include_deleted": true
    }
  }
}
```

```json Reponse
HTTP/1.1 200

{
    "meta": {
        "columns": [
            "direct_owner",
            "security",
            "value",
            "trade_date"
        ]
    },
    "data": [
        {
            "id": "7",
            "type": "transaction_query",
            "attributes": {
                "direct_owner": {
                    "name": "Person 1",
                    "entity_id": 22
                },
                "security": {
                    "name": "Holding Company 1 Display Name",
                    "entity_id": 21
                },
                "trade_date": "2000-01-01",
                "value": null
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
- `400 Bad Request`: Improperly formatted query or lacking necessary data permissions
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

**Optional Parameters:**
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "`filters`",
"0-1": "A transactions query filter may be attached to a transactions query to filter rows from the result. Array of Objects. \n \nTo learn more, reference the Filter Object section below.",
"0-2": "`[{\n\"operator\": \"include\",\n\"type\": \"discrete\",\n\"values\": [\"11112222\"],\n\"attribute\": \"security\"\n}]`",
"1-0": "`sortings`",
"1-1": "A transactions query sorting may be attached to a transactions query to sort rows. Accepts up to 3 columns to sort by. Array of objects. \n \nDefault to trade date.",
"1-2": "`[{\n\"attribute\": \"trade_date\",\n\"ascending\": false\n}]`",
"2-0": "`limit`",
"2-1": "The max number of transactions returned by the query. Number. \n \nDefault to null (No limit, returns everything unless request times out.)",
"2-2": "`500`",
"3-0": "`include_online_valuations`",
"3-1": "Whether online snapshots should be returned by the query. Boolean. \n \nDefault to false.",
"3-2": "`true`",
"4-0": "`include_unverified`",
"4-1": "Whether unverified transactions should be returned by the query. Boolean. \n \nDefault to false.",
"4-2": "`true`",
"5-0": "`include_deleted`",
"5-1": "Whether deleted online transactions should be returned by the query. Boolean. \n \nDefault to false.",
"5-2": "`true`"
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

## Filter Object

Filters are used in Transaction Views to filter data. For example, to see only certain transactions, you can filter by start date.

![](https://files.readme.io/fe380ad-Transactions_Filter.gif "Transactions Filter.gif")

**Parameters:**
[block:parameters]
{
"data": {
"h-0": "Parameters",
"h-1": "Description",
"h-2": "Example",
"0-0": "attribute",
"0-1": "The instance of the portfolio query attribute to be filtered on. String.",
"0-2": "`\"start_date\" `",
"1-0": "operator",
"1-1": "Specifies the operation of the filter. String. \n \nSupported Values: \n \n- `include`\n- `exclude`",
"1-2": "`\"include\"`",
"2-0": "type",
"2-1": "Specifies the type of filter to be applied, which is based on the output type of the attribute. String. \n \nSupported Values: \n-`DISCRETE` \n \n- `NUMBER`\n- `DATE` \n -`STRING`",
"2-2": "`\"discrete\"`",
"3-0": "values (plural)",
"3-1": "Required for type `DISCRETE`: `values`, a list of String values to match against, case-sensitive.",
"3-2": "`[\"Transaction ID\", \"Entity ID\"]`",
"4-0": "value (singular)",
"4-1": "Query transactions by comments or descriptions. \n \nRequired for type `STRING`: A single string with space separated tokens to match against is required.",
"4-2": "`\"stock Apple\"` \n \nThis will match any comment or description containing the word stock or Apple.",
"5-0": "date",
"5-1": "Required for type `DATE`: \n`period`, instance of date_filter_period. Array of objects. \n \nFor more information on date filter, see below.",
"5-2": "`{\"type\": \"static_time_period\",\n    \"start\": \"2021-01-01\",\n    \"end\": \"2021-12-30\"}`",
"6-0": "number",
"6-1": "Required for type `NUMBER`: \n`start`, numeric value denoting the starting point. \n`end`, numeric value denoting the ending point.",
"6-2": "`1, 30.5`"
},
"cols": 3,
"rows": 7,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions/query

{
  "data": {
    "type": "transaction_query",
    "attributes": {
      "columns": ["direct_owner", "value","trade_date"],
      "filters": [
        {
            "operator": "include",
            "type": "discrete",
            "values": ["Buy",
                       "Sell"],
            "attribute": "direct_owner"
          }
      ],
      "portfolio_type": "firm",
      "portfolio_id": [1],
      "start_date": "2021-09-05",
      "end_date": "2021-10-05",
      "include_online_valuations": false,
      "include_unverified": false,
      "include_deleted": true
    }
  }
}
```

```json Response
HTTP/1.1 200

{
    "meta": {
        "columns": [
            "direct_owner",
            "value",
            "trade_date"
        ]
    },
    "data": [
        {
            "id": "1919",
            "type": "transaction_query",
            "attributes": {
                "direct_owner": {
                    "name": "Integration Tester",
                    "entity_id": 183
                },
                "trade_date": "2005-01-01",
                "value": null
            }
        },
        {
            "id": "1960",
            "type": "transaction_query",
            "attributes": {
                "direct_owner": {
                    "name": "Integration Tester",
                    "entity_id": 183
                },
                "trade_date": "2007-01-01",
                "value": -100000
            }
        },
        {
            "type": "transaction_query",
            "attributes": {
                "direct_owner": {
                    "name": "Integration Tester",
                    "entity_id": 183
                },
                "trade_date": "2007-01-01",
                "value": 100000
            }
        },
        {
            "type": "transaction_query",
            "attributes": {
                "direct_owner": {
                    "name": "Integration Tester",
                    "entity_id": 183
                },
                "trade_date": "2015-02-01",
                "value": 100100
            }
        }
    ],
    "included": [],
    "links": {
        "next": null
    }
}
```

## Date Filters

To filter by dates, create a period object, then identify the type of date filter and use any required formatting.
[block:parameters]
{
"data": {
"h-0": "Parameters",
"h-1": "Details",
"h-2": "Example",
"0-0": "`type`",
"0-1": "Specifies the type of date filter to be applied. String. \n \nSupported values: \n-`current_time_period` \n-`inception_to_start_date_time_period` \n-`relative_time_period` \n-`since_inception_time_period` \n-`static_time_period` \n-`trailing_time_period` \n-`custom_time_period`",
"0-2": "`\"current_time_period\"`",
"1-0": "`start`",
"1-1": "Required for `static_time_period`. String. \n \n\"YYYY-MM-DD\"",
"1-2": "`\"2021-01-01\"`",
"2-0": "`end`",
"2-1": "Required for `static_time_period`. String. \n \n\"YYYY-MM-DD\"",
"2-2": "` \"2021-12-30\"`",
"3-0": "`period`",
"3-1": "Required for `relative_time_period`and `trailing_time_period`. String. \n \n`P1D,` `P2K,` `P1Q`, etc. \nD = Days \nK = weekdays \nW = Weeks \nM = Months \nQ = Quarters \nY = Years",
"3-2": "`\"P3K\"`"
},
"cols": 3,
"rows": 4,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Static Time Period Example**

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions/query

{
  "data": {
    "type": "transaction_query",
    "attributes": {
      "columns": ["direct_owner", "security", "value", "trade_date"],
      "filters": [
          {
            "attribute": "trade_date",
            "operator": "include",
            "type": "date",
            "period": {
                "type": "static_time_period",
                "start": "2020-01-02",
                "end": "2020-01-03"
            }
        }
        ],
      "portfolio_type": "entity",
      "portfolio_id": [206],
   		"start_date": "2019-12-01",
      "end_date": "2019-12-31",
      "include_online_valuations": false,
      "include_unverified": false,
      "include_deleted": true
    }
  }
}
```

```json Response
HTTP/1.1 200

{
    "meta": {
        "columns": [
            "direct_owner",
            "security",
            "value",
            "trade_date"
        ]
    },
    "data": [
        {
            "id": "1976",
            "type": "transaction_query",
            "attributes": {
                "direct_owner": {
                    "name": "11112222",
                    "entity_id": 208
                },
                "security": {
                    "name": "USD",
                    "entity_id": 20
                },
                "trade_date": "2020-01-03",
                "value": -100100
            }
        }
    ],
    "included": [],
    "links": {
        "next": null
    }
}
```

**Trailing Time Period Example**

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions/query


{
  "data": {
    "type": "transaction_query",
    "attributes": {
      "columns": ["direct_owner", "security", "value", "trade_date"],
      "filters": [
          {
            "attribute": "trade_date",
            "operator": "include",
            "type": "date",
            "period": {
                "type": "trailing_time_period",
                "period": "P2K"
            }
        }
        ],
      "portfolio_type": "entity",
      "portfolio_id": [206],
      "start_date": "2019-12-01",
      "end_date": "2019-12-31",
      "include_online_valuations": false,
      "include_unverified": false,
      "include_deleted": true
    }
  }
}
```

```json Response
HTTP/1.1 200


{
    "meta": {
        "columns": [
            "direct_owner",
            "security",
            "value",
            "trade_date"
        ]
    },
    "data": [
        {
            "id": "1971",
            "type": "transaction_query",
            "attributes": {
                "direct_owner": {
                    "name": "Conversions Client",
                    "entity_id": 206
                },
                "security": {
                    "name": "11112222",
                    "entity_id": 208
                },
                "trade_date": "2019-12-31",
                "value": null
            }
        },
        {
            "id": "1970",
            "type": "transaction_query",
            "attributes": {
                "direct_owner": {
                    "name": "Conversions Client",
                    "entity_id": 206
                },
                "security": {
                    "name": "33334444",
                    "entity_id": 212
                },
                "trade_date": "2019-12-31",
                "value": null
            }
        }
    ],
    "included": [],
    "links": {
        "next": null
    }
}
```

## Sorting

To narrow your response you can use sortings.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "sortings",
"0-1": "A transactions query sorting may be attached to a transactions query to sort rows. Accepts up to sorting 3 columns, and the order of the columns determines their priority in the request. Array of objects. \n \nDefault to trade date.",
"0-2": "`[{\n  \"attribute\": \"trade_date\", \n  \"ascending\": false,\n}] `"
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

**Example:**\
In this example, the request is first sorted by the newest trade date, then securities in alphabetical order.

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions/query

{
   "data":{
      "type":"transaction_query",
      "attributes":{
         "columns":["direct_owner", "security","trade_date", "id" ],
         "sorting":[
            {
               "attribute":"trade_date",
               "ascending":false
            },
            {
               "attribute":"security",
               "ascending":true
            }
         ],
         "portfolio_type":"GROUP",
         "portfolio_id":7,
         "start_date":"2021-06-30",
         "end_date":"2021-09-30",
         "include_online_valuations":true,
         "include_unverified":false,
         "include_deleted":true,
      }
   }
}
```

```json Response
HTTP/1.1 200

{
   "meta":{
      "columns":[
         "direct_owner",
         "security",
         "trade_date",
         "id"
      ]
   },
   "data":[
      {
         "id":"1919",
         "type":"transaction_query",
         "attributes":{
            "direct_owner":{
               "name":"Integration Tester 2",
               "entity_id":188
            },
            "security":{
               "name":"Integration Trust 2",
               "entity_id":188
            },
            "trade_date":"2005-01-02",
            "transaction_id":{
               "name":"Transaction ID 2",
               "entity_id":188
            }
         }
      },
      {
         "id":"1919",
         "type":"transaction_query",
         "attributes":{
            "direct_owner":{
               "name":"Integration Tester 1",
               "entity_id":183
            },
            "security":{
               "name":"Integration Trust 1",
               "entity_id":186
            },
            "trade_date":"2005-01-01",
            "transaction_id":{
               "name":"Transaction ID 1",
               "entity_id":186
            }
         }
      }
   ],
   "included":[ ],
   "links":{
      "next":null
   }
}
```
