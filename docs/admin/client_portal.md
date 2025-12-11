# Client Portal

Operationalize your client engagement by publishing a report or file to the Client Portal and notifying clients in a single API call.

As a pre-step to this workflow, you can [generate reports](https://developers.addepar.com/docs/report-generation), [upload files](https://developers.addepar.com/docs/files), or [associate a file to a portfolio ](https://developers.addepar.com/docs/files)via API, or do this manually in Addepar.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/ae78889427ae4be8c2d558bdc61685a0e7d2ca6b3478586b4f69703cba093cee-client_portal_api_doc_image.png",
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
"0-1": "/v1/portal/publish_files",
"1-0": "Endpoints",
"1-1": "**POST** \n/v1/portal/publish_files",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "Yes",
"4-0": "Application permissions required",
"4-1": "Portal: Share client files \nFiles: Create, edit, delete",
"5-0": "OAuth scopes",
"5-1": "`FILE_WRITE` and `PUBLISH_FILE`"
},
"cols": 2,
"rows": 6,
"align": [
"left",
"left"
]
}
[/block]

# Resource overview

The Publish to Portal API returns a resource object containing the file ID and status in a successful POST response.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`file_id`",
"0-1": "The ID of the file you want to associate with contacts.",
"0-2": "`\"37\"`",
"1-0": "`publish_status`",
"1-1": "Indicates if the file was published to the Portal. String. \n \n- If you share a file with multiple contacts, and the file fails to share with one contact, the job will say `\"fail\"`.\n- If the file is shared with all listed contacts without issue, it will say `\"success\"`.",
"1-2": "`\"success\"`",
"2-0": "`notify_status`",
"2-1": "Indicates if the contact was notified via email. String. \n \n- If you requested to notify multiple contacts, and one contact couldn't be notified, the job will say `“fail\"`.\n- If all contacts are notified without issue, the job will say `“success\"`.\n- If you don't notify any contacts, the message will return `“success\"`.",
"2-2": "`\"success\"`",
"3-0": "`error`",
"3-1": "A list of objects representing errors arising during publishing or notifying. See below for object details.",
"3-2": "See below."
},
"cols": 3,
"rows": 4,
"align": [
"left",
"left",
"left"
]
}
[/block]

## Error objects

| Attribute | Description                                                           | Example                                      |
| :-------- | :-------------------------------------------------------------------- | :------------------------------------------- |
| `code`    | The name of the error. String                                         | `“notification_failed"`                      |
| `title`   | The description of the error. String.                                 | `"Notification failed for some contacts."`   |
| `detail`  | The details of the error, including the contacts that failed. String. | `"Notification failed for contacts [1,2,3]"` |

# Parameters

[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`files_id`",
"0-1": "The IDs of the files you want to publish to contacts' portals. List of integers. Required. Maximum of 500 files.",
"0-2": "`[37,38,39]`",
"1-0": "`publish_override_contact_ids`",
"1-1": "The IDs of contacts that will always have the files published to portal, regardless of `portal_publishing` value. List of integers. Optional.",
"1-2": "`[23,25]`",
"2-0": "`portal_publishing`",
"2-1": "The scope of publishing the files to portal. String. Required. \n \nSupported values: \n-`do_not_publish` \n-`use_contact_preference` \n-`publish`",
"2-2": "`\"publish\"`",
"3-0": "`contact_notification`",
"3-1": "The scope of notifying contacts about successful publishes. String. Required. \n \nSupported values: \n \n- `do_not_notify`\n- `use_contact_preference`\n- `notify`",
"3-2": "`\"notify\"`"
},
"cols": 3,
"rows": 4,
"align": [
"left",
"left",
"left"
]
}
[/block]

# Publish to Portal

Requests to publish a file to the Client Portal.

**POST** `/v1/portal/publish_files`

**Example**

```json Request
GET https://examplefirm.addepar.com/api/v1/portal/publish_files

{
    "data": {
        "type": "publish_portal_files_request",
        "attributes": {
            "files_id": [37,38,39],
            "portal_publishing": "PUBLISH",
            "contact_notification": "DO_NOT_NOTIFY"
        }
    }
}
```

```json Response
HTTP/1.1 200

{
    "data": [
        {
            "id": "37",
            "type": "publish_files_result",
            "attributes": {
                "file_id": 37,
                "notify_status": "success",
                "publish_status": "success"
            },
            "links": {
                "self": "/v1/publish_files_result/37"
            }
        },
        {
            "id": "38",
            "type": "publish_files_result",
            "attributes": {
                "file_id": 38,
                "notify_status": "success",
                "publish_status": "success"
            },
            "links": {
                "self": "/v1/publish_files_result/38"
            }
        },
        {
            "id": "39",
            "type": "publish_files_result",
            "attributes": {
                "file_id": 39,
                "notify_status": "success",
                "publish_status": "success"
            },
            "links": {
                "self": "/v1/publish_files_result/39"
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

- `200 OK: Success`. This occurs even if failures during publish or notification occur.
- `400 Bad request`: Missing required fields or too many files.
- `403 Forbidden`: Lacking file permission or client portal publish file permission.

## Partial fail example

When you request to publish files to the portal, if the publish or notification fails for one or more contacts, the job will still be processed. However, you will receive a notice of the failures along with the contact IDs..

```json Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "37",
      "type": "publish_files_result",
      "attributes": {
        "file_id": 37,
        "notify_status": "fail",
        "publish_status": "success",
        "error": [
          {
            "code": "notification_failed",
            "title": "Notification failed for some contacts.",
            "detail": "Notification failed for contacts [1,2,3]."
          }
        ]
      },
      "links": {
        "self": "/v1/publish_files_result/37"
      }
    },
    {
      "id": "38",
      "type": "publish_files_result",
      "attributes": {
        "file_id": 38,
        "notify_status": "fail",
        "publish_status": "fail",
        "error": [
          {
            "code": "publish_failed",
            "title": "Publish failed for some contacts.",
            "detail": "Publish failed for contacts [4,5]."
          },
          {
            "code": "notification_failed",
            "title": "Notification failed for some contacts.",
            "detail": "Notification failed for contacts [1,2,3]."
          }
        ]
      },
      "links": {
        "self": "/v1/publish_files_result/38"
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
