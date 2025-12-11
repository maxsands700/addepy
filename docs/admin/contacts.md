# Contacts

Contacts are individuals who can access the Client Portal. You can use the Contacts API to create, view, update, and delete contacts. You can also update contact information and manage their affiliations.
[block:image]
{
"images": [
{
"image": [
"https://files.readme.io/bbe027268147168e8848429f9bd9cab1e7a0d15fb6a591ee74e7df21fe61db42-Screenshot_2024-12-10_at_12.38.13_PM.png",
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
"0-1": "/v1/contacts",
"1-0": "Endpoints",
"1-1": "**GET** \n/v1/contacts/:id \n/v1/contacts \n/v1/contacts/:id/relationships/entity_affiliations \n/v1/contacts/:id/relationships/group_affiliations \n/v1/contacts/:id/relationships/default_view_set \n/v1/contacts/:id/relationships/team \n \n**POST** \n/v1/contacts \n/v1/contacts/:id/relationships/entity_affiliations \n/v1/contacts/:id/relationships/group_affiliations \n/v1/contacts/:id/relationships/default_view_set \n/v1/contacts/:id/invite \n \n**PATCH** \n/v1/contacts/:id \n/v1/contacts/:id/relationships/entity_affiliations \n/v1/contacts/:id/relationships/group_affiliations \n/v1/contacts/:id/relationships/team \n/v1/contacts/:id/restore \n/v1/contacts/:id/revoke \n/v1/contacts/:id/exempt_two_factor_authentication \n/v1/contacts/:id/require_two_factor_authentication \n/v1/contacts/:id/enable_saml \n/v1/contacts/:id/disable_saml \n \n**DELETE** \n/v1/contacts/:id \n/v1/contacts/:id/relationships/entity_affiliations \n/v1/contacts/:id/relationships/group_affiliations \n/v1/contacts/:id/relationships/default_view_set \n/v1/contacts/:id/relationships/team",
"2-0": "Produces",
"2-1": "JSON",
"3-0": "Pagination",
"3-1": "[Yes](https://developers.addepar.com/docs/pagination-1)",
"4-0": "Application permissions required",
"4-1": "\"API Access: Create, edit, and delete\" \n \n\"Full Access\" for all operations.",
"5-0": "OAuth scopes",
"5-1": "**GET** \n`USERS_READ` \n \n**POST**, **PATCH**, and **DELETE** \n`USERS_WRITE`"
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

Contacts contain the below attributes. Required attributes are noted in the description.

All attributes will be returned in successful **GET**, **POST**, and **PATCH** responses containing the contacts resource.

| Attribute                               | Description                                                                                                                                                                                                                       | Example                    |
| :-------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------- |
| `title`                                 | The contact's title. String. The maximum length is 10 characters.                                                                                                                                                                 | `"Mr."`                    |
| `first_name`                            | The contact's first name. String. Required. The maximum length is 40 characters.                                                                                                                                                  | `"Adam"`                   |
| `last_name`                             | The contact's last name. String. Required. The maximum length is 80 characters.                                                                                                                                                   | `"Smith"`                  |
| `suffix`                                | The contact's suffix. String. The maximum length is 10 characters.                                                                                                                                                                | `"Jr."`                    |
| `external_user_id`                      | The firm's unique ID for the user, like an employee's ID number. String. The maximum length is 31 characters.                                                                                                                     | `"abc123"`                 |
| `login_email`                           | The email address a contact uses to sign in to the Portal. This field cannot be deleted.                                                                                                                                          | `"adam.smith@example.com"` |
| `portal_access`                         | The contact's portal access status. String. This field cannot be created, edited, or deleted.                                                                                                                                     | `"deactivated"`            |
| `birthday`                              | The contact’s birthday. String. Format as YYYY-MM-DD.                                                                                                                                                                             | `"1990-10-31"`             |
| `employer`                              | The contact’s employer. String. The maximum length is 80 characters.                                                                                                                                                              | `"Madison Capital"`        |
| `occupation`                            | The contact’s occupation. String. The maximum length is 80 characters.                                                                                                                                                            | `"Financial Services"`     |
| `ssn`                                   | The contact’s Social Security number. String. The maximum length is 9 characters.                                                                                                                                                 | `"123456789"`              |
| `is_exempt_from_two_factor_requirement` | The contact’s two-factor authentication exemption status. Boolean. This field cannot be created, edited, or deleted. It’s only returned for active contacts when your firm requires 2FA in Firm Administration > System security. | `false`                    |
| `mailing_addresses`                     | A list of objects forming the contact's mailing addresses. See below for object details. See below for object details.                                                                                                            | See below.                 |
| `emails`                                | A list of objects forming the contact's email addresses. See below for object details.                                                                                                                                            | See below.                 |
| `phone_numbers`                         | A list of objects forming the contact's phone numbers. See below for object details.                                                                                                                                              | See below.                 |
| `family_members`                        | A list of objects representing the contact's family members. See below for object details.                                                                                                                                        | See below.                 |
| `default_affiliation`                   | The default entity or group affiliated with this contact. See below for object details.                                                                                                                                           | See below.                 |
| `saml_settings`                         | The contact’s single sign-on (SSO) settings. Addepar’s SSO uses SAML 2.0. Only returned if the firm has SAML enabled. See below for object details.                                                                               | See below.                 |
| `view_set_overrides`                    | A list of objects representing the contact’s view set overrides for its portfolios. View only. See below for object details.                                                                                                      | See below.                 |

### Mailing address objects

| Attribute      | Description                                                                                        | Example             |
| :------------- | :------------------------------------------------------------------------------------------------- | :------------------ |
| `street`       | The first line of the street address. String. Required. The maximum length is 80 characters.       | `"335 Madison Ave"` |
| `street2`      | The second line of the street address. String. The maximum length is 80 characters.                | `"25th Floor"`      |
| `city`         | The city of the address. String. Required. The maximum length is 80 characters.                    | `"New York"`        |
| `state`        | The state or province of the address. String. Required. The maximum length is 80 characters.       | `"New York"`        |
| `zip`          | The zip or postal code of the address. String. Required. The maximum length is 10 characters.      | `"10017"`           |
| `country`      | The country of the address. String. The maximum length is 80 characters.                           | `"United States"`   |
| `address_type` | The type of the address, such as `Work`, `Home`, etc. String. The maximum length is 80 characters. | `"Work"`            |

### Email address objects

[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`email`",
"0-1": "The email address of the contact. String. Required.",
"0-2": "`\"user1@addepar.com\"`",
"1-0": "`email_type`",
"1-1": "The type of email address. String. Required. \n \nSupported values: \n \n- `PERSONAL`\n- `WORK`\n- `FAMILY`\n- `OTHER`",
"1-2": "`\"WORK\"`"
},
"cols": 3,
"rows": 2,
"align": [
"left",
"left",
"left"
]
}
[/block]

### Phone number objects

[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`number`",
"0-1": "The contact’s phone number. String. Required. The maximum length is 15 characters.",
"0-2": "`\"9179999999\"`",
"1-0": "`phone_type`",
"1-1": "The type of phone number. String. Required. \n \nSupported values: \n \n- `HOME`\n- `WORK`\n- `CELL`\n- `FAX`\n- `OTHER`",
"1-2": "`\"CELL\"`"
},
"cols": 3,
"rows": 2,
"align": [
"left",
"left",
"left"
]
}
[/block]

### Family member objects

[block:parameters]
{
"data": {
"h-0": "Attribute",
"h-1": "Description",
"h-2": "Example",
"0-0": "`first_name`",
"0-1": "The family member’s first name. String. Required. The maximum length is 40 characters.",
"0-2": "`\"Addison\"`",
"1-0": "`last_name`",
"1-1": "The family member’s last name. String. Required. The maximum length is 80 characters.",
"1-2": "`\"Smith\"`",
"2-0": "`relationship`",
"2-1": "The relationship of the family member to the contact. String. Required. \n \nSupported values: \n \n- `SPOUSE`\n- `MOTHER`\n- `FATHER`\n- `SISTER`\n- `BROTHER`\n- `DAUGHTER`\n- `SON`\n- `GRANDMOTHER`\n- `GRANDFATHER`\n- `GRANDDAUGHTER`\n- `GRANDSON`\n- `AUNT`\n- `UNCLE`\n- `COUSIN`\n- `OTHER`",
"2-2": "`\"SISTER\"`"
},
"cols": 3,
"rows": 3,
"align": [
"left",
"left",
"left"
]
}
[/block]

### Default affiliation object

The default affiliation is the first portfolio shown to the user in Portal views. A contact must be affiliated to either an entity or a group, not both. Whichever is selected is the default affiliation.

| Attribute   | Description                                                                                                                                                                                     | Example |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| `entity_id` | The entity affiliated with the contact, identified by its Entity ID. String. If this affiliation is not an entity, this field must be null. If `group_id` is null, this field must not be null. | `"22"`  |
| `group_id`  | The group affiliated with the contact, identified by its Group ID. String. If this affiliation is not a group, this field must be null. If `entity_id` is null, this field must not be null.    | `"7"`   |

### SAML Settings object for SSO

| Attribute      | Description                                                                                                                    | Example               |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------- | :-------------------- |
| `saml_enabled` | The SAML status to indicate if SSO is enabled for a contact. Boolean. Only returned if SSO is enabled for a firm.              | `true`                |
| `saml_user_id` | The contact’s SAML user ID for SSO. String. This field can only be updated via the `enable_saml` and `disable_saml` endpoints. | `"user1@addepar.com"` |

### View set override objects

Identify a contact’s view set that’s customized to be different than the default.

| Attribute     | Description                                                                                                | Example |
| :------------ | :--------------------------------------------------------------------------------------------------------- | :------ |
| `entity_id`   | The entity whose view set is overridden, identified by its Entity ID. Null if the override is for a group. | `22`    |
| `group_id`    | The group whose view set is overridden, identified by its Group ID. Null if the override is for an entity. | `20`    |
| `view_set_id` | The entity or group’s view set that replaces the default, identified by its ID.                            | `11`    |

## Relationships

| Relationship          | Description                                    |
| :-------------------- | :--------------------------------------------- |
| `entity_affiliations` | The entities affiliated with this contact.     |
| `group_affiliations`  | The groups affiliated with this contact.       |
| `default_view_set`    | The default view set assigned to this contact. |
| `team`                | The contact's team.                            |

```json Relationships
"relationships": {
    "entity_affiliations": {
        "links": {
            "self": "/v1/contacts/20/relationships/entity_affiliations",
            "related": "/v1/contacts/20/entity_affiliations"
        },
        "data": [
            {
                "type": "entities",
                "id": "22"
            }
        ]
    },
    "group_affiliations": {
        "links": {
            "self": "/v1/contacts/20/relationships/group_affiliations",
            "related": "/v1/contacts/20/group_affiliations"
        },
        "data": [
            {
                "type": "groups",
                "id": "7"
            }
        ]
    },
    "default_view_set": {
          "links": {
              "self": "/v1/contacts/20/relationships/default_view_set",
              "related": "/v1/contacts/20/default_view_set"
          },
          "data": {
                "type": "view_sets",
                "id": "11"
            }
    },
    "team": {
          "links": {
              "self": "/v1/contacts/20/relationships/team",
              "related": "/v1/contacts/20/team"
          },
          "data": {
              "type": "teams",
              "id": "1"
          }
    }
}
```

## Get a contact

Retrieves details for a specific contact.

**GET** `/v1/contacts/:id`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/contacts/2000
```

```json Response
HTTP/1.1 200

{
    "data":{
        "id":"2000",
        "type":"contacts",
        "attributes":{
            "title":"Mr.",
            "first_name":"Adam",
            "last_name":"Smith",
            "suffix":"Jr.",
            "external_user_id":"abc123",
            "login_email": "adam.smith@example.com",
            "portal_access": "deactivated",
            "birthday":"1990-10-31",
            "employer":"Addepar",
            "occupation":"Financial Services",
            "ssn": "123456789",
            "mailing_addresses": [
                {
                    "street": "335 Madison Ave",
                    "street2": "25th Floor",
                    "city": "New York",
                    "state": "New York",
                    "zip": "10017",
                    "country": "United States",
                    "address_type": "Work"
                }
            ],
            "emails": [
                {
                    "email": "example@addepar.com",
                    "email_type": "WORK"
                }
            ],
            "phone_numbers": [
                {
                    "number": "0987654321",
                    "phone_type": "WORK"
                }
            ],
            "family_members": [
                {
                    "first_name": "Addison",
                    "last_name": "Smith",
                    "relationship": "SISTER"
                }
            ],
            "default_affiliation": {
                "entity_id": "22",
                "group_id": null
            },
            "view_set_overrides": []
        },
        "relationships": {
            "entity_affiliations": {
                "links": {
                    "self": "/v1/contacts/20/relationships/entity_affiliations",
                    "related": "/v1/contacts/20/entity_affiliations"
                },
                "data": [
                    {
                        "type": "entities",
                        "id": "22"
                    }
                ]
            },
            "group_affiliations": {
                "links": {
                    "self": "/v1/contacts/20/relationships/group_affiliations",
                    "related": "/v1/contacts/20/group_affiliations"
                },
                "data": []
            },
            "default_view_set": {
                  "links": {
                      "self": "/v1/contacts/20/relationships/default_view_set",
                      "related": "/v1/contacts/20/default_view_set"
                  },
                  "data": null
            },
            "team": {
              	  "data": null
            }
        },
        "links": {
            "self": "/v1/contacts/20"
        }
    }
}
```

**Response codes**

- `200 OK`: Success
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact not found

## Get all contacts

Retrieves details for all contacts.

**GET** `/v1/contacts`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/contacts
```

```json Response
HTTP/1.1 200

{
    "data":[
      {
        "id":"2000",
        "type":"contacts",
        "attributes":{
            "title":"Mr.",
            "first_name":"Adam",
            "last_name":"Smith",
            "suffix":"Jr.",
            "external_user_id":"abc123",
            "login_email": "adam.smith@example.com",
            "portal_access": "deactivated",
            "birthday":"1990-10-31",
            "employer":"Addepar",
            "occupation":"Financial Services",
            "ssn": "123456789",
            "mailing_addresses": [
                {
                    "street": "335 Madison Ave",
                    "street2": "25th Floor",
                    "city": "New York",
                    "state": "New York",
                    "zip": "10017",
                    "country": "United States",
                    "address_type": "Work"
                }
            ],
            "emails": [
                {
                    "email": "example@addepar.com",
                    "email_type": "WORK"
                }
            ],
            "phone_numbers": [
                {
                    "number": "0987654321",
                    "phone_type": "WORK"
                }
            ],
            "family_members": [
                {
                    "first_name": "Addison",
                    "last_name": "Smith",
                    "relationship": "SISTER"
                }
            ],
            "default_affiliation": {
                "entity_id": "22",
                "group_id": null
            },
            "view_set_overrides": []
        },
        "relationships": {
            "entity_affiliations": {
                "links": {
                    "self": "/v1/contacts/20/relationships/entity_affiliations",
                    "related": "/v1/contacts/20/entity_affiliations"
                },
                "data": [
                    {
                        "type": "entities",
                        "id": "22"
                    }
                ]
            },
            "group_affiliations": {
                "links": {
                    "self": "/v1/contacts/20/relationships/group_affiliations",
                    "related": "/v1/contacts/20/group_affiliations"
                },
                "data": []
            },
            "default_view_set": {
                "links": {
                    "self": "/v1/contacts/20/relationships/default_view_set",
                    "related": "/v1/contacts/20/default_view_set"
                },
                "data": null
            },
            "team": {
              	"data": null
            }
        },
        "links": {
            "self": "/v1/contacts/20"
        }
      }
    ]
}
```

**Response codes**

- `200 OK`: Success
- `403 Forbidden`: You need full access permissions to perform this action

## Get a contact’s entity or group affiliations

Retrieves a list of IDs for the entities or groups the contact has been affiliated with.

**GET** `/v1/contacts/:contact-id/relationships/entity_affiliations`

**GET** `/v1/contacts/:contact-id/relationships/group_affiliations`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/entity_affiliations
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

\*\* Response codes\*\*

- `200 OK`: Success
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact not found

## Get a contact’s default view set

Retrieves the ID of the default view set assigned to the contact.

**GET** `/v1/contacts/:contact-id/relationships/default_view_set`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/default_view_set
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"10000",
    "type":"view_sets"
  }
}
```

\*\* Response codes\*\*

- `200 OK`: Success
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact not found

## Get a contact’s team

Retrieves the ID of the contact’s team.

**GET** `/v1/contacts/:contact-id/relationships/team`

**Example:**

```curl Request
GET https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/team
```

```json Response
HTTP/1.1 200

{
  "data":{
    "id":"1",
    "type":"teams"
  }
}
```

\*\* Response codes\*\*

- `200 OK`: Success
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact or team not found

## Create a contact

Creates a new contact.

**POST** `/v1/contacts`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/contacts

{
    "data":{
        "type":"contacts",
        "attributes":{
            "title":"Mr.",
            "first_name":"Adam",
            "last_name":"Smith",
            "suffix":"Jr.",
            "external_user_id":"abc123",
            "login_email": "adam.smith@example.com",
            "birthday":"1990-10-31",
            "employer":"Addepar",
            "occupation":"Financial Services",
            "ssn": "123456789",
            "mailing_addresses": [
                {
                    "street": "335 Madison Ave",
                    "street2": "25th Floor",
                    "city": "New York",
                    "state": "New York",
                    "zip": "10017",
                    "country": "United States",
                    "address_type": "Work"
                }
            ],
            "emails": [
                {
                    "email": "example@addepar.com",
                    "email_type": "WORK"
                }
            ],
            "phone_numbers": [
                {
                    "number": "0987654321",
                    "phone_type": "WORK"
                }
            ],
            "family_members": [
                {
                    "first_name": "Addison",
                    "last_name": "Smith",
                    "relationship": "SISTER"
                }
            ],
            "default_affiliation": null
        }
    }
}
```

```json Response
HTTP/1.1 201

{
    "data":{
        "id":"2000",
        "type":"contacts",
        "attributes":{
            "title":"Mr.",
            "first_name":"Adam",
            "last_name":"Smith",
            "suffix":"Jr.",
            "external_user_id":"abc123",
            "login_email": "adam.smith@example.com",
            "portal_access": "deactivated",
            "birthday":"1990-10-31",
            "employer":"Addepar",
            "occupation":"Financial Services",
            "ssn": "123456789",
            "mailing_addresses": [
                {
                    "street": "335 Madison Ave",
                    "street2": "25th Floor",
                    "city": "New York",
                    "state": "New York",
                    "zip": "10017",
                    "country": "United States",
                    "address_type": "Work"
                }
            ],
            "emails": [
                {
                    "email": "example@addepar.com",
                    "email_type": "WORK"
                }
            ],
            "phone_numbers": [
                {
                    "number": "0987654321",
                    "phone_type": "WORK"
                }
            ],
            "family_members": [
                {
                    "first_name": "Addison",
                    "last_name": "Smith",
                    "relationship": "SISTER"
                }
            ],
            "default_affiliation": null,
            "view_set_overrides": []
        },
        "relationships": {
            "entity_affiliations": {
                "links": {
                    "self": "/v1/contacts/20/relationships/entity_affiliations",
                    "related": "/v1/contacts/20/entity_affiliations"
                },
                "data": [

                ]
            },
            "group_affiliations": {
                "links": {
                    "self": "/v1/contacts/20/relationships/group_affiliations",
                    "related": "/v1/contacts/20/group_affiliations"
                },
                "data": [

                ]
            },
            "default_view_set": {
                  "links": {
                      "self": "/v1/contacts/20/relationships/default_view_set",
                      "related": "/v1/contacts/20/default_view_set"
                  },
                  "data": null
             },
            "team": {
                  "data": null
            }
        },
        "links": {
            "self": "/v1/contacts/20"
        }
    }
}
```

**Response codes**

- `201 Created`: Success
- `400 Bad Request`: Missing required fields or invalid login email
- `403 Forbidden`: You need full access permissions to perform this action, team and view set team do not match
- `404 Not Found`: Group, entity, or view set not found
- `409 Conflict`: Duplicate external user ID or login email is supplied

## Add an entity or group affiliation to a contact

Affiliates entities or groups with a contact.

**POST** `/v1/contacts/:contact-id/relationships/entity_affiliations`

**POST** `/v1/contacts/:contact-id/relationships/group_affiliations`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/group_affiliations

{
  "data":[
    {
      "id":"10000",
      "type":"groups"
    }
  ]
}
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact, group, or entity not found

## Set the default view set for a contact

Assigns a view set as the default for a contact.

**POST** `/v1/contacts/:contact-id/relationships/default_view_set`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/default_view_set

{
  "data":{
    "id":"10000",
    "type":"view_sets"
  }
}
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: You need full access permissions to perform this action, team and view set team do not match
- `404 Not Found`: Contact or view set not found

## Update a contact

Updates a contact with the specified details.

**PATCH** `/v1/contacts/:contact-id`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts

{
    "data":{
        "id":"2000",
        "type":"contacts",
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
        "id":"2000",
        "type":"contacts",
        "attributes":{
            "title":"Mr.",
            "first_name":"Second",
            "last_name":"User",
            "suffix":"Jr.",
            "external_user_id":"abc123",
            "login_email": "adam.smith@example.com",
            "portal_access": "deactivated",
            "birthday":"1990-10-31",
            "employer":"Addepar",
            "occupation":"Financial Services",
            "ssn": "123456789",
            "mailing_addresses": [
                {
                    "street": "335 Madison Ave",
                    "street2": "25th Floor",
                    "city": "New York",
                    "state": "New York",
                    "zip": "10017",
                    "country": "United States",
                    "address_type": "Work"
                }
            ],
            "emails": [
                {
                    "email": "example@addepar.com",
                    "email_type": "WORK"
                }
            ],
            "phone_numbers": [
                {
                    "number": "0987654321",
                    "phone_type": "WORK"
                }
            ],
            "family_members": [
                {
                    "first_name": "Addison",
                    "last_name": "Smith",
                    "relationship": "SISTER"
                }
            ],
            "default_affiliation": null,
            "view_set_overrides": []
        },
        "relationships": {
            "entity_affiliations": {
                "links": {
                    "self": "/v1/contacts/20/relationships/entity_affiliations",
                    "related": "/v1/contacts/20/entity_affiliations"
                },
                "data": [

                ]
            },
            "group_affiliations": {
                "links": {
                    "self": "/v1/contacts/20/relationships/group_affiliations",
                    "related": "/v1/contacts/20/group_affiliations"
                },
                "data": [

                ]
            },
            "default_view_set": {
                  "links": {
                      "self": "/v1/contacts/20/relationships/default_view_set",
                      "related": "/v1/contacts/20/default_view_set"
                  },
                  "data": null
            },
            "team": {
                  "data": null
            }
        },
        "links": {
            "self": "/v1/contacts/20"
        }
    }
}
```

**Response codes**

- `200 OK`: Success
- `400 Bad Request`: Missing required fields or invalid login email
- `403 Forbidden`: You need full access permissions to perform this action, team and view set team do not match
- `404 Not Found`: Contact, group, entity, or view set not found
- `409 Conflict`: Duplicate external user ID or login email is supplied

## Replace a contact's entity or group affiliations

Replaces a contacts entity or group affiliations with the given entities or groups.

**PATCH** `/v1/contacts/:contact-id/relationships/entity_affiliations`

**PATCH** `/v1/contacts/:contact-id/relationships/group_affiliations`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/group_affiliations

{
  "data":[
    {
      "id":"10000",
      "type":"groups"
    }
  ]
}
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact, group, or entity not found

## Replace a contact's team

Replaces a contact’s team.

**PATCH** `/v1/contacts/:contact-id/relationships/team`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/team

{
  "data":{
      "id":"1",
      "type":"teams"
  }
}
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact or team not found

## Delete a contact

Delete a specific contact.

**DELETE** `/v1/contacts/:contact-id`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/contacts/2000
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: You need full access permissions to perform this action

## Remove entity or group affiliations from a contact

Removes entities or groups from a contact’s affiliations.

**DELETE** `/v1/contacts/:contact-id/relationships/entity_affiliations`

**DELETE** `/v1/contacts/:contact-id/relationships/group_affiliations`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/group_affiliations

{
  "data":[
    {
      "id":"10000",
      "type":"groups"
    }
  ]
}
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: You need full access permissions to perform this action

## Remove the default view set from a contact

Removes the default view set from a contact.

**DELETE** `/v1/contacts/:contact-id/relationships/default_view_set`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/default_view_set
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: You need full access permissions to perform this action

## Remove the team from a contact

Removes the team from a contact.

**DELETE** `/v1/contacts/:contact-id/relationships/team`

**Example:**

```curl Request
DELETE https://examplefirm.addepar.com/api/v1/contacts/2000/relationships/team
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `403 Forbidden`: You need full access permissions to perform this action

## Invite a contact to the Client Portal

Send or resend a Client Portal invite to a contact's login email address.

**POST** `/v1/contacts/:contact-id/invite`

**Example:**

```curl Request
POST https://examplefirm.addepar.com/api/v1/contacts/2000/invite
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Missing required fields or invalid login email
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact not found
- `409 Conflict`: Contact is already activated or revoked

## Restore a contact's Client Portal access

Allow a client to once again sign into the Client Portal. You can only restore access for clients whose access is currently revoked.

**PATCH** `/v1/contacts/:contact-id/restore`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts/2000/restore
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Contact has invalid login email or contact is not activated or revoked
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact not found

## Revoke a contact's Client Portal access

Stop a client from being able to sign in to the Client Portal. You can only revoke access for clients whose access is currently activated.

**PATCH** `/v1/contacts/:contact-id/revoke`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts/2000/revoke
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Contact has invalid login email or contact is not activated or revoked
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact not found

## Make a contact’s two-factor authentication (2FA) optional

Exempt a contact from your firm’s 2FA Client Portal login requirement. You can only make 2FA optional for active contacts when your firm requires it in Firm Administration > System security.

**PATCH** `/v1/contacts/:contact-id/exempt_two_factor_authentication`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts/2000/exempt_two_factor_authentication
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Contact has invalid login email, contact is not activated, contact has SSO enabled, or Require for all Portal contacts is disabled
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact not found

## Require a contact to use two-factor authentication (2FA)

Require an exempted contact to follow your firm’s 2FA Client Portal login requirement. You can only require active contacts to use 2FA when your firm requires it in Firm Administration > System security.

**PATCH** `/v1/contacts/:contact-id/require_two_factor_authentication`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts/2000/require_two_factor_authentication
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Contact has invalid login email, contact is not activated, contact has SSO enabled, or Require for all Portal contacts is disabled
- `403 Forbidden`: You need full access permissions to perform this action
- `404 Not Found`: Contact not found

## Enable single sign-on (SSO) for a contact

Enable a contact’s SAML settings to require that contact to use single sign-on (SSO). You can only enable a contact’s SSO if their Client Portal access isn’t revoked and if SAML is set up for the firm.

**PATCH** `/v1/contacts/:contact-id/enable_saml`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts/2000/enable_saml

{
  "data": {
      "id": "2000",
      "type": "saml_settings",
      "attributes": {
          "saml_user_id": "user1@addepar.com"
      }
  }
}
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Contact is missing login email, is revoked, `saml_user_id` is null, empty, or exceeds the 80-character limit
- `403 Forbidden`: You need full access permissions to perform this action or SAML is not enabled for the firm
- `404 Not Found`: Contact not found
- `409 Conflict`: Duplicate SAML user ID is supplied

## Disable single sign-on (SSO) for a contact

Disable a contact’s SAML settings to prevent a contact from using single sign-on (SSO). You can only disable a contact’s SSO if their Client Portal access isn’t revoked and if SAML is set up for the firm.

**PATCH** `/v1/contacts/:contact-id/disable_saml`

**Example:**

```curl Request
PATCH https://examplefirm.addepar.com/api/v1/contacts/2000/disable_saml
```

```json Response
HTTP/1.1 204
```

**Response codes**

- `204 No Content`: Success
- `400 Bad Request`: Contact is missing login email, is revoked
- `403 Forbidden`: You need full access permissions to perform this action or SAML is not enabled for the firm
- `404 Not Found`: Contact not found
