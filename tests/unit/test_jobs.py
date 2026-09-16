"""Offline regressions for raw queries and resumable export workflows."""

from copy import deepcopy
import json
from pathlib import Path

import pytest
import requests

from addepy.exceptions import AddePyError, JobError, ValidationError
from addepy.resources.portfolio.jobs import JobsResource
from addepy.resources.portfolio.transaction_jobs import TransactionJobsResource


def response(body, status=200):
    result = requests.Response()
    result.status_code = status
    result._content = json.dumps(body).encode()
    result.headers["Content-Type"] = "application/vnd.api+json"
    return result


def job_document(status, *, errors=None):
    attributes = {"status": status}
    if errors is not None:
        attributes["errors"] = errors
    return {"data": {"id": "job-123", "attributes": attributes}}


def portfolio_result_document(total):
    """Synthetic example of the completed response confirmed against live jobs."""
    return {
        "meta": {"columns": [{"key": "value"}]},
        "data": {
            "type": "portfolio_query_results",
            "attributes": {"total": total},
        },
        "included": [],
    }


class FakeClient:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []
        self.downloads = []

    def _request(self, method, endpoint, **kwargs):
        self.calls.append((method, endpoint, kwargs))
        assert self.responses, "Unexpected request after the fixture was exhausted"
        return self.responses.pop(0)

    def download(self, endpoint, path):
        self.downloads.append((endpoint, path))
        return Path(path)


@pytest.fixture(params=[JobsResource, TransactionJobsResource])
def resource_class(request):
    return request.param


@pytest.mark.parametrize("envelope", [False, True])
@pytest.mark.parametrize("as_json", [False, True])
def test_raw_queries_preserve_unknown_fields_values_and_caller_input(
    resource_class, envelope, as_json
):
    parameters = {
        "portfolio_type": "ENTITY",
        "portfolio_id": [22, "003"],
        "columns": [{"key": "custom_attribute", "arguments": {"period": "inception"}}],
        "filters": [],
        "future_query_option": {"keep": [False, None, 0]},
    }
    query = (
        {"data": {"type": "portfolio_query", "attributes": parameters}}
        if envelope
        else parameters
    )
    original = deepcopy(query)
    supplied = json.dumps(query) if as_json else query
    client = FakeClient(response({"data": {"id": "job-123"}}, 202))

    assert resource_class(client).create_job(supplied) == "job-123"
    submitted = client.calls[0][2]["json"]["data"]["attributes"]["parameters"]
    assert submitted == parameters
    submitted["future_query_option"]["keep"].append("changed by transport")
    submitted["columns"][0]["arguments"]["period"] = "changed by transport"
    assert query == original


@pytest.mark.parametrize(
    "invalid",
    [
        None,
        [],
        7,
        "null",
        "[]",
        "{",
        {"data": []},
        {"data": {}},
        {"data": {"attributes": []}},
    ],
)
def test_bad_query_shapes_fail_before_network_io(resource_class, invalid):
    client = FakeClient()
    with pytest.raises(ValidationError):
        resource_class(client).create_job(invalid)
    assert client.calls == []


@pytest.mark.parametrize(
    "body", [{}, {"data": []}, {"data": {"id": None}}, {"data": {"id": True}}]
)
def test_creation_requires_usable_job_id(resource_class, body):
    client = FakeClient(response(body, 202))
    with pytest.raises(AddePyError, match="job ID"):
        resource_class(client).create_job({"portfolio_id": "22"})


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"data": None},
        {"data": {"attributes": {}}},
        job_document(None),
        job_document(""),
    ],
)
def test_missing_status_never_succeeds_or_downloads(resource_class, body):
    client = FakeClient(response(body))
    with pytest.raises(JobError) as caught:
        resource_class(client).resume_job("job-123", initial_wait=0.001)
    assert caught.value.job_id == "job-123"
    assert caught.value.job_data == body
    assert len(client.calls) == 1
    assert client.calls[0][0] == "GET"


@pytest.mark.parametrize(
    "status",
    [
        "Error",
        "Failed",
        "Rejected",
        "Timed Out",
        "Error Cancelled",
        "Canceled",
        "User Cancelled",
        "user_canceled",
    ],
)
def test_failed_jobs_retain_details_and_do_not_download(resource_class, status):
    errors = [
        {
            "status": "400",
            "title": "Bad Request",
            "detail": "Unsupported batch attribute",
        }
    ]
    document = job_document(status, errors=errors)
    client = FakeClient(response(document))
    with pytest.raises(JobError) as caught:
        resource_class(client).resume_job("job-123", initial_wait=0.001)
    assert caught.value.job_id == "job-123"
    assert caught.value.status == status
    assert caught.value.errors == errors
    assert caught.value.job_data == document
    assert len(client.calls) == 1


def test_resume_polls_unknown_states_then_fetches_results_without_new_job(
    resource_class,
):
    results = response({"rows": [{"value": 42}]})
    client = FakeClient(
        response(job_document("Future Processing State")),
        response(job_document("Completed")),
        results,
    )
    resource = resource_class(client)
    assert resource.resume_job("job-123", initial_wait=0.001, max_wait=0.001) is results
    assert [call[0] for call in client.calls] == ["GET", "GET", "GET"]
    assert client.calls[-1][1].endswith("/job-123/download")


def test_wait_returns_full_success_document_without_downloading(resource_class):
    document = job_document("Completed")
    document["meta"] = {"future": "metadata"}
    client = FakeClient(response(document))
    assert (
        resource_class(client).wait_for_job("job-123", initial_wait=0.001) == document
    )
    assert len(client.calls) == 1


@pytest.mark.parametrize(
    "total",
    [
        {"columns": {}},
        {"children": []},
        {"columns": {}, "children": None},
        {"columns": None, "children": []},
        {"columns": {"value": 42}, "children": [{"columns": {"value": 42}}]},
    ],
)
def test_portfolio_wait_accepts_completed_results_and_preserves_document(total):
    document = portfolio_result_document(total)
    original = deepcopy(document)
    result_response = response(document)
    result_response.json = lambda: document
    client = FakeClient(response(job_document("Queued")), result_response)

    completed = JobsResource(client).wait_for_job(
        "job-123", initial_wait=0.001, max_wait=0.001
    )

    assert completed is document
    assert completed == original
    assert "status" not in completed["data"]["attributes"]
    assert [call[:2] for call in client.calls] == [
        ("GET", "/jobs/job-123"),
        ("GET", "/jobs/job-123"),
    ]


@pytest.mark.parametrize("execute", [False, True], ids=["resume", "execute"])
def test_portfolio_completed_results_still_download_and_preserve_query(execute):
    document = portfolio_result_document({"columns": {"value": 42}, "children": []})
    query = {"portfolio_id": "22", "future_option": {"values": [None, False, 0]}}
    original_query = deepcopy(query)
    download_response = response(document)
    responses = [
        response(job_document("Queued")),
        response(document),
        download_response,
    ]
    if execute:
        responses.insert(0, response({"data": {"id": "job-123"}}, 202))
    client = FakeClient(*responses)
    resource = JobsResource(client)

    if execute:
        result = resource.execute_job(query, initial_wait=0.001, max_wait=0.001)
    else:
        result = resource.resume_job("job-123", initial_wait=0.001, max_wait=0.001)

    assert result is download_response
    assert query == original_query
    expected_calls = [
        ("GET", "/jobs/job-123"),
        ("GET", "/jobs/job-123"),
        ("GET", "/jobs/job-123/download"),
    ]
    if execute:
        expected_calls.insert(0, ("POST", "/jobs"))
        assert client.calls[0][2]["json"]["data"]["attributes"]["parameters"] == query
    assert [call[:2] for call in client.calls] == expected_calls


@pytest.mark.parametrize(
    "total",
    [
        None,
        [],
        {},
        {"value": 42},
        {"columns": []},
        {"children": {}},
    ],
)
def test_portfolio_malformed_results_do_not_imply_completion(total):
    document = portfolio_result_document(total)
    client = FakeClient(response(document))

    with pytest.raises(JobError) as caught:
        JobsResource(client).resume_job("job-123", initial_wait=0.001)

    assert caught.value.job_id == "job-123"
    assert caught.value.job_data == document
    assert [call[:2] for call in client.calls] == [("GET", "/jobs/job-123")]


@pytest.mark.parametrize(
    "contradiction",
    [
        "top_level_errors",
        "data_errors",
        "attribute_errors",
        "job",
        "jobs",
        "transaction_jobs",
        "job_type",
    ],
)
def test_portfolio_result_shape_does_not_override_errors_or_job_metadata(contradiction):
    document = portfolio_result_document({"columns": {}, "children": []})
    errors = [{"detail": "The export failed"}]
    if contradiction == "top_level_errors":
        document["errors"] = errors
    elif contradiction == "data_errors":
        document["data"]["errors"] = errors
    elif contradiction == "attribute_errors":
        document["data"]["attributes"]["errors"] = errors
    elif contradiction == "job_type":
        document["data"]["attributes"]["job_type"] = "PORTFOLIO_QUERY"
    else:
        document["data"]["type"] = contradiction
    client = FakeClient(response(document))

    with pytest.raises(JobError) as caught:
        JobsResource(client).resume_job("job-123", initial_wait=0.001)

    assert caught.value.job_id == "job-123"
    assert caught.value.job_data == document
    assert [call[:2] for call in client.calls] == [("GET", "/jobs/job-123")]


def test_portfolio_explicit_failure_takes_precedence_over_result_shape():
    document = portfolio_result_document({"columns": {}, "children": []})
    document["data"]["attributes"].update(
        {"status": "Failed", "errors": [{"detail": "The export failed"}]}
    )
    client = FakeClient(response(document))

    with pytest.raises(JobError) as caught:
        JobsResource(client).resume_job("job-123", initial_wait=0.001)

    assert caught.value.status == "Failed"
    assert caught.value.errors == document["data"]["attributes"]["errors"]
    assert caught.value.job_data == document
    assert len(client.calls) == 1


def test_portfolio_explicit_pending_status_keeps_polling_despite_result_shape():
    document = portfolio_result_document({"columns": {}, "children": []})
    document["data"]["attributes"]["status"] = "Queued"
    completed = job_document("Completed")
    client = FakeClient(response(document), response(completed))

    assert (
        JobsResource(client).wait_for_job("job-123", initial_wait=0.001, max_wait=0.001)
        == completed
    )
    assert len(client.calls) == 2


@pytest.mark.parametrize("status", [None, "", 0, []])
def test_portfolio_explicit_invalid_status_is_not_replaced_by_result_shape(status):
    document = portfolio_result_document({"columns": {}, "children": []})
    document["data"]["attributes"]["status"] = status
    client = FakeClient(response(document))

    with pytest.raises(JobError):
        JobsResource(client).resume_job("job-123", initial_wait=0.001)

    assert len(client.calls) == 1


def test_transaction_jobs_do_not_accept_portfolio_result_as_completion():
    document = portfolio_result_document({"columns": {"value": 42}, "children": []})
    client = FakeClient(response(document))

    with pytest.raises(JobError) as caught:
        TransactionJobsResource(client).resume_job("job-123", initial_wait=0.001)

    assert caught.value.job_id == "job-123"
    assert caught.value.job_data == document
    assert [call[:2] for call in client.calls] == [("GET", "/transaction_jobs/job-123")]


def test_invalid_status_json_retains_id_and_response(resource_class):
    invalid_response = response(None)
    invalid_response._content = b"<html>proxy error</html>"
    client = FakeClient(invalid_response)
    with pytest.raises(JobError) as caught:
        resource_class(client).get_job_status("job-123")
    assert caught.value.job_id == "job-123"
    assert caught.value.response is invalid_response


def test_non_object_status_retains_raw_job_data(resource_class):
    client = FakeClient(response(["unexpected"]))
    with pytest.raises(JobError) as caught:
        resource_class(client).get_job_status("job-123")
    assert caught.value.job_data == ["unexpected"]
    assert caught.value.job_id == "job-123"


def test_download_supports_file_streaming_and_raw_response(resource_class, tmp_path):
    result = response(None)
    result._content = b"binary-xlsx-data"
    client = FakeClient(result)
    resource = resource_class(client)
    target = tmp_path / "export.xlsx"

    assert resource.download_job_results("job-123", target) == target
    assert client.downloads == [(f"{resource._endpoint}/job-123/download", target)]
    assert resource.get_job_results("job-123", stream=True) is result
    assert client.calls[0][2]["stream"] is True


def test_cancel_does_not_expect_json_body(resource_class):
    result = requests.Response()
    result.status_code = 204
    client = FakeClient(result)
    resource = resource_class(client)
    assert resource.cancel_job("job-123") is None
    assert client.calls[0][:2] == ("DELETE", f"{resource._endpoint}/job-123")


@pytest.mark.parametrize(
    "method", ["execute_job", "execute_portfolio_query_job", "execute_portfolio_query"]
)
def test_portfolio_raw_execution_aliases(method):
    results = response({"value": 42})
    client = FakeClient(
        response({"data": {"id": "job-123"}}, 202),
        response(job_document("Completed")),
        results,
    )
    assert (
        getattr(JobsResource(client), method)(
            '{"portfolio_id": "22"}', initial_wait=0.001
        )
        is results
    )
    assert [call[0] for call in client.calls] == ["POST", "GET", "GET"]


def test_transaction_raw_execution_matches_portfolio_workflow():
    results = response({"data": [{"value": 42}]})
    client = FakeClient(
        response({"data": {"id": "job-123"}}, 202),
        response(job_document("Completed")),
        results,
    )
    resource = TransactionJobsResource(client)
    assert (
        resource.execute_job(
            '{"data": {"attributes": {"future_option": true}}}', initial_wait=0.001
        )
        is results
    )
    assert client.calls[0][1] == "/transaction_jobs"
    assert client.calls[0][2]["json"]["data"]["attributes"]["parameters"] == {
        "future_option": True
    }


def test_batch_is_opt_in_and_only_applies_to_submission():
    client = FakeClient(
        response({"data": {"id": "job-123"}}, 202),
        response(job_document("Completed")),
        response({"value": 42}),
        response({"data": {"id": "normal-job"}}, 202),
    )
    resource = JobsResource(client)
    resource.execute_job({"disable_total_row": True}, batch=True, initial_wait=0.001)
    resource.create_job({"portfolio_id": "22"})

    assert client.calls[0][2]["headers"] == {"Addepar-Compute-Type": "BATCH"}
    assert all(not call[2].get("headers") for call in client.calls[1:])
    assert (
        client.calls[0][2]["json"]["data"]["attributes"]["job_type"]
        == "PORTFOLIO_QUERY"
    )


def test_batch_query_type_can_follow_beta_guide_explicitly():
    client = FakeClient(response({"data": {"id": "job-123"}}, 202))
    JobsResource(client).create_job(
        {"portfolio_id": "22"}, batch=True, job_type="portfolio_query_results"
    )
    assert (
        client.calls[0][2]["json"]["data"]["attributes"]["job_type"]
        == "portfolio_query_results"
    )


def test_transaction_builder_retains_explicit_empty_options_and_zero_limit():
    client = FakeClient(response({"data": {"id": "job-123"}}, 202))
    TransactionJobsResource(client).create_query_job(
        ["value"],
        "ENTITY",
        "22",
        "2025-01-01",
        "2025-12-31",
        filters=[],
        sorting=[],
        limit=0,
    )
    parameters = client.calls[0][2]["json"]["data"]["attributes"]["parameters"]
    assert parameters["portfolio_id"] == ["22"]
    assert parameters["filters"] == []
    assert parameters["sorting"] == []
    assert parameters["limit"] == 0
