"""Addepar guide examples exercised through the real client, without network.

Sources reviewed 2026-09-16:
https://developers.addepar.com/docs/jobs
https://developers.addepar.com/docs/transaction-jobs
https://developers.addepar.com/docs/batched-jobs

These validate documented request/response shapes, not a live API guarantee.
"""

from copy import deepcopy
import json

import pytest
import requests

from addepy import AddePy
from addepy.exceptions import GoneError


class FixtureSession(requests.Session):
    def __init__(self, fixtures):
        super().__init__()
        self.fixtures = list(fixtures)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, deepcopy(kwargs)))
        assert self.fixtures, "Contract test attempted an unexpected request"
        status, body = self.fixtures.pop(0)
        result = requests.Response()
        result.status_code = status
        result.url = url
        result._content = json.dumps(body).encode()
        result.headers["Content-Type"] = "application/vnd.api+json"
        return result


def client_for(fixtures):
    session = FixtureSession(fixtures)
    client = AddePy(
        firm_name="example",
        firm_id="1",
        api_key="credentials",
        session=session,
    )
    return client, session


def test_portfolio_query_uses_documented_job_envelope_and_preserves_exported_query():
    query = {
        "data": {
            "type": "portfolio_query",
            "attributes": {
                "columns": [
                    {"key": "value"},
                    {
                        "key": "time_weighted_return",
                        "arguments": {"period": "2025-01-01 to 2025-12-31"},
                    },
                ],
                "groupings": [{"key": "asset_class"}],
                "filters": [
                    {
                        "attribute": "asset_class",
                        "type": "discrete",
                        "operator": "include",
                        "values": ["Equity"],
                    }
                ],
                "portfolio_type": "entity",
                "portfolio_id": [22],
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "disable_total_row": True,
            },
        }
    }
    client, session = client_for(
        [
            (
                202,
                {
                    "data": {
                        "type": "jobs",
                        "id": "b6c1b9da-4387-11ef-8636-dd826f8aeed1a",
                        "attributes": {"status": "Queued"},
                    }
                },
            )
        ]
    )
    with client:
        assert (
            client.portfolio.jobs.create_job(json.dumps(query))
            == "b6c1b9da-4387-11ef-8636-dd826f8aeed1a"
        )

    method, url, kwargs = session.calls[0]
    assert method == "POST"
    assert url == "https://example.addepar.com/api/v1/jobs"
    assert kwargs["json"] == {
        "data": {
            "type": "jobs",
            "attributes": {
                "job_type": "PORTFOLIO_QUERY",
                "parameters": query["data"]["attributes"],
            },
        }
    }


def test_transaction_query_matches_documented_request_and_download_lifecycle():
    parameters = {
        "columns": ["trade_date", "direct_owner", "security", "type", "value"],
        "filters": [],
        "sorting": [],
        "portfolio_type": "entity",
        "portfolio_id": [12345],
        "start_date": "2025-08-03",
        "end_date": "2025-09-03",
        "include_online_valuations": False,
        "include_unverified": False,
        "include_deleted": False,
    }
    results = {
        "data": [{"type": "transaction", "id": "654", "attributes": {"value": 123.45}}]
    }
    client, session = client_for(
        [
            (
                202,
                {
                    "data": {
                        "type": "transaction_jobs",
                        "id": "transaction-123",
                        "attributes": {"status": "Queued"},
                    }
                },
            ),
            (
                200,
                {
                    "data": {
                        "type": "transaction_jobs",
                        "id": "transaction-123",
                        "attributes": {
                            "status": "In Progress",
                            "percent_complete": 0.21,
                        },
                    }
                },
            ),
            (
                200,
                {
                    "data": {
                        "type": "transaction_jobs",
                        "id": "transaction-123",
                        "attributes": {"status": "Completed", "percent_complete": 1.0},
                    }
                },
            ),
            (200, results),
        ]
    )
    with client:
        result = client.portfolio.transaction_jobs.execute_job(
            parameters, initial_wait=0.001, max_wait=0.001
        )
        assert result.json() == results

    assert session.calls[0][2]["json"] == {
        "data": {
            "type": "transaction_jobs",
            "attributes": {"job_type": "transaction_query", "parameters": parameters},
        }
    }
    assert [
        (method, url.rsplit("/api/v1", 1)[1]) for method, url, _ in session.calls
    ] == [
        ("POST", "/transaction_jobs"),
        ("GET", "/transaction_jobs/transaction-123"),
        ("GET", "/transaction_jobs/transaction-123"),
        ("GET", "/transaction_jobs/transaction-123/download"),
    ]


def test_batch_saved_view_keeps_standard_endpoint_and_documented_header():
    client, session = client_for(
        [
            (
                202,
                {
                    "data": {
                        "id": "7",
                        "type": "jobs",
                        "attributes": {"status": "Queued"},
                    }
                },
            )
        ]
    )
    with client:
        assert (
            client.portfolio.jobs.create_view_job(
                "74894", "ENTITY", "22", "2011-12-31", "2013-01-15", batch=True
            )
            == "7"
        )
    method, url, kwargs = session.calls[0]
    assert method == "POST"
    assert url.endswith("/api/v1/jobs")
    assert kwargs["headers"]["Addepar-Compute-Type"] == "BATCH"
    assert kwargs["json"] == {
        "data": {
            "type": "jobs",
            "attributes": {
                "job_type": "portfolio_view_results",
                "parameters": {
                    "view_id": "74894",
                    "portfolio_type": "entity",
                    "portfolio_id": "22",
                    "output_type": "json",
                    "start_date": "2011-12-31",
                    "end_date": "2013-01-15",
                },
            },
        }
    }


@pytest.mark.parametrize("resource_name", ["jobs", "transaction_jobs"])
def test_expired_results_surface_documented_gone_error(resource_name):
    client, session = client_for(
        [
            (
                410,
                {
                    "errors": [
                        {"status": "410", "title": "Gone", "detail": "Results expired"}
                    ]
                },
            )
        ]
    )
    with client, pytest.raises(GoneError) as caught:
        getattr(client.portfolio, resource_name).get_job_results("expired-id")
    assert caught.value.status_code == 410
    assert len(session.calls) == 1
