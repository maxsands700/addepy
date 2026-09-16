"""Live diagnostic policies exercised against an offline HTTP adapter."""

import json

import pytest
import requests
from requests.adapters import BaseAdapter

from addepy import diagnostics
from addepy.exceptions import (
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
)


SANDBOX = "https://example.sandbox.addepar.com/api/v1"
PRIVATE_TOKEN = "private-token-never-report-this"
PRIVATE_VALUE = "private-query-value-never-report-this"


class OfflineAdapter(BaseAdapter):
    def __init__(self, fixtures):
        self.fixtures = list(fixtures)
        self.requests = []

    def send(self, request, **kwargs):
        self.requests.append(request)
        assert self.fixtures, "No real network is permitted by these tests"
        fixture = self.fixtures.pop(0)
        if isinstance(fixture, Exception):
            raise fixture
        status, body = fixture
        result = requests.Response()
        result.status_code = status
        result.url = request.url
        result.request = request
        result._content = json.dumps(body).encode()
        result._content_consumed = True
        result.headers["Content-Type"] = "application/vnd.api+json"
        return result

    def close(self):
        pass


@pytest.fixture
def env_file(tmp_path):
    path = tmp_path / ".env.sandbox"
    path.write_text(
        f"ADDEPAR_FIRM_NAME=example\nADDEPAR_FIRM_ID=1\nADDEPAR_ENVIRONMENT=sandbox\nADDEPAR_API_KEY={PRIVATE_TOKEN}\n"
    )
    return path


def run_cli(monkeypatch, tmp_path, env_file, fixtures, *options):
    adapter = OfflineAdapter(fixtures)
    real_session = diagnostics.GuardedSession

    def offline_session(guard):
        session = real_session(guard)
        session.mount("https://", adapter)
        return session

    monkeypatch.setattr(diagnostics, "GuardedSession", offline_session)
    report_dir = tmp_path / "reports"
    code = diagnostics.main(
        [
            "--env-file",
            str(env_file),
            "--report-dir",
            str(report_dir),
            "--poll-interval",
            "0.001",
            *options,
        ]
    )
    json_path = next(report_dir.glob("*.json"))
    markdown_path = next(report_dir.glob("*.md"))
    return code, json.loads(json_path.read_text()), markdown_path.read_text(), adapter


def prepared(method, route, body=None, *, base_url=SANDBOX, headers=None):
    return requests.Request(
        method, base_url + route, json=body, headers=headers
    ).prepare()


def export_body(resource="jobs", job_type="PORTFOLIO_QUERY"):
    return {
        "data": {
            "type": resource,
            "attributes": {
                "job_type": job_type,
                "parameters": {"future_option": PRIVATE_VALUE},
            },
        }
    }


@pytest.mark.parametrize("method", ["GET", "HEAD"])
def test_guard_permits_read_requests(method):
    guard = diagnostics.RequestGuard(SANDBOX, production=False, allow_exports=False)
    guard.validate(prepared(method, "/entities"))


@pytest.mark.parametrize(
    "route,body",
    [
        ("/jobs", export_body()),
        ("/transaction_jobs", export_body("transaction_jobs", "transaction_query")),
    ],
)
def test_guard_permits_only_documented_query_export_posts(route, body):
    guard = diagnostics.RequestGuard(SANDBOX, production=False, allow_exports=True)
    guard.validate(prepared("POST", route, body))


@pytest.mark.parametrize(
    "method,route,body",
    [
        ("POST", "/imports", export_body()),
        ("POST", "/entities", export_body()),
        ("POST", "/jobs/123", export_body()),
        ("POST", "/jobs?write=true", export_body()),
        ("POST", "/jobs", export_body(job_type="portfolio_view_results")),
        ("POST", "/jobs", export_body(job_type="IMPORT")),
        ("POST", "/jobs", export_body(job_type="portfolio_query_results")),
        ("POST", "/jobs", export_body("transaction_jobs", "transaction_query")),
        ("POST", "/jobs", {"data": []}),
        ("POST", "/jobs", None),
        ("POST", "/report_schedule/1/execute", {}),
        ("DELETE", "/jobs/123", None),
        ("PATCH", "/entities/1", {}),
        ("PUT", "/entities/1", {}),
        ("OPTIONS", "/entities", None),
    ],
)
def test_actual_session_guard_blocks_writes_before_adapter_io(method, route, body):
    guard = diagnostics.RequestGuard(SANDBOX, production=False, allow_exports=True)
    adapter = OfflineAdapter([])
    with diagnostics.GuardedSession(guard) as session:
        session.mount("https://", adapter)
        with pytest.raises(diagnostics.GuardViolation):
            session.send(prepared(method, route, body))
    assert adapter.requests == []


def test_read_only_guard_rejects_export_even_when_called_directly():
    guard = diagnostics.RequestGuard(SANDBOX, production=False, allow_exports=False)
    with pytest.raises(diagnostics.GuardViolation):
        guard.validate(prepared("POST", "/jobs", export_body()))


def test_primary_guard_disallows_other_hosts_and_download_guard_disallows_credentials():
    guard = diagnostics.RequestGuard(SANDBOX, production=False, allow_exports=True)
    external = requests.Request(
        "GET", "https://storage.example.test/result.json"
    ).prepare()
    with pytest.raises(diagnostics.GuardViolation):
        guard.validate(external)
    downloads = diagnostics.RequestGuard(
        SANDBOX, production=False, allow_exports=True, downloads=True
    )
    downloads.validate(external)
    for headers in (
        {"Authorization": PRIVATE_TOKEN},
        {"Addepar-Firm": "1"},
        {"Cookie": "session=secret"},
    ):
        request = requests.Request("GET", external.url, headers=headers).prepare()
        with pytest.raises(diagnostics.GuardViolation):
            downloads.validate(request)
    with pytest.raises(diagnostics.GuardViolation):
        downloads.validate(requests.Request("POST", external.url).prepare())


@pytest.mark.parametrize(
    "url",
    [
        "https://example.addepar.com/api/v1",
        "https://api.addepar.com/v1",
        "https://custom.example.test/api/v1",
        "https://example.sandbox.addepar.com.attacker.test/api/v1",
        "https://nested.example.sandbox.addepar.com/api/v1",
        "https://example.sandbox.addepar.com:444/api/v1",
    ],
)
def test_actual_production_and_unknown_hosts_require_explicit_flag(url):
    with pytest.raises(diagnostics.DiagnosticConfigError, match="--production"):
        diagnostics.validate_base_url(url, production=False)
    assert diagnostics.validate_base_url(url, production=True) == url


@pytest.mark.parametrize(
    "url",
    [
        "http://example.sandbox.addepar.com/api/v1",
        "https://user:password@example.sandbox.addepar.com/api/v1",
        "https://example.sandbox.addepar.com/api/v1?token=secret",
        "https://example.sandbox.addepar.com/api/v1#secret",
        "https://example.sandbox.addepar.com/api",
    ],
)
def test_invalid_base_urls_remain_blocked_with_production_flag(url):
    with pytest.raises(diagnostics.DiagnosticConfigError):
        diagnostics.validate_base_url(url, production=True)


def test_sandbox_environment_label_cannot_disguise_production_host(env_file):
    with env_file.open("a") as handle:
        handle.write("ADDEPAR_BASE_URL=https://example.addepar.com/api/v1\n")
    args = diagnostics.build_parser().parse_args(["--env-file", str(env_file)])
    with pytest.raises(diagnostics.DiagnosticConfigError, match="actual API host"):
        diagnostics.configuration(args)


def test_configuration_does_not_fall_back_to_ambient_env_or_dotenv(
    env_file, monkeypatch
):
    monkeypatch.setenv("ADDEPAR_API_KEY", "ambient-secret")
    monkeypatch.setenv("ADDEPAR_BASE_URL", "https://example.addepar.com/api/v1")
    args = diagnostics.build_parser().parse_args(["--env-file", str(env_file)])
    settings, _ = diagnostics.configuration(args)
    assert settings["base_url"] == SANDBOX
    assert settings["api_key"] == PRIVATE_TOKEN
    assert "load_env" not in settings
    env_file.write_text(
        "ADDEPAR_FIRM_ID=1\nADDEPAR_ENVIRONMENT=sandbox\nADDEPAR_FIRM_NAME=example\n"
    )
    with pytest.raises(diagnostics.DiagnosticConfigError, match="authentication"):
        diagnostics.configuration(args)


def test_configuration_requires_explicit_environment_and_disables_interpolation(
    env_file, monkeypatch
):
    env_file.write_text(
        f"ADDEPAR_FIRM_ID=1\nADDEPAR_FIRM_NAME=example\nADDEPAR_API_KEY={PRIVATE_TOKEN}\n"
    )
    monkeypatch.setenv("ADDEPAR_ENVIRONMENT", "production")
    args = diagnostics.build_parser().parse_args(["--env-file", str(env_file)])
    with pytest.raises(
        diagnostics.DiagnosticConfigError, match="no environment is assumed"
    ):
        diagnostics.configuration(args)
    env_file.write_text(
        "ADDEPAR_FIRM_ID=1\nADDEPAR_FIRM_NAME=example\nADDEPAR_ENVIRONMENT=sandbox\nADDEPAR_API_KEY=${SECRET}\n"
    )
    with pytest.raises(diagnostics.DiagnosticConfigError, match="interpolation"):
        diagnostics.configuration(args)


def test_default_suite_checks_three_reads_and_reports_no_body_data(
    monkeypatch, tmp_path, env_file
):
    fixtures = [
        (200, {"data": {"id": "1", "attributes": {"email": PRIVATE_VALUE}}}),
        (200, {"data": []}),
        (200, {"data": []}),
    ]
    code, report, markdown, adapter = run_cli(monkeypatch, tmp_path, env_file, fixtures)
    assert code == 0
    assert report["summary"] == {"pass": 3}
    assert [check["name"] for check in report["checks"]] == list(
        diagnostics.DEFAULT_CHECKS
    )
    assert all(request.method == "GET" for request in adapter.requests)
    assert all(
        check["source_url"].startswith("https://developers.addepar.com/")
        for check in report["checks"]
    )
    assert PRIVATE_TOKEN not in json.dumps(report) + markdown
    assert PRIVATE_VALUE not in json.dumps(report) + markdown
    assert "does not certify data writes" in markdown


@pytest.mark.parametrize(
    "http,status,exit_code",
    [
        (401, "auth_blocked", 2),
        (403, "permission_blocked", 2),
        (404, "unavailable", 2),
        (410, "unavailable", 2),
        (429, "rate_limited", 2),
        (422, "contract_failure", 1),
        (500, "unavailable", 2),
    ],
)
def test_http_classifications_never_report_blocked_as_pass(
    monkeypatch, tmp_path, env_file, http, status, exit_code
):
    body = {"errors": [{"detail": PRIVATE_TOKEN + PRIVATE_VALUE}]}
    code, report, markdown, adapter = run_cli(
        monkeypatch, tmp_path, env_file, [(http, body)], "--only", "entities"
    )
    assert code == exit_code
    assert report["checks"][0]["status"] == status
    assert report["checks"][0]["http_status"] == http
    assert PRIVATE_TOKEN not in json.dumps(report) + markdown
    assert PRIVATE_VALUE not in json.dumps(report) + markdown
    assert len(adapter.requests) == 1


@pytest.mark.parametrize("http,status", [(401, "auth_blocked"), (429, "rate_limited")])
def test_auth_and_rate_limits_stop_further_requests(
    monkeypatch, tmp_path, env_file, http, status
):
    code, report, _, adapter = run_cli(monkeypatch, tmp_path, env_file, [(http, {})])
    assert code == 2
    assert report["summary"] == {status: 3}
    assert len(adapter.requests) == 1


def test_missing_job_input_and_read_only_skip_are_inconclusive(
    monkeypatch, tmp_path, env_file
):
    code, report, _, adapter = run_cli(
        monkeypatch, tmp_path, env_file, [], "--only", "portfolio_job"
    )
    assert code == 2
    assert report["checks"][0]["status"] == "missing_input"
    assert adapter.requests == []


def test_read_only_skips_selected_query_before_opening_file(
    monkeypatch, tmp_path, env_file
):
    code, report, _, adapter = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        [],
        "--only",
        "portfolio_job",
        "--read-only",
        "--portfolio-query",
        "missing.json",
    )
    assert code == 2
    assert report["checks"][0]["status"] == "skipped"
    assert adapter.requests == []


def test_export_query_default_permission_and_sanitized_job_report(
    monkeypatch, tmp_path, env_file
):
    query = tmp_path / "query.json"
    query.write_text(json.dumps({"data": {"attributes": {"private": PRIVATE_VALUE}}}))
    fixtures = [
        (202, {"data": {"id": "job-123"}}),
        (
            200,
            {
                "data": {
                    "id": "job-123",
                    "attributes": {
                        "status": "Completed",
                        "percent_complete": 1.0,
                        "private": PRIVATE_VALUE,
                    },
                }
            },
        ),
        (
            200,
            {
                "data": {
                    "type": "portfolio_views",
                    "attributes": {
                        "total": {
                            "columns": {"value": 42, "private_result": PRIVATE_VALUE},
                            "children": [],
                        }
                    },
                }
            },
        ),
    ]
    code, report, markdown, adapter = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        fixtures,
        "--only",
        "portfolio_job",
        "--portfolio-query",
        str(query),
    )
    assert code == 0
    check = report["checks"][0]
    assert (check["job_id"], check["job_status"], check["progress"]) == (
        "job-123",
        "Completed",
        1.0,
    )
    assert [request.method for request in adapter.requests] == ["POST", "GET", "GET"]
    assert json.loads(adapter.requests[0].body)["data"]["attributes"]["parameters"] == {
        "private": PRIVATE_VALUE
    }
    assert PRIVATE_VALUE not in json.dumps(report) + markdown
    assert PRIVATE_TOKEN not in json.dumps(report) + markdown


def test_existing_transaction_job_can_resume_in_read_only_mode(
    monkeypatch, tmp_path, env_file
):
    fixtures = [
        (
            200,
            {"data": {"attributes": {"status": "Completed", "percent_complete": 1.0}}},
        ),
        (200, {"data": []}),
    ]
    code, report, _, adapter = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        fixtures,
        "--only",
        "transaction_job",
        "--transaction-job-id",
        "job-123",
        "--read-only",
    )
    assert code == 0
    assert report["checks"][0]["job_id"] == "job-123"
    assert all(request.method == "GET" for request in adapter.requests)


def test_failed_job_retains_id_but_no_private_error_details(
    monkeypatch, tmp_path, env_file
):
    fixture = (
        200,
        {
            "data": {
                "attributes": {
                    "status": "Error",
                    "errors": [{"detail": PRIVATE_TOKEN + PRIVATE_VALUE}],
                }
            }
        },
    )
    code, report, markdown, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        [fixture],
        "--only",
        "portfolio_job",
        "--portfolio-job-id",
        "job-123",
    )
    assert code == 1
    assert report["checks"][0]["job_id"] == "job-123"
    assert report["checks"][0]["job_status"] == "Error"
    assert PRIVATE_TOKEN not in json.dumps(report) + markdown
    assert PRIVATE_VALUE not in json.dumps(report) + markdown


def test_oversized_download_is_incomplete_not_success(monkeypatch, tmp_path, env_file):
    fixtures = [
        (200, {"data": {"attributes": {"status": "Completed"}}}),
        (200, {"private": PRIVATE_VALUE}),
    ]
    code, report, _, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        fixtures,
        "--only",
        "portfolio_job",
        "--portfolio-job-id",
        "job-123",
        "--max-result-bytes",
        "2",
    )
    assert code == 2
    assert report["checks"][0]["status"] == "incomplete"
    assert report["checks"][0]["job_status"] == "Completed"


def test_invalid_response_shape_is_contract_failure(monkeypatch, tmp_path, env_file):
    code, report, _, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        [(200, {"data": PRIVATE_VALUE})],
        "--only",
        "entities",
    )
    assert code == 1
    assert report["checks"][0]["status"] == "contract_failure"


def test_network_error_reports_no_exception_message(monkeypatch, tmp_path, env_file):
    code, report, markdown, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        [requests.ConnectionError(PRIVATE_TOKEN)],
        "--only",
        "entities",
    )
    assert code == 2
    assert report["checks"][0]["status"] == "network_error"
    assert PRIVATE_TOKEN not in json.dumps(report) + markdown


def test_unknown_selector_and_production_config_never_send(
    monkeypatch, tmp_path, env_file
):
    code, report, _, adapter = run_cli(
        monkeypatch, tmp_path, env_file, [], "--only", PRIVATE_VALUE
    )
    assert code == 2
    assert report["checks"][0]["status"] == "config_error"
    assert PRIVATE_VALUE not in json.dumps(report)
    assert adapter.requests == []


def test_short_secret_redaction_preserves_valid_json_types(tmp_path):
    report = diagnostics.DiagnosticReport("sandbox", False)
    report.checks.append(
        diagnostics.CheckResult("entities", "pass", "safe", job_id="a")
    )
    json_path, _ = diagnostics.write_reports(report, tmp_path, secrets=["a"])
    document = json.loads(json_path.read_text())
    assert document["read_only"] is False
    assert document["checks"][0]["job_id"] == "[REDACTED]"


def test_check_listing_requires_no_credentials_or_network(capsys):
    assert diagnostics.main(["--list-checks"]) == 0
    assert "portfolio_job" in capsys.readouterr().out


def test_extended_suite_uses_wrappers_and_skips_required_entity_input(
    monkeypatch, tmp_path, env_file
):
    fixtures = [
        (200, {"data": {"id": "1"} if check.shape is dict else []})
        for check in diagnostics.READ_CHECKS.values()
        if not check.requires_entity
    ]
    code, report, _, adapter = run_cli(
        monkeypatch, tmp_path, env_file, fixtures, "--extended"
    )
    assert code == 2
    assert report["summary"] == {
        "pass": len(diagnostics.READ_CHECKS) - 1,
        "missing_input": 1,
    }
    assert len(adapter.requests) == len(diagnostics.READ_CHECKS) - 1
    assert not any("estimated_returns" in request.url for request in adapter.requests)
    payouts = [
        request for request in adapter.requests if "/billing/payout/" in request.url
    ]
    assert len(payouts) == 2
    assert all(
        "offset=0" in request.url and "limit=1" in request.url for request in payouts
    )


def test_estimated_returns_uses_required_entity_filter_without_reporting_it(
    monkeypatch, tmp_path, env_file
):
    code, report, markdown, adapter = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        [(200, {"data": []})],
        "--only",
        "estimated_returns",
        "--entity-id",
        PRIVATE_VALUE,
    )
    assert code == 0
    assert "filter%5Bentity_id%5D=" + PRIVATE_VALUE in adapter.requests[0].url
    assert PRIVATE_VALUE not in json.dumps(report) + markdown


def test_public_wrapper_behavior_is_part_of_check(monkeypatch, tmp_path, env_file):
    from addepy.resources.ownership.entities import EntitiesResource

    original = EntitiesResource.list_entities

    def broken_wrapper(self, **kwargs):
        original(self, **kwargs)
        return {"wrong": "shape"}

    monkeypatch.setattr(EntitiesResource, "list_entities", broken_wrapper)
    code, report, _, _ = run_cli(
        monkeypatch, tmp_path, env_file, [(200, {"data": []})], "--only", "entities"
    )
    assert code == 1
    assert report["checks"][0]["status"] == "contract_failure"


def test_wrapper_cannot_hide_missing_json_api_data_by_returning_empty_list(
    monkeypatch, tmp_path, env_file
):
    code, report, _, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        [(200, {"errors": []})],
        "--only",
        "portfolio_views",
    )
    assert code == 1
    assert report["checks"][0]["status"] == "contract_failure"


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"data": {}},
        {"data": {"anything": "x"}},
        {"data": {"attributes": {}}},
        {"data": {"attributes": {"total": {}}}},
        {"data": {"attributes": {"total": {"columns": [], "children": {}}}}},
        {"data": {"type": "jobs", "attributes": {"status": "Queued"}}},
        {"data": {"type": "portfolio_query", "attributes": {"status": "Completed"}}},
        {"data": {"attributes": {"status": "Queued", "job_type": "PORTFOLIO_QUERY"}}},
    ],
)
def test_portfolio_download_must_be_query_data_not_status_or_empty_document(
    monkeypatch, tmp_path, env_file, body
):
    fixtures = [(200, {"data": {"attributes": {"status": "Completed"}}}), (200, body)]
    code, report, _, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        fixtures,
        "--only",
        "portfolio_job",
        "--portfolio-job-id",
        "job-123",
    )
    assert code == 1
    assert report["checks"][0]["status"] == "contract_failure"


def test_transaction_download_rejects_job_status_even_in_data_array(
    monkeypatch, tmp_path, env_file
):
    fixtures = [
        (200, {"data": {"attributes": {"status": "Completed"}}}),
        (
            200,
            {
                "data": [
                    {"type": "transaction_jobs", "attributes": {"status": "Queued"}}
                ]
            },
        ),
    ]
    code, report, _, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        fixtures,
        "--only",
        "transaction_job",
        "--transaction-job-id",
        "job-123",
    )
    assert code == 1
    assert report["checks"][0]["status"] == "contract_failure"


@pytest.mark.parametrize("row", [{}, {"attributes": None}, {"attributes": []}])
def test_transaction_download_requires_attributes_object_on_every_row(
    monkeypatch, tmp_path, env_file, row
):
    fixtures = [
        (200, {"data": {"attributes": {"status": "Completed"}}}),
        (200, {"data": [{"attributes": {"value": 42}}, row]}),
    ]
    code, report, _, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        fixtures,
        "--only",
        "transaction_job",
        "--transaction-job-id",
        "job-123",
    )
    assert code == 1
    assert report["checks"][0]["status"] == "contract_failure"


@pytest.mark.parametrize(
    "name,body",
    [
        (
            "portfolio",
            {
                "data": {
                    "type": "portfolio_views",
                    "attributes": {
                        "total": {"columns": {"custom_field": PRIVATE_VALUE}}
                    },
                    "unknown": True,
                }
            },
        ),
        (
            "portfolio",
            {
                "data": {
                    "attributes": {"total": {"children": []}, "unknown": PRIVATE_VALUE}
                }
            },
        ),
        (
            "transaction",
            {
                "data": [
                    {
                        "type": "transaction_query",
                        "attributes": {"value": 42, "unknown": PRIVATE_VALUE},
                        "future_field": True,
                    }
                ]
            },
        ),
    ],
)
def test_documented_query_result_layouts_allow_unknown_fields_without_reporting_values(
    monkeypatch, tmp_path, env_file, name, body
):
    fixtures = [(200, {"data": {"attributes": {"status": "Completed"}}}), (200, body)]
    code, report, markdown, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        fixtures,
        "--only",
        name + "_job",
        "--" + name + "-job-id",
        "job-123",
    )
    assert code == 0
    assert report["checks"][0]["status"] == "pass"
    assert PRIVATE_VALUE not in json.dumps(report) + markdown


@pytest.mark.parametrize(
    "name,body",
    [
        ("portfolio", {"data": {"attributes": {"total": {"columns": {"value": 42}}}}}),
        ("transaction", {"data": []}),
    ],
)
def test_query_download_requires_http_success_even_with_valid_json(
    monkeypatch, tmp_path, env_file, name, body
):
    fixtures = [(200, {"data": {"attributes": {"status": "Completed"}}}), (300, body)]
    code, report, _, _ = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        fixtures,
        "--only",
        name + "_job",
        "--" + name + "-job-id",
        "job-123",
    )
    assert code == 1
    assert report["checks"][0]["status"] == "contract_failure"
    assert report["checks"][0]["http_status"] == 300


def test_interrupted_wait_still_writes_report_with_submitted_job_id(
    monkeypatch, tmp_path, env_file
):
    from addepy.resources.job import JobResource

    def interrupted_wait(self, job_id, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(JobResource, "wait_for_job", interrupted_wait)
    query = tmp_path / "query.json"
    query.write_text('{"portfolio_id": "22"}')
    code, report, _, adapter = run_cli(
        monkeypatch,
        tmp_path,
        env_file,
        [(202, {"data": {"id": "job-123"}})],
        "--only",
        "portfolio_job",
        "--portfolio-query",
        str(query),
    )
    assert code == 2
    assert report["checks"][0]["status"] == "incomplete"
    assert report["checks"][0]["job_id"] == "job-123"
    assert len(adapter.requests) == 1


@pytest.mark.parametrize(
    "error,status",
    [
        (AuthenticationError(PRIVATE_TOKEN), "auth_blocked"),
        (ForbiddenError(PRIVATE_TOKEN), "permission_blocked"),
        (RateLimitError(PRIVATE_TOKEN), "rate_limited"),
        (NotFoundError(PRIVATE_TOKEN), "unavailable"),
        (GoneError(PRIVATE_TOKEN), "unavailable"),
        (TransportError(PRIVATE_TOKEN), "network_error"),
        (ProtocolError(PRIVATE_TOKEN), "contract_failure"),
        (JobError(PRIVATE_TOKEN, "job-123"), "contract_failure"),
        (AddePyTimeoutError(PRIVATE_TOKEN, "job-123"), "incomplete"),
        (AddePyError(PRIVATE_TOKEN), "contract_failure"),
    ],
)
def test_classification_uses_static_text(error, status):
    outcome, detail = diagnostics.classify_exception(error)
    assert outcome == status
    assert PRIVATE_TOKEN not in detail
