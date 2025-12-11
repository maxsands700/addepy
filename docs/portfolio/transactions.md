# Transactions

Transactions are used to model the flow of money into and out of a portfolio. Use the Transactions API to create and delete transactions in Addepar, retrieve, and update transaction details. You can use the [View API](https://developers.addepar.com/docs/transactions-view) to extract existing saved views and [Query API](https://developers.addepar.com/docs/transaction-query) to retrieve transactions data.

![](https://files.readme.io/3aed8ff-Transactions.png "Transactions.png")
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/transactions",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/transactions/:id \n/v1/transactions/:id/owner \n/v1/transactions/:id/relationships/owner \n/v1/transactions/:id/owned \n/v1/transactions/:id/relationships/owned \n/v1/transactions/:id/cash_position \n/v1/transactions/:id/relationships/cash_account \n \n**POST** \n/v1/transactions \n \n**PATCH** \n/v1/transactions \n/v1/transactions/:id \n \n**DELETE** \n/v1/transactions \n/v1/transactions/:id \n \nNote: You can't use these GET, POST, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[No](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Portfolio Access\" determines the entities that are accessible. \n \n\"Transactions\" create edit and delete. \n \n\"Online transaction details\" is required to update and delete online transactions.",
"5-0": "OAuth scopes",
"5-1": "`TRANSACTIONS` or `TRANSACTIONS_WRITE`"
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

Transactions are described by the below resource object attributes. Attributes required for creating transactions are noted.

All attributes will be returned in successful **GET**, **POST** & **PATCH** responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`type`",
"0-1": "Addepar's classification of the transaction, which generally matches the custodian's transaction type. String. \n \nSee \"Supported Transaction Types\" below.",
"0-2": "`\"buy\"`",
"1-0": "`currency `",
"1-1": "Three-letter currency code, representing the currency of the cash involved in the transaction. String.",
"1-2": "`\"USD\"`",
"2-0": "`trade_date `",
"2-1": "The date the transaction occurred. String. \n \n\"YYYY-MM-DD \"",
"2-2": "`\"2020-09-25\"`",
"3-0": "`units`",
"3-1": "The number of shares of a security. Number. \n \nRequired for share-based assets.",
"3-2": "`24.48`",
"4-0": "`amount`",
"4-1": "Default value for the transaction. Number. \n \nRequired for the transaction type \"valuation\" and value-based assets (except for \"distribution\" and \"cash_dividend\" transaction types).",
"4-2": "`1000`",
"5-0": "`created_at`",
"5-1": "Not editable and cannot be passed in. String.",
"5-2": "`\"2023-07-28T02:24:30Z\"`",
"6-0": "`modified_at`",
"6-1": "Not editable and cannot be passed in. String.",
"6-2": "`\"2023-07-30T10:43:21Z\"`",
"7-0": "Optional Attributes",
"7-1": "Additional attributes can be applied to transactions. Multiple. \n \nSee \"Optional Transaction Attributes\" below.",
"7-2": "` \"is_reversal\": false\"`",
"8-0": "Required for transaction types",
"8-1": "Some transaction types may require specific fields. \n \nSee the \"Required fields\" column in the [Supported transaction types](https://developers.addepar.com/docs/transaction-types) table.",
"8-2": "“other_units”. Units = shares received, other_units = shares removed."
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

\*\* Optional transaction attributes\*\*
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"0-0": "`posted_date`",
"0-1": "The date that the custodian reported the transaction. String. \n \n\"YYYY-MM-DD\"",
"1-0": "`settlement_date`",
"1-1": "The date on which a trade settles. String. \n \n\"YYYY-MM-DD\"",
"2-0": "`ex_date`",
"2-1": "The date on or after which a security is traded without a previously declared dividend or distribution. String. \n \n\"YYYY-MM-DD\"",
"3-0": "`description`",
"3-1": "A string attached to the transaction typically provided by the custodian. String.",
"4-0": "`price_factor`",
"4-1": "A multiplier affecting the total value of a security. Number.",
"5-0": "`affects_cost_basis`",
"5-1": "Specifies whether cost basis / paid-in capital is affected (only applies to fees & expenses). Boolean.",
"6-0": "`affects_unfunded_commitment`",
"6-1": "A boolean specifying whether this affects unfunded commitment (only apply for fees/expenses). Boolean.",
"7-0": "`affects_adjusted_value`",
"7-1": "Specify whether adjusted value is affected (only apply for fees/expenses). Boolean.",
"8-0": "`cancellation`",
"8-1": "Specifies whether the transaction is a cancellation of another transaction. Boolean. \n \nCanceling a transaction does not delete it from the portfolio. Instead, canceling removes the transaction’s effects and changes the transaction type to “Cancellation.” \n \nDeleting a transaction removes it from the portfolio entirely.",
"9-0": "`fee`",
"9-1": "Used for Total fees (should include all fee breakdowns). Number.",
"10-0": "`fee_breakdown`",
"10-1": "Any specific fees that were incurred along with a transaction. It could be a brokerage fee or government tax for a transaction. Includes `fee_type` and `fee_amount`. Object. See fee breakdown below.",
"11-0": "`accrued`",
"11-1": "Accrued interest. Number.",
"12-0": "`tags`",
"12-1": "Assign categories of transactions (not applicable to snapshots). [String] \n \nTags are append-only and cannot be removed.",
"13-0": "`comment`",
"13-1": "Describes the transaction. Max length of 4,000 characters for snapshots and 20,000 characters for all other transaction types. String.",
"14-0": "`generic`",
"14-1": "Amount from an unspecified type of distribution (applicable to distribution transactions). Number.",
"15-0": "`cap_gain`",
"15-1": "Capital gain of unknown term on the asset (applicable to distribution transactions). Number.",
"16-0": "`long_term`",
"16-1": "Long-Term capital gains on the asset (applicable to distribution transactions). Number.",
"17-0": "`short_term`",
"17-1": "Short-Term capital gains on the asset (applicable to distribution transactions). Number.",
"18-0": "`interest`",
"18-1": "Interest Income earned on the asset (applicable to distribution transactions). Number.",
"19-0": "`ordinary`",
"19-1": "Ordinary income earned on the asset (applicable to distribution transactions). Number",
"20-0": "`dividend`",
"20-1": "Dividend income earned on the asset (applicable to distribution transactions). Number.",
"21-0": "`return_of_capital`",
"21-1": "The return of capital from the asset (applicable to distribution transactions). Number.",
"22-0": "`recallable`",
"22-1": "The total amount of the distribution that is potentially liable to be returned to the distributor in a capital call. The recallable amount does not impact Paid-in capital. \n(applicable to distribution transactions). Number.",
"23-0": "`recallable_paid_in`",
"23-1": "Similar to recallable, but the recallable amount reduces paid-in capital. (applicable to distribution transactions). Number.",
"24-0": "`option_time_value`",
"24-1": "The underlying fee of the option (applicable to option transactions). Number.",
"25-0": "`underlying_fee`",
"25-1": "The underlying fee of an option (applicable to options transactions). Number.",
"26-0": "`vendor_id`",
"26-1": "Unique identifier of a transaction as designated by a custodial data provider. Autogenerated if the transaction does not come from a data feed. String."
},
"cols": 2,
"rows": 27,
"align": [
"left",
"left"
]
}
[/block]

**Fee breakdown**

| Attribute    | Description                                                                        |
| :----------- | :--------------------------------------------------------------------------------- |
| `fee_type`   | Fee type explains the type of the fee. String. See available fee breakdowns below. |
| `fee_amount` | The amount of the fee. Number                                                      |

**Available fee types**

| Fee type                  | Key                      | Description                                                                                                                                                                                         |
| :------------------------ | :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| External Broker Fee       | `external_brokerage_fee` | Fee charged by the broker.                                                                                                                                                                          |
| Internal Broker Fee       | `internal_brokerage_fee` | Self-clearing commission or fee charged by the broker or custodian.                                                                                                                                 |
| Other Government Tax      | `other_government_tax`   | Country-specific tax other than the stamp duty or value-added tax (e.g., cantonal tax for Switzerland).                                                                                             |
| Counterparty Fee          | `counterparty_fee`       | Fee charged by a counterparty.                                                                                                                                                                      |
| Entry and Exit Fee        | `entry_exit_fee`         | Fee charged to an investor when shares are sold from a fund, typically linked to mutual funds where the manager and the bank share a entry or exit fee tin addition to the regular transaction fee. |
| Foreign Fee               | `foreign_fee`            | Foreign fee applied to the transaction.                                                                                                                                                             |
| Matching/Confirmation Fee | `matching_fee`           | Fee levied by a transfer agent for matching and confirming trades.                                                                                                                                  |
| Market Fee                | `market_fee`             | Fee applied by a government or regulatory organization (e.g., SEC fee in the United States).                                                                                                        |
| Market Tax                | `market_tax`             | Tax levied on a specific type of financial transaction for a particular purpose (e.g., financial transaction tax levied in Belgium or Spain).                                                       |
| Other Fee                 | `other_fee`              | Any other type of fee.                                                                                                                                                                              |
| Stamp Duty                | `stamp_tax`              | Tax imposed by a government on documents required for certain types of transactions (e.g., the sale or transfer of property).                                                                       |
| Stock Exchange Tax        | `stock_exchange_tax`     | Tax charged by the exchange.                                                                                                                                                                        |
| Stock Exchange Fee        | `stock_exchange_fee`     | Fee charged by the exchange.                                                                                                                                                                        |
| Turnover Fee              | `turnover_fee`           | Turnover fee for the stock exchange order.                                                                                                                                                          |
| Value-Added Tax (VAT)     | `value_added_tax`        | Tax applied to nearly all goods and services bought and sold for use or consumption.                                                                                                                |
| Withholding Tax           | `withholding_tax`        | Tax deducted from interest earned by European Union residents on their investments made in another member state, by the state where the investment is held.                                         |

| Relationship    | Description                                              |
| :-------------- | :------------------------------------------------------- |
| `owner`         | The ID of the owning entity of the transaction.          |
| `owned`         | The ID of the owned entity of the transaction.           |
| `cash_position` | The ID of the position between the owner & cash account. |

## Relationships

```json Relationships
"relationships": {
      "owner": {
        "links": {
          "self": "/v1/transactions/1929/relationships/owner",
          "related": "/v1/transactions/1929/owner"
        },
        "data": {
          "type": "entities",
          "id": "117"
        }
      },
      "owned": {
        "links": {
          "self": "/v1/transactions/1929/relationships/owned",
          "related": "/v1/transactions/1929/owned"
        },
        "data": {
          "type": "entities",
          "id": "116"
        }
      },
      "cash_position": {
        "links": {
          "self": "/v1/transactions/1929/relationships/cash_position",
          "related": "/v1/transactions/1929/cash_position"
        }
```

## Supported transaction types

A full list can be found in the[Supported transaction types](https://dash.readme.com/project/addepar/v2.257/docs/transaction-types) table.

## Create a transaction

Adds a new transaction to your firm.

\*\*POST \*\* `/v1/transactions`

**Required fields**

- `type`
- `currency`
- `trade_date`
- `units` required for share based assets
- `amount` required for the transaction type "valuation" and value-based assets (except for "distribution" and "cash_dividend" transaction types).

**Optional fields**

See "Optional Transaction Attributes" above.

**Example:**

In this example, we create a buy for a share-based asset with a trade date of "2008-03-02". A cash position has not been specified in the relationship, so cash will reflect paid from "Unknown" in the application.

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions

{
   "data":{
      "type":"transactions",
      "attributes":{
         "amount":100010.0,
         "cancellation":false,
         "fee":10.0,
         "currency":"USD",
         "comment":"Comment 2",
         "units":1000.0,
         "type":"buy",
         "trade_date":"2008-03-02"
      },
      "relationships":{
         "owner":{
            "data":{
               "type":"entities",
               "id":"2138776"
            }
         },
         "owned":{
            "data":{
               "type":"entities",
               "id":"2363267"
            }
         }
      }
   }
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":{
      "id":"1016552763",
      "type":"transactions",
      "attributes":{
         "amount":100010.0,
         "cancellation":false,
         "vendor_id":"0a950423-0e3e-4a2b-9888-0153d0153bfd",
         "currency":"USD",
         "comment":"Comment 2",
         "units":1000.0,
         "type":"buy",
         "trade_date":"2008-03-02"
      },
      "relationships":{
         "owner":{
            "links":{
               "self":"/v1/transactions/1016552763/relationships/owner",
               "related":"/v1/transactions/1016552763/owner"
            },
            "data":{
               "type":"entities",
               "id":"2138776"
            }
         },
         "owned":{
            "links":{
               "self":"/v1/transactions/1016552763/relationships/owned",
               "related":"/v1/transactions/1016552763/owned"
            },
            "data":{
               "type":"entities",
               "id":"2363267"
            }
         }
      },
      "links":{
         "self":"/v1/transactions/1016552763"
      }
   },
   "included":[

   ]
}
```

A buy can be created with a fee breakdown.

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions

{
   "data":{
      "type":"transactions",
      "attributes":{
         "amount":100010.0,
         "cancellation":false,
         "fee":10.0,
         "fee_breakdown": [
          {
            "fee_type": "EXTERNAL_BROKERAGE_FEE",
            "fee_amount": 3.0
          },
          {
            "fee_type": "GENERAL_FEE",
            "fee_amount": 7.0
          }
        ],
         "currency":"USD",
         "comment":"Comment 2",
         "units":1000.0,
         "type":"buy",
         "trade_date":"2008-03-02"
      },
      "relationships":{
         "owner":{
            "data":{
               "type":"entities",
               "id":"2138776"
            }
         },
         "owned":{
            "data":{
               "type":"entities",
               "id":"2363267"
            }
         }
      }
   }
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":{
      "id":"2083",
      "type":"transactions",
      "attributes":{
         "amount":100010.0,
         "cancellation":false,
         "vendor_id":"d1f54331-4248-46b5-b002-124d175273c5",
         "fee":10,
         "fee_breakdown":[
            {
               "fee_type":"EXTERNAL_BROKERAGE_FEE",
               "fee_amount":3.0
            },
            {
               "fee_type":"INTERNAL_BROKERAGE_FEE",
               "fee_amount":4.0
            }
         ],
         "currency":"USD",
         "comment":"Comment 2",
         "units":1000,
         "type":"buy",
         "trade_date":"2008-03-02"
      },
      "relationships":{
         "owner":{
            "links":{
               "self":"/v1/transactions/2083/relationships/owner",
               "related":"/v1/transactions/2083/owner"
            },
            "data":{
               "type":"entities",
               "id":"21"
            }
         },
         "owned":{
            "links":{
               "self":"/v1/transactions/2083/relationships/owned",
               "related":"/v1/transactions/2083/owned"
            },
            "data":{
               "type":"entities",
               "id":"95"
            }
         }
      },
      "links":{
         "self":"/v1/transactions/2083"
      }
   },
   "included":[

   ]
}
```

A cash position can be specified by including the `cash_position` relationship.

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions

{
   "data":{
      "type":"transactions",
      "attributes":{
         "amount":100010.0,
         "cancellation":false,
         "fee":10.0,
         "currency":"GBP",
         "comment":"Comment 3",
         "units":1000.0,
         "type":"buy",
         "trade_date":"2008-03-02"
      },
      "relationships":{
         "owner":{
            "data":{
               "type":"entities",
               "id":"21"
            }
         },
         "cash_position":{
            "data":{
               "type":"positions",
               "id":"178"
            }
         },
         "owned":{
            "data":{
               "type":"entities",
               "id":"95"
            }
         }
      }
   }
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":{
      "id":"2083",
      "type":"transactions",
      "attributes":{
         "amount":100020,
         "cancellation":false,
         "vendor_id":"d1f54331-4248-46b5-b002-124d175273c5",
         "fee":10,
         "currency":"GBP",
         "comment":"Comment 3",
         "units":1000,
         "type":"buy",
         "trade_date":"2008-03-02"
      },
      "relationships":{
         "owner":{
            "links":{
               "self":"/v1/transactions/2083/relationships/owner",
               "related":"/v1/transactions/2083/owner"
            },
            "data":{
               "type":"entities",
               "id":"21"
            }
         },
         "cash_position":{
            "links":{
               "self":"/v1/transactions/2083/relationships/cash_position",
               "related":"/v1/transactions/2083/cash_position"
            },
            "data":{
               "type":"positions",
               "id":"178"
            }
         },
         "owned":{
            "links":{
               "self":"/v1/transactions/2083/relationships/owned",
               "related":"/v1/transactions/2083/owned"
            },
            "data":{
               "type":"entities",
               "id":"95"
            }
         }
      },
      "links":{
         "self":"/v1/transactions/2083"
      }
   },
   "included":[

   ]
}
```

**Example:**

In this example, we create a distribution for a value-based asset with a trade date of "2018-04-23" and a posted date of "2018-04-24". A short-term capital gain and generic distribution amount are reflected by including "short_term" and "generic" attribute values.

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions

{
   "data":{
      "type":"transactions",
      "attributes":{
         "currency":"USD",
         "comment":"Comment 2",
         "type":"distribution",
         "generic":25000,
         "short_term":2000,
         "trade_date":"2018-04-23",
         "posted_date":"2018-04-24"
      },
      "relationships":{
         "owner":{
            "data":{
               "type":"entities",
               "id":"2260650"
            }
         },
         "owned":{
            "data":{
               "type":"entities",
               "id":"2260679"
            }
         }
      }
   }
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":{
      "id":"1016553122",
      "type":"transactions",
      "attributes":{
         "cancellation":false,
         "vendor_id":"7e76ea22-1ffe-46de-9f6e-70df2fb2e1f6",
         "short_term":2000.0,
         "currency":"USD",
         "comment":"Comment 2",
         "type":"distribution",
         "trade_date":"2018-04-23",
         "posted_date":"2018-04-24",
         "generic":25000.0
      },
      "relationships":{
         "owner":{
            "links":{
               "self":"/v1/transactions/1016553122/relationships/owner",
               "related":"/v1/transactions/1016553122/owner"
            },
            "data":{
               "type":"entities",
               "id":"2260650"
            }
         },
         "owned":{
            "links":{
               "self":"/v1/transactions/1016553122/relationships/owned",
               "related":"/v1/transactions/1016553122/owned"
            },
            "data":{
               "type":"entities",
               "id":"2260679"
            }
         }
      },
      "links":{
         "self":"/v1/transactions/1016553122"
      }
   },
   "included":[

   ]
}
```

We can also create a valuation for "2018-04-30" to reflect the value of the position.

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions

{
   "data":{
      "type":"transactions",
      "attributes":{
         "currency":"USD",
         "amount":50000,
         "type":"valuation",
         "trade_date":"2018-04-30"
      },
      "relationships":{
         "owner":{
            "data":{
               "type":"entities",
               "id":"2260650"
            }
         },
         "owned":{
            "data":{
               "type":"entities",
               "id":"2260679"
            }
         }
      }
   }
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":{
      "id":"26359439434990835",
      "type":"transactions",
      "attributes":{
         "amount":50000.0,
         "currency":"USD",
         "comment":"",
         "type":"valuation",
         "trade_date":"2018-04-30"
      },
      "relationships":{
         "owner":{
            "links":{
               "self":"/v1/transactions/26359439434990835/relationships/owner",
               "related":"/v1/transactions/26359439434990835/owner"
            },
            "data":{
               "type":"entities",
               "id":"2260650"
            }
         },
         "owned":{
            "links":{
               "self":"/v1/transactions/26359439434990835/relationships/owned",
               "related":"/v1/transactions/26359439434990835/owned"
            },
            "data":{
               "type":"entities",
               "id":"2260679"
            }
         }
      },
      "links":{
         "self":"/v1/transactions/26359439434990835"
      }
   },
   "included":[

   ]
}
```

**Response codes**

- `201 OK`: Success
- `400 Bad Request`: If the generated fields are specified
- `400 Bad Request`: Non supported transaction type
- `400 Bad Request`: If the transaction fails to validate
- `403 Forbidden`: Insufficient application permissions

## Create multiple transactions

Adds multiple transactions to your firm. One request can create up to 500.

\*\*POST \*\* `/v1/transactions`

**Required fields**

- `type`
- `currency`
- `trade_date`
- `units` required for share based assets
- `amount` required for the transaction type "valuation" and value-based assets

**Optional fields**

See "Optional Transaction Attributes" above.

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/transactions

{
   "data":[
      {
         "type":"transactions",
         "attributes":{
            "amount":100010.0,
            "cancellation":false,
            "fee":10.0,
            "currency":"usd",
            "comment":"Comment 2",
            "units":1000.0,
            "type":"buy",
            "trade_date":"2008-03-02"
         },
         "relationships":{
            "owner":{
               "data":{
                  "type":"entities",
                  "id":"2260647"
               }
            },
            "owned":{
               "data":{
                  "type":"entities",
                  "id":"259847"
               }
            }
         }
      },
      {
         "type":"transactions",
         "attributes":{
            "posted_date":"2020-09-25",
            "trade_date":"2020-09-25",
            "type":"contribution",
            "currency":"usd",
            "description":"lorem prism",
            "amount":13.48,
            "comment":"Random comment",
            "tags":[
               "Unknown"
            ]
         },
         "relationships":{
            "owner":{
               "data":{
                  "type":"entities",
                  "id":"2260650"
               }
            },
            "owned":{
               "data":{
                  "type":"entities",
                  "id":"2260710"
               }
            }
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
         "id":"1016552771",
         "type":"transactions",
         "attributes":{
            "amount":100010.0,
            "cancellation":false,
            "vendor_id":"627fbe0d-ae79-4363-b8ed-bbdcdf9ec915",
            "currency":"USD",
            "comment":"Comment 2",
            "units":1000.0,
            "type":"buy",
            "trade_date":"2008-03-02"
         },
         "relationships":{
            "owner":{
               "links":{
                  "self":"/v1/transactions/1016552771/relationships/owner",
                  "related":"/v1/transactions/1016552771/owner"
               },
               "data":{
                  "type":"entities",
                  "id":"2260647"
               }
            },
            "owned":{
               "links":{
                  "self":"/v1/transactions/1016552771/relationships/owned",
                  "related":"/v1/transactions/1016552771/owned"
               },
               "data":{
                  "type":"entities",
                  "id":"259847"
               }
            }
         },
         "links":{
            "self":"/v1/transactions/1016552771"
         }
      },
      {
         "id":"1016552772",
         "type":"transactions",
         "attributes":{
            "amount":13.48,
            "cancellation":false,
            "vendor_id":"de7bf70f-ba88-40db-9011-2261ac5481c4",
            "description":"lorem prism",
            "currency":"USD",
            "comment":"Random comment",
            "type":"contribution",
            "trade_date":"2020-09-25",
            "posted_date":"2020-09-25",
            "tags":[
               "Unknown"
            ]
         },
         "relationships":{
            "owner":{
               "links":{
                  "self":"/v1/transactions/1016552772/relationships/owner",
                  "related":"/v1/transactions/1016552772/owner"
               },
               "data":{
                  "type":"entities",
                  "id":"2260650"
               }
            },
            "owned":{
               "links":{
                  "self":"/v1/transactions/1016552772/relationships/owned",
                  "related":"/v1/transactions/1016552772/owned"
               },
               "data":{
                  "type":"entities",
                  "id":"2260710"
               }
            }
         },
         "links":{
            "self":"/v1/transactions/1016552772"
         }
      }
   ],
   "included":[

   ],
   "links":{
      "next":null
   }
}
```

**Response codes**

- `201 OK`: Success
- `400 Bad Request`: If the generated fields are specified
- `400 Bad Request`: Non supported transaction type
- `400 Bad Request`: If the transaction fails to validate
- `403 Forbidden`: Insufficient application permissions

## Edit a transaction

Modifies an existing transaction.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

**PATCH** `/v1/transactions/:id`

The following attributes can not be updated:

- `vendor_id`
- `trade_date` applicable to snapshot and valuation transactions

The following relationship fields can not be updated:

- `owner`
- `owned`
- `cash_position`

Note: If a transaction includes fee breakdown, you must include the fee breakdowns in the request.

To remove an attribute value from the transaction, set the attribute value to null.

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/transactions/2083

{
   "data":{
      "id":"2083",
      "type":"transactions",
      "attributes":{
         "amount":999.0,
         "fee":10,
         "fee_breakdown":[
            {
               "fee_type":"EXTERNAL_BROKERAGE_FEE",
               "fee_amount":3.0
            },
            {
               "fee_type":"GENERAL_FEE",
               "fee_amount":7.0
            }
         ],
         "comment":"Edited Comment",
         "units":24.0,
         "trade_date":"2021-01-22"
      }
   }
}
```

```json Response
HTTP/1.1 200 Success

{
   "data":{
      "id":"2083",
      "type":"transactions",
      "attributes":{
         "amount":999,
         "cancellation":false,
         "vendor_id":"d1f54331-4248-46b5-b002-124d175273c5",
         "currency":"GBP",
         "fee":10,
         "fee_breakdown":[
            {
               "fee_type":"EXTERNAL_BROKERAGE_FEE",
               "fee_amount":3.0
            },
            {
               "fee_type":"GENERAL_FEE",
               "fee_amount":7.0
            }
         ],
         "comment":"Edited Comment",
         "units":24,
         "type":"buy",
         "trade_date":"2021-01-22"
      },
      "relationships":{
         "owner":{
            "links":{
               "self":"/v1/transactions/2083/relationships/owner",
               "related":"/v1/transactions/2083/owner"
            },
            "data":{
               "type":"entities",
               "id":"21"
            }
         },
         "cash_position":{
            "links":{
               "self":"/v1/transactions/2083/relationships/cash_position",
               "related":"/v1/transactions/2083/cash_position"
            },
            "data":{
               "type":"positions",
               "id":"178"
            }
         },
         "owned":{
            "links":{
               "self":"/v1/transactions/2083/relationships/owned",
               "related":"/v1/transactions/2083/owned"
            },
            "data":{
               "type":"entities",
               "id":"95"
            }
         }
      },
      "links":{
         "self":"/v1/transactions/2083"
      }
   },
   "included":[

   ]
}
```

**Response codes**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload
- `400 Bad Request`: If the transaction fails to validate
- `403 Forbidden`: If the user does not have write access for transactions
- `404 Not Found`: Nonexistent/non-permissioned transaction or snapshot

## Edit multiple transactions

Modifies existing transactions. One request can edit up to 500.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

**PATCH** `/v1/transactions`

The following attributes can not be updated:

- `vendor_id`
- `trade_date` (cannot be updated for snapshots as it changes the transaction id)

The following relationship fields can not be updated:

- `owner`
- `owned`
- `cash_position`

To remove an attribute value from the transaction, set the attribute value to null.

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/transactions

{
   "data":[
      {
         "id":"1978",
         "type":"transactions",
         "attributes":{
            "cancellation":true
         }
      },
      {
         "id":"300",
         "type":"transactions",
         "attributes":{
            "description":null
         }
      }
   ]
}
```

```json Response
HTTP/1.1 200 Success

{
   "data":[
      {
         "id":"1978",
         "type":"transactions",
         "attributes":{
            "amount":100000.0,
            "cancellation":true,
            "vendor_id":"193bd2d2-2626-401f-956d-88f083cbde19",
            "currency":"USD",
            "type":"distribution",
            "trade_date":"2020-01-02",
            "posted_date":"2020-01-02",
            "generic":100000.0
         },
         "relationships":{
            "owner":{
               "links":{
                  "self":"/v1/transactions/1978/relationships/owner",
                  "related":"/v1/transactions/1978/owner"
               },
               "data":{
                  "type":"entities",
                  "id":"208"
               }
            },
            "cash_position":{
               "links":{
                  "self":"/v1/transactions/1978/relationships/cash_position",
                  "related":"/v1/transactions/1978/cash_position"
               },
               "data":{
                  "type":"positions",
                  "id":"342"
               }
            },
            "owned":{
               "links":{
                  "self":"/v1/transactions/1978/relationships/owned",
                  "related":"/v1/transactions/1978/owned"
               },
               "data":{
                  "type":"entities",
                  "id":"213"
               }
            }
         },
         "links":{
            "self":"/v1/transactions/1978"
         }
      },
      {
         "id":"300",
         "type":"transactions",
         "attributes":{
            "amount":99980.0,
            "cancellation":false,
            "vendor_id":"d8c946f7-e515-4083-b6a2-7ef6218a4da1",
            "fee":10.0,
            "currency":"JPY",
            "units":1000.0,
            "type":"sell",
            "trade_date":"2008-10-18"
         },
         "relationships":{
            "owner":{
               "links":{
                  "self":"/v1/transactions/300/relationships/owner",
                  "related":"/v1/transactions/300/owner"
               },
               "data":{
                  "type":"entities",
                  "id":"23"
               }
            },
            "cash_position":{
               "links":{
                  "self":"/v1/transactions/300/relationships/cash_position",
                  "related":"/v1/transactions/300/cash_position"
               },
               "data":{
                  "type":"positions",
                  "id":"51"
               }
            },
            "owned":{
               "links":{
                  "self":"/v1/transactions/300/relationships/owned",
                  "related":"/v1/transactions/300/owned"
               },
               "data":{
                  "type":"entities",
                  "id":"97"
               }
            }
         },
         "links":{
            "self":"/v1/transactions/300"
         }
      }
   ],
   "included":[

   ],
   "links":{
      "next":null
   }
}
```

**Response codes**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload
- `400 Bad Request`: If the transaction fails to validate
- `403 Forbidden`: Insufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned transaction or snapshot

## Get a transaction

Returns a transaction with the given ID.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

\*\*GET \*\* `/v1/transactions/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/1968
```

```json Response
HTTP/1.1 200 Success

{
   "data":{
      "id":"1968",
      "type":"transactions",
      "attributes":{
         "created_at":"2023-07-28T02:24:30Z",
         "amount":10000,
         "cancellation":false,
         "vendor_id":"aca6bbdb-097f-46c0-b83a-709dfdae202b",
         "currency":"USD",
         "units":100,
         "type":"buy",
         "trade_date":"2019-01-02",
         "modified_at":"2023-07-30T10:43:21Z"
      },
      "relationships":{
         "owner":{
            "links":{
               "self":"/v1/transactions/1968/relationships/owner",
               "related":"/v1/transactions/1968/owner"
            },
            "data":{
               "type":"entities",
               "id":"196"
            }
         },
         "owned":{
            "links":{
               "self":"/v1/transactions/1968/relationships/owned",
               "related":"/v1/transactions/1968/owned"
            },
            "data":{
               "type":"entities",
               "id":"200"
            }
         }
      },
      "links":{
         "self":"/v1/transactions/1968"
      }
   },
   "included":[

   ]
}
```

**Response codes**

- `200 OK`: Success
- `403 Forbidden`: Insufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned transaction

## Get a transaction's direct owner

Will return the owner entity of the transaction.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

**GET** `/v1/transactions/:id/owner`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/1968/relationships/owner
```

```json Response
HTTP/1.1 200 Success

{
   "data":{
      "id":"196",
      "type":"entities",
      "attributes":{
         "account_number":"23975399",
         "last_verified_date":"2019-01-02",
         "currency_factor":"USD",
         "online_status":"ONLINE",
         "ownership_type":"PERCENT_BASED",
         "original_name":"Schwab Account",
         "model_type":"FINANCIAL_ACCOUNT",
         "is_rolled_up":false,
         "immediate_update_requested":"2019-07-19"
      },
      "links":{
         "self":"/v1/entities/196"
      }
   },
   "included":[

   ]
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned transaction
- `404 Not Found`: Nonexistent/non-permissioned entities IDs

## Get transaction owner relationship

Will return the relationship of the owner entity.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

\*\*GET \*\* `/v1/transactions/:id/relationships/owner`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/1968/relationships/owned
```

```json Response
HTTP/1.1 200 Success

{
   "data":{
      "id":196,
      "type":"entities"
   }
}
```

\*\*Response codes\
\*\*

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned transaction

## Get a transaction's owned entity

Will return the owned entity.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

\*\*GET \*\* `/v1/transactions/:id/owned`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/1968/owned
```

```json Response
HTTP/1.1 200 Success

{
   "data":{
      "id":"200",
      "type":"entities",
      "attributes":{
         "currency_factor":"USD",
         "ticker_symbol":[
            {
               "date":null,
               "value":"AAPL",
               "weight":1
            }
         ],
         "ownership_type":"SHARE_BASED",
         "original_name":"Apple",
         "model_type":"STOCK"
      },
      "links":{
         "self":"/v1/entities/200"
      }
   },
   "included":[

   ]
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned transaction
- `404 Not Found`: Nonexistent/non-permissioned entities IDs

## Get transaction owned relationship

Will return the relationship of the owned entity.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

\*\*GET \*\* `/v1/transactions/:id/relationships/owned`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/1968/relationships/owned
```

```json Response
HTTP/1.1 200 Success

{
   "data":{
      "id":200,
      "type":"entities"
   }
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned transaction

## Get transaction cash position

Will return the cash account entity.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

\*\*GET \*\* `/v1/transactions/:id/cash_position`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/1968/cash_position
```

```json Response
HTTP/1.1 200 Success

{
   "data":{
      "id":"178",
      "type":"positions",
      "attributes":{
         "name":"Cash"
      },
      "relationships":{
         "owner":{
            "links":{
               "self":"/v1/positions/178/relationships/owner",
               "related":"/v1/positions/178/owner"
            },
            "data":{
               "type":"entities",
               "id":"21"
            }
         },
         "owned":{
            "links":{
               "self":"/v1/positions/178/relationships/owned",
               "related":"/v1/positions/178/owned"
            },
            "data":{
               "type":"entities",
               "id":"32"
            }
         }
      },
      "links":{
         "self":"/v1/positions/178"
      }
   },
   "included":[

   ]
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned transaction
- `404 Not Found`: Nonexistent/non-permissioned entities IDs

## Get transaction cash position relationship

Will return the relationship of the cash account entity.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

\*\*GET \*\* `/v1/transactions/:id/relationships/cash_account`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/1968
```

```json Response
HTTP/1.1 200 Success

{
   "data":{
      "id":178,
      "type":"positions"
   }
}
```

**Response codes**

- `200 OK`: Success
- `404 Not Found`: Nonexistent/non-permissioned transaction

## Delete a transaction

Will delete the transaction if it exists.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

\*\*DELETE \*\* `/v1/transactions/:id`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/transactions/1968
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: Insufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned transaction ID

## Delete multiple transactions

Will delete the specified transactions. One request can delete up to 500.

Note: You can't use Transaction API GET, PATCH, or DELETE endpoints for snapshots and valuations. You can use the [Snapshots API](https://developers.addepar.com/docs/snapshots-beta) instead.

\*\*DELETE \*\* `/v1/transactions`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/transactions

{
   "data":[
      {
         "id":"1968",
         "type":"transactions",
      },
      {
         "id":"1978",
         "type":"transactions",
      }
   ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: Insufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned transaction IDs
- `409 Conflict` : The "type" for one or more transactions was not specified as "transactions"
