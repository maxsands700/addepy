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
    │   ├── external_id_types.py  # External system mappings
    │   ├── groups.py          # Group management
    │   ├── group_types.py     # Group type definitions
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

### 1. Daily Portfolio Valuation Report

```python
from addepy import AddePy
import pandas as pd

addepy = AddePy()

# Get all client entities
clients = addepy.ownership.entities.list_entities(entity_type="client")

# Run a portfolio query for each client's holdings
results = addepy.portfolio.jobs.execute_portfolio_query({
    "columns": [{"key": "value"}, {"key": "cost_basis"}, {"key": "unrealized_gain_loss"}],
    "groupings": [{"key": "asset_class"}, {"key": "security"}],
    "portfolio_type": "FIRM_CLIENTS",
    "portfolio_id": 1,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
})

# Export to Excel for distribution
df = pd.DataFrame(results)
df.to_excel("daily_valuations.xlsx")
```

### 2. Automated Client Onboarding

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
addepy.ownership.external_id_types.create_external_id_type(
    external_type_key="salesforce",
    display_name="Salesforce"
)
```

### 3. Monthly Performance Reporting

```python
# Execute saved view for all households
households = addepy.ownership.groups.list_groups(group_type="household")

for household in households:
    # Generate performance report as Excel
    report_data = addepy.portfolio.analysis.get_view_results(
        view_id="quarterly_performance",
        portfolio_id=int(household["id"]),
        portfolio_type="GROUP",
        start_date="2024-10-01",
        end_date="2024-12-31",
        output_type="XLSX"
    )

    # Upload to client portal
    file = addepy.admin.files.upload_file(
        file_data=report_data,
        name=f"{household['attributes']['name']}_Q4_Performance.xlsx",
        group_ids=[household["id"]]
    )

    # Publish to client portal with notification
    addepy.admin.client_portal.publish_files(
        files_id=[int(file["id"])],
        portal_publishing="publish",
        contact_notification="notify"
    )
```

### 4. Billing Data Preparation

```python
# Get all billable portfolios
billable = addepy.admin.billable_portfolios.list_billable_portfolios()

# Query AUM for billing calculations
billing_data = addepy.portfolio.analysis.query(
    columns=[
        {"key": "value", "arguments": {"time_point": "end"}},
        {"key": "average_daily_value"}
    ],
    groupings=[{"key": "owner_name"}],
    portfolio_type="FIRM",
    portfolio_id=1,
    start_date="2024-10-01",
    end_date="2024-12-31"
)

# Export for billing system
df = pd.DataFrame(billing_data["data"]["attributes"]["total"]["children"])
df.to_csv("quarterly_billing_aum.csv")
```

### 5. Rebalancing Analysis

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

### 6. Bulk Transaction Import

```python
import pandas as pd

# Prepare transaction data
transactions_df = pd.DataFrame({
    "Account": ["ABC-123", "ABC-123", "DEF-456"],
    "Security": ["AAPL", "GOOGL", "MSFT"],
    "Transaction Type": ["BUY", "BUY", "SELL"],
    "Trade Date": ["2024-12-01", "2024-12-01", "2024-12-02"],
    "Quantity": [100, 50, 75],
    "Price": [150.00, 140.00, 380.00]
})

# Execute import with polling
result = addepy.admin.import_tool.execute_import(
    data=transactions_df,
    import_type="TRANSACTIONS"
)

print(f"Imported {result['success_count']} transactions")
```

### 7. Audit & Compliance Monitoring

```python
from datetime import datetime, timedelta

# Monitor login attempts for the past week
week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

login_attempts = addepy.admin.audit.query_login_attempts(
    start_date=week_ago,
    end_date=datetime.now().strftime("%Y-%m-%d")
)

# Flag failed attempts
failed_logins = [l for l in login_attempts if l["attributes"]["success"] == False]
if failed_logins:
    print(f"Alert: {len(failed_logins)} failed login attempts this week")

# Track attribute changes on sensitive fields
changes = addepy.admin.audit.query_attribute_changes(
    start_date=week_ago,
    attribute_keys=["cost_basis", "value", "owner"]
)
```

### 8. CRM Integration via External IDs

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

### 9. Historical Price Backfill

```python
# Backfill prices for a private security
prices = [
    {"date": "2024-01-01", "nodeId": 12345, "value": 100.00},
    {"date": "2024-02-01", "nodeId": 12345, "value": 102.50},
    {"date": "2024-03-01", "nodeId": 12345, "value": 105.25},
    {"date": "2024-04-01", "nodeId": 12345, "value": 103.00},
]

job_id = addepy.portfolio.historical_prices.create_prices(
    entity_id="12345",
    prices=prices
)

print(f"Price backfill job submitted: {job_id}")
```

### 10. Team Access Management

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
