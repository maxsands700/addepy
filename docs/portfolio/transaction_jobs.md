# Transaction Jobs

The Transaction Jobs API allows you to export large sets of transaction data asynchronously and download the results any time within 24 hours of the initial request. This is useful for protection from long-running requests that may be impacted by unreliable networks.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"0-1": "/v1/transaction_jobs",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/transaction_jobs \n/v1/transaction_jobs/:id \n/v1/transaction_jobs/:id/download \n \n**POST** \n/v1/transaction_jobs \n \n**DELETE** \n/v1/transaction_jobs/:id",
"2-0": "Produces",
"2-1": "JSON (query only), CSV (views only), TSV (views only), or XLSX (views only)",
"3-0": "Pagination",
"3-1": "No",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" and access to view the transaction data requested.",
"5-0": "OAuth Scopes",
"5-1": "`TRANSACTIONS_READ`"
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

The Transaction Jobs API returns a resource object described by the below attributes, including the status, errors, and any Transaction Query/View API parameters used in the job. Asynchronous job requests can be made for both the Transaction Query and View APIs.

All attributes will be returned in successful **GET** & **POST** responses.

| Attribute          | Description                                                         | Example                      |
| :----------------- | :------------------------------------------------------------------ | :--------------------------- |
| `job_type`         | Type of job. String. Required.                                      | `"transaction_view_results"` |
| `started_at`       | The start time of the job in UTC. String. ISO 8601 date format.     | `"2020-04-15T21:30:16Z"`     |
| `completed_at`     | The completed time of the job in UTC. String. ISO 8601 date format. | `"2020-04-15T21:30:17Z"`     |
| `percent_complete` | Percentage complete. Number.                                        | `1.0`                        |
| `status`           | The current status of the job. String.                              | See "Status" below.          |
| `errors`           | Errors that occurred running the job. Object.                       | See "Errors" below.          |

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
"0-1": "Required for transaction view and transaction query jobs. \n \nSupported types: \n-`ENTITY` \n-`GROUP` \n-`FIRM` \n \nThe type of portfolio.",
"0-2": "`entity`",
"1-0": "`portfolio_id`",
"1-1": "Required for transaction view and transaction query jobs. \n \nPortfolio IDs can be configured in Addepar. IDs can represent one entity or a group of entities (query jobs only). \n \nIf the `portfolio_type` is `FIRM`, the `portfolio_id` must be `1.`",
"1-2": "`1`",
"2-0": "`view_id`",
"2-1": "Required for transaction view jobs. \n \nID of the transaction view.",
"2-2": "`123`",
"3-0": "`output_type`",
"3-1": "Required for transaction view jobs. \n \nThe output format of the exported result. \n \nSupported types: \n-`CSV` \n-`TSV` \n-`XLSX`",
"3-2": "`csv`",
"4-0": "`start_date`",
"4-1": "Required for transaction view and transaction query jobs. \n \nThe start date of the time period of portfolio data. \"YYYY-MM-DD.\"",
"4-2": "`2016-01-01`",
"5-0": "`end_date`",
"5-1": "Required for transaction view and transaction query jobs. \n \nThe end date of the time period of portfolio data. \"YYYY-MM-DD.\"",
"5-2": "`2016-02-02`",
"6-0": "`columns`",
"6-1": "Required for transaction query jobs. \n \nList of column attribute keys. [String].",
"6-2": "`[\"trade_date\", \"security\"]`",
"7-0": "`filters`",
"7-1": "Optional for portfolio query jobs. \n \nFilters rows from the result. Array of Objects. \n \nTo learn more, reference the[ Filter Object](https://developers.addepar.com/docs/transactions-query#filter-object) within Transaction Query Jobs.",
"7-2": "`[{\"attribute\": \"asset_class\", \"type\": \"discrete\", \"operator\": \"include\", \"values\": [\"Equity\", \"Fixed Income\"]}`",
"8-0": "`sortings`",
"8-1": "A transactions query sorting may be attached to a transactions query to sort rows. Accepts up to 3 columns to sort by. Array of objects. \n \nDefault to trade date.",
"8-2": "`[{ \"attribute\": \"trade_date\", \"ascending\": false }]`",
"9-0": "`limit`",
"9-1": "The max number of transactions returned by the query. Number. \n \nDefaults to 1,048,576 for XLSX output type, no limit for other types.",
"9-2": "`500`",
"10-0": "`include_online_valuations`",
"10-1": "Whether online snapshots should be returned by the query. Boolean. \n \nDefault to false.",
"10-2": "`true`",
"11-0": "`include_unverified`",
"11-1": "Whether unverified transactions should be returned by the query. Boolean. \n \nDefault to false.",
"11-2": "`true`",
"12-0": "`include_deleted`",
"12-1": "Whether deleted online transactions should be returned by the query. Boolean. \n \nDefault to false.",
"12-2": "`true`"
},
"cols": 3,
"rows": 13,
"align": [
"left",
"left",
"left"
]
}
[/block]

## Create a transaction view job

Creates an asynchronous job to extract transaction data for a saved transaction view in Addepar.

> 📘 Note
>
> Each job has a timeout limit of 4 hours.

**POST** `/v1/transaction_jobs`

**Example:**

```json Request
POST https://examplefirm.com/api/v1/transaction_jobs

{
    "data": {
        "type": "transaction_jobs",
        "attributes": {
            "job_type": "transaction_view_results",
            "parameters": {
                "view_id": 5,
                "portfolio_id": 193,
                "portfolio_type": "entity",
                "output_type": "xlsx",
                "start_date": "2024-01-01",
                "end_date": "2024-06-30"
            }
        }
    }
}
```

```json Response
HTTP/1.1 202 Accepted

{
    "data": {
        "id": "47d7e547-7f5a-11ef-8162-dde0088e926a",
        "type": "transaction_jobs",
        "attributes": {
            "job_type": "TRANSACTION_VIEW_RESULTS",
            "percent_complete": 0.0,
            "status": "Queued"
        },
        "relationships": {
            "creator": {
                "links": {
                    "self": "/v1/transaction_jobs/47d7e547-7f5a-11ef-8162-dde0088e926a/relationships/creator",
                    "related": "/v1/transaction_jobs/47d7e547-7f5a-11ef-8162-dde0088e926a/creator"
                },
                "data": {
                    "type": "users",
                    "id": "22"
                }
            }
        },
        "links": {
            "self": "/v1/transaction_jobs/47d7e547-7f5a-11ef-8162-dde0088e926a"
        }
    },
    "included": []
}
```

**Response codes:**

- `202 Accepted`: Success. Returns JSON with created job information.
- `400 Bad Request`: Bad JSON: API format, missing parameters or badly formatted parameters
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Create a transaction query job

Creates an asynchronous job to extract transaction data with a query.

**POST** `/v1/transaction_jobs`

**Example:**

```json Request
POST https://examplefirm.com/api/v1/transaction_jobs

{
    "data": {
        "type": "transaction_jobs",
        "attributes": {
            "job_type": "transaction_query",
            "parameters": {
                "columns": [
                    "trade_date",
                    "direct_owner",
                    "security",
                    "type",
                    "value",
                    "last_edit_by",
                    "last_edit_date"
                ],
                "filters": [],
                "sorting": [
                ],
                // "limit": 1,
                "portfolio_type": "entity",
                "portfolio_id": [
                    12345
                ],
                "start_date": "2024-08-03",
                "end_date": "2024-09-03",
                "include_online_valuations": false,
                "include_unverified": false,
                "include_deleted": true
            }
        }
    }
}
```

```json Response
HTTP/1.1 202 Accepted

{
    "data": {
        "id": "204da3ed-7de0-11ef-99fa-25422e3df74b",
        "type": "transaction_jobs",
        "attributes": {
            "job_type": "TRANSACTION_QUERY",
            "percent_complete": 0.0,
            "status": "Queued"
        },
        "relationships": {
            "creator": {
                "links": {
                    "self": "/v1/transaction_jobs/204da3ed-7de0-11ef-99fa-25422e3df74b/relationships/creator",
                    "related": "/v1/transaction_jobs/204da3ed-7de0-11ef-99fa-25422e3df74b/creator"
                },
                "data": {
                    "type": "users",
                    "id": "1000314556"
                }
            }
        },
        "links": {
            "self": "/v1/transaction_jobs/204da3ed-7de0-11ef-99fa-25422e3df74b"
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

**GET** `/v1/transaction_jobs/:id`

**Example:**

```json Request
GET https://examplefirm.com/api/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c
```

```json Response
HTTP/1.1 200

{
    "data": {
        "id": "39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c",
        "type": "transaction_jobs",
        "attributes": {
            "job_type": "TRANSACTION_QUERY",
            "percent_complete": 0.0,
            "status": "Queued"
        },
        "relationships": {
            "creator": {
                "links": {
                    "self": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/relationships/creator",
                    "related": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/creator"
                },
                "data": {
                    "type": "users",
                    "id": "22"
                }
            }
        },
        "links": {
            "self": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c"
        }
    },
    "included": []
}
```

**Response codes:**

- `200 OK`: Success
- `404 Not Found`: Unable to locate the job with the given id, or user does not have permission to view the given job
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Download a job's results

Returns the results of the given job. If the job has not yet completed, this endpoint will return the job status payload.

> 📘 Note
>
> Job results are deleted 24 hours after a job is created.

**GET** `/v1/transaction_jobs/:id/download`

**Example for in progress job:**

```curl Request
GET https://examplefirm.com/api/v1/jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/download
```

```json Response
HTTP/1.1 200

{
    "data": {
        "id": "39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c",
        "type": "transaction_jobs",
        "attributes": {
            "job_type": "TRANSACTION_QUERY",
            "percent_complete": 0.21,
            "status": "In Progress"
        },
        "relationships": {
            "creator": {
                "links": {
                    "self": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/relationships/creator",
                    "related": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/creator"
                },
                "data": {
                    "type": "users",
                    "id": "22"
                }
            }
        },
        "links": {
            "self": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c"
        }
    },
    "included": []
}
```

**Example for completed job:**

```curl Request
GET https://examplefirm.com/api/v1/jobs/657c5d9b-7f5d-11ef-a01d-2900745d31ff/download
```

```json Response
HTTP/1.1 200

Content-Disposition: attachment; file name="transaction_data.xlsx"
Content-Type: application/binary

<DOWNLOAD_CONTENT>
```

**Response codes:**

- `200 OK`: Success. Returns a JSON, CSV, TSV or XLSX as requested.
- `303 See Other`: Completed asynchronous job. Follow the link in the "Location" header to retrieve the results.
- `404 Not Found`: Unable to locate the job with the given id.
- `410 Gone`: Results have expired

## Check the status of all jobs

Retrieves the status and parameters of all jobs.

**GET** `/v1/transaction_jobs`

**Example:**

```curl Request
GET https://examplefirm.com/api/v1/transaction_jobs
```

```json Response
HTTP/1.1 200

{
    "data": [
        {
            "id": "39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c",
            "type": "transaction_jobs",
            "attributes": {
                "job_type": "TRANSACTION_QUERY",
                "completed_at": "2024-09-30T18:53:10Z",
                "started_at": "2024-09-30T18:53:10Z",
                "percent_complete": 1.0,
                "status": "Completed"
            },
            "relationships": {
                "creator": {
                    "links": {
                        "self": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/relationships/creator",
                        "related": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/creator"
                    },
                    "data": {
                        "type": "users",
                        "id": "22"
                    }
                }
            },
            "links": {
                "self": "/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c"
            }
        },
        {
            "id": "657c5d9b-7f5d-11ef-a01d-2900745d31ff",
            "type": "transaction_jobs",
            "attributes": {
                "job_type": "TRANSACTION_VIEW_RESULTS",
                "completed_at": "2024-09-30T18:54:22Z",
                "started_at": "2024-09-30T18:54:20Z",
                "percent_complete": 1.0,
                "status": "Completed"
            },
            "relationships": {
                "creator": {
                    "links": {
                        "self": "/v1/transaction_jobs/657c5d9b-7f5d-11ef-a01d-2900745d31ff/relationships/creator",
                        "related": "/v1/transaction_jobs/657c5d9b-7f5d-11ef-a01d-2900745d31ff/creator"
                    },
                    "data": {
                        "type": "users",
                        "id": "22"
                    }
                }
            },
            "links": {
                "self": "/v1/transaction_jobs/657c5d9b-7f5d-11ef-a01d-2900745d31ff"
            }
        }
    ],
    "included": [],
    "links": {
        "prev": null,
        "next": null
    }
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: User lacks API permission or has not granted the appropriate scope

## Check who created a job

Retrieves [the user](https://developers.addepar.com/v2.231/docs/users#get-a-user) who created the job.

**GET** `/v1/transaction_jobs/:id/creator`

**Example:**

```curl Request
GET https://examplefirm.com/api/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/creator
```

```json Response
HTTP/1.1 200

{
    "data": {
        "id": "22",
        "type": "users",
        "attributes": {
            "two_factor_auth_enabled": false,
            "admin_access": true,
            "all_data_access": true,
            "login_method": "email_password",
            "email": "example@addepar.com"
        },
        "relationships": {
            "permissioned_entities": {
                "links": {
                    "self": "/v1/users/22/relationships/permissioned_entities",
                    "related": "/v1/users/22/permissioned_entities"
                },
                "data": []
            },
            "assigned_role": {
                "data": null
            },
            "permissioned_groups": {
                "links": {
                    "self": "/v1/users/22/relationships/permissioned_groups",
                    "related": "/v1/users/22/permissioned_groups"
                },
                "data": []
            }
        },
        "links": {
            "self": "/v1/users/22"
        }
    },
    "included": []
}
```

## Check the job creator's relationship

Retrieves the relationship of the job creator.

**GET** `/v1/transaction_jobs/:id/relationships/creator`

**Example:**

```curl Request
GET https://examplefirm.com/api/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c/relationships/creator
```

```json Response
HTTP/1.1 200

{
    "data": {
        "id": 22,
        "type": "users"
    }
}
```

## Cancel a job

Cancel a job that is has yet to start, is running, or already completed.

**DELETE** `/v1/transaction_jobs/:id`

When canceling a job with the status:

- `waiting_for_capacity` the job will not run. Status change: `user_canceled`.
- `in_progress` a request to cancel is submitted. Status change:`cancel_requested`, then `user_canceled`.
- `completed` the results are archived. Status change: `user_canceled`.

**Example**

```json Request
DELETE https://examplefirm.com/api/v1/transaction_jobs/39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c
```

```json Response
204 No Content
```

**Response codes:**

- `204 No Content`: Success. Cancel request submitted.
- `404 Not Found`: Cannot locate the job with the given ID, or you don't have permission to view the job.
