# Pagination

Pagination is supported for the Entities API, Jobs API, Positions API, Users API, Groups API, Files API, Archived Files API, and Target Allocations API so that large result sets can be batched into multiple responses.

The maximum page size of 2000 results is enforced per response. If the complete results cannot fit into a single response, the set will be truncated automatically, and the remaining values linked from the "next" URL appended to the end of the set.

**Query parameters:**

| Parameter     | Description                                                                                                                               | Example |
| :------------ | :---------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| `page[limit]` | The number of results to be returned. The maximum result set size is 2000. If not specified, the default value is 500.                    | `100`   |
| `page[after]` | The next page; the returned paginated data must have as its first item the item that is immediately after the cursor in the results list. | `10001` |

**Links:**

| Name     | Description                                                                          | Example                                            |
| :------- | :----------------------------------------------------------------------------------- | :------------------------------------------------- |
| `"next"` | The URL of the "next" page of the result set. Null if there are no additional pages. | `"/v1/entities?page[limit]=100&page[after]=10001"` |

**Example:**

```curl Request
GET /v1/entities?page[limit]=100
```

```json Response
HTTP/1.1 200

{
  "data": [
    ...
  ],
  "links": {
    "next": "/v1/entities?page[limit]=100&page[after]=10001"
  }
}
```
