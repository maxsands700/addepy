# View

The Transaction View API provides the ability to extract transaction data for an existing Transaction View, saved in Addepar.

The Transactions section of Addepar is a repository of all transactions for a given portfolio or asset, including those that come in automatically from custodial data feeds and those manually added by your firm.

![](https://files.readme.io/4eaef43-Transactions.png "Transactions.png")
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"0-1": "/v1/transactions",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/transactions/views/:id/results",
"2-0": "Produces",
"2-1": "CSV, TSV, or XLSX",
"3-0": "Pagination",
"3-1": "No",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Transaction firm view: View only\" and \"Transactions: View-only\" to extract view data.",
"5-0": "OAuth Scopes",
"5-1": "`TRANSACTIONS`"
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

The Transaction View API supports exporting views in CSV, TSV, or XLSX formats.

## Parameters

**Required Parameters**
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "`portfolio_id`",
"0-1": "The ID of a portfolio configured in Addepar. \n \nA portfolio can be either an entity (i.e. a client, account, legal entity etc.) or a group of entities. \n \n If the`portfolio_type` is `FIRM`, the `portfolio_id` must be `1`",
"0-2": "`portfolio_id=10`",
"1-0": "`portfolio_type`",
"1-1": "The type of portfolio. \n \nSupported Values: \n \n- `ENTITY`\n- `ENTITY_FUNDS`\n- `GROUP`\n- `GROUP_FUNDS`\n- `FIRM`\n- `FIRM_ACCOUNTS`\n- `FIRM_CLIENTS`\n- `FIRM_HOUSEHOLDS`\n- `FIRM_UNVERIFIED_ACCOUNTS`",
"1-2": "`portfolio_type=ENTITY`",
"2-0": "`output_type`",
"2-1": "The output format of the exported result. \n \nSupported Values: \n \n- `CSV`\n- `TSV`\n- `XLSX`",
"2-2": "`output_type=CSV`",
"3-0": "`start_date`",
"3-1": "The start date of the time period of portfolio data. \n \n“YYYY-MM-DD”",
"3-2": "`start_date=2016-01-01`",
"4-0": "`end_date`",
"4-1": "The end date of the time period of portfolio data. \n \n“YYYY-MM-DD”",
"4-2": "`end_date=2016-01-02`"
},
"cols": 3,
"rows": 5,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Required Arguments**
[block:parameters]
{
"data": {
"h-0": "Argument",
"h-1": "Description",
"h-2": "Example",
"0-0": "`id`",
"0-1": "The ID of the transactions view. \n \nYou can find the view ID by generating an API URL. See \"Generate an API URL\"",
"0-2": "`/views/1`"
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

## Generate an API URL

You can generate an API URL in Addepar by following the below steps:

1. Sign in to Addepar.
2. Select the portfolio on the left menu.
3. Select the Transactions tab.
4. Select a view from the drop-down menu and adjust the view as needed to display the data you want to export.
5. Click Export at the top right of the table > Generate API URL > Copy Link.

The URL will include the view id, portfolio id, output type, start date, and end date.

Example API URL:\
`https://examplefirm.addepar.com/api/v1/transactions/views/1/results?portfolio_id=10&portfolio_type=entity&output_type=csv&start_date=2020-09-07&end_date=2020-10-07`

## Get Transactions View Data

Returns data based on the transactions view, portfolio, and time period.

> 📘 Restrictions
>
> - Transaction Views for “Summary Data” are not supported.
> - Values must follow one of the following types: Currency, Date, Money Value, Number, Percent, Word, Yes/No.

Additional Notes (CSV & TSV):

- If the view includes a column for an entity (e.g., Security, Direct Owner), the output will include an additional column for "\[Entity Name] \[Entity ID],” which is the unique identifier for the entity.
- If the view includes Position as a column, then the output will include an additional column for Position ID, which is the unique identifier for each position.
- Formatting applied to numerical values ($, K, M, etc.) is ignored for number and money value columns: the output will include the raw values up to four decimal places.
- Percentages are represented as a fraction up to four decimal places.
- Boolean values are represented as “Yes” or “No.”\
  All CSV/TSV responses have the Byte-Order-Mark prefixed to the data stream to indicate the content's UTF-8 encoding.

**GET** `/v1/transactions/views/:id/results`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/transactions/views/1/results?portfolio_id=10&portfolio_type=ENTITY&output_type=CSV&start_date=2000-09-01&end_date=2020-1-01
```

```json Response
HTTP/1.1 200

Content-Disposition: attachment; filename="transactions_data.csv"
Content-Type: text/csv

<VIEW_CONTENT>
```

**Response Codes:**

- `200 OK`: Success
- `400 Bad Request`: Improperly specified query parameters
- `403 Forbidden`: Insufficient application permissions
- `404 Not Found`: View not found
