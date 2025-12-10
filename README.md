# AddePy

A Python SDK for the Addepar API (Work In Progress).

## Quick Start

### Authentication

Set up your Addepar credentials in a `.env` file:

```bash
ADDEPAR_FIRM_NAME=your_firm_name
ADDEPAR_FIRM_ID=your_firm_id
ADDEPAR_API_KEY=your_base64_encoded_api_key
```

`ADDEPAR_FIRM_NAME` represents the url subdomain: `www.{ADDEPAR_FIRM_NAME}.addepar.com`.

### Basic Usage

1. Initialize an `AddePy()` instance.

```python
from addepy import AddePy

# Initialize the client (reads from .env by default)
addepy = AddePy()

# Or specify credentials explicitly
addepy = AddePy(
    firm_name="your_firm",
    firm_id="12345",
    api_key="your_base64_key"
)
```

2. Use methods to perform operations

```python
addepy.admin.import_tool.create_import(
  import_dataframe=your_import_dataframe,
  import_type=your_import_type, # e.g. 'ATTRIBUTES'
  is_dry_run=TRUE, # Test Run or Production Run
  ignore_warnings=False # Do warnings stop the import or do you ignore
)

addepy.admin.import_tool.get_import_status(import_id=import_id)

addepy.admin.import_tool.get_import_results(import_id=import_id)
```

## Design Philosophy

Just like the Addepar API documentation, there are 3 main resources: `admin`, `ownership`, and `portfolio`; each resource has sub classes for specific endpoints like `import_tool`.

## Method Architecture: Tier 1 vs Tier 2

We have designed two Tiers of methods for your convenience. Tier 1 methods are basic CRUD operations wrapped around the Addepar API endpoints (shown above in basic usage). However for things like imports, it makes sense to do all 3 steps in a single call, so we created Tier 2 methods:

### Tier 1 Methods (CRUD Operations)

**Pattern**: `create_*`, `get_*`, `update_*`, `delete_*`, `list_*`

**Purpose**: Fine-grained control over individual API operations.

**When to use**:

- You need to inspect intermediate states
- You want custom polling logic
- You're building complex workflows
- You need to integrate with existing systems

**Examples**:

- `create_job()` → Returns job ID
- `get_job_status()` → Returns status dict
- `get_job_results()` → Returns results
- `create_import()` → Returns import ID
- `get_import_status()` → Returns status string
- `get_import_results()` → Returns results dict

### Tier 2 Methods (Orchestration)

**Pattern**: `execute_*`

**Purpose**: High-level convenience methods that combine multiple Tier 1 operations.

**When to use**:

- You want the simplest possible API
- You don't need to inspect intermediate states
- Standard polling behavior is acceptable
- You prefer fewer lines of code

**Examples**:

- `execute_portfolio_query()` → Submits, polls, downloads (returns results)
- `execute_import()` → Submits, polls, fetches results (returns results dict)

**What Tier 2 methods do**:

1. Call the appropriate `create_*` method
2. Poll using exponential backoff (configurable intervals)
3. Check for completion or timeout
4. Call the appropriate `get_*` method to fetch results
5. Raise exceptions on errors

## Context Manager Support

```python
# Automatically manages session lifecycle
with AddePy() as client:
    results = client.admin.import_tool.execute_import(df, 'TRANSACTIONS')
    print(results)
# Session automatically closed
```

## Logging

Enable logging to see detailed SDK operations:

```python
import logging

# Enable all addepy logs
logging.getLogger("addepy").setLevel(logging.DEBUG)
logging.getLogger("addepy").addHandler(logging.StreamHandler())

# Or just info level
logging.basicConfig(level=logging.INFO)
```

Log levels:

- **DEBUG**: HTTP request/response details
- **INFO**: Job creation, polling status, completion
- **WARNING**: Retryable errors, warnings in responses
- **ERROR**: Failures (before raising exception)

## Error Handling

All methods raise descriptive exceptions on errors:

```python
from addepy import AddePy, AddeparError, AddeparTimeoutError, ValidationError

try:
    results = client.admin.import_tool.execute_import(df, 'INVALID_TYPE')
except ValidationError as e:
    print(f"Invalid input: {e}")
except AddeparTimeoutError as e:
    print(f"Job {e.job_id} timed out. Last status: {e.last_status}")
except AddeparError as e:
    print(f"API error: {e}")
```

Available exceptions:

- `AddeparError` - Base exception for all errors
- `AuthenticationError` - 401 authentication failures
- `RateLimitError` - 429 rate limit exceeded (includes `retry_after`)
- `ValidationError` - 400/422 validation errors
- `NotFoundError` - 404 resource not found
- `AddeparTimeoutError` - Job polling timeout (includes `job_id`, `last_status`)

# Repository Structure

The structure of the repository should align with the Addepar API documentation organization. As such, the repository is structured as:

```
addepy/
├── __init__.py          # Exposes the main AddeparClient
├── client.py            # Main entry point (Handles Auth, HTTP session)
├── exceptions.py        # Custom exceptions (e.g., RateLimitExceeded)
├── models/              # Pydantic models for type safety
│   ├── __init__.py
│   ├── portfolio/
│   │   ├── __init__.py
│   │   ├── transaction.py
│   │   ├── benchmark.py
│   │   └── ...
│   ├── ownership/
│   │   ├── __init__.py
│   │   ├── entity.py
│   │   └── ...
│   └── admin/
│       ├── __init__.py
│       ├── user.py
│       └── ...
└── resources/           # Separate modules for each endpoint group
    ├── __init__.py
    ├── portfolio/
    │   ├── __init__.py  # Re-exports all portfolio resources
    │   ├── arguments.py
    │   ├── attributes.py
    │   ├── benchmarks.py
    │   ├── composite_securities.py
    │   ├── constituent_attributes.py
    │   ├── historical_prices.py
    │   ├── jobs.py
    │   ├── portfolio.py
    │   ├── snapshots.py
    │   └── transactions.py
    ├── ownership/
    │   ├── __init__.py  # Re-exports all ownership resources
    │   ├── entities.py
    │   ├── external_ids.py
    │   ├── groups.py
    │   └── positions.py
    └── admin/
        ├── __init__.py  # Re-exports all admin resources
        ├── audit.py
        ├── billable_portfolios.py
        ├── client_portal.py
        ├── contacts.py
        ├── files.py
        ├── generated_reports.py
        ├── import_tool.py
        ├── report_list.py
        ├── report_generation.py
        ├── target_allocations.py
        ├── roles.py
        ├── teams.py
        ├── users.py
        └── view_sets.py
```

# ADDEPAR API Docs

[https://developers.addepar.com/docs/resource-overview]

## Data Format: JSON:API Specification

The Addepar API strictly follows the JSON:API 1.0 specification.

### Response Structure

- `data`: Contains the primary resource(s).
  - If fetching a list: An array of resource objects.
  - If fetching a single item: A single resource object.
- Resource Object Structure:
  - `id`: The unique string identifier.
  - `type`: The resource type (e.g., entities, views, transactions).
  - `attributes`: A dictionary containing the actual data fields (e.g., `name`, `inception_date`).
  - `relationships`: References to related objects (contains `data` with `type` and `id`).
- `included`: (Optional) If the request uses the include parameter, this array contains the full objects referenced in relationships, effectively sideloading data to prevent N+1 queries.
- `meta`: Contains metadata, predominantly used for pagination.
- `links`: Contains navigation links (e.g., self, next, prev, first, last).

## Resource Sections

### PORTFOLIO (Market Data & Holdings)

- Arguments
- Attributes
- Benchmarks
  - Benchmark Compositions
  - Imported Benchmark Data
  - Benchmark Associations Strategies
- Composite Securities
- Constituent Attributes
- Historical Prices
- Jobs
- Portfolio
  - View List
  - View
  - Query
- Snapshots
- Transactions
  - View
  - Query
  - Transaction Jobs
  - Supported Transaction Types

### OWNERSHIP (Entity Management)

- Entities
  - Model Types
- External IDs
  - External ID Types
- Groups
  - Group Types
- Positions

### ADMIN (System & User Management)

- Audit
- Billable Portfolios
- Client Portal
- Contacts
- Files
- Generated Reports
- Import Tool (beta)
- Report List
- Report Generation
- Target Allocations
- Roles
- Teams
- Users
- View Sets
