# Query

The Portfolio Query API allows you to make dynamic portfolio query requests without referencing an Addepar view ID. The interface is useful for portfolio integrations that allow end-users to adjust Addepar attribute such as Time Weighted Return.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/65b99c3-Analysis_View.png",
"Analysis View.png",
3104
],
"align": "center",
"sizing": "smart",
"caption": "Analysis View Configuration (In-App)"
}
]
}
[/block]

## Resource Overview

The Portfolio Query API returns a resource object described by the below attributes and will appear in successful **POST** responses. A meta-object will also be returned in the response detailing the columns and groupings used in the query.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`total`",
"0-1": "The total portfolio value for each column attribute. Object. \n \n`null` column values are not included.",
"0-2": "`{ \"name\": \"Total\", \"columns\": { \"time_weighted_return\": 0.014858065416061494, \"value\": 4.394550141172772E8}`",
"1-0": "`children`",
"1-1": "The grouping level values of the query. Includes a value for each column and grouping attribute. Array of Objects.",
"1-2": "`{ \"name\": \"Cash & Cash Equivalent\", \"grouping\": \"asset_class\", \"columns\": {                     \"time_weighted_return\": -0.059294573135900364,\n\"value\": 1.1442715559999999E7}`"
},
"cols": 3,
"rows": 2,
"align": [
"left",
"left",
"left"
]
}
[/block]

## Parameters

**Required Parameters:**
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "`columns`",
"0-1": "List of column attribute keys with optional arguments. Array of Objects. \n \nOmitted arguments will use default values. \n \nSee [Attributes](https://developers.addepar.com/docs/attributes) to discover supported attributes. \n \nSee [Arguments](https://developers.addepar.com/docs/arguments) to discover supported attribute arguments.",
"0-2": "`[{\"key\": \"time_weighted_return\"}]`",
"1-0": "`groupings`",
"1-1": "List of grouping attribute keys with optional arguments. Array of Objects. \n \nOmitted arguments will use default values. \n \nSee [Attributes](https://developers.addepar.com/docs/attributes) to discover supported attributes. \n \nSee [Arguments](https://developers.addepar.com/docs/arguments) to discover supported attribute arguments.",
"1-2": "` [{\"key\": \"asset_class\"}]`",
"2-0": "`start_date`",
"2-1": "The start date of the time period of portfolio data. String. \n \n\"YYYY-MM-DD\"",
"2-2": "`\"2011-12-31\"`",
"3-0": "`end_date`",
"3-1": "The end date of the time period of portfolio data. String. \n \n“YYYY-MM-DD”",
"3-2": "`\"2013-01-15\"`",
"4-0": "`portfolio_type`",
"4-1": "The type of portfolio. String. \n \nSupported values: \n \n- `ENTITY`\n- `ENTITY_FUNDS`\n- `GROUP`\n- `GROUP_FUNDS`\n- `FIRM`\n- `FIRM_ACCOUNTS`\n- `FIRM_CLIENTS`\n- `FIRM_HOUSEHOLDS`\n- `FIRM_UNVERIFIED_ACCOUNTS`",
"4-2": "`\"ENTITY\"`",
"5-0": "`portfolio_id` or `external_ids` See below.",
"5-1": "The ID of a portfolio configured in Addepar. Number or [Number]. \n \nA portfolio can be either an entity (i.e. a client, account, legal entity etc.) or a group of entities. \n \n If the`portfolio_type` is `FIRM`, the `portfolio_id` must be `1`",
"5-2": "`7` \n \n`[22, 24]`",
"6-0": "`external_ids`",
"6-1": "The external ID of a portfolio configured in Addepar. [String]. \n \nSee [External IDs (Beta)](https://developers.addepar.com/docs/external-identifiers-beta) to learn more about External IDs.",
"6-2": "`[{\n\"external_type_key\": \"salesforce\", \"external_id\": \"example_salesforce_id\"\n}]`"
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

## Query Portfolio Data

> 👍
>
> [The Portfolio Query Builder](https://developers.addepar.com/docs/portfolio-query-builder) can be used to convert an analysis view table into a Portfolio Query API request body.

Returns portfolio data based on the given query parameters.

**POST** `/v1/portfolio/query`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/portfolio/query

{
  "data": {
    "type": "portfolio_query",
    "attributes": {
      "columns": [
        {"key": "time_weighted_return"}
      ],
      "groupings": [
        {"key": "asset_class"}
      ],
      "portfolio_type": "ENTITY",
      "portfolio_id": [329263, 259910],
      "start_date": "2018-06-30",
      "end_date": "2018-09-30"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "meta":{
    "columns":[
      {
        "key":"time_weighted_return",
        "display_name":"TWR (USD)",
        "output_type":"Percent",
        "currency":"USD"
      }
    ],
    "groupings":[
      {
        "key":"asset_class",
        "display_name":"Asset Class"
      }
    ]
  },
  "data":{
    "type":"portfolio_views",
    "attributes":{
      "total":{
        "name":"Total",
        "columns":{
          "time_weighted_return":0.023992155163590434
        },
        "children":[
          {
            "name":"Cash & Cash Equivalent",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":-0.002332896014161534
            },
            "children":[

            ]
          },
          {
            "name":"Equity",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":0.09047133778274707
            },
            "children":[

            ]
          },
          {
            "name":"Fixed Income",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":5.433985661802421E-4
            },
            "children":[

            ]
          },
          {
            "name":"Hedge Fund",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":0.0
            },
            "children":[

            ]
          },
          {
            "name":"Private Equity",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":-9.164759058766236E-5
            },
            "children":[

            ]
          },
          {
            "name":"Alternative",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":null
            },
            "children":[

            ]
          },
          {
            "name":"Real Assets",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":0.0
            },
            "children":[

            ]
          },
          {
            "name":"Unknown",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":null
            },
            "children":[

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
- `400 Bad Request`: Improperly formatted query or lacking necessary data permissions
  - Certain market data attributes may not be used in developer APIs without additional licenses. If encountered, reach out to Addepar Support for additional information.
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

**Optional Parameters:**
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "`filters`",
"0-1": "A portfolio query filter may be attached to a portfolio query to filter rows from the result. Array of Objects. \n \nTo learn more, reference the Filter Object section below.",
"0-2": "`[{\"attribute\": \"asset_class\",\n        \"type\": \"discrete\",\n        \"operator\": \"include\",\n        \"values\": [\"Equity\", \"Fixed Income\"]}`",
"1-0": "`hide_previous_holdings`",
"1-1": "Set to true to exclude holdings not held at end of current period. Boolean. (default: false)",
"1-2": "`false`",
"2-0": "`group_by_historical_values`",
"2-1": "Set to true to include previous values when grouping on a time varying attribute. Boolean. (default: false)",
"2-2": "`true`",
"3-0": "`group_by_multiple_attribute_values`",
"3-1": "Set to true to breakout groupings by each value in an attribute with multiple values. Boolean. (default: false)",
"3-2": "`false`",
"4-0": "`look_through_composite_securities`",
"4-1": "Set to true to look through components of composite securities (eg. funds). Boolean. (default: false)",
"4-2": "`false`",
"5-0": "`look_through_constituent_holdings`",
"5-1": "Set how many constituents are returned in the response by lookthrough type and threshold. \n \nThreshold is a number or can be null. \n \nSupported type values: \n \n- `\"none\"`\n- `\"top\"`\n- `\"all\"`\n- `\"weighted\"`",
"5-2": "`\"look_through_constituent_holdings\": {\n        \"type\": \"top\",\n        \"threshold\": 10\n      },`",
"6-0": "`display_account_fees`",
"6-1": "Set to true to show account fees. Boolean. (default: false)",
"6-2": "`false`"
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
POST https://examplefirm.addepar.com/api/v1/portfolio/query

{
  "data":{
    "type":"portfolio_query",
    "attributes":{
      "columns":[
        {
          "key":"value"
        }
      ],
      "groupings":[
        "asset_class"
      ],
      "portfolio_type":"FIRM",
      "portfolio_id":1,
      "start_date":"2020-02-01",
      "end_date":"2020-06-01",
      "hide_previous_holdings":true,
      "group_by_multiple_attribute_values":true
    }
  }
}
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
        "key":"asset_class",
        "display_name":"Asset Class"
      }
    ]
  },
  "data":{
    "type":"portfolio_views",
    "attributes":{
      "total":{
        "name":"Total",
        "columns":{
          "value":4.371024413999725E8
        },
        "children":[
          {
            "name":"Cash & Cash Equivalent",
            "grouping":"asset_class",
            "columns":{
              "value":1.1442713893333333E7
            },
            "children":[

            ]
          },
          {
            "name":"Equity",
            "grouping":"asset_class",
            "columns":{
              "value":2.5993525600627503E8
            },
            "children":[

            ]
          },
          {
            "name":"Fixed Income",
            "grouping":"asset_class",
            "columns":{
              "value":4.555629874790781E7
            },
            "children":[

            ]
          },
          {
            "name":"Derivative",
            "grouping":"asset_class",
            "columns":{
              "value":9548725.0
            },
            "children":[

            ]
          },
          {
            "name":"Hedge Fund",
            "grouping":"asset_class",
            "columns":{
              "value":4.175902058892848E7
            },
            "children":[

            ]
          },
          {
            "name":"Private Equity",
            "grouping":"asset_class",
            "columns":{
              "value":6411993.603527796
            },
            "children":[

            ]
          },
          {
            "name":"Alternative",
            "grouping":"asset_class",
            "columns":{
              "value":1.0651418879999999E7
            },
            "children":[

            ]
          },
          {
            "name":"Real Assets",
            "grouping":"asset_class",
            "columns":{
              "value":219414.12
            },
            "children":[

            ]
          },
          {
            "name":"Unknown",
            "grouping":"asset_class",
            "columns":{
              "value":5.157760056E7
            },
            "children":[

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

> 📘 Note
>
> The below attributes are currently unsupported:
>
> - Allocation Deviation
> - Allocation Deviation (%)
> - Benchmark
> - Benchmark (Rollup)
> - Target Allocation
> - Benchmark (Rollup)
> - Target Allocation Range

## Filter Object

Filters are used in Analysis Views to filter data. For example, to see only equities, you can filter by asset class.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/f9028cd-Query.gif",
"Query.gif",
1425
],
"align": "center",
"caption": "Analysis View Filters (In-App)"
}
]
}
[/block]

> 📘 Note
>
> Date Filters are not currently supported.

**Filter Parameters**
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "`attribute`",
"0-1": "The instance of the portfolio query attribute to be filtered on. String.",
"0-2": "`\"asset_class\"`",
"1-0": "`type`",
"1-1": "Specifies the type of filter to be applied, which is based on the output type of the attribute. String. \n \nSupported Values: \n \n- `discrete`\n- `number`",
"1-2": "`\"discrete\"`",
"2-0": "`operator`",
"2-1": "Specifies the operation of the filter. String. \n \nSupported Values (`discrete`): \n \n- `include`\n\n- `exclude`Supported Values (`number`):\n\n- `range`\n\n- `rank`",
"2-2": "`\"include\"`",
"3-0": "`values`",
"3-1": "List of String values to include or exclude. [String]",
"3-2": "`[\"Equity\", \"Fixed Income\"]`",
"4-0": "`ranges`",
"4-1": "List of to / from pairs. \n \nRequired for `type: number`, `operator: range`",
"4-2": "`[{\"from\": 0.01, \"to\": 10000}, {\"from\": -10000, \"to\": -0.01}]`",
"5-0": "`rank_order`",
"5-1": "Returns either the top or bottom results of the rank filter operation. String. \n \nRequired for` type: number`, `operator: rank` \n \nSupported Values: \n \n- `top`\n- `bottom`",
"5-2": "`\"top\"`",
"6-0": "`rank_value`",
"6-1": "The # of values to return in the rank filter operation. Number. \n \nRequired for `type: number`, `operator: rank`",
"6-2": "`10`",
"7-0": "`grouping_attribute`",
"7-1": "Narrow the data according to the values of aggregated positions. String. \n \nOptional for number.",
"7-2": "`\"asset_class\"`",
"8-0": "`unassigned_account_fees`",
"8-1": "Set to include or exclude unassigned account fees. Boolean. \n \nFees are “unassigned” when the results do not include the asset they’re associated with. \n \nOptional for discrete. \n \nDefault is `true` for inclusion filters, `false` for exclusion.",
"8-2": "`true`"
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

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/portfolio/query

{
  "data":{
    "type":"portfolio_query",
    "attributes":{
      "columns":[
        {
          "key":"cost_basis"
        }
      ],
      "groupings":[
        {
          "key":"holding_account"
        }
      ],
      "filters":[
        {
          "attribute":"asset_class",
          "type":"discrete",
          "operator":"include",
          "values":[
            "Equity",
            "Fixed Income"
          ]
        },
        {
          "attribute":{
            "key":"investment_type"
          },
          "type":"discrete",
          "operator":"exclude",
          "values":[
            "Hedge Fund"
          ]
        }
      ],
      "portfolio_type":"GROUP",
      "portfolio_id":9559,
      "start_date":"2018-06-30",
      "end_date":"2018-09-30"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
    "meta": {
        "columns": [
            {
                "key": "cost_basis",
                "display_name": "Original Cost Basis (USD)",
                "output_type": "Number",
                "currency": "USD"
            }
        ],
        "groupings": [
            {
                "key": "holding_account",
                "display_name": "Holding Account"
            }
        ]
    },
    "data": {
        "type": "portfolio_views",
        "attributes": {
            "total": {
                "name": "Total",
                "columns": {
                    "cost_basis": 2.1105883993468016E7
                },
                "children": [
                    {
                        "entity_id": 2260636,
                        "name": "Adam Smith IRA (786581)",
                        "grouping": "holding_account",
                        "columns": {
                            "cost_basis": 1255000.0
                        },
                        "children": [
                            {
                                "entity_id": 2260640,
                                "name": "Pershing (DMA 859658)",
                                "grouping": "holding_account",
                                "columns": {
                                    "cost_basis": 690000.0
                                },
                                "children": []
                            },
                            {
                                "name": "Directly Owned",
                                "grouping": "holding_account",
                                "columns": {
                                    "cost_basis": 565000.0
                                },
                                "children": []
                            }
                        ]
                    },
                    {
                        "entity_id": 259885,
                        "name": "Manager A",
                        "grouping": "holding_account",
                        "columns": {
                            "cost_basis": 4516070.2846626425
                        },
                        "children": [
                            {
                                "entity_id": 259825,
                                "name": "DJIA ETF 90",
                                "grouping": "holding_account",
                                "columns": {
                                    "cost_basis": 367853.25000000006
                                },
                                "children": []
                            },
                            {
                                "name": "Directly Owned",
                                "grouping": "holding_account",
                                "columns": {
                                    "cost_basis": 4148217.034662644
                                },
                                "children": []
                            }
                        ]
                    },
                    {
                        "entity_id": 260654,
                        "name": "Manager C",
                        "grouping": "holding_account",
                        "columns": {
                            "cost_basis": 3021140.808805371
                        },
                        "children": []
                    },
                    {
                        "entity_id": 259875,
                        "name": "Manager I",
                        "grouping": "holding_account",
                        "columns": {
                            "cost_basis": 679996.67
                        },
                        "children": []
                    },
                    {
                        "entity_id": 260737,
                        "name": "Manager K",
                        "grouping": "holding_account",
                        "columns": {
                            "cost_basis": 1283492.04
                        },
                        "children": []
                    },
                    {
                        "entity_id": 260740,
                        "name": "Manager M",
                        "grouping": "holding_account",
                        "columns": {
                            "cost_basis": 2379993.2
                        },
                        "children": []
                    },
                    {
                        "entity_id": 2260638,
                        "name": "Southern Trust Fixed Income SMA (600551984)",
                        "grouping": "holding_account",
                        "columns": {
                            "cost_basis": 7970190.99
                        },
                        "children": []
                    }
                ]
            }
        }
    },
    "included": []
}
```

## Arguments

Addepar uses arguments or parameters to modify the settings of a calculation. Some examples are Currency and Adjusted Value for the Value attribute.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/508e741-Adjusted_Value.png",
"Adjusted Value.png",
3104
],
"align": "center",
"sizing": "auto",
"caption": "Adjusted Value (In-App)"
}
]
}
[/block]

**Example:**

```json Request
POST https://examplefirm.addepar.com/api/v1/portfolio/query

{
  "data":{
    "type":"portfolio_query",
    "attributes":{
      "columns":[
        {
          "key":"value",
          "arguments":{
            "adjusted":true
          }
        }
      ],
      "groupings":[
        "asset_class"
      ],
      "portfolio_type":"FIRM",
      "portfolio_id":1,
      "start_date":"2020-02-01",
      "end_date":"2020-06-01"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "meta":{
    "columns":[
      {
        "key":"value",
        "display_name":"Adjusted Value (USD)",
        "output_type":"Number",
        "currency":"USD"
      }
    ],
    "groupings":[
      {
        "key":"asset_class",
        "display_name":"Asset Class"
      }
    ]
  },
  "data":{
    "type":"portfolio_views",
    "attributes":{
      "total":{
        "name":"Total",
        "columns":{
          "value":4.5070496789997244E8
        },
        "children":[
          {
            "name":"Cash & Cash Equivalent",
            "grouping":"asset_class",
            "columns":{
              "value":1.1442713893333333E7
            },
            "children":[

            ]
          },
          {
            "name":"Equity",
            "grouping":"asset_class",
            "columns":{
              "value":2.63985255006275E8
            },
            "children":[

            ]
          },
          {
            "name":"U.S. Equity",
            "grouping":"asset_class",
            "columns":{
              "value":0.0
            },
            "children":[

            ]
          },
          {
            "name":"Fixed Income",
            "grouping":"asset_class",
            "columns":{
              "value":4.555629874790781E7
            },
            "children":[

            ]
          },
          {
            "name":"Derivative",
            "grouping":"asset_class",
            "columns":{
              "value":9548725.0
            },
            "children":[

            ]
          },
          {
            "name":"Hedge Fund",
            "grouping":"asset_class",
            "columns":{
              "value":4.114859252892848E7
            },
            "children":[

            ]
          },
          {
            "name":"Private Equity",
            "grouping":"asset_class",
            "columns":{
              "value":5802100.663527796
            },
            "children":[

            ]
          },
          {
            "name":"Alternative",
            "grouping":"asset_class",
            "columns":{
              "value":2.1890773380000003E7
            },
            "children":[

            ]
          },
          {
            "name":"Real Assets",
            "grouping":"asset_class",
            "columns":{
              "value":219414.12
            },
            "children":[

            ]
          },
          {
            "name":"Unknown",
            "grouping":"asset_class",
            "columns":{
              "value":5.111109456E7
            },
            "children":[

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

## Time Arguments

Configuration options that are available for single `time_point` or multiple `time period`, time-dependent attributes, such as TWR.

**Time Point Argument Parameters:**
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/ce7127e-Time-Point_Arguments.png",
"Time-Point Arguments.png",
3104
],
"align": "center",
"sizing": "smart",
"caption": "Time-Point Arguments (In-App)"
}
]
}
[/block]
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "current (default)",
"0-1": "Current Time Point.",
"0-2": "`\"time_point\": \"current\"`",
"1-0": "P<quantity><interval> later (\\<rounding_type>)",
"1-1": "Future Time Point.",
"1-2": "`\"time_point\": \"P2M later (exact)\"`",
"2-0": "inception",
"2-1": "Inception Time Point.",
"2-2": "`\"time_point\": \"inception\"`",
"3-0": "Not supported",
"3-1": "Performance Time Point.",
"3-2": "N/A",
"4-0": "P<quantity><interval> ago (\\<rounding_type>)",
"4-1": "Relative Time Point.",
"4-2": "`\"time_point\": \"P1Q ago (ceiling)\"`",
"5-0": "starting",
"5-1": "Starting Time Point.",
"5-2": "`\"time_point\":  \"starting\"`",
"6-0": "\\<date:YYYY-MM-DD>",
"6-1": "Static Time Point.",
"6-2": "`\"time_point\": \"2019-12-31\"`",
"7-0": "P<quantity><interval> inception (\\<rounding_type>)",
"7-1": "Time Point From Inception.",
"7-2": "`\"time_point\": \"P3Y inception (floor)\"`"
},
"cols": 3,
"rows": 8,
"align": [
"left",
"left",
"left"
]
}
[/block]

**Interval & Rounding Legend:**
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/c8a58d7-Rounding_Values.png",
"Rounding Values.png",
3104
],
"align": "center",
"caption": "Rounding Values (In-App)"
}
]
}
[/block]
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/0f5ce12-Intervals.png",
"Intervals.png",
3104
],
"align": "center",
"caption": "Intervals (In-App)"
}
]
}
[/block]

<details><summary>interval values</summary>
<p>

- D (Days)
- K (Weekdays)
- W (Weeks)
- M (Months)
- Q (Quarters)
- Y (Years)

If omitted, uses defaults.

</p>
</details>

<details><summary>rounding_types values</summary>
<p>

- floor (Start)
- exact (Exact)
- ceiling (End)

</p>
</details>

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/portfolio/query

{
  "data":{
    "type":"portfolio_query",
    "attributes":{
      "columns":[
        {
          "key":"value",
          "arguments":{
            "adjusted":true,
            "time_point":"2019-12-31"
          }
        }
      ],
      "groupings":[
        {
          "key":"asset_class"
        }
      ],
      "portfolio_type":"firm",
      "portfolio_id":1,
      "start_date":"2018-06-30",
      "end_date":"2020-07-01"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "meta":{
    "columns":[
      {
        "key":"value",
        "display_name":"Adjusted Value (12/31/2019, USD)",
        "output_type":"Number",
        "currency":"USD"
      }
    ],
    "groupings":[
      {
        "key":"asset_class",
        "display_name":"Asset Class"
      }
    ]
  },
  "data":{
    "type":"portfolio_views",
    "attributes":{
      "total":{
        "name":"Total",
        "columns":{
          "value":4.519257871178911E8
        },
        "children":[
          {
            "name":"Cash & Cash Equivalent",
            "grouping":"asset_class",
            "columns":{
              "value":1.212095901E7
            },
            "children":[

            ]
          },
          {
            "name":"Equity",
            "grouping":"asset_class",
            "columns":{
              "value":2.6726534756527504E8
            },
            "children":[

            ]
          },
          {
            "name":"U.S. Equity",
            "grouping":"asset_class",
            "columns":{
              "value":0.0
            },
            "children":[

            ]
          },
          {
            "name":"Fixed Income",
            "grouping":"asset_class",
            "columns":{
              "value":4.367422731923816E7
            },
            "children":[

            ]
          },
          {
            "name":"Derivative",
            "grouping":"asset_class",
            "columns":{
              "value":8647625.0
            },
            "children":[

            ]
          },
          {
            "name":"Hedge Fund",
            "grouping":"asset_class",
            "columns":{
              "value":4.114859252892848E7
            },
            "children":[

            ]
          },
          {
            "name":"Private Equity",
            "grouping":"asset_class",
            "columns":{
              "value":5857038.349449425
            },
            "children":[

            ]
          },
          {
            "name":"Alternative",
            "grouping":"asset_class",
            "columns":{
              "value":2.189076738E7
            },
            "children":[

            ]
          },
          {
            "name":"Real Assets",
            "grouping":"asset_class",
            "columns":{
              "value":210135.405
            },
            "children":[

            ]
          },
          {
            "name":"Unknown",
            "grouping":"asset_class",
            "columns":{
              "value":5.111109456E7
            },
            "children":[

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

**Time Period Argument Parameters:**
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/7d3069c-Time_Period.png",
"Time Period.png",
3104
],
"align": "center",
"caption": "Time Period (In-App)"
}
]
}
[/block]
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "current (default)",
"0-1": "Current Time Period.",
"0-2": "`\"period\": \"current\"`",
"1-0": "\\<time_point> to \\<time_point>",
"1-1": "Custom Time Period.",
"1-2": "`\"period\": \"P2M ago (exact) to 2020-06-30\"`",
"2-0": "inception to start",
"2-1": "Inception to Current Start Date.",
"2-2": "`\"period\": \"inception to start\"`",
"3-0": "relative P<quantity><interval>",
"3-1": "Relative Time Period.",
"3-2": "`\"period\": \"relative P5Y\"`",
"4-0": "since inception",
"4-1": "Since Inception Time Period.",
"4-2": "`\"period\": \"since inception\"`",
"5-0": "\\<date:YYYY-MM-DD> to \\<date:YYYY-MM-DD>",
"5-1": "Static Time Period.",
"5-2": "`\"period\": \"2019-12-31 to 2020-03-31\"`",
"6-0": "trailing P<quantity><interval>",
"6-1": "Trailing Time Period.",
"6-2": "`\"period\": \"trailing P5Y\"`"
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

**Interval & Rounding Legend:**

<details><summary>interval values</summary>
<p>

- D (Days)
- K (Weekdays)
- W (Weeks)
- M (Months)
- Q (Quarters)
- Y (Years)

If omitted, uses defaults.

</p>
</details>

<details><summary>rounding_types values</summary>
<p>

- floor (Start)
- exact (Exact)
- ceiling (End)

</p>
</details>

<details><summary>time_point values</summary>
<p>

- Any formulation of time point arguments above.

</p>
</details>

**Example:**

```curl REQUEST
POST https://examplefirm.addepar.com/api/v1/portfolio/query

{
  "data":{
    "type":"portfolio_query",
    "attributes":{
      "columns":[
        {
          "key":"time_weighted_return",
          "arguments":{
            "period":"trailing P5Y"
          }
        }
      ],
      "groupings":[
        {
          "key":"asset_class"
        }
      ],
      "portfolio_type":"FIRM",
      "portfolio_id":1,
      "start_date":"2018-06-30",
      "end_date":"2018-09-30"
    }
  }
}
```

```json RESPONSE
HTTP/1.1 200

{
  "meta":{
    "columns":[
      {
        "key":"time_weighted_return",
        "display_name":"5 Yr. TWR (USD)",
        "output_type":"Percent",
        "currency":"USD"
      }
    ],
    "groupings":[
      {
        "key":"asset_class",
        "display_name":"Asset Class"
      }
    ]
  },
  "data":{
    "type":"portfolio_views",
    "attributes":{
      "total":{
        "name":"Total",
        "columns":{
          "time_weighted_return":0.6001516639410265
        },
        "children":[
          {
            "name":"Cash & Cash Equivalent",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":-0.09253003508289892
            },
            "children":[

            ]
          },
          {
            "name":"Equity",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":0.09482032818914576
            },
            "children":[

            ]
          },
          {
            "name":"U.S. Equity",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":0.010000000000000009
            },
            "children":[

            ]
          },
          {
            "name":"Fixed Income",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":-0.035795553494806676
            },
            "children":[

            ]
          },
          {
            "name":"Derivative",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":2.325451087920276
            },
            "children":[

            ]
          },
          {
            "name":"Hedge Fund",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":-0.16028249805399108
            },
            "children":[

            ]
          },
          {
            "name":"Private Equity",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":0.1584577889571086
            },
            "children":[

            ]
          },
          {
            "name":"Alternative",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":1.8333800108804938
            },
            "children":[

            ]
          },
          {
            "name":"Real Assets",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":-0.23312214337687043
            },
            "children":[

            ]
          },
          {
            "name":"Unknown",
            "grouping":"asset_class",
            "columns":{
              "time_weighted_return":745.1347086793872
            },
            "children":[

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
