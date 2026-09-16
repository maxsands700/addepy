# Changelog

All notable changes to this project will be documented in this file.

## [0.6.0] - 2026-09-16

### Added
- Raw dictionary/JSON-string queries for portfolio and transaction jobs, shared wait/resume/download helpers, and optional beta batched portfolio jobs.
- Raw synchronous portfolio/transaction queries.
- OAuth bearer/refresh support, explicit environment URLs, injected sessions, public raw requests, full-page iteration, and atomic streaming downloads.
- Fees, fee schedules, payouts, report schedules, expanded billable portfolios, estimated returns, derivative underlying assets, benchmark proxy reads/deletes, and model-type changes.
- Offline unit/contract suite with network blocking and CI; an explicit guarded live diagnostic command with JSON/Markdown reports.

### Changed
- pandas is optional; imports accept CSV text/bytes, Path, file objects, and DataFrames.
- Read requests retry transient failures within configured limits; writes require explicit retry opt-in.
- Polling uses immediate status checks and monotonic deadlines; pagination follows returned endpoint-specific coordinates.
- HTTP exceptions retain status, structured errors and request IDs without copying bodies into their messages.

### Fixed
- Missing job status no longer signals success; documented failure states terminate polling.
- Bulk transaction/benchmark methods preserve caller inputs.
- Historical-price submissions reject missing async job IDs.
- File uploads use the shared authenticated transport.
- README method aliases and package version metadata are consistent.

See MIGRATION.md, TESTING.md, and docs/API_COVERAGE.md for behavior changes and live-verification limits.

## [0.2.0] - 2025-12-12

### Added
- Complete Portfolio namespace with:
  - Analysis/Views API for portfolio queries
  - Arguments API for attribute arguments
  - Attributes API for attribute discovery
  - Benchmarks API for benchmark management
  - Composite Securities API for ETF constituents
  - Historical Prices API
  - Snapshots API for point-in-time data
  - Transaction management and queries

- Complete Ownership namespace with:
  - Entities API with entity types
  - Groups API with group member management and child groups
  - Group Types API (merged into Groups resource)
  - Positions API for ownership relationships
  - External IDs API for system mappings

- Complete Admin namespace with:
  - Audit trail queries
  - Billable Portfolios API
  - Client Portal publishing
  - Contacts management
  - File management
  - Reports generation
  - Roles and Permissions
  - Teams management
  - Users management
  - View Sets (Client Portal views)
  - Target Allocations API

### Changed
- Merged `GroupTypesResource` into `GroupsResource` for better ergonomics
- Renamed `external_id_types.py` to `external_ids.py` for conciseness
- Updated `OwnershipNamespace` to use `external_ids` property

### Removed
- Removed separate `group_types.py` file (functionality merged into `groups.py`)

## [0.1.0] - 2025-12-10

### Initial Release
- Core SDK framework and authentication
- Portfolio Jobs API (`client.portfolio.jobs`)
- Ownership Entities API (`client.ownership.entities`)
- Admin Import Tool API (`client.admin.import_tool`)
- Async job polling with exponential backoff
- Pagination support for list endpoints
- Custom exception handling and logging
