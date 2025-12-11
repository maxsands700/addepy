# Resource Overview

Addepar is an open platform that facilitates the secure exchange of data with other applications or products through a REST API. The API is divided into three workflow categories: Portfolio, Ownership Graph, and Admin.

The Addepar API provides access to data via HTTPS using unique API endpoints, and provides programmatic access to data in [JSON:API](https://jsonapi.org/) spec format for the following resources:

## Portfolio

[block:parameters]
{
"data": {
"h-0": "Resource Area",
"h-1": "Base Route",
"h-2": "Description",
"0-0": "Arguments",
"0-1": "`/v1/arguments`",
"0-2": "Discover the available Addepar attribute arguments.",
"1-0": "Attributes",
"1-1": "`/v1/attributes`",
"1-2": "Discover available Addepar attributes.",
"2-0": "Jobs",
"2-1": "`/v1/jobs`",
"2-2": "Submit asynchronous portfolio jobs, monitor the status, and download the results.",
"3-0": "Portfolio",
"3-1": "`/v1/portfolio/query` \n \n`/v1/portfolio/views`",
"3-2": "Extract portfolio data for a saved analysis view or with a direct query.",
"4-0": "Transactions",
"4-1": "`/v1/transactions` \n \n`/v1/transactions/views` \n \n`/v1/transactions/query`",
"4-2": "Create and delete transactions in Addepar, retrieve, and update transaction details. \n \nExtract transaction data from an existing view or a query directly using specific parameters.",
"5-0": "Snapshots",
"5-1": "`/v1/snapshots`",
"5-2": "Retrieve snapshot and valuation details.",
"6-0": "Benchmarks",
"6-1": "`/v1/benchmarks`",
"6-2": "Get, create, update, and delete benchmarks.",
"7-0": "Benchmark Compositions",
"7-1": "`/v1/benchmark_compositions`",
"7-2": "Retrieve or update benchmark compositions.",
"8-0": "Imported Benchmark Data",
"8-1": "`/v1/imported_benchmark_data`",
"8-2": "Maintain your own custom benchmarks.",
"9-0": "Benchmark Associations Strategies",
"9-1": "`/v1/benchmark_associations_strategies`",
"9-2": "Manage benchmark associations."
},
"cols": 3,
"rows": 10,
"align": [
"left",
"left",
"left"
]
}
[/block]

## Ownership

| Resource Area | Base Route              | Description                                                                                                                               |
| :------------ | :---------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| Entities      | `/v1/entities`          | Create and delete entities, as well as retrieve and update entity details.                                                                |
| Entity Types  | `/v1/entity_types`      | Discover the available entity types including associated attributes, attributes required for creation, and which attributes are editable. |
| Groups        | `/v1/groups`            | Create and delete groups, as well as retrieve and update group details.                                                                   |
| Positions     | `/v1/positions`         | Create and delete positions, as well as retrieve and update position details.                                                             |
| External IDs  | `/v1/external_id_types` | Create External IDs to seamlessly query portfolio data across Addepar and non-Addepar systems and applications.                           |

## Admin

[block:parameters]
{
"data": {
"h-0": "Resource Area",
"h-1": "Base Route",
"h-2": "Description",
"0-0": "Audit",
"0-1": "`/v1/audit_trail`",
"0-2": "Retrieve audit logs.",
"1-0": "Billable Portfolios",
"1-1": "`/v1/billable_portfolios`",
"1-2": "Create billable portfolios.",
"2-0": "Client Portal",
"2-1": "`/v1/portal/publish_files`",
"2-2": "Publish reports or files to the Client Portal and notify clients.",
"3-0": "Contacts",
"3-1": "`v1/contacts`",
"3-2": "Create, view, update, and delete contacts, as well as update their information and affiliations.",
"4-0": "Files",
"4-1": "`/v1/files`",
"4-2": "Access to files that have been uploaded into the file vault including any reports generated.",
"5-0": "Generated Reports",
"5-1": "`/v1/generated_reports `",
"5-2": "Access to generated report objects.",
"6-0": "Import Tool",
"6-1": "`/v1/imports  ` \n`/v1/import_results`",
"6-2": "Automate all data import workflows currently available in the import tool.",
"7-0": "Report List",
"7-1": "`/v1/reports`",
"7-2": "Get a list of reports to streamline various operations workflows.",
"8-0": "Report Generation",
"8-1": "`/v1/report_generation_job`",
"8-2": "Run reports.",
"9-0": "Roles",
"9-1": "`/v1/roles`",
"9-2": "View roles created by your firm, as well as add or remove the users assigned to each role.",
"10-0": "Teams",
"10-1": "`/v1/teams`",
"10-2": "Create, view, update, and delete teams, as well as update the users in teams.",
"11-0": "Users",
"11-1": "`/v1/users`",
"11-2": "View, create, and delete users, update user information, tool permissions, and portfolio access."
},
"cols": 3,
"rows": 12,
"align": [
"left",
"left",
"left"
]
}
[/block]
