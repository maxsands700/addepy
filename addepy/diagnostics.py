"""Explicit, guarded live compatibility checks with sanitized local reports.

Run ``python -m addepy.diagnostics --env-file .env.sandbox``. Importing this
module never reads credentials or makes requests. Reports contain outcomes,
HTTP codes and job identifiers, never API bodies or copied query contents.
"""

import argparse
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import time
from typing import Any
from urllib.parse import urlparse

from dotenv import dotenv_values
import requests

from ._version import __version__
from .client import AddePy
from .exceptions import (
    AddePyError,
    AddePyTimeoutError,
    AuthenticationError,
    ForbiddenError,
    GoneError,
    JobError,
    NotFoundError,
    ProtocolError,
    RateLimitError,
    TransportError,
    ValidationError,
)
from .resources.query import query_parameters


class DiagnosticConfigError(ValueError):
    """A configuration problem described without including configuration values."""


class GuardViolation(AddePyError):
    """A live check attempted a request outside the diagnostic policy."""


@dataclass(frozen=True)
class Check:
    endpoint: str
    method: str
    shape: type
    paginated: bool = True
    requires_entity: bool = False


READ_CHECKS = {
    "current_user": Check("/users/me", "admin.users.get_current_user", dict, False),
    "entities": Check("/entities", "ownership.entities.list_entities", list),
    "portfolio_views": Check(
        "/portfolio/views", "portfolio.analysis.list_views", list, False
    ),
    "attributes": Check("/attributes", "portfolio.attributes.list_attributes", list),
    "benchmarks": Check("/benchmarks", "portfolio.benchmarks.list_benchmarks", list),
    "benchmark_proxies": Check(
        "/benchmark_proxies", "portfolio.benchmarks.list_benchmark_proxies", list
    ),
    "estimated_returns": Check(
        "/estimated_returns",
        "portfolio.estimated_returns.list_estimated_returns",
        list,
        requires_entity=True,
    ),
    "underlying_assets": Check(
        "/derivatives/underlying_assets",
        "portfolio.underlying_assets.list_underlying_assets",
        list,
    ),
    "report_schedules": Check(
        "/report_schedule", "admin.report_schedules.list_schedules", list
    ),
    "fees": Check("/fees", "admin.fees.list_fees", list),
    "fee_schedules": Check(
        "/fee_schedules", "admin.fee_schedules.list_fee_schedules", list
    ),
    "billable_portfolios": Check(
        "/billable_portfolios",
        "admin.billable_portfolios.list_billable_portfolios",
        list,
    ),
    "payout_recipients": Check(
        "/billing/payout/recipients",
        "admin.payout_recipients.list_payout_recipients",
        list,
    ),
    "payout_rules": Check(
        "/billing/payout/rules", "admin.payout_rules.list_payout_rules", list
    ),
}
DEFAULT_CHECKS = ("current_user", "entities", "portfolio_views")
JOB_CHECKS = ("portfolio_job", "transaction_job")
ALL_CHECKS = (*READ_CHECKS, *JOB_CHECKS)
DOC_LINKS = {
    "current_user": "https://developers.addepar.com/docs/users",
    "entities": "https://developers.addepar.com/docs/entities",
    "portfolio_views": "https://developers.addepar.com/docs/portfolio-views",
    "attributes": "https://developers.addepar.com/docs/attributes",
    "benchmarks": "https://developers.addepar.com/docs/benchmarks",
    "benchmark_proxies": "https://developers.addepar.com/reference/listbenchmarkproxies",
    "estimated_returns": "https://developers.addepar.com/docs/estimated-returns",
    "underlying_assets": "https://developers.addepar.com/docs/underlying-assets",
    "report_schedules": "https://developers.addepar.com/docs/report-schedules",
    "fees": "https://developers.addepar.com/docs/fee-rules",
    "fee_schedules": "https://developers.addepar.com/docs/fee-schedules",
    "billable_portfolios": "https://developers.addepar.com/docs/billing",
    "payout_recipients": "https://developers.addepar.com/docs/payout-recipients",
    "payout_rules": "https://developers.addepar.com/docs/payout-rules",
    "portfolio_job": "https://developers.addepar.com/docs/jobs",
    "transaction_job": "https://developers.addepar.com/docs/transaction-jobs",
}
KNOWN_JOB_STATUSES = {
    "Queued",
    "In Progress",
    "In Progress - Waiting For Capacity",
    "Picked Up By Job Runner",
    "Completed",
    "Canceled",
    "Timed Out",
    "Failed",
    "Rejected",
    "Error",
    "Error Cancelled",
    "Cancel Requested",
    "User Cancelled",
}


def _origin(url: str) -> tuple[str, str | None, int]:
    parsed = urlparse(url)
    return parsed.scheme, parsed.hostname, parsed.port or 443


def host_environment(base_url: str) -> str:
    """Identify documented non-production hosts, without trusting an env label."""
    parsed = urlparse(base_url)
    if parsed.port not in (None, 443):
        return "production_or_custom"
    hostname = parsed.hostname or ""
    tenant = r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    if re.fullmatch(tenant + r"\.sandbox\.addepar\.com", hostname):
        return "sandbox"
    if re.fullmatch(tenant + r"\.clientdev\.addepar\.com", hostname):
        return "development"
    return "production_or_custom"


def validate_base_url(base_url: str, *, production: bool) -> str:
    try:
        parsed = urlparse(base_url)
        valid = (
            parsed.scheme == "https"
            and parsed.hostname
            and not parsed.username
            and not parsed.password
            and not parsed.query
            and not parsed.fragment
            and parsed.path.rstrip("/") in ("/api/v1", "/v1")
        )
        environment = host_environment(base_url)
    except ValueError as exc:
        raise DiagnosticConfigError("The API base URL is invalid.") from exc
    if not valid:
        raise DiagnosticConfigError(
            "Use an HTTPS API base URL ending in /api/v1 or /v1, without credentials or query parameters."
        )
    if environment == "production_or_custom" and not production:
        raise DiagnosticConfigError(
            "The actual API host requires --production; an environment label cannot bypass this check."
        )
    return base_url.rstrip("/")


class RequestGuard:
    """Check prepared requests immediately before the session sends them."""

    def __init__(
        self,
        base_url: str,
        *,
        production: bool,
        allow_exports: bool,
        downloads: bool = False,
    ) -> None:
        self.base_url = validate_base_url(base_url, production=production)
        self.origin = _origin(self.base_url)
        self.allow_exports = allow_exports
        self.downloads = downloads
        prefix = urlparse(self.base_url).path
        self.export_routes = {
            prefix + "/jobs": ("jobs", "PORTFOLIO_QUERY"),
            prefix + "/transaction_jobs": ("transaction_jobs", "transaction_query"),
        }

    def validate(self, request: requests.PreparedRequest) -> None:
        method = (request.method or "").upper()
        try:
            parsed = urlparse(request.url or "")
            valid_url = (
                parsed.scheme == "https"
                and parsed.hostname
                and not parsed.username
                and not parsed.password
                and not parsed.fragment
            )
            same_origin = _origin(request.url or "") == self.origin
        except ValueError:
            valid_url = False
            same_origin = False
        if not valid_url or (not self.downloads and not same_origin):
            raise GuardViolation("Diagnostic request blocked by the host policy.")
        if self.downloads:
            if method not in ("GET", "HEAD") or any(
                name in request.headers
                for name in ("Authorization", "Addepar-Firm", "Cookie")
            ):
                raise GuardViolation(
                    "Download requests must be reads without API credentials or cookies."
                )
            return
        if method in ("GET", "HEAD"):
            return
        expected = self.export_routes.get(parsed.path)
        if (
            method != "POST"
            or not self.allow_exports
            or expected is None
            or parsed.query
        ):
            raise GuardViolation(
                "Only reads and explicitly selected query-export submissions are permitted."
            )
        try:
            document = json.loads(request.body)
            data = document["data"]
            attributes = data["attributes"]
            valid_body = (
                set(document) == {"data"}
                and set(data) == {"type", "attributes"}
                and set(attributes) == {"job_type", "parameters"}
                and data["type"] == expected[0]
                and attributes["job_type"] == expected[1]
                and isinstance(attributes["parameters"], dict)
            )
        except (ValueError, TypeError, KeyError):
            valid_body = False
        if not valid_body:
            raise GuardViolation(
                "Job submission does not match an allowed query-export contract."
            )


class GuardedSession(requests.Session):
    def __init__(self, guard: RequestGuard) -> None:
        super().__init__()
        self.guard = guard
        # Only the chosen env file supplies credentials; ignore netrc settings.
        self.trust_env = False
        self.last_status: int | None = None
        self.last_path: str | None = None
        self.last_data_shape: type | None = None

    def send(
        self, request: requests.PreparedRequest, **kwargs: Any
    ) -> requests.Response:
        self.guard.validate(request)
        response = super().send(request, **kwargs)
        self.last_status = response.status_code
        self.last_path = urlparse(request.url).path
        self.last_data_shape = None
        if not kwargs.get("stream"):
            try:
                document = response.json()
                if isinstance(document, dict) and "data" in document:
                    self.last_data_shape = type(document["data"])
            except ValueError:
                pass
        return response


@dataclass
class CheckResult:
    name: str
    status: str = "incomplete"
    detail: str = "Check did not complete."
    http_status: int | None = None
    elapsed_seconds: float = 0
    job_id: str | None = None
    job_status: str | None = None
    progress: float | None = None
    source_url: str | None = None


@dataclass
class DiagnosticReport:
    environment: str
    read_only: bool
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    sdk_version: str = __version__
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        if any(
            check.status in {"contract_failure", "internal_error"}
            for check in self.checks
        ):
            return 1
        if not self.checks or any(check.status != "pass" for check in self.checks):
            return 2
        return 0


def classify_exception(error: Exception) -> tuple[str, str]:
    """Return only fixed report text, never exception messages or response data."""
    if isinstance(error, AuthenticationError):
        return (
            "auth_blocked",
            "Authentication failed; no compatibility conclusion is available.",
        )
    if isinstance(error, ForbiddenError):
        return (
            "permission_blocked",
            "The credential lacks permission for this endpoint.",
        )
    if isinstance(error, RateLimitError):
        return "rate_limited", "The server rate limit blocked the check; retry later."
    if isinstance(error, (NotFoundError, GoneError)):
        return (
            "unavailable",
            "The endpoint/resource is unavailable, hidden, or expired.",
        )
    if isinstance(error, GuardViolation):
        return "policy_blocked", "The request guard prevented an unapproved request."
    if isinstance(error, AddePyTimeoutError):
        return (
            "incomplete",
            "The wait deadline elapsed; use the job ID to resume without resubmission.",
        )
    if isinstance(error, (TransportError, requests.RequestException)):
        return "network_error", "A network request failed or timed out."
    if isinstance(error, (JobError, ProtocolError, ValidationError, ValueError)):
        return (
            "contract_failure",
            "The request, job state, or response did not satisfy the check; verify the supplied query and API contract.",
        )
    if isinstance(error, AddePyError):
        if error.status_code is not None and error.status_code >= 500:
            return "unavailable", "The server could not complete the request."
        return "contract_failure", "The API rejected the compatibility check."
    return (
        "internal_error",
        "The check encountered an unexpected SDK error; details are intentionally omitted.",
    )


def _job_metadata(result: CheckResult, job_id: Any, document: Any = None) -> None:
    if isinstance(job_id, (str, int)) and re.fullmatch(
        r"[A-Za-z0-9_-]{1,128}", str(job_id)
    ):
        result.job_id = str(job_id)
    attributes = (
        document.get("data", {}).get("attributes", {})
        if isinstance(document, dict) and isinstance(document.get("data"), dict)
        else {}
    )
    if not isinstance(attributes, dict):
        return
    status = attributes.get("status")
    if isinstance(status, str):
        result.job_status = status if status in KNOWN_JOB_STATUSES else "Unknown"
    progress = attributes.get("percent_complete")
    if (
        isinstance(progress, (float, int))
        and not isinstance(progress, bool)
        and math.isfinite(progress)
        and 0 <= progress <= 1
    ):
        result.progress = float(progress)


def _check_read(client: AddePy, check: Check, *, entity_id: str | None) -> int | None:
    method: Any = client
    for name in check.method.split("."):
        method = getattr(method, name)
    kwargs: dict[str, Any] = {"limit": 1, "page_limit": 1} if check.paginated else {}
    if check.requires_entity:
        kwargs["entity_ids"] = [entity_id]
    value = method(**kwargs)
    if not isinstance(value, check.shape):
        raise ProtocolError("The resource method returned an unexpected data shape.")
    if check.shape is dict and not value:
        raise ProtocolError("The resource method returned an empty resource object.")
    if check.shape is list and any(not isinstance(item, dict) for item in value):
        raise ProtocolError("Collection items must be resource objects.")
    # This instrumentation retains only types, paths, and status codes. It also
    # catches wrappers that silently turn a malformed response into {} or [].
    session = client._session
    if hasattr(session, "last_data_shape"):
        if session.last_data_shape is not check.shape:
            raise ProtocolError(
                "The API did not return the documented JSON:API data shape."
            )
        if session.last_path != urlparse(client.base_url).path + check.endpoint:
            raise ProtocolError(
                "The resource method requested an unexpected API route."
            )
    status = getattr(session, "last_status", None)
    if status is not None and not 200 <= status < 300:
        raise ProtocolError("The read did not return a successful response.")
    return status


def _check_job(
    client: AddePy,
    name: str,
    result: CheckResult,
    *,
    query_file: str | None,
    job_id: str | None,
    read_only: bool,
    timeout: float,
    poll_interval: float,
    max_result_bytes: int,
) -> None:
    if not job_id and read_only:
        result.status, result.detail = (
            "skipped",
            "Query-job submission was disabled by --read-only.",
        )
        return
    if not job_id and not query_file:
        result.status, result.detail = (
            "missing_input",
            "Supply a query JSON file or an existing job ID to run this check.",
        )
        return
    resource = (
        client.portfolio.jobs
        if name == "portfolio_job"
        else client.portfolio.transaction_jobs
    )
    if job_id is None:
        try:
            query = Path(query_file).read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            result.status, result.detail = (
                "missing_input",
                "The selected query JSON file could not be read.",
            )
            return
        query_parameters(query)  # Validate before any submission; retain raw input.
        job_id = resource.create_job(query)
    _job_metadata(result, job_id)
    result.job_status = "Pending"
    document = resource.wait_for_job(
        job_id, timeout=timeout, initial_wait=poll_interval, max_wait=poll_interval
    )
    _job_metadata(result, job_id, document)
    response = resource.get_job_results(job_id, stream=True)
    result.http_status = response.status_code
    try:
        if not 200 <= response.status_code < 300:
            raise ProtocolError(
                "The query download did not return a successful response.", response
            )
        payload = bytearray()
        for chunk in response.iter_content(chunk_size=65536):
            if len(payload) + len(chunk) > max_result_bytes:
                result.status, result.detail = (
                    "incomplete",
                    "The job completed, but its JSON result exceeds the diagnostic size limit.",
                )
                return
            payload.extend(chunk)
        document = json.loads(payload)
        data = document.get("data") if isinstance(document, dict) else None
        expected = dict if name == "portfolio_job" else list
        if not isinstance(data, expected) or (expected is dict and not data):
            raise ProtocolError(
                "Query results do not have the documented data envelope.", response
            )
        resources = [data] if isinstance(data, dict) else data
        for item in resources:
            if not isinstance(item, dict) or item.get("type") in {
                "jobs",
                "job",
                "transaction_jobs",
            }:
                raise ProtocolError(
                    "The download returned job status rather than query results.",
                    response,
                )
            attributes = item.get("attributes")
            if not isinstance(attributes, dict):
                result.status, result.detail = (
                    "contract_failure",
                    "Downloaded query resources lack the documented attributes object; compatibility is unverified.",
                )
                return
            if "status" in attributes and (
                expected is dict or "job_type" in attributes
            ):
                raise ProtocolError(
                    "The download returned job status rather than query results.",
                    response,
                )
            if expected is dict:
                total = attributes.get("total")
                if not isinstance(total, dict) or not (
                    isinstance(total.get("columns"), dict)
                    or isinstance(total.get("children"), list)
                ):
                    result.status, result.detail = (
                        "contract_failure",
                        "The portfolio result lacks data.attributes.total with columns or children; compatibility is unverified.",
                    )
                    return
    finally:
        response.close()
    result.status, result.detail = (
        "pass",
        "Query job completed and its result was valid JSON; contents were discarded.",
    )
    result.http_status = response.status_code


def selected_checks(args: argparse.Namespace) -> list[str]:
    if args.only:
        selected = list(
            dict.fromkeys(
                name.strip()
                for group in args.only
                for name in group.split(",")
                if name.strip()
            )
        )
        if not selected or any(name not in ALL_CHECKS for name in selected):
            raise DiagnosticConfigError(
                "--only contains an unknown check; use --list-checks."
            )
        return selected
    selected = list(READ_CHECKS if args.extended else DEFAULT_CHECKS)
    if args.portfolio_query or args.portfolio_job_id:
        selected.append("portfolio_job")
    if args.transaction_query or args.transaction_job_id:
        selected.append("transaction_job")
    return selected


def run_diagnostics(
    client: AddePy, args: argparse.Namespace, *, environment: str
) -> DiagnosticReport:
    report = DiagnosticReport(environment=environment, read_only=args.read_only)
    stop_status = None
    for name in selected_checks(args):
        result = CheckResult(name, source_url=DOC_LINKS[name])
        report.checks.append(result)
        if stop_status is not None:
            result.status = stop_status
            result.detail = (
                "Not attempted after an earlier authentication failure or rate limit."
            )
            continue
        start = time.monotonic()
        try:
            if name in READ_CHECKS:
                check = READ_CHECKS[name]
                if check.requires_entity and not args.entity_id:
                    result.status, result.detail = (
                        "missing_input",
                        "Supply --entity-id to check estimated returns; no unfiltered request was sent.",
                    )
                    continue
                result.http_status = _check_read(
                    client, check, entity_id=args.entity_id
                )
                result.status, result.detail = (
                    "pass",
                    "The endpoint returned the expected JSON:API data shape.",
                )
            else:
                prefix = "portfolio" if name == "portfolio_job" else "transaction"
                _check_job(
                    client,
                    name,
                    result,
                    query_file=getattr(args, prefix + "_query"),
                    job_id=getattr(args, prefix + "_job_id"),
                    read_only=args.read_only,
                    timeout=args.job_timeout,
                    poll_interval=args.poll_interval,
                    max_result_bytes=args.max_result_bytes,
                )
        except KeyboardInterrupt:
            result.status, result.detail = (
                "incomplete",
                "The run was interrupted; retain any reported job ID to resume without resubmission.",
            )
            return report
        except Exception as exc:
            result.status, result.detail = classify_exception(exc)
            http_status = getattr(exc, "status_code", None)
            result.http_status = (
                http_status
                if isinstance(http_status, int) and 100 <= http_status <= 599
                else None
            )
            _job_metadata(
                result, getattr(exc, "job_id", None), getattr(exc, "job_data", None)
            )
            if result.status in {"auth_blocked", "rate_limited"}:
                stop_status = result.status
        finally:
            result.elapsed_seconds = round(time.monotonic() - start, 3)
    return report


def configuration(args: argparse.Namespace) -> tuple[dict[str, Any], list[str]]:
    if not args.env_file or not Path(args.env_file).is_file():
        raise DiagnosticConfigError(
            "Choose an existing credential file with --env-file; no default .env file is loaded."
        )
    values = dotenv_values(args.env_file, interpolate=False)
    environment = args.environment or values.get("ADDEPAR_ENVIRONMENT")
    base_url = args.base_url or values.get("ADDEPAR_BASE_URL")
    if environment is not None and environment not in {
        "production",
        "development",
        "sandbox",
    }:
        raise DiagnosticConfigError(
            "The configured environment must be production, development, or sandbox."
        )
    if base_url is None:
        if environment is None:
            raise DiagnosticConfigError(
                "Choose --environment or --base-url (or the corresponding ADDEPAR setting); no environment is assumed."
            )
        firm_name = values.get("ADDEPAR_FIRM_NAME") or ""
        if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?", firm_name):
            raise DiagnosticConfigError(
                "Provide a valid ADDEPAR_FIRM_NAME or an explicit API base URL."
            )
        suffix = {
            "production": "addepar.com",
            "sandbox": "sandbox.addepar.com",
            "development": "clientdev.addepar.com",
        }[environment]
        base_url = f"https://{firm_name}.{suffix}/api/v1"
    base_url = validate_base_url(base_url, production=args.production)
    actual_environment = host_environment(base_url)
    firm_id = values.get("ADDEPAR_FIRM_ID")
    if not firm_id:
        raise DiagnosticConfigError("The credential file must specify ADDEPAR_FIRM_ID.")
    credentials = {
        key: values.get(env)
        for key, env in (
            ("api_key", "ADDEPAR_API_KEY"),
            ("access_token", "ADDEPAR_ACCESS_TOKEN"),
            ("key_id", "ADDEPAR_KEY_ID"),
            ("key_secret", "ADDEPAR_KEY_SECRET"),
        )
    }
    if bool(credentials["key_id"]) != bool(credentials["key_secret"]):
        raise DiagnosticConfigError(
            "The credential file must provide both key ID and key secret."
        )
    if (
        sum(bool(credentials[key]) for key in ("api_key", "access_token", "key_id"))
        != 1
    ):
        raise DiagnosticConfigError(
            "The credential file must supply exactly one authentication method."
        )
    if any(value is not None and "${" in value for value in values.values()):
        raise DiagnosticConfigError(
            "Variable interpolation is disabled; provide literal values in the chosen credential file."
        )
    settings = {
        "base_url": base_url,
        "firm_id": firm_id,
        "load_env": False,
        "environment": environment
        or (
            actual_environment
            if actual_environment != "production_or_custom"
            else "production"
        ),
        "timeout": (min(10.0, args.request_timeout), args.request_timeout),
        "max_retries": 0,
        **{key: value for key, value in credentials.items() if value},
    }
    secrets = [value for value in credentials.values() if value]
    return settings, secrets


def write_reports(
    report: DiagnosticReport, directory: str | Path, *, secrets: list[str] | None = None
) -> tuple[Path, Path]:
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    stem = datetime.now(timezone.utc).strftime("diagnostics-%Y%m%dT%H%M%S%fZ")
    json_path, markdown_path = target / (stem + ".json"), target / (stem + ".md")
    document = asdict(report)
    document["exit_code"] = report.exit_code
    document["summary"] = dict(Counter(check.status for check in report.checks))
    secret_values = sorted(
        (secret for secret in secrets or [] if secret), key=len, reverse=True
    )

    def redact(value: Any) -> Any:
        if isinstance(value, str):
            for secret in secret_values:
                value = value.replace(secret, "[REDACTED]")
            return value
        if isinstance(value, list):
            return [redact(item) for item in value]
        if isinstance(value, dict):
            return {key: redact(item) for key, item in value.items()}
        return value

    document = redact(document)
    json_text = json.dumps(document, indent=2, allow_nan=False) + "\n"
    lines = [
        "# AddePy live compatibility report",
        "",
        f"Environment: {report.environment}",
        f"Started: {report.started_at}",
        f"SDK: {report.sdk_version}",
        f"Exit code: {report.exit_code}",
        "",
        "| Check | Outcome | HTTP | Job ID | Job status | Progress | Detail |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for check in report.checks:
        name = f"[{check.name}]({check.source_url})" if check.source_url else check.name
        lines.append(
            f"| {name} | {check.status} | {check.http_status or ''} | {check.job_id or ''} | {check.job_status or ''} | {check.progress if check.progress is not None else ''} | {check.detail} |"
        )
    lines.extend(
        [
            "",
            "Only passed checks establish compatibility. Blocked, skipped, unavailable, and incomplete checks do not pass.",
            "Reports omit API bodies, credentials, query contents, and firm identifiers. Job IDs are retained for resumption.",
            "This run only checks the reads and query exports listed above. It does not certify data writes or unexecuted endpoints.",
            "",
        ]
    )
    markdown_text = "\n".join(lines)
    markdown_text = redact(markdown_text)
    json_path.write_text(json_text, encoding="utf-8")
    markdown_path.write_text(markdown_text, encoding="utf-8")
    return json_path, markdown_path


def _positive_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be a positive finite number")
    return number


def _positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def _job_id(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value):
        raise argparse.ArgumentTypeError(
            "must be a job identifier containing letters, digits, hyphens or underscores"
        )
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--env-file", help="Explicit credential file; no implicit .env loading"
    )
    parser.add_argument(
        "--environment", choices=("sandbox", "development", "production")
    )
    parser.add_argument("--base-url", help="Explicit HTTPS API URL, including /v1")
    parser.add_argument(
        "--production",
        action="store_true",
        help="Allow the actual production or custom API host",
    )
    parser.add_argument("--report-dir", default="test-results/live")
    parser.add_argument(
        "--read-only",
        action="store_true",
        help="Disable query-job POSTs; existing jobs may still be inspected",
    )
    parser.add_argument(
        "--extended",
        action="store_true",
        help="Include one-page checks of additional resources",
    )
    parser.add_argument(
        "--only", action="append", help="Comma-separated check names; repeatable"
    )
    parser.add_argument(
        "--list-checks",
        action="store_true",
        help="Print check names and exit without credentials or network",
    )
    parser.add_argument(
        "--entity-id", help="Entity filter for estimated_returns; excluded from reports"
    )
    for name in ("portfolio", "transaction"):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            f"--{name}-query",
            help="Raw query JSON file; submit and verify an export job",
        )
        group.add_argument(
            f"--{name}-job-id",
            type=_job_id,
            help="Verify an existing job without resubmitting",
        )
    parser.add_argument("--job-timeout", type=_positive_float, default=120.0)
    parser.add_argument("--poll-interval", type=_positive_float, default=5.0)
    parser.add_argument("--request-timeout", type=_positive_float, default=30.0)
    parser.add_argument(
        "--max-result-bytes", type=_positive_int, default=10 * 1024 * 1024
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.list_checks:
        print("\n".join(ALL_CHECKS))
        return 0
    report = DiagnosticReport("unconfigured", args.read_only)
    secrets: list[str] = []
    try:
        selected_checks(args)  # Reject unknown selectors before building a client.
        settings, secrets = configuration(args)
        base_url = settings["base_url"]
        common = {"production": args.production, "allow_exports": not args.read_only}
        with (
            GuardedSession(RequestGuard(base_url, **common)) as session,
            GuardedSession(
                RequestGuard(base_url, **common, downloads=True)
            ) as download_session,
        ):
            with AddePy(
                **settings, session=session, download_session=download_session
            ) as client:
                report = run_diagnostics(
                    client, args, environment=host_environment(client.base_url)
                )
    except DiagnosticConfigError as exc:
        report.checks.append(CheckResult("configuration", "config_error", str(exc)))
    except (OSError, UnicodeError, ValueError):
        report.checks.append(
            CheckResult(
                "configuration",
                "config_error",
                "Configuration could not initialize the diagnostic client.",
            )
        )
    try:
        json_path, markdown_path = write_reports(
            report, args.report_dir, secrets=secrets
        )
    except OSError:
        print("Reports could not be written to the selected directory.")
        return 2
    counts = ", ".join(
        f"{status}: {count}"
        for status, count in sorted(
            Counter(check.status for check in report.checks).items()
        )
    )
    print(f"{counts}. Exit code: {report.exit_code}.")
    print(f"JSON report: {json_path}\nMarkdown report: {markdown_path}")
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
