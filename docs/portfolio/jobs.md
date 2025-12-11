# Jobs

The Jobs API allows you to export large sets of analysis data asynchronously and download the results any time within 24 hours of the initial request. This is useful for protection from long-running requests that may be impacted by unreliable networks.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"0-1": "/v1/jobs",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/jobs \n/v1/jobs/:id \n/v1/jobs/:id/download \n \n**POST** \n/v1/jobs \n \n**DELETE** \n/v1/jobs/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" and access to view the portfolio data requested.",
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

## Resource overview

The Jobs API returns a resource object described by the below attributes, including the status, errors, and any Portfolio API parameters used in the job. Asynchronous job requests can be made for both the Portfolio Query and View APIs.

All attributes will be returned in successful **GET** & **POST** responses.

| Attribute          | Description                                                                    | Example                    |
| :----------------- | :----------------------------------------------------------------------------- | :------------------------- |
| `job_type`         | Type of job. String. Required.                                                 | `"portfolio_view_results"` |
| `started_at`       | The start time of the job in UTC. String. ISO 8601 date format.                | `"2020-04-15T21:30:16Z"`   |
| `completed_at`     | The completed time of the job in UTC. String. ISO 8601 date format.            | `"2020-04-15T21:30:17Z"`   |
| `percent_complete` | Percentage complete. Number.                                                   | `1.0`                      |
| `status`           | The current status of the job. String.                                         | See "Status" below.        |
| `errors`           | Errors that occurred running the job. Object.                                  | See "Errors" below.        |
| `parameters`       | The parameters required to create the type of job specified. Array of Objects. | See "Parameters" below.    |

**Status**

| Status                               | Description                                                                                                  |
| :----------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| `Queued`                             | Job has not yet been processed by Addepar servers.                                                           |
| `In Progress - Waiting For Capacity` | Job has been placed back in queue because there is no available capacity.                                    |
| `In Progress`                        | Job is currently being processed by Addepar servers.                                                         |
| `Picked Up By Job Runner`            | Job has been picked up by the server and is waiting to run.                                                  |
| `Completed`                          | Job has finished processing. Results can be retrieved from the URL in the Location header.                   |
| `Canceled`                           | Job was canceled by the user.                                                                                |
| `Timed Out`                          | Job results have expired and results have been deleted. Results are deleted 24 hours after a job is created. |
| `Failed`                             | Job processing failed due to a server issue. Error details are unavailable.                                  |
| `Rejected`                           | Job exceeds the maximum quota of the queue.                                                                  |
| `Error Cancelled`                    | Job canceled due to an error. Details are provided within the error field of the response.                   |
| `Cancel Requested`                   | Job in progress and has received a request to cancel.                                                        |
| `User Cancelled`                     | Job canceled.                                                                                                |

**Errors**

| Parameter | Description        | Example                          |
| :-------- | :----------------- | :------------------------------- |
| `status`  | HTTP status code.  | `"400"`                          |
| `title`   | HTTP status title. | `"Bad Request"`                  |
| `detail`  | Error details.     | `"Invalid portfolio: ENTITY 10"` |

## Relationships

| Relationship | Description                   |
| :----------- | :---------------------------- |
| `creator`    | The user who created the job. |

```json Relationships
"relationships":{
  "creator":{
    "links":{
      "self":"/v1/jobs/2/relationships/creator",
      "related":"/v1/jobs/2/creator"
    },
    "data":{
      "type":"users",
      "id":"22"
    }
  }
}
```

## Parameters

Required parameters are specified for portfolio view and query jobs within each description.
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "`portfolio_type`",
"0-1": "Required for portfolio view and portfolio query jobs. \n \nSupported types: \n \n- `ENTITY`\n- `ENTITY_FUNDS`\n- `GROUP`\n- `GROUP_FUNDS`\n- `FIRM`\n- `FIRM_ACCOUNTS`\n- `FIRM_CLIENTS`\n- `FIRM_HOUSEHOLDS`\n- `FIRM_UNVERIFIED_ACCOUNTS`",
"0-2": "`entity`",
"1-0": "`portfolio_id`",
"1-1": "Required for portfolio view and portfolio query jobs. \n \nPortfolio IDs can be configured in Addepar. IDs can represent one entity or a group of entities (query jobs only). \n \nIf the `portfolio_type` is `FIRM`, the `portfolio_id` must be `1.`",
"1-2": "`1`",
"2-0": "`view_id`",
"2-1": "Required for portfolio view jobs. \n \nID of the portfolio view.",
"2-2": "`12`",
"3-0": "`output_type`",
"3-1": "Required for portfolio view jobs. \n \nThe output format of the exported result. \n \nSupported types: \n-`CSV` \n-`TSV` \n-`XLSX`",
"3-2": "`csv`",
"4-0": "`start_date`",
"4-1": "Required for portfolio view and portfolio query jobs. \n \nThe start date of the time period of portfolio data. \"YYYY-MM-DD.\"",
"4-2": "`2016-01-01`",
"5-0": "`end_date`",
"5-1": "Required for portfolio view and portfolio query jobs. \n \nThe end date of the time period of portfolio data. \"YYYY-MM-DD.\"",
"5-2": "`2016-02-02`",
"6-0": "`columns`",
"6-1": "Required for portfolio query jobs. \n \nSee [Attributes](https://developers.addepar.com/docs/attributes) to discover supported attributes. \n \nSee [Arguments](https://developers.addepar.com/docs/arguments) to discover supported attribute arguments.",
"6-2": "`[{\"key\": \"time_weighted_return\"}]`",
"7-0": "`groupings`",
"7-1": "Required for portfolio query jobs. \n \nList of grouping attribute keys with optional arguments. Array of Objects. \n \nOmitted arguments will use default values. \n \nSee [Attributes](https://developers.addepar.com/docs/attributes) to discover supported attributes. \n \nSee [Arguments](https://developers.addepar.com/docs/arguments) to discover supported attribute arguments.",
"7-2": "`[{\"key\": \"asset_class\"}]`",
"8-0": "`filters`",
"8-1": "Optional for portfolio query jobs. \n \nFilters rows from the result. Array of Objects. \n \nTo learn more, reference the[ Filter Object](https://developers.addepar.com/docs/portfolio-query) within Portfolio Query Jobs.",
"8-2": "`[{\"attribute\": \"asset_class\", \"type\": \"discrete\", \"operator\": \"include\", \"values\": [\"Equity\", \"Fixed Income\"]}`",
"9-0": "`hide_previous_holdings `",
"9-1": "Optional for portfolio query jobs. \n \nSet to true to exclude holdings not held at end of current period. Boolean. (default: false)",
"9-2": "`false`"
},
"cols": 3,
"rows": 10,
"align": [
"left",
"left",
"left"
]
}
[/block]

## Create a portfolio view job

Creates an asynchronous job to extract portfolio data for a saved view in Addepar.

> 📘 Note
>
> Each job has a timeout limit of 4 hours.

**POST** `/v1/jobs`

**Example:**

```json Request
POST https://examplefirm.com/api/v1/jobs?useStringId=true

{
  "data":{
    "type":"jobs",
    "attributes":{
      "job_type":"portfolio_view_results",
      "parameters":{
        "view_id":"2",
        "portfolio_type":"entity",
        "portfolio_id":"22",
        "output_type":"json",
        "start_date":"2011-12-31",
        "end_date":"2013-01-15"
      }
    }
  }
}
```

```json Response
HTTP/1.1 202 Accepted

{
  "data":{
    "id":"b6c1b9da-4387-11ef-8636-dd826f8aeed1a",
    "type":"jobs",
    "attributes":{
      "job_type":"portfolio_view_results",
      "parameters":{
        "view_id":2,
        "portfolio_type":"entity",
        "portfolio_id":"22",
        "output_type":"json",
        "start_date":"2011-12-31",
        "end_date":"2013-01-15"
      },
      "status":"Queued"
    },
    "relationships":{
      "creator":{
        "links":{
          "self":"/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a/relationships/creator",
          "related":"/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a/creator"
        },
        "data":{
          "type":"users",
          "id":"44"
        }
      }
    },
    "links":{
      "self":"/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a"
    }
  }
}
```

**Response codes:**

- `202 Accepted`: Success. Returns JSON with created job information.
- `400 Bad Request`: Bad JSON: API format, missing parameters or badly formatted parameters
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Create a portfolio query job

Creates an asynchronous job to extract portfolio data with a query.

**POST** `/v1/jobs`

**Example:**

```json Request
POST https://examplefirm.com/api/v1/jobs

{
  "data":{
    "type":"job",
    "attributes":{
      "job_type":"PORTFOLIO_QUERY",
      "parameters":{
        "columns":[
          {
            "key":"value"
          },
          {
            "key":"value",
            "arguments":{
              "time_point":"2018-12-31"
            }
          },
          {
            "key":"time_weighted_return",
            "arguments":{
              "period":"2019-12-31 to 2020-03-31"
            }
          }
        ],
        "groupings":[
          {
            "key":"asset_class"
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
          }
        ],
        "portfolio_type":"entity",
        "portfolio_id":[
          22
        ],
        "start_date":"2020-02-18",
        "end_date":"2020-03-18"
      }
    }
  }
}
```

```json Response
HTTP/1.1 202 Accepted

{
  "data": {
    "id": "b6c1b9da-4387-11ef-8636-dd826f8aeed1a",
    "type": "jobs",
    "attributes": {
      "job_type": "PORTFOLIO_QUERY",
      "parameters": {
        "columns": [{
            "key": "value",
            "arguments": {}
          },
          {
            "key": "value",
            "arguments": {
              "time_point": "2018-12-31"
            }
          },
          {
            "key": "time_weighted_return",
            "arguments": {
              "period": "2019-12-31 to 2020-03-31"
            }
          }
        ],
        "groupings": [{
          "key": "asset_class",
          "arguments": {}
        }],
        "filters": [{
          "attribute": {
            "key": "asset_class",
            "arguments": {}
          },
          "type": "discrete",
          "operator": "include",
          "values": [
            "Equity",
            "Fixed Income"
          ]
        }],
        "portfolio_type": "entity",
        "portfolio_id": [
          22
        ],
        "start_date": "2020-02-18",
        "end_date": "2020-03-18",
        "hide_previous_holdings": false
      },
      "percent_complete": 0.0,
      "status": "Queued"
    },
    "relationships": {
      "creator": {
        "links": {
          "self": "/v1/jobs/7/relationships/creator",
          "related": "/v1/jobs/7/creator"
        },
        "data": {
          "type": "users",
          "id": "22"
        }
      }
    },
    "links": {
      "self": "/v1/jobs/7"
    }
  },
  "included": []
}
```

**Response codes:**

- `202 Accepted`: Success. Returns JSON with created job information.
- `400 Bad Request`: Bad JSON: API format, missing or badly formatted parameters
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Check a job's status

Retrieves the status and parameters for a specific job.

**GET** `/v1/jobs/:id`

**Example:**

```json Request
GET https://examplefirm.com/api/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"b6c1b9da-4387-11ef-8636-dd826f8aeed1a",
    "type":"jobs",
    "attributes":{
      "job_type":"portfolio_view_results",
      "completed_at":"2020-04-03T15:15:28Z",
      "started_at":"2020-04-03T15:15:28Z",
      "parameters":{
        "view_id":"2",
        "portfolio_type":"entity",
        "portfolio_id":"22",
        "output_type":"json",
        "start_date":"2011-12-31",
        "end_date":"2013-01-15"
      },
      "status":"Completed"
    },
    "relationships":{
      "creator":{
        "links":{
          "self":"/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a/relationships/creator",
          "related":"/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a/creator"
        },
        "data":{
          "type":"users",
          "id":"44"
        }
      }
    },
    "links":{
      "self":"/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a"
    }
  }
}
```

**Response codes:**

- `200 OK`: Success
- `404 Not Found`: Unable to locate the job with the given id, or user does not have permission to view the given job
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Download a job's results

Returns the results of the given job.

> 📘 Note
>
> Job results are deleted 24 hours after a job is created.

**GET** `/v1/jobs/:id/download`

**Example:**

```curl Request
GET https://examplefirm.com/api/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a/download
```

```json Response
HTTP/1.1 200

Content-Disposition: attachment; file name="portfolio_data.json"
Content-Type: application/vnd.api+json

<DOWNLOAD_CONTENT>
```

**Response codes:**

- `200 OK`: Success. Returns a JSON, CSV, TSV or XLSX as requested.
- `303 See Other`: Completed asynchronous job. Follow the link in the "Location" header to retrieve the results.
- `404 Not Found`: Job has not completed or does not return any results
- `410 Gone`: Results have expired.

## Check the status of all jobs

Retrieves the status and parameters of all jobs.

**GET** `/v1/jobs`

**Example:**

```curl Request
GET https://examplefirm.com/api/v1/jobs
```

```json Response
HTTP/1.1 200

{
  "data":[
    {
      "id":"b6c1b9da-4387-11ef-8636-dd826f8aeed1a",
      "type":"jobs",
      "attributes":{
        "job_type":"portfolio_view_results",
        "completed_at":"2020-04-02T21:49:16Z",
        "started_at":"2020-04-02T21:4915Z",
        "parameters":{
          "view_id":"2",
          "portfolio_type":"entity",
          "portfolio_id":"22",
          "output_type":"json",
          "start_date":"2011-12-31",
          "end_date":"2013-01-15"
        },
        "status":"Completed"
      },
      "links":{
        "self":"/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1a"
      }
    },
    {
      "id":"b6c1b9da-4387-11ef-8636-dd826f8aeed1b",
      "type":"jobs",
      "attributes":{
        "job_type":"portfolio_view_results",
        "completed_at":"2020-04-03T15:15:28Z",
        "started_at":"2020-04-03T15:15:28Z",
        "parameters":{
          "view_id":"3",
          "portfolio_type":"entity",
          "portfolio_id":"10",
          "output_type":"csv",
          "start_date":"2016-01-01",
          "end_date":"2016-01-02"
        },
        "errors":[
          {
            "status":"400",
            "title":"Bad Request",
            "detail":"Invalid portfolio: ENTITY 10"
          }
        ],
        "status":"Error"
      },
      "links":{
        "self":"/v1/jobs/b6c1b9da-4387-11ef-8636-dd826f8aeed1b"
      }
    }
  ],
  "links":{
    "next":null
  }
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Cancel a job

Cancel a job that is has yet to start, is running, or already completed.

**DELETE** `/v1/jobs/:id`

When canceling a job with the status:

- `waiting_for_capacity` the job will not run. Status change: `user_canceled`.
- `in_progress` a request to cancel is submitted. Status change:`cancel_requested`, then `user_canceled`.
- `completed` the results are archived. Status change: `user_canceled`.

**Example**

```json Request
DELETE https://examplefirm.com/api/v1/jobs/:b6c1b9da-4387-11ef-8636-dd826f8aeed1a
```

```json Response
204 No Content
```

**Response codes:**

- `204 No Content`: Success. Cancel request submitted.
- `404 Not Found`: Cannot locate the job with the given ID, or you don't have permission to view the job.
