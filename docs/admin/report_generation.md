# Report Generation

Running a report generates a PDF for each stated portfolio for a given time period. Use the Report Generation API to run reports from outside of Addepar, publish reports to the Client Portal, and notify clients when their report is available.

You can get report ID via the [Report List API](https://developers.addepar.com/docs/report-list). After you run a report, you can access a portfolio's report PDF from its Generated PDFs tab in Addepar, or via the [Generated Reports API](https://developers.addepar.com/docs/generated-reports-beta).
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/08be36d-Screenshot_2024-02-22_at_3.48.09_PM.png",
"",
""
],
"align": "center"
}
]
}
[/block]

|                                  |                                       |
| :------------------------------- | :------------------------------------ |
| Base route                       | /v1/report_generation_job             |
| Endpoints                        | **POST**                              |
| Produces                         | JSON                                  |
| Pagination                       | Yes                                   |
| OAuth scopes                     | `REPORTS_WRITE`                       |
| Application permissions required | "Access to all tools and portfolios." |

# Resource overview

The Report Generation API returns a resource object containing the Report Job ID in successful POST responses.

| Attributes | Description                                         | Example                                  |
| :--------- | :-------------------------------------------------- | :--------------------------------------- |
| `job_id`   | The unique id of the report generation job. String. | `"b37e4e27-14b8-486c-b2c9-d0d6c9991fcb"` |

# Parameters

## **Required parameters**

You can request a report generation job by providing the below resource object attributes.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"h-3": "Validation",
"0-0": "`report_id`",
"0-1": "The ID of the report that you want to run. Integer. \n \nYou can find a report's ID in its Addepar web application URL.",
"0-2": "`4` ",
"0-3": "`400 bad request`returned if missing `report_id`. \n \n`404 not found` returned if you don't have access to the report, or the report was deleted.",
"1-0": "`portfolios`",
"1-1": "The list of entities or groups that you want to run reports for. The provided portfolios can be associated with the report, but don't need to be. JSON object. \n \nFor each portfolio, provide both: \n \n- `portfolio_type`, either \"entity\" or \"group. String.\n\n- `portfolio_id`, the portfolio's Entity ID or Group ID. String.",
"1-2": "`[\n{\"portfolio_type\": \"entity\",\n\"portfolio_id\": \"22\"}, \n{\"portfolio_type\": \"group\",\n\"portfolio_id\": \"3\"}\n]`",
"1-3": "`400 bad request`returned if missing portfolio type, missing portfolio ID, or if the types for the request are not supported. \n \n`400 bad request` returned if you don't have permission to access them, or if some portfolio IDs don't exist.",
"2-0": "`start_date`",
"2-1": "The report's start date. String, formatted as YYYY-MM-DD. \n \nCan't be later than `end_date`.",
"2-2": "`\"2023-07-01\"`",
"2-3": "`400 bad request`returned if `start_date` is on or after `end_date.`",
"3-0": "`end_date`",
"3-1": "The report's end date. String, formatted as YYYY-MM-DD. \n \nCan't be earlier than `start_date`.",
"3-2": "`\"2023-08-01\"`",
"3-3": "`400 bad request` returned if `end_date` is on or before `start_date`."
},
"cols": 4,
"rows": 4,
"align": [
"left",
"left",
"left",
"left"
]
}
[/block]

## **Optional parameters**

[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"h-3": "Validation",
"0-0": "`portal_publishing`",
"0-1": "Determines if the report should also be published to Portal. The value for this field should be: \n \n- `PUBLISH`\n- `DO_NOT_PUBLISH`\n- `USE_CONTACT_PREFERENCE`You must specify a `contact_notification` when publishing to Portal.",
"0-2": "`\"portal_publishing\": \"PUBLISH\"` ",
"0-3": "`400 bad request` returned if `portal_publishing` is set to `PUBLISH `or `USE_CONTACT_PREFERENCE `and `contact_notification `isn't provided. \n \n`400 bad request `returned if `portal_publishing` is `DO_NOT_PUBLISH` and `contact_notification` is `NOTIFY` or `USE_CONTACT_PREFERENCE`. Because the report isn't being published, there's no need to contact the client. \n \n`400 Bad Request` returned if the value is invalid.",
"1-0": "`contact_notification`",
"1-1": "When the report is published to the Portal, this determines if the contact is notified. The value for this field should be: \n \n- `NOTIFY`\n- \\`DO_NOT_NOTIFY\n- USE_CONTACT_PREFERENCE\\`You must specify `portal_publishing` when notifying a contact. ",
"1-2": "`[\n{\"portfolio_type\": \"entity\",\n\"portfolio_id\": \"22\"}, \n{\"portfolio_type\": \"group\",\n\"portfolio_id\": \"3\"}\n]`",
"1-3": "`400 bad request `returned if the value is invalid or if the request is missing the`portal_publishing` attribute.",
"2-0": "`label`",
"2-1": "List the label IDs you'd like to attach to the generated pdf. Labels must already exist in Addepar.",
"2-2": "`\"label\": [1,2,3]`",
"2-3": "`400 bad request` returned if the label doesn't exist in Addepar, if the label is invalid."
},
"cols": 4,
"rows": 3,
"align": [
"left",
"left",
"left",
"left"
]
}
[/block]

# Run a report

Requests to generate a report PDF for each associated and specified portfolio.

**POST** `/v1/report_generation_job`

**Example**:

```Text REQUEST
POST: https://examplefirm.addepar.com/api/v1/report_generation_job

{
    "data": {
        "type": "report_generation_job",
        "attributes": {
            "report_id": "5",
            "portfolios": [
                {
                "portfolio_type": "entity",
                "portfolio_id": "22"
                }
            ],
            "start_date": "2023-07-01",
            "end_date": "2023-08-01",
            "portal_publishing": "PUBLISH",
            "contact_notification": "NOTIFY",
            "label": [1,2,3]
            }
    }
}
```

```json RESPONSE
HTTP/1.1 200

{
    "data": {
        "id": "b37e4e27-14b8-486c-b2c9-d0d6c9991fcb",
        "type": "report_generation_job_id",
        "links": {
            "self": "/v1/report_generation_job_id/b37e4e27-14b8-486c-b2c9-d0d6c9991fcb"
        }
    },
    "included": []
}
```

**Response Codes**

- `200 OK`: Success

- `400 Bad Request` : Incorrect or missing parameters. See parameter tables for more information.

- `403 Forbidden`: You don't have the correct reporting or Portal permission to complete a certain action in Addepar. Reach out to your Addepar firm administrator.

- `404 Not Found` : The requested report was not found.
