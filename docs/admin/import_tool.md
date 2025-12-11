# Import Tool (beta)

Importing data is helpful when onboarding a new client portfolio or managing any data that's not available via a portfolio data feed.

You can programmatically automate all data import workflows with the Import Tool API. All existing and future import types are supported.

> 📘 The Import Tool API is in closed beta
>
> The ability to use the Import Tool API described herein is available only to a pre-selected group of Addepar clients within the Addepar Beta Program. All beta features described herein are provided “as is'” and “as available” with no warranty or guarantee of functionality and may be modified or removed at any time by Addepar.
> [block:image]
> {
> "images": [

    {
      "image": [
        "https://files.readme.io/6ca2aa249b0e7c94c1094df46f73c2c28f8254b071c54b5d703ee5f5fbb583b3-import_fro_api_doc.png",
        null,
        ""
      ],
      "align": "center"
    }

]
}
[/block]
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/imports \n/v1/import_results",
"1-0": "Endpoints",
"1-1": "**POST** \n/v1/imports \n \n**DELETE** \n/v1/imports \n \n**GET** \n/v1/imports/:id \n/v1/import_results/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "No",
"4-0": "Application \npermissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n“Import Tool (In-app): Access to in-app tool” \n \n\"Portfolio Access\" determines the entities that are accessible. \n \nAdditional required permissions will vary based on import type. \nDetails can be found [in the Help Center](https://help.addepar.com/hc/en-us/articles/360042571933-About-importing-data).",
"5-0": "OAuth scopes",
"5-1": "None"
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

The payload must follow the same CSV format as when importing data in the Addepar app. For detailed information on each import type and their required columns, [learn more in the Help Center](https://help.addepar.com/hc/en-us/articles/360042571933-About-importing-data).

**Status**

| Status                                   | Description                                                        |
| :--------------------------------------- | :----------------------------------------------------------------- |
| `IN_QUEUE`                               | The data is in the queue.                                          |
| `VALIDATING`                             | The uploaded data is being checked for errors and inconsistencies. |
| `IMPORTING`                              | The validated data is being imported.                              |
| `ERRORS_READY_FOR_REVIEW`                | Errors were found; review is required.                             |
| `WARNINGS_READY_FOR_REVIEW`              | Warnings were detected; review is recommended but not mandatory.   |
| `ERRORS_AND_WARNINGS  _READY_FOR_REVIEW` | Both errors and warnings were found; review is required.           |
| `DRY_RUN_SUCCESSFUL`                     | Dry run has been completed and no errors were found.               |
| `IMPORT_SUCCESSFUL`                      | The data imported successfully.                                    |
| `VALIDATION_FAILED`                      | Validation was unsuccessful due to unknown error.                  |
| `IMPORT_FAILED`                          | Import was unsuccessful due to unknown error.                      |

## Required parameters

There are 3 parameters that you must specify with the`POST` and `DELETE`call.

1. `import_type`
2. `is_dry_run`
3. `ignore_warnings`

### 1. Import type parameter

All possible import type routes for the`POST` call are listed below. They are case-sensitive and must be in all caps.

/v1/imports?import_type=`IMPORT_TYPE`
[block:parameters]
{
"data": {
"h-0": "Import type",
"h-1": "Description",
"0-0": "`ATTRIBUTES`",
"0-1": "Import static, multi-value and historical attribute values onto entities and positions. More details [here](https://help.addepar.com/hc/en-us/articles/13482127536663-Import-attribute-values-in-app).",
"1-0": "`BENCHMARKS`",
"1-1": "Import custom benchmarks and benchmark returns. \nMore details [here](https://help.addepar.com/hc/en-us/articles/4403876639383-Import-benchmarks-in-app).",
"2-0": "`BENCHMARK_ASSOCIATIONS`",
"2-1": "Update benchmark associations. \nMore details [here](https://help.addepar.com/hc/en-us/articles/19458557809943-Import-benchmark-associations-in-app).",
"3-0": "`CONTACTS`",
"3-1": "Create or update contacts. \nMore details [here](https://help.addepar.com/hc/en-us/articles/19363861092887).",
"4-0": "`COST_BASIS`",
"4-1": "Add or update original and/or adjusted tax lot values for share-based assets. \nMore details [here](https://help.addepar.com/hc/en-us/articles/18336597937559-Import-cost-basis-in-app).",
"5-0": "`ESTIMATED_RETURNS`",
"5-1": "Import estimated returns to existing value-based assets. \nMore details [here](https://help.addepar.com/hc/en-us/articles/17534691567511).",
"6-0": "`GROUPS`",
"6-1": "Create groups, add group members, or delete group members. \nMore details [here](https://help.addepar.com/hc/en-us/articles/18337465584151).",
"7-0": "`HISTORICAL_PRICES`",
"7-1": "Import historical prices for share-based assets. \nMore details [here](https://help.addepar.com/hc/en-us/articles/17534612781719).",
"8-0": "`MANAGE_INVESTMENTS`",
"8-1": "Create new investments and/or update attributes on existing investments. \nMore details [here](https://help.addepar.com/hc/en-us/articles/13762554895767-Import-investments-in-app-beta-).",
"9-0": "`MANAGE_OWNERSHIP`",
"9-1": "Create new ownership entities and set up ownership structure. \nMore details [here](https://help.addepar.com/hc/en-us/articles/15169886580375-Import-an-ownership-structure-in-app-beta-).",
"10-0": "`MANUAL_ADJUSTMENTS`",
"10-1": "Apply fee adjustments to bills. \nMore details [here](https://help.addepar.com/hc/en-us/articles/9909572131351-Import-Billing-fee-adjustments-in-app-beta-).",
"11-0": "`CONSTITUENTS`",
"11-1": "Import ETF constituent data. \nMore details [here](https://help.addepar.com/hc/en-us/articles/23378019395735).",
"12-0": "`POSITION_VALUATIONS`",
"12-1": "Add or update valuations of value-based assets, as well as snapshots for share-based assets. \nMore details [here](https://help.addepar.com/hc/en-us/articles/4405081688599-Import-valuations-and-snapshots-in-app-beta-).",
"13-0": "`SUMMARY_DATA`",
"13-1": "Add or update historical performance data. \nMore details [here](https://help.addepar.com/hc/en-us/articles/19363793393303).",
"14-0": "`TARGET_ALLOCATIONS`",
"14-1": "Create target allocation models and create, edit, and/or assign target allocations to entities or groups. \nMore details [here](https://help.addepar.com/hc/en-us/articles/17534696661655).",
"15-0": "`TOTAL_OUTSTANDING_SHARES`",
"15-1": "Add total outstanding shares for existing share based managed funds. \nMore details [here](https://help.addepar.com/hc/en-us/articles/22548114743575-Import-total-outstanding-shares-in-app).",
"16-0": "`TRANSACTIONS`",
"16-1": "Create and/or update transactions. \nMore details [here](https://help.addepar.com/hc/en-us/articles/14166182309015-Import-transactions-in-app-beta-).",
"17-0": "`VALUES_AND_FLOWS`",
"17-1": "Link a segment of historical performance data with online data. \nMore details [here](https://help.addepar.com/hc/en-us/articles/21014322234263-Import-values-and-flows-internal-only)."
},
"cols": 2,
"rows": 18,
"align": [
"left",
"left"
]
}
[/block]

All possible import type routes for the`DELETE` call are listed below. They are case-sensitive and must be in all caps.
[block:parameters]
{
"data": {
"h-0": "Import type",
"h-1": "Description",
"0-0": "`DELETE_TRANSACTIONS`",
"0-1": "Delete transactions in bulk. \nMore details [here](https://help.addepar.com/hc/en-us/articles/32099518551063-Delete-transactions-via-import)."
},
"cols": 2,
"rows": 1,
"align": [
"left",
"left"
]
}
[/block]

### 2. Dry run parameter

/v1/imports?is_dry_run=`true`

When set to true, the parameter allows you to simulate the import and review the results, errors, and warnings without making any actual changes to Addepar.

### 3. Ignore warnings parameter

/v1/imports?ignore_warnings=`true`

This parameter determines how warnings are handled during the import process. When set to true, the import will proceed even if warnings are encountered. Errors cannot be ignored and must be addressed before import can be complete.

## Import data

Imports data for one import type.

Provide the payload in plain text format.

\*\*POST \*\* `/v1/imports`

**Example:**

```Text Request
POST https://examplefirm.addepar.com/api/v1/imports?import_type=ATTRIBUTES&is_dry_run=false&ignore_warnings=true

Owned Id, Asset Class
123, Equity
```

```json Response
{
  "data": {
    "id": "86e53d26-d69b-4590-aa61-c94cf7755d57",
    "type": "imports",
    "attributes": {
      "status": "UPLOADING"
    },
    "links": {
      "self": "/v1/imports/"
    }
  },
  "included": []
}
```

**Response codes**

- `200 OK`: Success. Returns json with import id.
- `400 Bad Request`: Incorrect Formatting.
- `400 Bad Request`: Missing or incorrectly formatted parameters.
- `400 Bad Request`: Payload size exceeded 20 MB.

## Delete data

Deletes data for one import type.

Provide the payload in plain text format.

\*\*DELETE \*\* `/v1/imports`

**Example:**

```Text Request
DELETE https://examplefirm.addepar.com/api/v1/imports?import_type=DELETE_TRANSACTIONS&is_dry_run=false&ignore_warnings=true

Vendor ID, Transaction ID
6583b5a4-314d-4281-a84b-85c935846d0d,
```

```json Response
{
  "data": {
    "id": "1602da11-db76-4cc0-b3c0-54e81b33df50",
    "type": "imports",
    "attributes": {
      "status": "IN_QUEUE"
    },
    "links": {
      "self": "/v1/imports/1602da11-db76-4cc0-b3c0-54e81b33df50"
    }
  },
  "included": []
}
```

**Response codes**

- `200 OK`: Success. Returns json with import id.
- `400 Bad Request`: Incorrect Formatting.
- `400 Bad Request`: Missing or incorrectly formatted parameters.
- `400 Bad Request`: Payload size exceeded 20 MB.

## Get import status

Check an import's status by its ID.

**GET** `/v1/imports/:id`

```Text Request
GET https://examplefirm.addepar.com/api/v1/imports/86e53d26-d69b-4590-aa61-c94cf7755d57
```

```json Response
{
  "data": {
    "id": "86e53d26-d69b-4590-aa61-c94cf7755d57",
    "type": "imports",
    "attributes": {
      "status": "IMPORT_SUCCESSFUL"
    },
    "links": {
      "self": "/v1/imports/"
    }
  },
  "included": []
}
```

**Response codes**

- `200 OK`: Success.
- `404 Not Found`: Import ID not found.
- `404 Not Found`: User does not have permission to view import information.

## Get import results

See information about an import's results with digests, warnings, and errors.

- `digests`: A summary of everything that will be created or updated. Digests are only shown when there are no errors.
- `warnings`: A list of warnings encountered during the validation process broken down by row, column, or table based on the type of warning.
- `errors`: A list of errors encountered during the validation process broken down by row, column, or table based on the type of error.

**GET** `/v1/import_results/:id`

```Text Request
GET https://examplefirm.addepar.com/api/v1/import_results/86e53d26-d69b-4590-aa61-c94cf7755d57
```

```json No errors
{
  "data": {
    "id": "86e53d26-d69b-4590-aa61-c94cf7755d57",
    "type": "import_results",
    "attributes": {
      "digests": ["1 attribute will be created"]
    },
    "links": {
      "self": "/v1/import_results/86e53d26-d69b-4590-aa61-c94cf7755d57"
    }
  },
  "included": []
}
```

```json Error response
{
  "data": {
    "id": "86e53d26-d69b-4590-aa61-c94cf7755d57",
    "type": "import_results",
    "attributes": {
      "warnings": [
        {
          "message": "attribute value: column not recognized and will be ignored.",
          "type": "COLUMN",
          "affected_members": ["Column D"]
        },
        {
          "message": "attribute name: column not recognized and will be ignored.",
          "type": "COLUMN",
          "affected_members": ["Column C"]
        }
      ],
      "errors": [
        {
          "message": "Missing required field: Date.",
          "type": "COLUMN",
          "affected_members": ["Column null"]
        },
        {
          "message": "Missing required field: Type.",
          "type": "COLUMN",
          "affected_members": ["Column null"]
        }
      ]
    },
    "links": {
      "self": "/v1/import_results/86e53d26-d69b-4590-aa61-c94cf7755d57"
    }
  },
  "included": []
}
```

**Response codes**

- `200 OK`: Success.
- `404 Not Found`: Import ID not found.
- `404 Not Found`: User does not have permission to view import information.
