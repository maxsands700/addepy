# View

The Portfolio View API allows you to extract portfolio data for a saved analysis view in Addepar.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/9f50f5b-Key_and_Secret_1.gif",
"Key and Secret 1.gif",
1425
],
"align": "center",
"caption": "Generating API URL (In-App)"
}
]
}
[/block]

## Resource Overview

The Portfolio View API returns a resource object described by the below attributes and will appear in successful **GET** responses. A meta-object will also be returned in the response detailing the columns and groupings saved in the view. The API supports exporting views in JSON, CSV, TSV, or XLSX formats.

| Attribute  | Description                                                                                                        | Example                                                                                                                                                                         |
| :--------- | :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `total`    | The total portfolio value for each column attribute. Object.                                                       | `{ "name": "Total", "columns": { "time_weighted_return": 0.014858065416061494, "value": 4.394550141172772E8}`                                                                   |
| `children` | The grouping level values of the query. Includes a value for each column and grouping attribute. Array of Objects. | `{ "name": "Cash & Cash Equivalent", "grouping": "asset_class", "columns": {                     "time_weighted_return": -0.059294573135900364, "value": 1.1442715559999999E7}` |

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
"2-1": "The output format of the exported result. \n \nSupported Values: \n \n- `JSON`\n- `CSV`\n- `TSV`\n- `XLSX`",
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

\*\* Required Arguments\*\*
[block:parameters]
{
"data": {
"h-0": "Argument",
"h-1": "Description",
"h-2": "Example",
"0-0": "`id`",
"0-1": "The ID of the analysis view. \n \nThe view ID follows the “/views/” section of the URL. \n \nYou can also find the view ID by generating an API URL. See Generate an API URL.",
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
3. Select the Analysis or tab.
4. Select a view from the drop-down menu and adjust the view as needed to display the data you want to export.
5. Click Export at the top right of the table > Generate API URL > Copy Link.

The URL will include the view id, portfolio id, output type, start date, and end date.

Example API URL:\
`https://examplefirm.addepar.com/api/v1/portfolio/views/1/results?portfolio_id=10 &portfolio_type=entity&output_type=csv&start_date=2016-01-01&end_date=2016-01-02`

Try out one of the below view configurations as a starting point.

- All clients: Group by Top Level Owner > Securities.
- All accounts associated with all clients: Group by Top Level Owner > Direct Owner and include a Top Level Owner column.
- All Securities by owner: Group by Direct Owner > Security. Include columns for Position and Direct Owner.
- All Securities: Group by Securities.

## Get Analysis View Data

Returns portfolio data based on the analysis view, portfolio, and time period.

**JSON**

JSON format provides an easy way to integrate portfolio data into other systems with minimal maintenance.

If the view includes groupings, then all grouping-level values will be included. If the view does not include groupings, then the response will only return a `total` for the total portfolio value.

Values must follow one of the following types: Currency, Date, Money Value, Number, Percent, Word, Yes/No.

> 📘 JSON Restrictions
>
> - “Advanced” and “Pivot” tables are not supported.

**GET** `/v1/portfolio/views/:id/results`

**Example:**

```json Request
GET https://examplefirm.addepar.com/api/v1/portfolio/views/1/results?portfolio_id=10&portfolio_type=ENTITY&output_type=JSON&start_date=2016-01-01&end_date=2016-01-02
```

```json Response
HTTP/1.1 200

{
  "meta":{
    "columns":[
      {
        "key":"value",
        "display_name":"Value (USD)",
        "output_type":"Number",
        "currency":"USD"
      }
    ],
    "groupings":[
      {
        "key":"holding_account",
        "display_name":"Holding Account"
      },
      {
        "key":"position",
        "display_name":"Position"
      }
    ]
  },
  "data":{
    "type":"portfolio_views",
    "attributes":{
      "total":{
        "name":"Total",
        "columns":{
          "value":1.037535456E7
        },
        "children":[
          {
            "name":"Directly Owned",
            "grouping":"holding_account",
            "columns":{
              "value":1.037535456E7
            },
            "children":[
              {
                "name":"Anchorage Illiquid Opportunities III Access Fund LP",
                "grouping":"position",
                "columns":{
                  "value":1746188.0
                },
                "children":[

                ]
              },
              {
                "name":"GS Liquidity Partners 2007 LP",
                "grouping":"position",
                "columns":{
                  "value":8629166.56
                },
                "children":[

                ]
              }
            ]
          }
        ]
      }
    }
  },
  "included":[

  ]
}
```

**Response Codes:**

- `200 OK`: Success
- `400 Bad Request`: Improperly specified query parameters
  - A limited set of market data attributes may not be used in developer APIs without additional licenses. If encountered, reach out to Addepar Support for additional information. Removing these attributes from the view or creating a new view without these attributes will resolve the request errors.
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: View not found

**CSV, TSV, or XLSX**

XLSX supports exporting advanced and pivot tables.

If the view does not include groupings, then the output includes a "TOTAL" column that includes the total portfolio value.

Formatting applied to numerical values ($, K, M, etc.) is ignored for number and money value columns: the output will include the raw values up to 10 decimal places.

Values must follow one of the following types: Currency, Date, Money Value, Number, Percent, Word, Yes/No.

> 📘 CSV & TSV Restrictions
>
> - “Advanced” and “Pivot” tables are not supported.
> - Benchmarks cannot be included at the grouping level.
> - Holding Account, Ownership Structure, and Legal Entity attributes are not allowed at the lowest grouping level.

Additional Notes (CSV & TSV):

- Benchmarks at the bottom of the table will be omitted.
- If the view includes groupings, then only the lowest-level grouping data will be included: higher-level groupings and rollup values are omitted. For example, if the asset table is grouped by Asset Class > Security, only security values will appear in the output.
- If the view includes a column for an entity (e.g., Security, Top Level Owner, Direct Owner), the output will include an additional column for "\[Entity Name] \[Entity ID],” which is the unique identifier for the entity.
- If the view includes Position as a column, then the output will include an additional column for Position ID, which is the unique identifier for each position.
- Percentages are represented as a fraction of up to ten decimal places.
- Boolean values are represented as “true” or “false.”
- All CSV/TSV responses have the Byte-Order-Markprefixed to the data stream to indicate the content's UTF-8 encoding.

**GET** `/v1/portfolio/views/:id/results`

**Example:**

```json Request
GET https://examplefirm.addepar.com/api/v1/portfolio/views/1/results?portfolio_id=10&portfolio_type=ENTITY&output_type=CSV&start_date=2016-01-01&end_date=2016-01-02
```

```json RESPONSE
HTTP/1.1 200

Content-Disposition: attachment; filename="portfolio_data.csv"
Content-Type: text/csv

<VIEW_CONTENT>
```

**Response Codes:**

- `200 OK`: Success
- `400 Bad Request`: Improperly specified query parameters
- `403 Forbidden`: Insufficient application permissions or appropriate scope not granted
- `404 Not Found`: View not found
