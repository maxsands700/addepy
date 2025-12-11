# Groups

Groups are a collection of entities in Addepar. Use the Groups API to create and delete groups in Addepar, and retrieve and update group details.
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base route",
"0-1": "/v1/groups",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/groups \n/v1/groups/:id \n/v1/groups/:id/relationships/members \n/v1/groups/:id/members \n/v1/groups/:id/child_groups \n \n**POST** \n/v1/groups \n/v1/groups/:id/relationships/members \n/v1/groups/:id/relationships/child_groups \n/v1/groups/query \n \n**PATCH** \n/v1/groups/:id \n/v1/groups \n/v1/groups/:id/relationships/members \n /v1/groups/:id/relationships/child_groups \n \n**DELETE** \nv1/groups/:id \n/v1/groups \n/v1/groups/:id/relationships/members",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Portfolio Access\" determines the groups that are accesible and entities that can be added as members. \n \n\"Groups: Manage all groups\" is required to create, edit, and delete groups. \n \n\"Manage Attributes: Only edit certain attribute values or Manage all values and settings” is required to apply, edit, or delete attributes.",
"5-0": "OAuth scopes",
"5-1": "`GROUPS` or `GROUPS_WRITE`"
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

Groups are described by the below resource object attributes. Attributes required for creating, updating, or deleting Groups are noted. You can assign additional standard and custom attributes to Groups.

All attributes will be returned in successful **GET**, **POST** & **PATCH** responses.

| Attribute           | Description                                     | Example                                                                              |
| :------------------ | :---------------------------------------------- | :----------------------------------------------------------------------------------- |
| `name`              | Group name. String. Required.                   | `"Smith Family"`                                                                     |
| `created_at`        | Not editable and cannot be passed in. String.   | `"2023-07-28T02:24:30Z"`                                                             |
| `modified_at`       | Not editable and cannot be passed in. String.   | `"2023-07-30T10:43:21Z"`                                                             |
| Optional Attributes | Additional attributes can be applied to groups. | See ["Addepar Attributes"](https://developers.addepar.com/docs/addepar-attributes-1) |

## Relationships

[block:parameters]
{
"data": {
"h-0": "Relationship",
"h-1": "Description",
"0-0": "`members`",
"0-1": "A group can consist of one or more of the following portfolios: \n \n- Client (`PERSON_NODE`)\n- Managed fund (`MANAGED_PARTNERSHIP`)\n- Trust (`TRUST`)\n- Holding company (`HOLDING_COMPANY`)\n- Holding account (`FINANCIAL_ACCOUNT`)It is guaranteed that the array does not contain duplicates.",
"1-0": "`group_type`",
"1-1": "A group type is a way to categorize a group and adjust access to the group's members. A group's type must be specified during creation. The standard value is \\``GROUPS`, which represents out of the box Addepar groups.",
"2-0": "`child_groups`",
"2-1": "A nested member of the group that enables groups within a group."
},
"cols": 2,
"rows": 3,
"align": [
"left",
"left"
]
}
[/block]

```json Relationships
"relationships": {
        "members": {
          "links": {
            "self": "/v1/groups/100/relationships/members",
            "related": "/v1/groups/100/members"
          },
          "data": [
            { "type": "entities", "id": "200" },
            { "type": "entities", "id": "204" },
            { "type": "entities", "id": "360" },
            { "type": "entities", "id": "486" }
          ]
        },
        "group_type": {
          "links": {
            "self": "/v1/groups/100/relationships/group_type",
             "related": "/v1/groups/100/group_type"
          },
          "data": {
            "type": "group_types",
            "id": "GROUPS"
          }
        },
        "child_groups": {
          "links": {
            "self": "/v1/groups/100/relationships/child_groups",
            "related": "/v1/groups/100/child_groups"
          },
          "data": []
        }
      }
```

## Get all groups

Retrieves all groups you have access to. Returns attributes for each group, as well as a list of all entities within each group.

**GET** `/v1/groups`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/groups
```

```json Response
HTTP/1.1 200

{
   "data":[
      {
         "type":"groups",
         "id":"100",
         "attributes":{
            "name":"Group 1",
            "created_at": "2023-07-28T02:24:30Z",
          	"modified_at": "2023-07-30T10:43:21Z"
         },
         "relationships":{
            "members":{
               "links":{
                  "self":"/v1/groups/100/relationships/members",
                  "related":"/v1/groups/100/members"
               },
               "data":[
                  {
                     "type":"entities",
                     "id":"200"
                  },
                  {
                     "type":"entities",
                     "id":"204"
                  },
                  {
                     "type":"entities",
                     "id":"360"
                  },
                  {
                     "type":"entities",
                     "id":"486"
                  }
               ]
            },
            "group_type":{
               "links":{
                  "self":"/v1/groups/100/relationships/group_type",
                  "related":"/v1/groups/100/group_type"
               },
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            },
            "child_groups":{
               "links":{
                  "self":"/v1/groups/100/relationships/child_groups",
                  "related":"/v1/groups/100/child_groups"
               },
               "data":[

               ]
            }
         },
         "links":{
            "self":"/v1/groups/100"
         }
      },
      {
         "type":"groups",
         "id":"101",
         "attributes":{
            "name":"Group 2",
           	"created_at": "2023-07-28T02:24:30Z",
          	"modified_at": "2023-07-30T10:43:21Z"
         },
         "relationships":{
            "members":{
               "links":{
                  "self":"/v1/groups/101/relationships/members",
                  "related":"/v1/groups/101/members"
               },
               "data":[
                  {
                     "type":"entities",
                     "id":"102"
                  },
                  {
                     "type":"entities",
                     "id":"289"
                  },
                  {
                     "type":"entities",
                     "id":"349"
                  },
                  {
                     "type":"entities",
                     "id":"438"
                  }
               ]
            },
            "group_type":{
               "links":{
                  "self":"/v1/groups/101/relationships/group_type",
                  "related":"/v1/groups/101/group_type"
               },
               "data":{
                  "type":"group_types",
                  "id":"HH_GROUPS"
               }
            },
            "child_groups":{
               "links":{
                  "self":"/v1/groups/101/relationships/child_groups",
                  "related":"/v1/groups/101/child_groups"
               },
               "data":[
                  {
                     "type":"groups",
                     "id":"102"
                  }
               ]
            }
         },
         "links":{
            "self":"/v1/groups/101"
         }
      }
   ],
   "included":[

   ]
}
```

**Optional parameters**
[block:parameters]
{
"data": {
"h-0": "Filter",
"h-1": "Description",
"h-2": "Example",
"0-0": "group_types",
"0-1": "Returns only groups matching group type ID specified.",
"0-2": "`filter[group_types]=\"Advisor Group\"`",
"1-0": "created_before",
"1-1": "Returns all groups created on or before a date, formatted as YYYY-MM-DD.",
"1-2": "`filter[created_before]=\"2023-04-12\"`",
"2-0": "created_after",
"2-1": "Returns all groups created on or after a date, formatted as YYYY-MM-DD.",
"2-2": "`filter[created_after]=\"2023-04-12\"`",
"3-0": "modified_before",
"3-1": "Returns all groups last modified on or before a date, formatted as YYYY-MM-DD.",
"3-2": "`filter[modified_before]=\"2023-04-12\"`",
"4-0": "modified_after",
"4-1": "Returns all groups last modified on or after a date, formatted as YYYY-MM-DD.",
"4-2": "`filter[modified_after]=\"2023-04-12\"`",
"5-0": "ids",
"5-1": "Returns all groups matching the group IDs specified",
"5-2": "`filter[ids]=1,2,3`",
"6-0": "fields[groups]",
"6-1": "Returns only the attributes specified for each group. Ignores spaces. \n \nYou can filter by `fields[groups]=[]` to omit all attributes.",
"6-2": "`fields[groups]=name`"
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

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: You do not have permission to access the API
- `404 Not Found`: The group does not exist or you do not have access to it

## Get a group

Retrieves a specific group based on its ID. Returns all group attributes, as well as a list of all members within the group.

**GET** `/v1/groups/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/groups/5
```

```json Response
HTTP/1.1 200

{
   "data":{
      "type":"groups",
      "id":"5",
      "attributes":{
         "name":"Group 1",
          "created_at": "2023-07-28T02:24:30Z",
         "modified_at": "2023-07-30T10:43:21Z"
      },
      "relationships":{
         "members":{
            "links":{
               "self":"/v1/groups/5/relationships/members",
               "related":"/v1/groups/5/members"
            },
            "data":[
               {
                  "type":"entities",
                  "id":"22"
               },
               {
                  "type":"entities",
                  "id":"24"
               },
               {
                  "type":"entities",
                  "id":"117"
               }
            ]
         },
         "group_type":{
            "links":{
               "self":"/v1/groups/5/relationships/group_type",
               "related":"/v1/groups/5/group_type"
            },
            "data":{
               "type":"group_types",
               "id":"GROUPS"
            }
         },
         "child_groups":{
            "links":{
               "self":"/v1/groups/5/relationships/child_groups",
               "related":"/v1/groups/5/child_groups"
            },
            "data":[
               {
                  "type":"groups",
                  "id":"6"
               }
            ]
         }
      },
      "links":{
         "self":"/v1/groups/5"
      }
   },
   "included":[

   ]
}
```

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload
- `403 Forbidden`: You do not have permission to access the API
- `404 Not Found`: The group does not exist or you do not have access to it

## Get a group's members

Returns a list of all relationships for the portfolios in the specified group.

**GET** `/v1/groups/:id/relationships/members`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/groups/5678/relationships/members
```

```json Response
HTTP/1.1 200

{
  "data": [
    {
       "type": "entities",
       "id": "2000001"
     },
     {
       "type": "entities",
       "id": "2000002"
     }
  ]
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: You do not have permission to access the API
- `404 Not Found`: The group does not exist or you do not have access to it.

## Get a group's member details

Returns details of all the entities that are members of the specified group. Refer to the Entities API for details about the supported attributes and relationships, including sample responses.

**GET** `/v1/groups/:id/members`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/groups/5678/members
```

```json Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "2000001",
      "type": "entities",
      "attributes": {
        "currency_factor": "USD",
        "original_name": "Adam Smith",
        "model_type": "PERSON_NODE"
      },
      "links": {
        "self": "/v1/entities/2000001"
      }
    },
    {
      "id": "2000002",
      "type": "entities",
      "attributes": {
        "currency_factor": "USD",
        "ownership_type": "PERCENT_BASED",
        "original_name": "X092849032",
        "display_name": "Citco",
        "model_type": "FINANCIAL_ACCOUNT",
        "is_rolled_up": false
      },
      "links": {
        "self": "/v1/entities/2000002"
      }
    }
  ],
  "links": {
    "next": null
  }
}
```

**Response codes:**

- `200 OK`: Success
- `403 Forbidden`: You do not have permission to access the API
- `404 Not Found`: The group does not exist or you do not have access to it

## Get a group's child groups

Retrieve a group's child groups.

**GET** `/v1/groups/:id/child_groups `

**Example:**

```curl Request
GET https://examplefirm.addepar.com/v1/groups/1/child_groups
```

```json Response
HTTP/1.1 200

{
   "data":[
      {
         "id":"92",
         "type":"groups",
         "attributes":{
            "name":"Child Group",
            "created_at": "2023-07-28T02:24:30Z",
          	"modified_at": "2023-07-30T10:43:21Z"
         },
         "relationships":{
            "members":{
               "links":{
                  "self":"/v1/groups/92/relationships/members",
                  "related":"/v1/groups/92/members"
               },
               "data":[
                  {
                     "type":"entities",
                     "id":"12"
                  }
               ]
            },
            "child_groups":{
               "links":{
                  "self":"/v1/groups/92/relationships/child_groups",
                  "related":"/v1/groups/92/child_groups"
               },
               "data":[

               ]
            },
            "group_type":{
               "links":{
                  "self":"/v1/groups/92/relationships/group_type",
                  "related":"/v1/groups/92/group_type"
               },
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            }
         },
         "links":{
            "self":"/v1/groups/92"
         }
      }
   ],
   "included":[

   ],
   "links":{
      "next":null
   }
}
```

**Response codes:**

- `200 Ok`: Success
- `403 Forbidden`: You do not have permission to access the API
- `404 Not Found`: The child group does not exist or you do not have access to it

## Create a group

Adds a new group to your firm. You must specify the `type`, `name`, and `group_type` of the group.

Returns the details of the new group.

**POST** `/v1/groups`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/groups

{
   "data":{
      "type":"groups",
      "attributes":{
         "name":"New Group"
      },
      "relationships":{
         "group_type":{
            "data":{
               "type":"group_types",
               "id":"GROUPS"
            }
         }
      }
   }
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":{
      "id":"1494728",
      "type":"groups",
      "attributes":{
         "name":"New Group"
      },
      "relationships":{
         "members":{
            "links":{
               "self":"/v1/groups/1494728/relationships/members",
               "related":"/v1/groups/1494728/members"
            },
            "data":[

            ]
         },
         "child_groups":{
            "links":{
               "self":"/v1/groups/1494728/relationships/child_groups",
               "related":"/v1/groups/1494728/child_groups"
            },
            "data":[

            ]
         },
         "group_type":{
            "links":{
               "self":"/v1/groups/1494728/relationships/group_type",
               "related":"/v1/groups/1494728/group_type"
            },
            "data":{
               "type":"group_types",
               "id":"GROUPS"
            }
         }
      },
      "links":{
         "self":"/v1/groups/1494728"
      }
   },
   "included":[

   ]
}
```

**Response codes:**

- `201 Created`: Success
- `400 Bad Request`: Invalid payload; an entity included either does not exist, or you do not have access to it or the group_type ID does not exist, or you do not have access to it
- `403 Forbidden`: You do not have permission to access the API, or you can't modify a passed in attribute
- `404 Not Found`: You don't have access to one or more group members or one or more members don't exist, or one or more attributes don't exist
- `409 Conflict`: "Type" was not specified as "groups" or one or more members were not specified as "entities"

## Create a child group

Adds a new child group to an existing group.

**POST** `/v1/groups/:id/relationships/child_groups `

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/groups/1/relationships/child_groups

{
  "data": [
    {
      "type": "groups",
      "id": "92"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `201 OK`: Success
- `403 Forbidden`: You do not have permission to access the API
- `404 Not Found`: The group does not exist or you do not have access to it

## Create multiple groups

Adds a new group to your firm. You must specify the `type`, `name`, and `group_type` of the group.

Returns the details of each group created.

**POST** `/v1/groups/`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/groups

{
   "data":[
      {
         "type":"groups",
         "attributes":{
            "name":"Group 1"
         },
         "relationships":{
            "members":{
               "data":[
                  {
                     "type":"entities",
                     "id":"34"
                  },
                  {
                     "type":"entities",
                     "id":"219"
                  }
               ]
            },
            "group_type":{
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            }
         }
      },
      {
         "type":"groups",
         "attributes":{
            "name":"Group 2"
         },
         "relationships":{
            "members":{
               "data":[
                  {
                     "type":"entities",
                     "id":"22"
                  },
                  {
                     "type":"entities",
                     "id":"24"
                  }
               ]
            },
            "group_type":{
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            }
         }
      }
   ]
}
```

```json Response
HTTP/1.1 201 Created

{
   "data":[
      {
         "id":"11",
         "type":"groups",
         "attributes":{
            "name":"Group 1"
         },
         "relationships":{
            "members":{
               "links":{
                  "self":"/v1/groups/11/relationships/members",
                  "related":"/v1/groups/11/members"
               },
               "data":[
                  {
                     "type":"entities",
                     "id":"34"
                  },
                  {
                     "type":"entities",
                     "id":"219"
                  }
               ]
            },
            "group_type":{
               "links":{
                  "self":"/v1/groups/11/relationships/group_type",
                  "related":"/v1/groups/11/group_type"
               },
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            },
            "child_groups":{
               "links":{
                  "self":"/v1/groups/11/relationships/child_groups",
                  "related":"/v1/groups/11/child_groups"
               },
               "data":[

               ]
            }
         },
         "links":{
            "self":"/v1/groups/11"
         }
      },
      {
         "id":"169",
         "type":"groups",
         "attributes":{
            "name":"Group 2"
         },
         "relationships":{
            "members":{
               "links":{
                  "self":"/v1/groups/169/relationships/members",
                  "related":"/v1/groups/169/members"
               },
               "data":[
                  {
                     "type":"entities",
                     "id":"22"
                  },
                  {
                     "type":"entities",
                     "id":"24"
                  }
               ]
            },
            "group_type":{
               "links":{
                  "self":"/v1/groups/169/relationships/group_type",
                  "related":"/v1/groups/169/group_type"
               },
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            },
            "child_groups":{
               "links":{
                  "self":"/v1/groups/169/relationships/child_groups",
                  "related":"/v1/groups/169/child_groups"
               },
               "data":[

               ]
            }
         },
         "links":{
            "self":"/v1/groups/169"
         }
      }
   ],
   "included":[

   ]
}
```

**Response codes:**

- `201 Created`: Success
- `400 Unauthorized`: Invalid payload; or an entity included either does not exist, or you do not have access to it
- `403 Forbidden`: You do not have permission to access the API
- `404 Not Found`: The group_type ID does not exist, or you do not have access to it
- `409 Conflict`: "Type" was not specified as "groups" or one or more members were not specified as "entities"

## Add group members

Adds existing entities as members to a group. Returns an empty response.

**POST** `/v1/groups/:id/relationships/members`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/groups/5678/relationships/members

{
  "data": [
    {
      "type": "entities",
      "id": "100"
    },
    {
      "type": "entities",
      "id": "101"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `400 Bad Request`: One or more group members is not a valid type: client, account, holding company, trust, managed fund
- `403 Forbidden`: You do not have permission to access the API, you don't have access to the group itself, or you do not have access to the type of group
- `404 Not Found`: The group does not exist, or you do not have access to it
- `409 Conflict`: The input type of member is not "entities"

## Search for groups by name, group type, and external ID

For a refined list of results, you can retrieve only groups with a specific display name, group type or external ID.

**POST** `/v1/groups/query`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/groups/query

{
   "data":{
      "type":"group_search",
      "attributes":{
         "display_names":[
            "All",
            "Limited",
            "Group"
         ],
         "group_types":[
            "GROUPS",
            "HOUSEHOLDS"
         ],
         "external_ids":[
            {
               "external_id_type":"random_system",
               "external_id":"34e0ec90-9ebb-4f25-9ee4-b86121c14c67"
            }
         ]
      }
   }
}
```

```json Response
HTTP/1.1 200

{
   "data":[
      {
         "id":"7",
         "type":"groups",
         "attributes":{
            "name":"Limited Clients Access Group",
            "external_id_random_system":"34e0ec90-9ebb-4f25-9ee4-b86121c14c67"
         },
         "relationships":{
            "members":{
               "links":{
                  "self":"/v1/groups/7/relationships/members",
                  "related":"/v1/groups/7/members"
               },
               "data":[

               ]
            },
            "group_type":{
               "links":{
                  "self":"/v1/groups/7/relationships/group_type",
                  "related":"/v1/groups/7/group_type"
               },
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            },
            "child_groups":{
               "links":{
                  "self":"/v1/groups/7/relationships/child_groups",
                  "related":"/v1/groups/7/child_groups"
               },
               "data":[

               ]
            }
         },
         "links":{
            "self":"/v1/groups/7"
         }
      }
   ],
   "included":[

   ],
   "links":{
      "next":null
   }
}
```

**Response codes:**

- `200 OK`: Success
- `400 Forbidden`: Missing or invalid attribute. One of \[`display_names`, `group_types`, `external_ids`] is required.
- `403 Forbidden`: You do not have permission to access the API

## Edit a group

Adds, modifies, or deletes the attributes of an existing group.

**PATCH** `/v1/groups/:id`

**Example:**

This example is for Addepar's Standard Attributes. See [Addepar Attributes](https://developers.addepar.com/docs/addepar-attributes-1) for a Custom Attribute example.

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/groups/1111

{
  "data": {
	"id": "1111"
       "type": "groups",
       "attributes": {
         "name": "Updated Group Name"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
   "data":{
      "id":"1111",
      "type":"groups",
      "attributes":{
         "name":"Updated Group Name"
      },
      "relationships":{
         "members":{
            "links":{
               "self":"/v1/groups/1111/relationships/members",
               "related":"/v1/groups/1111/members"
            },
            "data":[
               {
                  "type":"entities",
                  "id":"2000001"
               },
               {
                  "type":"entities",
                  "id":"2000002"
               }
            ]
         }
      },
      "child_groups":{
         "links":{
            "self":"/v1/groups/169/relationships/child_groups",
            "related":"/v1/groups/169/child_groups"
         },
         "data":[

         ]
      },
      "links":{
         "self":"/v1/groups/1111"
      }
   }
}
```

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload; or an entity included either does not exist, or you do not have access to it
- `403 Forbidden`: You do not have permission to access the API, or you do not have access to the group
- `404 Not Found`: The group ID does not exist, or you do not have access to it

## Edit multiple groups

Adds, modifies, or deletes attributes of existing groups.

**PATCH** `/v1/groups`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/groups

{
   "data":[
      {
         "type":"groups",
         "id":"169",
         "attributes":{
            "name":"Group 1"
         },
         "relationships":{
            "members":{
               "data":[
                  {
                     "type":"entities",
                     "id":"22"
                  },
                  {
                     "type":"entities",
                     "id":"117"
                  }
               ]
            },
            "child_groups":{
               "data":[
                  {
                     "type":"groups",
                     "id":"85"
                  }
               ]
            }
         }
      },
      {
         "type":"groups",
         "id":"185",
         "attributes":{
            "name":"Group 2"
         },
         "relationships":{
            "members":{
               "data":[
                  {
                     "type":"entities",
                     "id":"22"
                  },
                  {
                     "type":"entities",
                     "id":"24"
                  }
               ]
            }
         }
      }
   ]
}
```

```json Response
HTTP/1.1 200

{
   "data":[
      {
         "id":"11",
         "type":"groups",
         "attributes":{
            "name":"Group 1"
         },
         "relationships":{
            "members":{
               "links":{
                  "self":"/v1/groups/11/relationships/members",
                  "related":"/v1/groups/11/members"
               },
               "data":[
                  {
                     "type":"entities",
                     "id":"34"
                  },
                  {
                     "type":"entities",
                     "id":"219"
                  },
                  {
                     "type":"entities",
                     "id":"957"
                  }
               ]
            },
            "group_type":{
               "links":{
                  "self":"/v1/groups/11/relationships/group_type",
                  "related":"/v1/groups/11/group_type"
               },
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            },
            "child_groups":{
               "links":{
                  "self":"/v1/groups/11/relationships/child_groups",
                  "related":"/v1/groups/11/child_groups"
               },
               "data":[

               ]
            }
         },
         "links":{
            "self":"/v1/groups/11"
         }
      },
      {
         "id":"169",
         "type":"groups",
         "attributes":{
            "name":"Group 2"
         },
         "relationships":{
            "members":{
               "links":{
                  "self":"/v1/groups/169/relationships/members",
                  "related":"/v1/groups/169/members"
               },
               "data":[
                  {
                     "type":"entities",
                     "id":"22"
                  },
                  {
                     "type":"entities",
                     "id":"24"
                  },
                  {
                     "type":"entities",
                     "id":"117"
                  }
               ]
            },
            "group_type":{
               "links":{
                  "self":"/v1/groups/169/relationships/group_type",
                  "related":"/v1/groups/169/group_type"
               },
               "data":{
                  "type":"group_types",
                  "id":"GROUPS"
               }
            },
            "child_groups":{
               "links":{
                  "self":"/v1/groups/169/relationships/child_groups",
                  "related":"/v1/groups/169/child_groups"
               },
               "data":[
                  {
                     "type":"groups",
                     "id":"85"
                  }
               ]
            }
         },
         "links":{
            "self":"/v1/groups/169"
         }
      }
   ],
   "included":[

   ]
}
```

**Response codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid payload; or an entity included in not a valid type: client, account, holding company, trust, managed fund
- `403 Forbidden`: You do not have permission to access the API; you do not have access to the type of group, or you can't modify one or more passed in attributes
- `404 Not Found`: The group_type ID does not exist, or you do not have access to it; you don't have access to one or more members or they don't exist; or a passed in attribute does not exist
- `409 Conflict`: The ID in the URL doesn't match the ID in the payload; the "type" was not specified as "groups"; or one or more members is not an entity

## Update group members

Replaces all the existing group members with new ones. Returns an empty response.

**PATCH** `/v1/groups/:id/relationships/members`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/groups/5678/relationships/members

{
  "data": [
    {
      "type": "entities",
      "id": "100"
    },
    {
      "type": "entities",
      "id": "101"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `400 Bad Request`: One or more group members in not a valid type: client, account, holding company, trust, managed fund
- `403 Forbidden`: You do not have permission to access the API, you don't have access to the group itself, or you do not have access to the type of group
- `404 Not Found`: The group does not exist, or you do not have access to it
- `409 Conflict`: The input type of member is not "entities"

## Replace a group's child groups

Replaces all the existing group members with new ones. Returns an empty response.

**PATCH** `/v1/groups/:id/relationships/child_groups`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/groups/111/relationships/child_groups

{
  "data": [
    {
      "type": "groups",
      "id": "92"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `400 Bad Request`: One or more group members in not a valid type: client, account, holding company, trust, managed fund
- `403 Forbidden`: You do not have permission to access the API, you don't have access to the group itself, or you do not have access to the type of group
- `404 Not Found`: The group does not exist, or you do not have access to it

## Delete a group

Deletes a group from your firm. Returns an empty response.

**DELETE** `/v1/groups/:id`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/groups/1111
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `403 Forbidden`: You do not have access to the group itself or the type of group
- `404 Not Found`: The group does not exist
- `409 Conflict`: The ID in the URL doesn't match the ID in the payload; the "type" was not specified as "groups"; or one or more members is not an entity

## Delete multiple groups

Deletes multiple existing groups from your firm. Returns an empty response.

**DELETE** `/v1/groups`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/groups

{
  "data": [ {
	"id": "1111",
       "type": "groups"
   },
      {
      "id": "1112",
      "type": "groups"
   }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `403 Forbidden`: You do not have access to one or more groups or types of groups
- `404 Not Found`: One or more groups do not exist
- `409 Conflict`: The ID in the URL doesn't match the ID in the payload; the "type" for one or more groups was not specified as "groups"; or one or more members is not an entity

## Remove group members

Removes members of a group. Returns an empty response.

**DELETE** `/v1/groups/:id/relationships/members`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/groups/5678/relationships/members

{
  "data": [
    {
      "type": "entities",
      "id": "2000001"
    }
  ]
}
```

```json Response
HTTP/1.1 204 No Content
```

**Response codes:**

- `204 No Content`: Success
- `400 Bad Request`: One or more group members in not a valid type: client, account, holding company, trust, managed fund
- `403 Forbidden`: You do not have permission to access the API, you don't have access to the group itself, or you do not have access to the type of group
- `404 Not Found`: The group does not exist, or you do not have access to it
- `409 Conflict`: The input type of member is not "entities"
