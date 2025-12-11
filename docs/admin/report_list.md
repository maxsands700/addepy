# Report List

Get a list of reports to streamline various operations workflows, like the process of [report generation.](https://developers.addepar.com/docs/report-generation)
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/5630c72-Reports_API_.png",
"",
""
],
"align": "center"
}
]
}
[/block]

|                                  |                   |
| :------------------------------- | :---------------- |
| Base route                       | /v1/reports       |
| Endpoints                        | **GET**           |
| Produces                         | JSON              |
| Pagination                       | Yes               |
| OAuth Scopes                     | `REPORTS_READ`    |
| Application permissions required | Access to reports |

# Resource overview

All attributes will be returned in successful **GET** responses.

| Attributes                  | Description                                          | Example                        |
| :-------------------------- | :--------------------------------------------------- | :----------------------------- |
| `report_id`                 | The ID of the report.                                | `37`                           |
| `report_name`               | The name of the report.                              | `Quarterly Performance Report` |
| `created_on_date`           | The date the report was created.                     | `2023-05-18`                   |
| `last_update_date`          | The date the report was last updated.                | `2023-05-20`                   |
| `num_associated_portfolios` | Then number of portfolio associations on the report. | `5`                            |

# Parameters

<br />
[block:parameters]
{
  "data": {
    "h-0": "Attribute",
    "h-1": "Description",
    "h-2": "Example",
    "h-3": "Validation",
    "0-0": "`filter[createdAfter]`",
    "0-1": "Returns only reports created after a specific time.",
    "0-2": "`/v1/reports/?filter[createdAfter]=2017-04-06T20:12:45Z`",
    "0-3": "- Must be a valid date.\n- Must be less than ‘createdBefore’, if both are provided.\n- Must be less than ‘modifiedBefore’, if both are provided.",
    "1-0": "`filter[modifiedAfter]`",
    "1-1": "Returns only reports modified after a specific time.",
    "1-2": "`/v1/reports/?filter[modifiedAfter]=2017-04-06T20:12:45Z`",
    "1-3": "- Must be a valid date.\n- Must be less than ‘modifiedBefore’, if both are provided.",
    "2-0": "`filter[createdBefore]`",
    "2-1": "Returns only reports created before a specific time.",
    "2-2": "`/v1/reports/?filter[createdBefore]=2017-04-06T20:12:45Z`",
    "2-3": "- Must be a valid date.\n- Must be greater than ‘createdAfter’, if both are provided.",
    "3-0": "`filter[modifiedBefore]`",
    "3-1": "Returns only reports modified before a specific time.",
    "3-2": "`/v1/reports/?filter[modifiedBefore]=2017-04-06T20:12:45Z`",
    "3-3": "- Must be a valid date.\n- Must be greater than ‘modifiedAfter’, if both are provided.\n- Must be greater than ‘createdAfter’, if both are provided.",
    "4-0": "`filter[name]`",
    "4-1": "Returns only reports that contain a specific word or phrase. String.",
    "4-2": "`/v1/reports/?filter[name]=test`",
    "4-3": "N/A",
    "5-0": "`filter[entityId]`",
    "5-1": "Returns only reports associated with the entity ID.",
    "5-2": "`/v1/reports?[reports]=100`",
    "5-3": "- Must be a valid ID and exist on the platform.\n- You must have access the entity in Addepar.\n- Only 1 entity ID or group Id can be provided, not both or multiple.",
    "6-0": "`filter[groupId]`",
    "6-1": "Returns only reports associated with the group ID.",
    "6-2": "`/v1/reports?[reports]=200`",
    "6-3": "- Must be a valid ID and exist on the platform.\n- You must have access the group in Addepar.\n- Only 1 entity Id or group Id can be provided, not both or multiple.",
    "7-0": "`page[limit]`",
    "7-1": "The number of reports returned in the list.  The default and maximum number of reports listed per page is 500.",
    "7-2": "`100`",
    "7-3": "- Must be integer not exceeding 500.",
    "8-0": "`page[after]\n(cursor)`",
    "8-1": "Determines which reports you get back in the response. Based on report ID. Integer.  \n  \nFor example, say you have 5 reports in Addepar, with report IDs 1, 2, 3, 4, and 5. If you specify `page[after]=2`, then the response will include reports 3, 4, and 5.",
    "8-2": "`0`",
    "8-3": "N/A"
  },
  "cols": 4,
  "rows": 9,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

# Get a list of reports

Obtain a list of reports to use as a starting point for other API workflows. For example, you could get reports created after April 5th, 2017 that have an ID greater than or equal to 2. Then, [generate reports](https://developers.addepar.com/docs/report-generation) as needed.

```curl Request
GET:*/v1/reports/?filter[createdAfter]=2017-04-05T20:12:45Z&page[limit]=2&page[after]=2
```

```json Reponse
HTTP/1.1 200

{
  "data": {
    "type": "reports",
    "id": "13",
    "attributes": {
      "num_associated_perspectives": 2,
      "name": "Billing Attributes Report",
      "created_at": "2017-05-24T01:19:34Z",
      "modified_at": "2017-05-24T01:20:44Z"
    },
    "links": {
      "self": "/v1/files/13"
    }
  },
  "included": []
}
```

**Response codes**

- `200 OK:` Success
- `400 Bad Request : `Incorrect or missing parameters. See parameter tables for more information.
- `404 Not Found :`The entity or group was not found.
