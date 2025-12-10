# AddePy

Unofficial Python SDK for the Addepar API.

## Installation

```bash
pip install addepy
```

## Setup

Create a `.env` file in your project with your Addepar credentials:

```
ADDEPAR_FIRM_NAME=yourfirm
ADDEPAR_FIRM_ID=12345
ADDEPAR_API_KEY=your_base64_encoded_api_key
```

`ADDEPAR_FIRM_NAME` is your URL subdomain: `https://{ADDEPAR_FIRM_NAME}.addepar.com`

## Usage

```python
from addepy import AddePy

addepy = AddePy()  # Reads from .env automatically, or pass in config variables yourself

# List entities - Tier 1 Method
entity_types = addepy.ownership.entities.list_entity_types()

# Execute a portfolio query (submit, poll, download) - Tier 2 Method
results = addepy.portfolio.jobs.execute_portfolio_query(query_dict)

# Run an import (submit, poll, download) - Tier 2 Method
results = addepy.admin.import_tool.execute_import(df, "TRANSACTIONS")
```

_The Import Tool via API is in Beta (as of 12/10/2025), so you may need to request access for your firm. However, this is a great tool... the Import Tool allows data management of almost resources in Addepar..._

## Design Philosophy

### Namespaces & Resources

The SDK mirrors the Addepar API documentation structure with three namespaces:

```
addepy.portfolio    → Market data & holdings
addepy.ownership    → Entity management
addepy.admin        → System & user management
```

Each namespace contains resources that map to API endpoints:

```python
addepy.portfolio.jobs           # /v1/jobs
addepy.ownership.entities       # /v1/entities
addepy.admin.import_tool        # /v1/imports
```

### Tier 1 vs Tier 2 Methods

**Tier 1 - CRUD Operations**

Direct wrappers around individual API endpoints.

| Pattern    | Purpose                          |
| ---------- | -------------------------------- |
| `create_*` | Create a resource                |
| `get_*`    | Retrieve a resource              |
| `list_*`   | List resources (with pagination) |
| `update_*` | Update a resource                |
| `delete_*` | Delete a resource                |

```python
job_id = addepy.portfolio.jobs.create_job(query_dict)
status = addepy.portfolio.jobs.get_job_status(job_id)
results = addepy.portfolio.jobs.get_job_results(job_id)
```

**Tier 2 - Orchestration**

Combine multiple Tier 1 operations into a single call.

| Pattern     | Purpose                        |
| ----------- | ------------------------------ |
| `execute_*` | Submit → Poll → Return results |

```python
# Does create_job + poll for completion + get_job_results
results = addepy.portfolio.jobs.execute_portfolio_query(query_dict)
```

Use Tier 1 when you need fine-grained control. Use Tier 2 for convenience.

## Error Handling

```python
from addepy import AddePyError, AuthenticationError, RateLimitError, ValidationError

try:
    results = addepy.ownership.entities.create_entity(...)
except ValidationError as e:
    print(f"Invalid input: {e}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except AddePyError as e:
    print(f"API error: {e}")
```

## Logging

```python
import logging

logging.getLogger("addepy").setLevel(logging.DEBUG)
logging.getLogger("addepy").addHandler(logging.StreamHandler())
```

## Repository Structure

Mirrors the [Addepar API documentation](https://developers.addepar.com/docs/resource-overview):

```
addepy/
├── client.py              # Main entry point
├── exceptions.py          # Custom exceptions
├── constants.py           # SDK constants
└── resources/
    ├── base.py            # Base resource class
    ├── portfolio/         # PORTFOLIO endpoints
    │   └── jobs.py
    ├── ownership/         # OWNERSHIP endpoints
    │   └── entities.py
    └── admin/             # ADMIN endpoints
        └── import_tool.py
```

## Addepar API Documentation

Official docs: [developers.addepar.com](https://developers.addepar.com/docs/resource-overview)

**API Sections:**

- **Portfolio** - Jobs, Transactions, Historical Prices, Benchmarks, etc.
- **Ownership** - Entities, Groups, Positions, External IDs
- **Admin** - Import Tool, Users, Files, Reports, etc.
