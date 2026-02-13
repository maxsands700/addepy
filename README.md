# AddePy

Unofficial Python SDK for the Addepar API.

## Installation
Create a `venv` for your Python project, and then install `addepy` with:

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

## Basic Usage

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

_The Import Tool via API is in Beta (as of 12/10/2025), so you may need to request access for your firm. However, this is a great tool... the Import Tool allows data management of almost all resources in Addepar..._

## Design Philosophy

### Repository Structure

Mirrors the [Addepar API documentation](https://developers.addepar.com/docs/resource-overview):

```
addepy/
├── client.py                  # Main entry point
├── exceptions.py              # Custom exceptions
├── constants.py               # SDK constants
└── resources/
    ├── base.py                # Base resource class
    │
    ├── portfolio/             # PORTFOLIO namespace
    │   ├── analysis.py        # Views & queries
    │   ├── arguments.py       # Attribute arguments
    │   ├── attributes.py      # Attribute discovery
    │   ├── benchmarks.py      # Benchmark management
    │   ├── composite_securities.py  # ETF constituents
    │   ├── constituent_attributes.py
    │   ├── historical_prices.py
    │   ├── jobs.py            # Async query jobs
    │   ├── snapshots.py       # Point-in-time snapshots
    │   ├── transactions.py    # Transaction management
    │   └── transaction_jobs.py
    │
    ├── ownership/             # OWNERSHIP namespace
    │   ├── entities.py        # Entities & entity types
    │   ├── external_ids.py    # External system mappings
    │   ├── groups.py          # Groups & group types
    │   └── positions.py       # Ownership relationships
    │
    └── admin/                 # ADMIN namespace
        ├── audit.py           # Audit trail queries
        ├── billable_portfolios.py
        ├── client_portal.py   # Portal publishing
        ├── contacts.py        # Contact management
        ├── files.py           # File management
        ├── import_tool.py     # Bulk data imports
        ├── reports.py         # Report generation
        ├── roles.py           # Role definitions
        ├── target_allocations.py
        ├── teams.py           # Team management
        ├── users.py           # User management
        └── view_sets.py       # Client portal views
```

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

### Pagination: `list_*` vs `iter_*`

Every paginated endpoint has two methods:

| Method   | Returns     | Default limit | Use when...                              |
| -------- | ----------- | ------------- | ---------------------------------------- |
| `list_*` | `list`      | 10,000        | You need all results in memory at once   |
| `iter_*` | `Generator` | No limit      | You want to process items one at a time  |

**`list_*`** fetches pages behind the scenes and returns a plain list. It caps results at 10,000 by default to prevent runaway API calls, and logs a warning if the cap is hit.

```python
# Returns up to 10,000 entities as a list
entities = addepy.ownership.entities.list_entities()

# Override the default limit
entities = addepy.ownership.entities.list_entities(limit=50_000)
```

**`iter_*`** returns a lazy generator that yields one item at a time, only fetching the next page when needed. This keeps memory usage constant regardless of result size and gives you full control over when to stop.

```python
# Process entities one at a time - memory-efficient for large datasets
for entity in addepy.ownership.entities.iter_entities():
    process(entity)

# Stop early whenever you want
for entity in addepy.ownership.entities.iter_entities():
    if found_what_i_need(entity):
        break

# Cap results on the iterator too
for entity in addepy.ownership.entities.iter_entities(limit=100):
    process(entity)
```

Use `list_*` for small-to-medium datasets where you need random access or the full list. Use `iter_*` when working with large datasets or when you want to process results as they arrive.

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

## Example Workflows

Real-world automation examples for wealth management firms:

### Bulk Imports

```python
import pandas as pd

# Prepare transaction data
attributes_df = pd.DataFrame({
    "Entity ID": [11111111, 22222222, 33333333],
    "Attribute Name": ["Portfolio Manager", "Trust Advisor", "Account Status"],
    "Attribute Value": ["Michael Scott", "Dwight Schrute", "Closed"],
})

# Execute import with polling
result = addepy.admin.import_tool.execute_import(
    data=attributes_df,
    import_type="ATTRIBUTES"
)

print(f"Imported {result['success_count']} transactions")
```

### Audit & Compliance Monitoring

```python
from addepy import AddePy
from datetime import datetime, timedelta

# 1. Query recent attribute changes on sensitive fields
week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
changes = addepy.admin.audit.query_attribute_changes(
    start_date=week_ago,
    attribute_keys=["portfolio_manager"]
)

# 2. Flag changes for compliance review
flagged = flag_for_compliance(changes)  # Your custom logic

# 3. Generate report and notify stakeholders
send_compliance_report(flagged)  # Your email/Slack integration
```

### Prospecting & Client Onboarding Workflows

```python
# Create new client entity
client = addepy.ownership.entities.create_entity(
    entity_type_id="client",
    name="Smith Family Trust",
    attributes={"inception_date": "2024-01-15"}
)

# Create associated accounts
account = addepy.ownership.entities.create_entity(
    entity_type_id="account",
    name="Smith Brokerage Account",
    attributes={"account_number": "ABC-123456"}
)

# Link account to client via position
addepy.ownership.positions.create_position(
    owner_id=client["id"],
    owned_id=account["id"],
    inception_date="2024-01-15"
)

# Map to CRM system
addepy.ownership.external_ids.create_external_id_type(
    external_type_key="salesforce",
    display_name="Salesforce"
)
```

### Rebalancing Analysis, Integrations w/ Trading Systems

```python
# Get target allocations for a portfolio
allocations = addepy.admin.target_allocations.list_allocation_models()

# Compare current vs target
current_holdings = addepy.portfolio.analysis.query(
    columns=[{"key": "value"}, {"key": "weight"}],
    groupings=[{"key": "asset_class"}],
    portfolio_type="ENTITY",
    portfolio_id=12345,
    start_date="2024-12-01",
    end_date="2024-12-31"
)

# Calculate drift from targets
for holding in current_holdings["data"]["attributes"]["total"]["children"]:
    asset_class = holding["name"]
    current_weight = holding["columns"]["weight"]
    # Compare to target and flag if drift > threshold
```

### Integration with External Systems (CRM, Custodians, Trading, etc.)

```python
# Sync Salesforce contacts with Addepar entities
salesforce_contacts = get_salesforce_contacts()  # Your CRM API

for contact in salesforce_contacts:
    # Find matching Addepar entity by external ID
    entities = addepy.ownership.entities.list_entities(
        external_id_type="salesforce",
        external_id=contact["sf_id"]
    )

    if entities:
        # Update existing entity
        addepy.ownership.entities.update_entity(
            entity_id=entities[0]["id"],
            attributes={"email": contact["email"], "phone": contact["phone"]}
        )
    else:
        # Create new entity with external ID mapping
        addepy.ownership.entities.create_entity(
            entity_type_id="contact",
            name=contact["name"],
            external_ids=[{
                "external_type_key": "salesforce",
                "external_id": contact["sf_id"]
            }]
        )
```

### Team Access Management

```python
# Create a new team for junior analysts
team = addepy.admin.teams.create_team(
    name="Junior Analysts",
    description="Read-only access to client portfolios"
)

# Get the appropriate role
roles = addepy.admin.roles.list_roles()
analyst_role = next(r for r in roles if r["attributes"]["name"] == "Analyst")

# Add users to the team
users = addepy.admin.users.list_users()
junior_users = [u for u in users if "junior" in u["attributes"]["email"].lower()]

for user in junior_users:
    addepy.admin.teams.add_team_member(
        team_id=team["id"],
        user_id=user["id"],
        role_id=analyst_role["id"]
    )
```
