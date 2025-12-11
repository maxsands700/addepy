# Users

Users are members of your firm that have access to Addepar. The Users API can be used to view, create, and delete users. You can also update user information, tool permissions, and portfolio access.

![](https://files.readme.io/06de136-Users.png "Users.png")
[block:parameters]
{
"data": {
"h-0": "",
"h-1": "",
"0-0": "Base Route",
"0-1": "/v1/users",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/users/:id \n/v1/users \n/v1/users/me \n/v1/users/:id/relationships/assigned_role \n/v1/users/:id/relationships/permissioned_entities \n/v1/users/:id/relationships/permissioned_groups \n \n**POST** \nv1/users/email_query \n/v1/users/external_user_id_query \n/v1/users \n/v1/users/:id/relationships/permissioned_entities \n/v1/users/:id/relationships/permissioned_groups \n \n**PATCH** \n/v1/users/:id \n/v1/users/:id/relationships/assigned_role \n \n**DELETE** \n/v1/users/:id",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application Permissions Required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Manage firm settings: Users and permissions\" for all operations.",
"5-0": "OAuth Scopes",
"5-1": "**GET** \n`USERS_WRITE` \n \n**POST**, **PATCH**, and **DELETE** \n`USERS_WRITE`except **POST** `v1/users/external_user_id_query` which requires `USERS` or `USERS_WRITE`"
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

Users are described by the below resource object attributes. Attributes required for creating, updating, or deleting Users are noted.

All attributes will be returned in successful **GET**, **POST** & **PATCH** responses containing the Users resource.
[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`email`",
"0-1": "The email address used for authentication. Not editable. String.",
"0-2": "`\"user1@addepar.com\"`",
"1-0": "`first_name`",
"1-1": "String.",
"1-2": "`\"Adam\"`",
"2-0": "`last_name`",
"2-1": "String.",
"2-2": "`\"Smith\"`",
"3-0": "`login_method`",
"3-1": "Not editable. String. \n \nSupported values: \n \n- email_password\n- saml",
"3-2": "`\"email_password\"`",
"4-0": "`saml_user_id`",
"4-1": "Not editable. String. \n \nRequired if login_method is \"saml\".",
"4-2": "`\"asmith\"`",
"5-0": "`admin_access`",
"5-1": "Indicates whether the user has access to all permissions. Boolean.",
"5-2": "`false`",
"6-0": "`all_data_access`",
"6-1": "Indicates whether the user has permission to access all current and future portfolio data. Boolean.",
"6-2": "`true`",
"7-0": "`two_factor_auth_enabled`",
"7-1": "Indicates whether the user has two-factor authentication enabled. Not editable. Boolean.",
"7-2": "`true`",
"8-0": "`external_user_id`",
"8-1": "Reflects the firm’s unique ID for the user, like the employee's ID number or ID from a human resources system, etc. String.",
"8-2": "`\"A67890\"`"
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

## Relationships

| Relationship            | Description                                   |
| :---------------------- | :-------------------------------------------- |
| `assigned_role`         | The role that the user is assigned to.        |
| `permissioned_entities` | The client portfolios the user has access to. |
| `permissioned_groups`   | The groups the user has access to.            |

```json Relationships
"relationships": {
        "permissioned_entities": {
          "links": {
            "self": "/v1/users/2000/relationships/permissioned_entities",
            "related": "/v1/users/2000/permissioned_entities"
          },
          "data": [
            {
               "type": "entities",
               "id": 10000
            },
            {
               "type": "entities",
               "id": 10001
            }
          ]
        },
        "assigned_role": {
          "links": {
            "self": "/v1/users/2000/relationships/assigned_role",
            "related": "/v1/users/2000/assigned_role"
          },
          "data": []
        },
        "permissioned_groups": {
          "links": {
            "self": "/v1/users/2000/relationships/permissioned_groups",
            "related": "/v1/users/2000/permissioned_groups"
          },
          "data": [
            {
               "type": "entities",
               "id": 20000
            },
            {
               "type": "entities",
               "id": 20001
            }
          ]
        }
      }
```

## Get a user

Retrieves details for a specific user.

**GET** `/v1/users/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/users/2000
```

```json Response
HTTP/1.1 200

{
  "meta":{
    "exclude_self_link":false,
    "link":null,
    "pagination_params":null,
    "included_params":null,
    "filter_params":null,
    "fields_param":null
  },
  "data":{
    "id":"22",
    "type":"users",
    "attributes":{
      "two_factor_auth_enabled":false,
      "admin_access":true,
      "all_data_access":true,
      "login_method":"email_password",
      "email":"example@addepar.com"
    },
    "relationships":{
      "permissioned_entities":{
        "links":{
          "self":"/v1/users/22/relationships/permissioned_entities",
          "related":"/v1/users/22/permissioned_entities"
        },
        "data":[

        ]
      },
      "assigned_role":{
        "links":{
          "self":"/v1/users/22/relationships/assigned_role",
          "related":"/v1/users/22/assigned_role"
        },
        "data":null
      },
      "permissioned_groups":{
        "links":{
          "self":"/v1/users/22/relationships/permissioned_groups",
          "related":"/v1/users/22/permissioned_groups"
        },
        "data":[

        ]
      }
    },
    "links":{
      "self":"/v1/users/22"
    }
  },
  "included":[

  ]
}
```

**Responses**

- `200 OK`: Success
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned user ID

## Get all users

Retrieves details for all users.

**GET** `/v1/users`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/users
```

```json Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "1000",
      "type": "users",
      "attributes": {
        "email": "user1@addepar.com",
        "first_name": "Adam",
        "last_name": "Smith",
        "login_method": "email_password",
        "two_factor_auth_enabled": true,
        "admin_access": false,
        "all_data_access": true,
        "external_user_id": "A12345"
      },
      "relationships": {
        "permissioned_entities": {
          "links": {
            "self": "/v1/users/1000/relationships/permissioned_entities",
            "related": "/v1/users/1000/permissioned_entities"
          },
          "data": []
        },
        "assigned_role": {
          "links": {
            "self": "/v1/users/1000/relationships/assigned_role",
            "related": "/v1/users/1000/assigned_role"
          },
          "data": []
        },
        "permissioned_groups": {
          "links": {
            "self": "/v1/users/1000/relationships/permissioned_groups",
            "related": "/v1/users/1000/permissioned_groups"
          },
          "data": []
        }
      },
      "links": {
        "self": "/v1/users/1000"
      }
    },
    {
      "id": "2000",
      "type": "users",
      "attributes": {
        "email": "user2@addepar.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "login_method": "email_password",
        "two_factor_auth_enabled": true,
        "admin_access": false,
        "all_data_access": false,
        "external_user_id": "A67890"
      },
      "relationships": {
        "permissioned_entities": {
          "links": {
            "self": "/v1/users/2000/relationships/permissioned_entities",
            "related": "/v1/users/2000/permissioned_entities"
          },
          "data": [
            {
               "type": "entities",
               "id": 10000
            },
            {
               "type": "entities",
               "id": 10001
            }
          ]
        },
        "assigned_role": {
          "links": {
            "self": "/v1/users/2000/relationships/assigned_role",
            "related": "/v1/users/2000/assigned_role"
          },
          "data": []
        },
        "permissioned_groups": {
          "links": {
            "self": "/v1/users/2000/relationships/permissioned_groups",
            "related": "/v1/users/2000/permissioned_groups"
          },
          "data": [
            {
               "type": "entities",
               "id": 20000
            },
            {
               "type": "entities",
               "id": 20001
            }
          ]
        }
      },
      "links": {
        "self": "/v1/users/2000"
      }
    }
  ],
  "links": {
    "next": null
  }
}
```

**Responses:**

- `200 OK`: Success
- `403 Forbidden`: Lacking permission to view users

## Get current user

Retrieves details for the currently authenticated user. This is the user who created the API key that was used to authenticate the request.

**GET** `/v1/users/me`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/users/me
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
            "email": "notdev@addepar.com"
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

**Response Codes:**

- `200 OK`: Success
- `401 Unauthorized`: The API key is invalid

## Get a user's assigned role

If no role is assigned to a user, data will return as `null`.

**GET** `/v1/users/:user-id/relationships/assigned_role`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/users/101/relationships/assigned_role
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"1",
    "type":"role"
  }
}
```

\*\* Response Codes:\*\*

- `200 OK`: Success
- `400 Bad Request`: Invalid relationship queried
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned user ID

## Get a user's permissioned entities or groups

Retrieves a list of IDs for the clients or group portfolios that the user has access to.

**GET** `/v1/users/:user-id/relationships/permissioned_entities`

**GET** `/v1/users/:user-id/relationships/permissioned_groups`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/users/5678/relationships/permissioned_groups
```

```json Response
HTTP/1.1 200

{
  "data":[
    {
      "id":"10000",
      "type":"entities"
    }
  ]
}
```

\*\* Response Codes:\*\*

- `200 OK`: Success
- `400 Bad Request`: Invalid relationship queried
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned user ID

## Get users by email

Retrieves details for a specific user.

**POST** `/v1/users/email_query`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/users/email_query

{
  "data":{
    "type":"email_query",
    "attributes":{
      "email_ids":[
        "user1@addepar.com",
        "user2@addepar.com"
      ]
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "1000",
      "type": "users",
      "attributes": {
        "email": "user1@addepar.com",
        "first_name": "Adam",
        "last_name": "Smith",
        "login_method": "email_password",
        "two_factor_auth_enabled": true,
        "admin_access": false,
        "all_data_access": true,
        "external_user_id": "A12345"
      },
      "relationships": {
        "permissioned_entities": {
          "links": {
            "self": "/v1/users/1000/relationships/permissioned_entities",
            "related": "/v1/users/1000/permissioned_entities"
          },
          "data": []
        },
        "assigned_role": {
          "links": {
            "self": "/v1/users/1000/relationships/assigned_role",
            "related": "/v1/users/1000/assigned_role"
          },
          "data": []
        },
        "permissioned_groups": {
          "links": {
            "self": "/v1/users/1000/relationships/permissioned_groups",
            "related": "/v1/users/1000/permissioned_groups"
          },
          "data": []
        }
      },
      "links": {
        "self": "/v1/users/1000"
      }
    },
    {
      "id": "2000",
      "type": "users",
      "attributes": {
        "email": "user2@addepar.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "login_method": "email_password",
        "two_factor_auth_enabled": true,
        "admin_access": false,
        "all_data_access": false,
        "external_user_id": "A67890"
      },
      "relationships": {
        "permissioned_entities": {
          "links": {
            "self": "/v1/users/2000/relationships/permissioned_entities",
            "related": "/v1/users/2000/permissioned_entities"
          },
          "data": [
            {
               "type": "entities",
               "id": 10000
            },
            {
               "type": "entities",
               "id": 10001
            }
          ]
        },
        "assigned_role": {
          "links": {
            "self": "/v1/users/2000/relationships/assigned_role",
            "related": "/v1/users/2000/assigned_role"
          },
          "data": []
        },
        "permissioned_groups": {
          "links": {
            "self": "/v1/users/2000/relationships/permissioned_groups",
            "related": "/v1/users/2000/permissioned_groups"
          },
          "data": [
            {
               "type": "entities",
               "id": 20000
            },
            {
               "type": "entities",
               "id": 20001
            }
          ]
        }
      },
      "links": {
        "self": "/v1/users/2000"
      }
    }
  ],
  "links": {
    "next": null
  }
}
```

**Response Codes:**

- `200 OK`: Success
- `403 Forbidden`: User lacks sufficient application permissions

## Get users by external user ID

Retrieves details for a specific user.

**POST** `/v1/users/external_user_id_query`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/users/external_user_id_query

{
  "data":{
    "type":"external_user_id_query",
    "attributes":{
      "external_user_ids":[
        "A12345",
        "A67890"
      ]
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "data": [
    {
      "id": "1000",
      "type": "users",
      "attributes": {
        "email": "user1@addepar.com",
        "first_name": "Adam",
        "last_name": "Smith",
        "login_method": "email_password",
        "two_factor_auth_enabled": true,
        "admin_access": false,
        "all_data_access": true,
        "external_user_id": "A12345"
      },
      "relationships": {
        "permissioned_entities": {
          "links": {
            "self": "/v1/users/1000/relationships/permissioned_entities",
            "related": "/v1/users/1000/permissioned_entities"
          },
          "data": []
        },
        "assigned_role": {
          "links": {
            "self": "/v1/users/1000/relationships/assigned_role",
            "related": "/v1/users/1000/assigned_role"
          },
          "data": []
        },
        "permissioned_groups": {
          "links": {
            "self": "/v1/users/1000/relationships/permissioned_groups",
            "related": "/v1/users/1000/permissioned_groups"
          },
          "data": []
        }
      },
      "links": {
        "self": "/v1/users/1000"
      }
    },
    {
      "id": "2000",
      "type": "users",
      "attributes": {
        "email": "user2@addepar.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "login_method": "email_password",
        "two_factor_auth_enabled": true,
        "admin_access": false,
        "all_data_access": false,
        "external_user_id": "A67890"
      },
      "relationships": {
        "permissioned_entities": {
          "links": {
            "self": "/v1/users/2000/relationships/permissioned_entities",
            "related": "/v1/users/2000/permissioned_entities"
          },
          "data": [
            {
               "type": "entities",
               "id": 10000
            },
            {
               "type": "entities",
               "id": 10001
            }
          ]
        },
        "assigned_role": {
          "links": {
            "self": "/v1/users/2000/relationships/assigned_role",
            "related": "/v1/users/2000/assigned_role"
          },
          "data": []
        },
        "permissioned_groups": {
          "links": {
            "self": "/v1/users/2000/relationships/permissioned_groups",
            "related": "/v1/users/2000/permissioned_groups"
          },
          "data": [
            {
               "type": "entities",
               "id": 20000
            },
            {
               "type": "entities",
               "id": 20001
            }
          ]
        }
      },
      "links": {
        "self": "/v1/users/2000"
      }
    }
  ],
  "links": {
    "next": null
  }
}
```

**Responses:**

- `200 OK`: Success
- `403 Forbidden`: User lacks sufficient application permissions

## Create a user

By default, users are created in custom mode with no permissions. You can keep them in custom mode and manually assign permissions to each user in the Addepar application.

If you want to assign user permissions based upon a specific role, you can do so using the Update User Relationships method in the Users API or the Assign Role to Users method in the Roles API.

**POST** `/v1/users`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/users

{
  "data":{
    "type":"users",
    "attributes":{
      "email":"example.user@addepar.com",
      "first_name":"Example",
      "last_name":"User",
      "login_method":"email_password"
    }
  }
}
```

```json Response
HTTP/1.1 201

{
  "data":{
    "id":"82",
    "type":"users",
    "attributes":{
      "two_factor_auth_enabled":false,
      "admin_access":false,
      "all_data_access":false,
      "login_method":"email_password",
      "last_name":"User",
      "first_name":"Example",
      "email":"example.user@addepar.com"
    },
    "relationships":{
      "permissioned_entities":{
        "links":{
          "self":"/v1/users/82/relationships/permissioned_entities",
          "related":"/v1/users/82/permissioned_entities"
        },
        "data":[

        ]
      },
      "assigned_role":{
        "links":{
          "self":"/v1/users/82/relationships/assigned_role",
          "related":"/v1/users/82/assigned_role"
        },
        "data":null
      },
      "permissioned_groups":{
        "links":{
          "self":"/v1/users/82/relationships/permissioned_groups",
          "related":"/v1/users/82/permissioned_groups"
        },
        "data":[

        ]
      }
    },
    "links":{
      "self":"/v1/users/82"
    }
  },
  "included":[

  ]
}
```

_Response Codes:_

- `201 Created`: Success
- `400 Bad Request`: Invalid email provided
- `400 Bad Request`: SAML User ID already in use
- `400 Bad Request`: Email is already in use
- `403 Forbidden`: User lacks sufficient application permissions
- `409 Conflict`: A duplicate external_user_id exists for the firm

## Add user's access to entities or groups

Grants a user access to a specific client or group of portfolios.

**POST** `/v1/users/:id/relationships/permissioned_entities`

**POST** `/v1/users/:id/relationships/permissioned_groups`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/users/101/relationships/permissioned_groups

{
  "data":[
  	{
    	"id":"10",
    	"type":"groups"
  	}
  ]
}
```

```json Response
HTTP/1.1 204
```

- `204 No Content`: Success
- `400 Bad Request`: Nonexistent/non-permissioned client IDs
- `404 Not Found`: Nonexistent/non-permissioned user ID

## Update a user

Updates the user's `first_name`, `last_name`, `all_data_access`, or `admin_access`.

**PATCH** `/v1/users/:id`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/users/101

{
  "data":{
    "type":"users",
    "id":"621500",
    "attributes":{
      "first_name":"Second",
      "last_name":"User"
    }
  }
}
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"621500",
    "type":"users",
    "attributes":{
      "two_factor_auth_enabled":false,
      "admin_access":false,
      "all_data_access":false,
      "login_method":"email_password",
      "last_name":"User",
      "first_name":"Second",
      "email":"example.user@addepar.com"
    },
    "relationships":{
      "permissioned_entities":{
        "links":{
          "self":"/v1/users/621500/relationships/permissioned_entities",
          "related":"/v1/users/621500/permissioned_entities"
        },
        "data":[

        ]
      },
      "assigned_role":{
        "links":{
          "self":"/v1/users/621500/relationships/assigned_role",
          "related":"/v1/users/621500/assigned_role"
        },
        "data":{
          "type":"roles",
          "id":"455914"
        }
      },
      "permissioned_groups":{
        "links":{
          "self":"/v1/users/621500/relationships/permissioned_groups",
          "related":"/v1/users/621500/permissioned_groups"
        },
        "data":[
          {
            "type":"groups",
            "id":"1020871"
          },
          {
            "type":"groups",
            "id":"1021710"
          },
          {
            "type":"groups",
            "id":"9559"
          }
        ]
      }
    },
    "links":{
      "self":"/v1/users/621500"
    }
  },
  "included":[

  ]
}
```

**Response Codes**

- `200 OK`: Success
- `400 Bad Request`: Attempted to update relationships
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned user ID
- `409 Conflict`: A duplicate external user ID exists for the firm

## Update a user's role

> 📘 Note
>
> Before using this method, you must assign a role to a user in the Addepar application.

**PATCH** `/v1/users/:id/relationships/assigned_role`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/users/101/relationships/assigned_role

{
  "data":{
    "id":"1",
    "type":"role"
  }
}
```

```json Response
HTTP/1.1 204
```

**Responses**

- `204 No Content`: Success
- `400 Bad Request`: Nonexistent/non-permissioned role ID
- `404 Not Found`: Nonexistent/non-permissioned user ID

## Delete a user

Removes a specified user.

**DELETE** `/v1/users/:id`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/users/101

{
  "data":{
    "type":"users",
    "id":"users",
    "attributes":{
      "first_name":"Example",
      "last_name":"User"
    }
  }
}
```

```json Response
HTTP/1.1 204
```

**Response Codes:**

- `204 No Content`: Success
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned user ID

## Delete a user's access to entities or groups

Removes access to specific client and group portfolios.

**DELETE** `/v1/users/:id/relationships/permissioned_entities`

**DELETE** `/v1/users/:id/relationships/permissioned_groups`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/users/101/relationships/permissioned_groups

{
  "data":[
    {
      "id":"1",
      "type":"groups"
    }
  ]
}
```

```json Response
HTTP/1.1 204
```

**Response Codes:**

- `400 Bad Request`: Invalid relationship queried
- `403 Forbidden`: User lacks sufficient application permissions
- `404 Not Found`: Nonexistent/non-permissioned user ID
