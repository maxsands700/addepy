# Generated Reports

The Generated Reports API provides access to generated report objects representing the metadata associated with a single completed run of a report generation job.

A report generation job is initiated from the Addepar web application or the [Report Generation API](https://developers.addepar.com/docs/report-generation) and generates report PDFs for the portfolios associated with a given report.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/47c0d40-Screenshot_2024-02-22_at_4.02.56_PM.png",
"",
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
"0-1": "/v1/generated_reports",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/generated_reports \n/v1/generated_reports/:id \n/v1/generated_reports/:id/creator \n/v1/generated_reports/:id/zipped_file \n/v1/generated_reports/:id/zipped_file/download",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "Yes",
"4-0": "OAuth Scopes",
"4-1": "`FILES` for all except /v1/generated_reports/:id/creator, which requires `FILES` and `USERS`",
"5-0": "Application Permissions Required",
"5-1": "\"Access to all tools and portfolios.\""
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

All attributes will be returned in successful GET responses.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Type",
"h-2": "Example",
"0-0": "`report_id`",
"0-1": "The unique id of the report for which the report generation job was run.",
"0-2": "`46`",
"1-0": "`report_name`",
"1-1": "The name of the report for which the report generation job was run.",
"1-2": "`\"Quarterly Performance Report\"`",
"2-0": "`status`",
"2-1": "The status of the completed job. Either, `FINISHED`, `ERROR`, or `CANCELED`. \n \n`ERROR` is due to system failure. `CANCELED` is an action taken by a user. Both these statuses might still result in one or more successful portfolios.",
"2-2": "`\"ERROR\"`",
"3-0": "`started_at`",
"3-1": "String representing the time instant in UTC at which this report generation job was started.",
"3-2": "`\"2021-02-14T10:15:30.00Z\"`",
"4-0": "`completed_at`",
"4-1": "String representing the time instant in UTC at which this report generation job finished.",
"4-2": "`\"2021-02-14T14:25:45.00Z\"`",
"5-0": "`job_type`",
"5-1": "Specifies whether the report job was scheduled or ad hoc. ",
"5-2": "`\"SCHEDULED\"` or `\"AD_HOC\"`",
"6-0": "`generated_portfolios`",
"6-1": "An array of objects providing information of successfully generated portfolios. Includes portfolio type, portfolio id, portfolio name, file id, and publish to portal status.",
"6-2": "`\"generated_portfolios\"`",
"7-0": "`portfolio_type`",
"7-1": "One of entity or group.",
"7-2": "`\"entity\"`",
"8-0": "`portfolio_id`",
"8-1": "Unique id of the portfolio.",
"8-2": "`21`",
"9-0": "`portfolio_name`",
"9-1": "Name of the portfolio.",
"9-2": "`\"Tony Stark\"`",
"10-0": "`file_id`",
"10-1": "Unique id of the generated file. It can be used to download the actual binary file from `GET /v1/files/:id/download`.",
"10-2": "`101`",
"11-0": "`failed_portfolios`",
"11-1": "An array of objects providing information of failed portfolios during report generation. Includes portfolio type, portfolio ID, and portfolio name.",
"11-2": "`\"failed_portfolios\"`"
},
"cols": 3,
"rows": 12,
"align": [
"left",
"left",
"left"
]
}
[/block]

| Relationships |                                                                                     |
| :------------ | :---------------------------------------------------------------------------------- |
| `creator`     | The user who created the report generation job that generated the associated files. |

## Optional parameters

[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"0-0": "filter[completed_after]=YYYY-MM-DDTHH:MM:SSZ",
"0-1": "Returns jobs run after this date. The timestamp is in UTC.",
"0-2": "`[completed_after]=2021-05-14T12:03:39Z`",
"1-0": "filter[completed_before]=YYYY-MM-DDTHH:MM:SSZ",
"1-1": "Returns jobs run before this date. The timestamp is in UTC.",
"1-2": "`[completed_before]=2021-05-14T12:03:39Z`",
"2-0": "filter[status]=[FINISHED, ERROR, CANCELED]",
"2-1": "Returns jobs by status. Filter by one or more of the following: \n`FINISHED` - done running \n`ERROR` - report ended in an error with one or more jobs failing \n`CANCELED` - A user stopped the job while it was in progress",
"2-2": "`[status]=FINISHED,ERROR`",
"3-0": "filter[xxx][entityId]",
"3-1": "Returns the jobs for this entity's portfolio.",
"3-2": "[entityId]=12345",
"4-0": "filter[xxx][groupId]",
"4-1": "Returns the jobs for this group's portfolio.",
"4-2": "[groupId]=54789"
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

## Get all generated reports

Retrieves all generated reports that a user is authenticated to view, sorted in reverse chronological order of completion time.

**GET** /v1/generated_reports/

```curl Request
GET https://examplefirm.addepar.com/api/v1/generated_reports
```

```json Response
200 OK: Success

{
  "data": [
    {
      "type": "generated_reports",
      "id": "A-UUID-ASSOCIATED-WITH-EACH-RUN",
      "attributes": {
        "report_id": 42,
        "report_name": "Quarterly Performance Report",
        "status": "ERROR",
        "started_at": "2021-02-14T10:15:30.00Z",
        "completed_at": "2021-02-14T14:25:45.00Z",
        "job_type": "AD_HOC",
        "generated_portfolios": [
          {
            "portfolio_type": "entity",
            "portfolio_id": 21,
            "portfolio_name": "Tony Stark",
            "file_id": 101,
            "has_been_published": false
          },
          {
            "portfolio_type": "group",
            "portfolio_id": 31,
            "portfolio_name": "Avengers",
            "file_id": 102,
            "has_been_published": false
          }
        ],
        "failed_portfolios": [
          {
            "portfolio_type": "entity",
            "portfolio_id": 22,
            "portfolio_name": "Thanos"
          },
          {
            "portfolio_type": "group",
            "portfolio_id": 32,
            "portfolio_name": "Chitauri"
          }
        ]
      },
      "relationships": {
        "creator": {
          "data": {
            "type": "users",
            "id": "84"
          },
          "links": {
            "self": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/creator",
            "related": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/creator"
          }
        },
        "zipped_file": {
          "data": {
            "type": "archive/files",
            "id": "61"
          },
          "links": {
            "self": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/zipped_file",
            "related": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/zipped_file"
          }
        }
      }
    },
    {
      "type": "generated_reports",
      "id": "ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN",
      "attributes": {
        "report_id": 43,
        "report_name": "Market Benchmark Report",
        "status": "FINISHED",
        "started_at": "2021-02-14T11:15:30.00Z",
        "completed_at": "2021-02-14T13:25:45.00Z",
        "job_type": "AD_HOC",
        "generated_portfolios": [
          {
            "portfolio_type": "entity",
            "portfolio_id": 21,
            "portfolio_name": "Tony Stark",
            "file_id": 103
          },
          {
            "portfolio_type": "group",
            "portfolio_id": 31,
            "portfolio_name": "Avengers",
            "file_id": 104
          }
        ],
        "failed_portfolios": []
      },
      "relationships": {
        "creator": {
          "data": {
            "type": "users",
            "id": "84"
          },
          "links": {
            "self": "/v1/generated_reports/ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/creator",
            "related": "/v1/generated_reports/ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN/creator"
          }
        },
        "zipped_file": {
          "data": {
            "type": "archive/files",
            "id": "62"
          },
          "links": {
            "self": "/v1/generated_reports/ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/zipped_file",
            "related": "/v1/generated_reports/ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN/zipped_file"
          }
        }
      }
    }
  ],
  "included": [],
  "links": {
    "next": "/v1/generated_reports?page[number]=1&page[size]=50"
  }
}
```

**Example with various parameters**

```curl Request
GET /v1/generated_reports/?page[size]=50&page[number]=0&filter[status]=FINISHED,ERROR&filter[completed_before]=2021-05-14T12:03:39Z
```

```json Response
200 OK: Success

{
  "data": {
    "type": "generated_reports",
    "id": "A-UUID-ASSOCIATED-WITH-EACH-RUN",
    "attributes": {
      "report_id": 42,
      "report_name": "Quarterly Performance Report",
      "status": "ERROR",
      "started_at": "2021-02-14T10:15:30.00Z",
      "completed_at": "2021-02-14T14:25:45.00Z",
      "job_type": "AD_HOC",
      "generated_portfolios": [
        {
          "portfolio_type": "entity",
          "portfolio_id": 21,
          "portfolio_name": "Tony Stark",
          "file_id": 101,
          "has_been_published": false
        },
        {
          "portfolio_type": "group",
          "portfolio_id": 31,
          "portfolio_name": "Avengers",
          "file_id": 102,
          "has_been_published": false
        }
      ],
      "failed_portfolios": [
        {
          "portfolio_type": "entity",
          "portfolio_id": 22,
          "portfolio_name": "Thanos"
        },
        {
          "portfolio_type": "group",
          "portfolio_id": 32,
          "portfolio_name": "Chitauri"
        }
      ]
    },
    "relationships": {
      "creator": {
        "data": {
          "type": "users",
          "id": "84"
        },
        "links": {
          "self": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/creator",
          "related": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/creator"
        }
      },
      "zipped_file": {
        "data": {
          "type": "files",
          "id": "61"
        },
        "links": {
          "self": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/zipped_file",
          "related": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/zipped_file"
        }
      }
    }
  }
}
```

**Example with portfolio filter parameter**

```Text Request
GET /v1/generated_reports/?page[size]=50&page[number]=0&filter[entityId]=1234
```

```Text Response
{
  "data": [
    {
      "type": "generated_reports",
      "id": "A-UUID-ASSOCIATED-WITH-EACH-RUN",
      "attributes": {
        "report_id": 42,
        "report_name": "Quarterly Performance Report",
        "status": "FINISHED",
        "started_at": "2021-02-14T10:15:30.00Z",
        "completed_at": "2021-02-14T14:25:45.00Z",
        "job_type": "AD_HOC",
        "generated_portfolios": [
          {
            "portfolio_type": "entity",
            "portfolio_id": 1234,
            "portfolio_name": "Tony Stark",
            "file_id": 101,
            "has_been_published": false
          },
          {
            "portfolio_type": "group",
            "portfolio_id": 31,
            "portfolio_name": "Avengers",
            "file_id": 102,
            "has_been_published": false
          }
        ],
        "failed_portfolios": []
      },
      "relationships": {
        "creator": {
          "data": {
            "type": "users",
            "id": "84"
          },
          "links": {
            "self": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/creator",
            "related": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/creator"
          }
        },
        "zipped_file": {
          "data": {
            "type": "archive/files",
            "id": "61"
          },
          "links": {
            "self": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/zipped_file",
            "related": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/zipped_file"
          }
        }
      }
    },
    {
      "type": "generated_reports",
      "id": "ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN",
      "attributes": {
        "report_id": 43,
        "report_name": "Market Benchmark Report",
        "status": "FINISHED",
        "started_at": "2021-02-14T11:15:30.00Z",
        "completed_at": "2021-02-14T13:25:45.00Z",
        "job_type": "AD_HOC",
        "generated_portfolios": [
          {
            "portfolio_type": "entity",
            "portfolio_id": 1234,
            "portfolio_name": "Tony Stark",
            "file_id": 103
          },
          {
            "portfolio_type": "group",
            "portfolio_id": 31,
            "portfolio_name": "Avengers",
            "file_id": 104
          }
        ],
        "failed_portfolios": []
      },
      "relationships": {
        "creator": {
          "data": {
            "type": "users",
            "id": "84"
          },
          "links": {
            "self": "/v1/generated_reports/ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/creator",
            "related": "/v1/generated_reports/ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN/creator"
          }
        },
        "zipped_file": {
          "data": {
            "type": "archive/files",
            "id": "62"
          },
          "links": {
            "self": "/v1/generated_reports/ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/zipped_file",
            "related": "/v1/generated_reports/ANOTHER-UUID-ASSOCIATED-WITH-EACH-RUN/zipped_file"
          }
        }
      }
    }
  ],
  "included": [],
  "links": {
    "next": "/v1/generated_reports?page[number]=1&page[size]=50&filter[entityId]=1234"
  }
}
```

**Responses**

- `200 OK`: Success
- `400 Bad Request`: `include` query parameter not allowed
- `403 Forbidden`: Lacking admin permission

## Get generated report by job ID

Retrieves a generated report by job ID within the authenticated user's firm.

\*\*GET \*\*`/v1/generated_reports/:id`

```curl Request
GET https://examplefirm.addepar.com/v1/generated_reports/42
```

```json Response
200 OK: Success

{
  "data": {
    "type": "generated_reports",
    "id": "A-UUID-ASSOCIATED-WITH-EACH-RUN",
    "attributes": {
      "report_id": 42,
      "report_name": "Quarterly Performance Report",
      "status": "ERROR",
      "started_at": "2021-02-14T10:15:30.00Z",
      "completed_at": "2021-02-14T14:25:45.00Z",
      "job_type": "AD_HOC",
      "generated_portfolios": [
        {
          "portfolio_type": "entity",
          "portfolio_id": 21,
          "portfolio_name": "Tony Stark",
          "file_id": 101,
          "has_been_published": false
        },
        {
          "portfolio_type": "group",
          "portfolio_id": 31,
          "portfolio_name": "Avengers",
          "file_id": 102,
          "has_been_published": false
        }
      ],
      "failed_portfolios": [
        {
          "portfolio_type": "entity",
          "portfolio_id": 22,
          "portfolio_name": "Thanos"
        },
        {
          "portfolio_type": "group",
          "portfolio_id": 32,
          "portfolio_name": "Chitauri"
        }
      ]
    },
    "relationships": {
      "creator": {
        "data": {
          "type": "users",
          "id": "84"
        },
        "links": {
          "self": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/creator",
          "related": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/creator"
        }
      },
      "zipped_file": {
        "data": {
          "type": "files",
          "id": "61"
        },
        "links": {
          "self": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/relationships/zipped_file",
          "related": "/v1/generated_reports/A-UUID-ASSOCIATED-WITH-EACH-RUN/zipped_file"
        }
      }
    }
  }
}
```

**Responses**

- `200 OK`: Success
- `400 Bad Request`: `include` query parameter not allowed
- `403 Forbidden`: Lacking admin permission
- `404 Not Found`: Nonexistent/non-permissioned generated report ID or the report is currently being generated

## Get report creator by ID

Retrieves all information related to the user who generated the reports for the job id.

\*\*GET \*\*`/v1/generated_reports/:id/creator`

```curl Request
GET https://examplefirm.addepar.com/v1/generated_reports/42/creator
```

```json Response
200 OK: Success

{
    "data": {
        "id": "84",
        "type": "users",
        "attributes": {
            "first_name": "Nick",
            "last_name": "Fury",
            "two_factor_auth_enabled": false,
            "admin_access": true,
            "all_data_access": true,
            "login_method": "email_password",
            "email": "nfury@shield.com"
        },
        "relationships": {
            "permissioned_entities": {
                "links": {
                    "self": "/v1/users/84/relationships/permissioned_entities",
                    "related": "/v1/users/84/permissioned_entities"
                },
                "data": []
            },
            "assigned_role": {
                "data": null
            },
            "permissioned_groups": {
                "links": {
                    "self": "/v1/users/84/relationships/permissioned_groups",
                    "related": "/v1/users/84/permissioned_groups"
                },
                "data": []
            }
        },
        "links": {
            "self": "/v1/users/84"
        }
    },
    "included": []
}
```

**Responses**

- `200 OK`: Success
- `400 Bad Request`: Invalid relationship queried
- `403 Forbidden`: Lacking admin permission
- `404 Not Found`

## Get reports in a zipped file by ID

Retrieves all information related to the zipped file generated for the job ID.

\*\*GET \*\*`/v1/generated_reports/:id/zipped_file`

```curl Request
GET https://examplefirm.addepar.com/v1/generated_reports/61/zipped_file
```

```json Response
200 OK: Success

{
    "data": {
        "id": "61",
        "type": "files",
        "attributes": {
            "content_type": "application/zip",
            "bytes": 36599,
            "name": "Quarterly Performance Report at 05-15-2021.zip",
            "created_at": "2021-05-17T12:34:38Z"
        },
        "relationships": {
            "associated_groups": {
                "links": {
                    "self": "/v1/files/61/relationships/associated_groups",
                    "related": "/v1/files/61/associated_groups"
                },
                "data": []
            },
            "associated_entities": {
                "links": {
                    "self": "/v1/files/61/relationships/associated_entities",
                    "related": "/v1/files/61/associated_entities"
                },
                "data": []
            }
        },
        "links": {
            "self": "/v1/files/61"
        }
    },
    "included": []
}
```

**Responses**

- `200 OK`: Success
- `400 Bad Request`: Invalid relationship queried
- `403 Forbidden`: Lacking admin permission
- `404 Not Found`

## Download reports in a zipped file by ID

Returns a binary zipped file.

\*\*GET \*\*`/v1/generated_reports/:id/zipped_file/download`

```curl Request
GET https://examplefirm.addepar.com/v1/generated_reports/61/zipped_file
```

```json Response
HTTP/1.1 200

Content-DispositionL attachment; filename="Quarterly Performance Report at 05-15-2021.zip"
Content-Type: application/binary

<RAW_FILE_DATA>
```

**Responses**

- `200 OK`: Success
- `403 Forbidden`: Lacking admin permission
- `404 Not Found`

See more types of [file downloads](https://developers.addepar.com/docs/files#download-a-file)
