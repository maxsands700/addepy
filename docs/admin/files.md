# Files

See and manage files stored in Addepar. For example, you can upload files to a specific folder or move, delete, and download them. You can also link files to portfolios.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/7e13a87-files_for_dev_portal.png",
"Files.png",
3104
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
"0-0": "Base Route",
"0-1": "/v1/files",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/files \n/v1/files/:id \n/v1/files/:id/download \n/v1/archive/files/:id \n/v1/archive/files/:id/download \n/v1/files/:id/relationships/associated_groups \n/v1/files/:idrelationships/associated_entities \n \n**POST** \n/v1/files/ \n/v1/files/:id/relationships/associated_groups \n/v1/files/:id/relationships/associated_entities \n \n**PATCH** \n/v1/files/:id \n/v1/files/:id/relationships/associated_groups \n/v1/files/:id/relationships/associated_entities \n \n**DELETE** \n/v1/files/:id \n/v1/files/:id/relationships/associated_groups \n/v1/files/:id/relationships/associated_entities",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Files: View Only\" is required to retrieve and download files. All other operations require \"Files: Create, edit and delete\" permissions.",
"5-0": "OAuth Scopes",
"5-1": "`FILES` or `FILES_WRITE`"
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

Responses include a resource object described by the below attributes.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`name`",
"0-1": "The file or folder's name. String. Required for creation.",
"0-2": "`\"Sample File.txt\"` \n`\"Test Folder\"`",
"1-0": "`content_type`",
"1-1": "The content type of the file or folder. String. Not editable.",
"1-2": "`\"application/PDF\"` \n`\"folder\"`",
"2-0": "`created_at`",
"2-1": "Time stamp of the file or folder's creation. String. ISO 8601 date format.",
"2-2": "`\"2014-12-01T13:22:40Z\"`",
"3-0": "`modified_at`",
"3-1": "Time stamp of the file or folder’s modification. String. ISO 8601 date format.",
"3-2": "`“2014-12-01T13:22:40Z”`",
"4-0": "`deleted_at`",
"4-1": "Time stamp of the file or folder's deletion. String. ISO 8601 date format.",
"4-2": "`\"2014-12-01T13:22:40Z\"`",
"5-0": "`bytes`",
"5-1": "The size of the file in bytes. Number. Not editable.",
"5-2": "`100000`",
"6-0": "`is_folder`",
"6-1": "The designation of file or folder. String. Not editable.",
"6-2": "`\"true\"`",
"7-0": "`parent_folder_id`",
"7-1": "The ID of the parent folder. Number. Not editable.",
"7-2": "`12345`"
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

## Optional parameters

You can use these parameters to specify responses from **GET** `/v1/files`, **GET** `/v1/files/:id`, and **GET** `/v1/archive/files`.
[block:parameters]
{
"data": {
"h-0": "Parameter",
"h-1": "Description",
"h-2": "Example",
"h-3": "Validation",
"0-0": "`filter[files][createdAfter]`",
"0-1": "Returns files or folders created after a specific time.",
"0-2": "`/v1/files/?filter[files][createdAfter]=2017-04-06T20:12:45Z`",
"0-3": "Uses YYYY-MM-DD date format (ISO 8601)",
"1-0": "`filter[files][createdBefore]`",
"1-1": "Returns files or folders created before a specific time.",
"1-2": "`/v1/files/?filter[files][createdBefore]=2017-04-06T20:12:45Z`",
"1-3": "Uses YYYY-MM-DD date format (ISO 8601)",
"2-0": "`filter[files][createdAfter] &filter[files][createdBefore]`",
"2-1": "Returns files or folders created within a specific time range.",
"2-2": "`/v1/files/?filter[files][createdAfter]=2017-04-05T20:12:45Z&filter[files][createdBefore]=2017-04-06T20:12:45Z`",
"2-3": "Uses YYYY-MM-DD date format (ISO 8601) \n \ncreatedBefore must be earlier than createdAfter",
"3-0": "`filter[files][entityId]`",
"3-1": "Returns files or folders associated with an entity ID.",
"3-2": "`/v1/files?[files][entityId]=100`",
"3-3": "",
"4-0": "`filter[files][groupId]`",
"4-1": "Returns files or folders associated with a group ID.",
"4-2": "`/v1/files?[files][groupId]=20`",
"4-3": "",
"5-0": "`filter[files][entityId]&filter[files][groupId]`",
"5-1": "If IDs for both an entity and a group are included in a request, the API will ignore the group and return only the files or folders associated with the entity.",
"5-2": "`/v1/files?[files][entityId]=100&filter[files][groupId]=20`",
"5-3": "",
"6-0": "`filter[files][includedObjects]`",
"6-1": "Returns only files, only folders, or both. \n \n- `FOLDERS_ONLY`\n- `FILES_ONLY`\n- `FILES_AND_FOLDERS`If not specified, defaults to FILES_ONLY.",
"6-2": "`=FOLDERS_ONLY`",
"6-3": "Must be one of the three valid inputs. Any other input results in an error.",
"7-0": "`filter[files][parentFolderId]`",
"7-1": "Returns only the objects in the specified folder",
"7-2": "`=12345`",
"7-3": "You must have access to this active folder."
},
"cols": 4,
"rows": 8,
"align": [
"left",
"left",
"left",
"left"
]
}
[/block]

## Relationships

| Relationship          | Description                      |
| :-------------------- | :------------------------------- |
| `associated_groups`   | Groups associated with a file.   |
| `associated_entities` | Entities associated with a file. |

```json Relationships
"relationships": {
      "associated_groups": {
        "links": {
          "self": "/v1/files/123/relationships/associated_groups",
          "related": "/v1/files/123/associated_groups"
        },
        "data": [
          {
            "type": "groups",
            "id": "1234"
          },
          {
            "type": "groups",
            "id": "5678"
          }
        ]
      },
      "associated_entities": {
        "links": {
          "self": "/v1/files/123/relationships/associated_entities",
          "related": "/v1/files/123/associated_entities"
        },
        "data": [
          {
            "type": "entities",
            "id": "10000"
          },
          {
            "type": "entities",
            "id": "10001"
          }
        ]
      }
    },
```

## Get a file or folder

Retrieves details for a specific file or folder, such as when it was created, the type of content it holds, its name and size, and the groups and entities associated with it.

**GET** `/v1/files/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/files/123
```

```json Response
HTTP/1.1 200

{
  "data": {
    "id": "123",
    "type": "files",
    "attributes": {
      "content_type": "application/PDF",
      "bytes": 256201,
      "name": "Sample.pdf",
      "created_at": "2014-06-20T20:55:07Z"
    },
    "relationships": {
      "associated_groups": {
        "links": {
          "self": "/v1/files/123/relationships/associated_groups",
          "related": "/v1/files/123/associated_groups"
        },
        "data": [
          {
            "type": "groups",
            "id": "1234"
          },
          {
            "type": "groups",
            "id": "5678"
          }
        ]
      },
      "associated_entities": {
        "links": {
          "self": "/v1/files/123/relationships/associated_entities",
          "related": "/v1/files/123/associated_entities"
        },
        "data": [
          {
            "type": "entities",
            "id": "10000"
          },
          {
            "type": "entities",
            "id": "10001"
          }
        ]
      }
    },
    "links": {
      "self": "/v1/files/123"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success
- `400 Bad Request`: "include" query parameter not allowed
- `403 Forbidden`: Lacking files read permission

## Get all files and/or folders

Retrieves a list of all files and/or folders you have permission to access, as well as details about when each was created, the type of content it holds, its name and size, and the groups and entities associated with it.

**GET** `/v1/files`

**Example to get all files:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/files
```

```json Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "123",
      "type": "files",
      "attributes": {
        "content_type": "application/PDF",
        "bytes": 256201,
        "name": "Sample.pdf",
        "created_at": "2014-06-20T20:55:07Z"
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/123/relationships/associated_groups",
            "related": "/v1/files/123/associated_groups"
          },
          "data": [
            {
              "type": "groups",
              "id": "1234"
            },
            {
              "type": "groups",
              "id": "5678"
            }
          ]
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/123/relationships/associated_entities",
            "related": "/v1/files/123/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "10000"
            },
            {
              "type": "entities",
              "id": "10001"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/123"
      }
    },
    {
      "id": "345",
      "type": "files",
      "attributes": {
        "content_type": "application/PDF",
        "bytes": 798121,
        "name": "Report.pdf",
        "created_at": "2014-06-20T20:55:19Z"
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/345/relationships/associated_groups",
            "related": "/v1/files/345/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/345/relationships/associated_entities",
            "related": "/v1/files/345/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "123400"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/345"
      }
    }
  ],
  "links": {
    "next": null
  }
}
```

**Example to get all folders:**

```Text Request
GET https://examplefirm.addepar.com/api/v1/files?filter[files][includedObjects]=FOLDERS_ONLY
```

```Text Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "5",
      "type": "files",
      "attributes": {
        "name": "folder1",
        "created_at": "2014-08-12T21:15:56Z",
        "modified_at": "2014-08-12T21:15:56Z",
        "is_folder": true,
        "parent_folder_id": 0
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/5/relationships/associated_groups",
            "related": "/v1/files/5/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/5/relationships/associated_entities",
            "related": "/v1/files/5/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "22"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/5"
      }
    },
    {
      "id": "7",
      "type": "files",
      "attributes": {
        "name": "folder2",
        "created_at": "2014-08-12T21:38:59Z",
        "modified_at": "2014-08-12T21:38:59Z",
        "is_folder": true,
        "parent_folder_id": 0
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/7/relationships/associated_groups",
            "related": "/v1/files/7/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/7/relationships/associated_entities",
            "related": "/v1/files/7/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "22"
            },
            {
              "type": "entities",
              "id": "151"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/7"
      }
    },
    {
      "id": "11",
      "type": "files",
      "attributes": {
        "name": "folder3",
        "created_at": "2014-08-12T21:38:58Z",
        "modified_at": "2014-12-02T19:40:25Z",
        "is_folder": true,
        "parent_folder_id": 0
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/11/relationships/associated_groups",
            "related": "/v1/files/11/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/11/relationships/associated_entities",
            "related": "/v1/files/11/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "22"
            },
            {
              "type": "entities",
              "id": "151"
            },
            {
              "type": "entities",
              "id": "183"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/11"
      }
    },
    {
      "id": "12",
      "type": "files",
      "attributes": {
        "name": "folder4",
        "created_at": "2014-08-12T21:15:57Z",
        "modified_at": "2014-08-12T21:15:57Z",
        "is_folder": true,
        "parent_folder_id": 0
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/12/relationships/associated_groups",
            "related": "/v1/files/12/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/12/relationships/associated_entities",
            "related": "/v1/files/12/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "22"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/12"
      }
    },
    {
      "id": "13",
      "type": "files",
      "attributes": {
        "name": "folder5",
        "created_at": "2014-12-01T21:22:40Z",
        "modified_at": "2014-12-01T21:24:00Z",
        "is_folder": true,
        "parent_folder_id": 0
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/13/relationships/associated_groups",
            "related": "/v1/files/13/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/13/relationships/associated_entities",
            "related": "/v1/files/13/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "183"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/13"
      }
    }
  ],
  "included": [],
  "links": {
    "next": null
  }
}
```

**Response Codes**

- `200 OK`: Success
- `400 Bad Request`: "include" query parameter not allowed or not valid
- `403 Forbidden`: Lacking files read permission

## Get files and/or folders from within a folder

Retrieve information for files or folders you have permission to access within a specific folder, including creation date, name, and associated groups and entities.

**GET** `/v1/files`

**Example:**

```Text Request
GET https://examplefirm.addepar.com/api/v1/files?filter[files][includedObjects]=FILES_AND_FOLDERS&filter[files][parentFolderId]=12345
```

```Text Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "5",
      "type": "files",
      "attributes": {
        "content_type": "image/png",
        "bytes": 37909,
        "name": "bleed.png",
        "created_at": "2014-08-12T21:15:56Z",
        "modified_at": "2014-08-12T21:15:56Z",
        "is_folder": false,
        "parent_folder_id": 12345
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/5/relationships/associated_groups",
            "related": "/v1/files/5/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/5/relationships/associated_entities",
            "related": "/v1/files/5/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "22"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/5"
      }
    },
    {
      "id": "7",
      "type": "files",
      "attributes": {
        "content_type": "image/png",
        "bytes": 6859,
        "name": "cutoff.png",
        "created_at": "2014-08-12T21:38:59Z",
        "modified_at": "2014-08-12T21:38:59Z",
        "is_folder": false,
        "parent_folder_id": 12345
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/7/relationships/associated_groups",
            "related": "/v1/files/7/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/7/relationships/associated_entities",
            "related": "/v1/files/7/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "22"
            },
            {
              "type": "entities",
              "id": "151"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/7"
      }
    },
    {
      "id": "11",
      "type": "files",
      "attributes": {
        "content_type": "image/png",
        "bytes": 30834,
        "name": "is.png",
        "created_at": "2014-08-12T21:38:58Z",
        "modified_at": "2014-12-02T19:40:25Z",
        "is_folder": false,
        "parent_folder_id": 12345
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/11/relationships/associated_groups",
            "related": "/v1/files/11/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/11/relationships/associated_entities",
            "related": "/v1/files/11/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "22"
            },
            {
              "type": "entities",
              "id": "151"
            },
            {
              "type": "entities",
              "id": "183"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/11"
      }
    },
    {
      "id": "12",
      "type": "files",
      "attributes": {
        "content_type": "image/png",
        "bytes": 9553,
        "name": "header.png",
        "created_at": "2014-08-12T21:15:57Z",
        "modified_at": "2014-08-12T21:15:57Z",
        "is_folder": false,
        "parent_folder_id": 12345
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/12/relationships/associated_groups",
            "related": "/v1/files/12/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/12/relationships/associated_entities",
            "related": "/v1/files/12/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "22"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/12"
      }
    },
    {
      "id": "13",
      "type": "files",
      "attributes": {
        "name": "folder1",
        "created_at": "2014-12-01T21:22:40Z",
        "modified_at": "2014-12-01T21:24:00Z",
        "deleted_at": "2021-05-28T12:24:00Z",
        "is_folder": true,
        "parent_folder_id": 12345
      },
      "relationships": {
        "associated_groups": {
          "links": {
            "self": "/v1/files/13/relationships/associated_groups",
            "related": "/v1/files/13/associated_groups"
          },
          "data": []
        },
        "associated_entities": {
          "links": {
            "self": "/v1/files/13/relationships/associated_entities",
            "related": "/v1/files/13/associated_entities"
          },
          "data": [
            {
              "type": "entities",
              "id": "183"
            }
          ]
        }
      },
      "links": {
        "self": "/v1/files/13"
      }
    }
  ],
  "included": [],
  "links": {
    "next": null
  }
}

```

**Response codes**

- `200 OK`: Success
- `400 Bad Request`: "include" query parameter not allowed
- `403 Forbidden`: Lacking files read permission

## Download a file

Retrieves the raw contents of a specific file.

**GET** `/v1/files/:id/download`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/files/123/download
```

```json Response
HTTP/1.1 200

Content-DispositionL attachment; filename="Sample.pdf"
Content-Type: application/binary

<RAW_FILE_DATA>
```

**Response Codes**

- `200 OK`: Success
- `403 Forbidden`: Lacking files read permission
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Get an archived file

Retrieves an archived (deleted) file, as well as information about when it was created, the type of content it holds, its name and size, the groups and entities associated with it, and when it was deleted.

**GET** `/v1/archive/files/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/archive/files/319
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"319",
    "type":"files",
    "attributes":{
      "content_type":"text/plain",
      "bytes":21607,
      "name":"archived_transactions.csv",
      "created_at":"2017-03-15T20:31:49Z",
      "deleted_at":"2017-03-15T20:32:16Z"
    },
    "relationships":{
      "associated_groups":{
        "links":{
          "self":"/v1/archive/files/319/relationships/associated_groups",
          "related":"/v1/archive/files/319/associated_groups"
        },
        "data":[

        ]
      },
      "associated_entities":{
        "links":{
          "self":"/v1/archive/files/319/relationships/associated_entities",
          "related":"/v1/archive/files/319/associated_entities"
        },
        "data":[
          {
            "type":"entities",
            "id":"22"
          }
        ]
      }
    },
    "links":{
      "self":"/v1/archive/files/319"
    }
  }
}
```

**Response Codes**

- `200 OK`: Success
- `400 Bad Request`: "include" query parameter not allowed
- `403 Forbidden`: Lacking files read permission

## Get all archived files and/or folders

Retrieves a list of all archived (deleted) files and/or folders, as well as information about when each was created, the type of content it holds, its name and size, the groups and entities associated with it, and when it was deleted.

**GET** `/v1/archive/files`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/archive/files
```

```json Response
HTTP/1.1 200

{
  "data":[
    {
      "id":"319",
      "type":"files",
      "attributes":{
        "content_type":"text/plain",
        "bytes":21607,
        "name":"archived_transactions.csv",
        "created_at":"2017-03-15T20:31:49Z",
        "deleted_at":"2017-03-15T20:32:16Z"
      },
      "relationships":{
        "associated_groups":{
          "links":{
            "self":"/v1/archive/files/319/relationships/associated_groups",
            "related":"/v1/archive/files/319/associated_groups"
          },
          "data":[

          ]
        },
        "associated_entities":{
          "links":{
            "self":"/v1/archive/files/319/relationships/associated_entities",
            "related":"/v1/archive/files/319/associated_entities"
          },
          "data":[
            {
              "type":"entities",
              "id":"22"
            }
          ]
        }
      },
      "links":{
        "self":"/v1/archive/files/319"
      }
    }
  ],
  "links":{
    "next":null
  }
}
```

**Example request to get all archived folders:**

```Text Request
GET https://examplefirm.addepar.com/api/v1/archive/files?filter[files][includedObjects]=FOLDERS_ONLY
```

**Response Codes**

- `200 OK`: Success
- `400 Bad Request`: "include" query parameter not allowed
- `403 Forbidden`: Lacking files read permission

## Get archived files and/or folders within a folder

Retrieves archived (deleted) files and/or folders within a specified folder, as well as information about when it was created, the type of content it holds, its name, the groups and entities associated with it, and when it was deleted.

**GET** `/v1/archive/files`

**Example:**

```Text Request
GET https://examplefirm.addepar.com/api/v1/archive/files?filter[files][includedObjects]=FOLDERS_ONLY&filter[files][parentFolderId]=319
```

**Response Codes**

- `200 OK`: Success
- `400 Bad Request`: "include" query parameter not allowed
- `403 Forbidden`: Lacking files read permission

## Download an archived file

Retrieves the raw contents of an archived file.

**GET** `/v1/archive/files/:id/download`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/archive/files/319/download
```

```json Response
HTTP/1.1 200

Content-Disposition: attachment; filename="Sample.pdf"
Content-Type: application/binary

<RAW_FILE_DATA>
```

**Response Codes**

- `200 OK`: Success
- `403 Forbidden`: Lacking files read permission
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Get all groups associated with a file

Retrieves the full object of groups associated with the file.

**GET** `/v1/files/:id/relationships/associated_groups`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/files/123/relationships/associated_groups
```

```json Response
HTTP/1.1 200

{
  "links":{
    "self":"/v1/files/123/relationships/associated_groups",
    "related":"/v1/files/123/associated_groups"
  },
  "data":[
    {
      "type":"groups",
      "id":"1234"
    },
    {
      "type":"groups",
      "id":"5678"
    }
  ]
}
```

**Response Codes**

- `200 OK`: Success
- `403 Forbidden`: Lacking file read permission or API permission
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Get all entities associated with a file

Retrieves the full object of entities associated with the file.

**GET** `/v1/files/:id/relationships/associated_entities`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/files/123/relationships/associated_entities
```

```json Response
HTTP/1.1 200

{
  "links":{
    "self":"/v1/files/123/relationships/associated_entities",
    "related":"/v1/files/123/associated_entities"
  },
  "data":[
    {
      "type":"entities",
      "id":"10000"
    },
    {
      "type":"entities",
      "id":"10001"
    }
  ]
}
```

**Response Codes**

- `200 OK`: Success
- `403 Forbidden`: Lacking file read permission or API permission
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Create a file

Adds a new file to your firm. You can specify the name of the file and the groups and entities associated with the file.

> ❗️
>
> The file extension provided in the metadata must match the file extension of filename in "Content-Disposition".

**POST** `/v1/files/`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/files
Content-Type: multipart/form-data; boundary=<UNIQUE_BOUNDARY>
Content-Length: 2198

--<UNIQUE_BOUNDARY>
Content-Disposition: form-data; name="file"; file name="Sample.txt"
Content-Type: text/plain

<RAW_FILE_DATA>

--<UNIQUE_BOUNDARY>
Content-Disposition: form-data; name="metadata"

{
  "data":{
    "type":"files",
    "attributes":{
      "name":"Sample.txt"
    }
  }
}
--<UNIQUE_BOUNDARY>--
```

```json Response
HTTP/1.1 201 Created

{
  "data": {
	"id": 1111,
    "type": "files",
    "attributes": {
      "content_type": "application/PDF",
      "bytes": 256201,
      "name": "Sample.txt",
      "created_at": "2017-01-01T20:55:07Z"
    },
    "relationships": {
      "associated_groups": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_groups",
          "related": "/v1/files/111113/associated_groups"
        },
        "data": []
      },
      "associated_entities": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_entities",
          "related": "/v1/files/1111/associated_entities"
        },
        "data": []
      }
    },
    "links": {
      "self": "/v1/files/1111"
    }
  }
}
```

**Response Codes**

- `200 OK`: Successfully created the file
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups,\
  or file is missing
- `403 Forbidden`: Lacking file write permission or API permission

## Create a file in a folder

When uploading a file to a top-level folder that has nested folders, set "parent_folder_id = 0" and include the portfolio relationship node in the request.

When uploading a file to a nested folder, you can either:

- Identify the parent folder by its ID. You don't need to provide the portfolio relationship because it's inherited from the parent folder. You can specify the file's name and the groups and entities associated with it.
- Specify the file path using the optional `file_path` parameter. As long as the file path is a unique series of folder names, your file will be uploaded to the intended file path.

| Optional parameter | Description                                              | Example                              |
| :----------------- | :------------------------------------------------------- | :----------------------------------- |
| `file_path`        | Specifies where a file is in a folder structure. String. | `"file_path": "Sample/Folder/Path/"` |

**POST** `/v1/files/`

**Example using parent folder ID:**

```Text Request
POST https://examplefirm.addepar.com/api/v1/files
Content-Type: multipart/form-data; boundary=<UNIQUE_BOUNDARY>
Content-Length: 2198

--<UNIQUE_BOUNDARY>
Content-Disposition: form-data; name="file"; file name="Sample.txt"
Content-Type: text/plain

<RAW_FILE_DATA>

--<UNIQUE_BOUNDARY>
Content-Disposition: form-data; name="metadata"

{
  "data":{
    "type":"files",
    "attributes":{
      "name":"Sample.txt",
	“parent_folder_id”: 12345
    }
  }
}
--<UNIQUE_BOUNDARY>--
```

```Text Response
{
  "data": {
	"id": 1111,
    "type": "files",
    "attributes": {
      "content_type": "application/PDF",
      "bytes": 256201,
      "name": "Sample.txt",
      "created_at": "2017-01-01T20:55:07Z",
	“is_folder”: false,
	“parent_folder_id”: 12345
    },
    "relationships": {
      "associated_groups": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_groups",
          "related": "/v1/files/111113/associated_groups"
        },
        "data": []
      },
      "associated_entities": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_entities",
          "related": "/v1/files/1111/associated_entities"
        },
        "data": []
      }
    },
    "links": {
      "self": "/v1/files/1111"
    }
  }
}
```

**Example using file path string:**

```Text Request
POST https://examplefirm.addepar.com/api/v1/files
Content-Type: multipart/form-data; boundary=<UNIQUE_BOUNDARY>
Content-Length: 2198

--<UNIQUE_BOUNDARY>
Content-Disposition: form-data; name="file"; file name="Sample.txt"
Content-Type: text/plain

<RAW_FILE_DATA>

--<UNIQUE_BOUNDARY>
Content-Disposition: form-data; name="metadata"

{
  "data":{
    "type":"files",
    "attributes":{
      "name":"Sample.txt",
	"file_path": "Sample/Folder/Path/"
    }
  }
}
--<UNIQUE_BOUNDARY>--
```

```Text Response
{
  "data": {
	"id": 1111,
    "type": "files",
    "attributes": {
      "content_type": "application/PDF",
      "bytes": 256201,
      "name": "Sample.txt",
      "created_at": "2017-01-01T20:55:07Z",
	“is_folder”: false,
	“parent_folder_id”: 12345
    },
    "relationships": {
      "associated_groups": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_groups",
          "related": "/v1/files/111113/associated_groups"
        },
        "data": []
      },
      "associated_entities": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_entities",
          "related": "/v1/files/1111/associated_entities"
        },
        "data": []
      }
    },
    "links": {
      "self": "/v1/files/1111"
    }
  }
```

**Response codes**

- `200 OK`: Successfully created the file
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups,\
  or file is missing
- `403 Forbidden`: Lacking file write permission or API permission

## Associate groups with a file

Adds to the list of groups associated to the file.

**POST** `/v1/files/:id/relationships/associated_groups`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/files/123/relationships/associated_groups

{
  "data":[
    {
      "type":"groups",
      "id":"200"
    },
    {
      "type":"groups",
      "id":"201"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response Codes**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups
- `403 Forbidden`: Lacking file write permission or complete access to file and all entities/groups\
  related to file
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Associate entities with a file

Adds to the list of entities associated to the file.

**POST** `/v1/files/:id/relationships/associated_entities`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/files/123/relationships/associated_entities

{
  "data":[
    {
      "type":"entities",
      "id":"100"
    },
    {
      "type":"entities",
      "id":"101"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response Codes**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups
- `403 Forbidden`: Lacking file write permission or complete access to file and all entities/groups\
  related to file
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Update a file

Updates the attributes and relationships for a specific file.

**PATCH** `/v1/files/:id`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/files/1111

{
  "data":{
    "id":1111,
    "type":"files",
    "attributes":{
      "name":"RenamedFile.txt"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "data": {
	"id": 1111,
    "type": "files",
    "attributes": {
      "content_type": "application/PDF",
      "bytes": 256201,
      "name": "RenamedFile.txt",
      "created_at": "2017-01-01T20:55:07Z"
    },
    "relationships": {
      "associated_groups": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_groups",
          "related": "/v1/files/111113/associated_groups"
        },
        "data": []
      },
      "associated_entities": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_entities",
          "related": "/v1/files/1111/associated_entities"
        },
        "data": []
      }
    },
    "links": {
      "self": "/v1/files/1111"
    }
  }
}
```

**Response Codes**

- `200 OK`: Successfully modified the file
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups
- `403 Forbidden`: Lacking file write permission or complete access to file and all entities/groups\
  related to file
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Replace groups associated with a file

Replaces all groups currently associated with different groups.

**PATCH** `/v1/files/:id/relationships/associated_groups`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/files/123/relationships/associated_groups

{
  "data":[
    {
      "type":"groups",
      "id":"200"
    },
    {
      "type":"groups",
      "id":"201"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**ResponseCodes**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups
- `403 Forbidden`: Lacking file write permission or complete access to file and all entities/groups\
  related to file
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Replace entities associated with a file

Replaces all entities currently associated with different entities.

**PATCH** `/v1/files/:id/relationships/associated_entities`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/files/123/relationships/associated_entities

{
  "data":[
    {
      "type":"entities",
      "id":"100"
    },
    {
      "type":"entities",
      "id":"101"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups
- `403 Forbidden`: Lacking file write permission or complete access to file and all entities/groups\
  related to file
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Move a file or folder to another folder

Move any file to a specific folder. You can also move a folder into another folder.

**PATCH** `/v1/files/:id`

**Example:**

```Text Request
PATCH https://examplefirm.addepar.com/api/v1/files/1111

{
  "data":{
    "id":1111,
    "type":"files",
    "attributes":{
      "parent_folder_id":54321
    }
  }
}
```

```Text Response
{
  "data": {
	"id": 1111,
    "type": "files",
    "attributes": {
      "content_type": "application/PDF",
      "bytes": 256201,
      "name": "Sample.txt",
      "created_at": "2017-01-01T20:55:07Z",
	“is_folder”: false,
	“parent_folder_id”: 54321
    },
    "relationships": {
      "associated_groups": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_groups",
          "related": "/v1/files/111113/associated_groups"
        },
        "data": []
      },
      "associated_entities": {
        "links": {
          "self": "/v1/files/1111/relationships/associated_entities",
          "related": "/v1/files/1111/associated_entities"
        },
        "data": []
      }
    },
    "links": {
      "self": "/v1/files/1111"
    }
  }
}
```

**Response codes**

- `200 OK`: Successfully created the file
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups
- `403 Forbidden`: Lacking file write permission or API permission

## Delete a file or folder

Archives a file available in Addepar or a folder and everything in it. The archived file or folder and its associated metadata will remain available through separate routes. You can retrieve archived folders and their associated metadata via API.

**DELETE** `/v1/files/:id`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/files/1111
```

```json Response
HTTP/1.1 204 No Content
```

**Response Codes**

- `204 No Content`: Success
- `403 Forbidden`: Lacking file write permission or complete access to file and all entities/groups\
  related to file
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Remove groups associated with a file

Removes the list of groups specified from the file associations.

**DELETE** `/v1/files/:id/relationships/associated_groups`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/files/123/relationships/associated_groups

{
  "data":[
    {
      "type":"entities",
      "id":"10000"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response Codes**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups
- `403 Forbidden`: Lacking file write permission or complete access to file and all entities/groups\
  related to file
- `404 Not Found`: Nonexistent/non-permissioned file ID

## Remove entities associated with a file

Removes the list of entities specified from the file associations.

**DELETE** `/v1/files/:id/relationships/associated_entities`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/files/123/relationships/associated_entities

{
  "data":[
    {
      "type":"entities",
      "id":"10000"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response Codes**

- `204 No Content`: Success
- `400 Bad Request`: Invalid payload such as non-permissioned entities and groups
- `403 Forbidden`: Lacking file write permission or complete access to file and all entities/groups\
  related to file
- `404 Not Found`: Nonexistent/non-permissioned file ID
