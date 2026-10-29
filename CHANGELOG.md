# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-10-29

### Added
- `client.billing` owns fees, fee schedules, billable portfolios, payout recipients, and payout rules.
- Transaction destination and relationship lookups, attachment retrieval, and file association/removal methods.
- Creator resource and relationship lookups for portfolio and transaction jobs.
- Billing read expansions and complete-document/page access, snapshot knowledge dates, transaction destination relationships, external-ID query scopes, optional audit dates/action filters, and additional file filters.
- Import support for `BENCHMARK_PROXIES` and `CONSTITUENT_ATTRIBUTES`, and `node_fee` transaction type hints.

### Changed
- Removed billing properties and resource exports from `client.admin`; use `client.billing` and imports from `addepy.resources.billing`.
- Fee schedule creation now sends a JSON:API array. Billing validates documented batch sizes, fee schedule associations, and read-only fee relationships.
- Snapshot single updates send explicit `None` as JSON null; omitted fields remain unchanged. Snapshot creation permits omitted units for assets that do not require them.
- Synchronous portfolio query grouping strings become attribute objects. Report and benchmark pagination respect resource-specific limits.
- Portfolio query-job submission, polling, completion detection, and downloads remain unchanged.

## [1.0.0] - 2026-10-28

First stable release of AddePy.

### Fixed
- All four audit query methods now follow pagination through the shared authenticated transport, retaining timeout, retry, and SDK error handling. Shared pagination handles absolute, API-prefixed, and dictionary links and detects repeated pages.
- Import creation (including deletion imports), status, and results requests now send `Accept: application/json`, matching the Import Tool endpoints. CSV request bodies retain `Content-Type: text/plain`.
- Benchmark proxy listing and iteration require a nonempty `entity_ids` sequence, matching Addepar's required filter. The benchmark-proxy diagnostic now uses `--entity-id` and reports missing input when it is absent.

### Changed
- Package metadata now identifies AddePy as Production/Stable.
- The migration guide covers upgrades from 0.6 and earlier releases to 1.0.

## [0.6.0] - 2026-09-16

### Added
- Explicit configuration factories: `AddePy.from_env()` for process variables and `AddePy.from_dotenv()` for a consuming Git repository's root `.env` or an explicit file path.
- Raw dictionary/JSON-string queries for portfolio and transaction jobs, shared wait/resume/download helpers, and optional beta batched portfolio jobs.
- Raw synchronous portfolio/transaction queries.
- OAuth bearer/refresh support, explicit environment URLs, injected sessions, public raw requests, full-page iteration, and atomic streaming downloads.
- Fees, fee schedules, payouts, report schedules, expanded billable portfolios, estimated returns, derivative underlying assets, benchmark proxy reads/deletes, and model-type changes.
- Offline unit/contract suite with network blocking and CI; an explicit guarded live diagnostic command with JSON/Markdown reports.

### Changed
- `AddePy(...)` now uses only explicit settings; `load_env` is removed. Factories do not merge file/process settings, interpolate values, or modify the environment. See the configuration migration examples.
- pandas is optional; imports accept CSV text/bytes, Path, file objects, and DataFrames.
- Read requests retry transient failures within configured limits; writes require explicit retry opt-in.
- Polling uses immediate status checks and monotonic deadlines; pagination follows returned endpoint-specific coordinates.
- HTTP exceptions retain status, structured errors and request IDs without copying bodies into their messages.

### Fixed
- Portfolio polling recognizes completed result documents without a status, matching user-confirmed live behavior despite the online documentation. Other missing-status responses still fail; explicit failure states terminate polling.
- Diagnostics no longer label jobs `Pending` before receiving a status; completed portfolio results are reported as `Completed` even when the API omits status and progress.
- Bulk transaction/benchmark methods preserve caller inputs.
- Historical-price submissions reject missing async job IDs.
- File uploads use the shared authenticated transport.
- README method aliases and package version metadata are consistent.

See [SDK documentation](docs/README.md) and [development](docs/development.md) for API usage and testing.

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
