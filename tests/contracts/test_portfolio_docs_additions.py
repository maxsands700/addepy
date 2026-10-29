"""Offline contracts for routes added from the October 2026 docs snapshot."""

from copy import deepcopy
import json

import pytest
import requests

from addepy.resources.portfolio.jobs import JobsResource
from addepy.resources.portfolio.transaction_jobs import TransactionJobsResource
from addepy.resources.portfolio.transactions import TransactionsResource


class FakeClient:
    def __init__(self, document=None):
        self.document = document
        self.calls = []

    def _request(self, method, endpoint, **kwargs):
        self.calls.append((method, endpoint, deepcopy(kwargs)))
        response = requests.Response()
        response.status_code = 204 if self.document is None else 200
        response._content = (
            b"" if self.document is None else json.dumps(self.document).encode()
        )
        return response


@pytest.mark.parametrize(
    "method,suffix,resource_type",
    [
        ("get_transaction_new_owner", "new_owner", "entities"),
        ("get_transaction_new_owned", "new_owned", "entities"),
        ("get_transaction_owner_relationship", "relationships/owner", "entities"),
        ("get_transaction_owned_relationship", "relationships/owned", "entities"),
        (
            "get_transaction_new_owner_relationship",
            "relationships/new_owner",
            "entities",
        ),
        (
            "get_transaction_new_owned_relationship",
            "relationships/new_owned",
            "entities",
        ),
        (
            "get_transaction_cash_account_relationship",
            "relationships/cash_account",
            "positions",
        ),
    ],
)
def test_transaction_related_resources_and_linkage(method, suffix, resource_type):
    data = {"id": "117", "type": resource_type, "future_field": {"enabled": False}}
    client = FakeClient({"data": data})
    assert getattr(TransactionsResource(client), method)("1967") == data
    assert client.calls == [("GET", f"/transactions/1967/{suffix}", {"params": None})]


@pytest.mark.parametrize(
    "resource,endpoint", [(JobsResource, "jobs"), (TransactionJobsResource, "transaction_jobs")]
)
@pytest.mark.parametrize(
    "method,suffix",
    [
        ("get_job_creator", "creator"),
        ("get_job_creator_relationship", "relationships/creator"),
    ],
)
def test_job_creator_routes_use_the_correct_job_namespace(resource, endpoint, method, suffix):
    creator = {"id": 22, "type": "users", "attributes": {"email": "user@example.com"}}
    client = FakeClient({"data": creator})
    job_id = "39cee0a7-7f5d-11ef-a01d-45a1a34a1c7c"
    assert getattr(resource(client), method)(job_id) == creator
    assert client.calls == [("GET", f"/{endpoint}/{job_id}/{suffix}", {"params": None})]


def test_transaction_files_keep_visibility_permissions_and_items():
    files = {
        "visible": False,
        "can_manage_files": False,
        "items": [{"id": "42", "type": "files", "attributes": {"filename": "trade.pdf"}}],
        "future_field": None,
    }
    client = FakeClient({"data": files})
    assert TransactionsResource(client).get_transaction_files("1968") == files
    assert client.calls == [("GET", "/transactions/1968/files", {"params": None})]


def test_attach_file_sends_single_file_linkage_and_accepts_no_content():
    client = FakeClient()
    assert TransactionsResource(client).attach_transaction_file("1968", "42") is None
    assert client.calls == [
        (
            "POST",
            "/transactions/1968/files",
            {
                "json": {"data": {"id": "42", "type": "files"}},
                "data": None,
                "params": None,
                "headers": None,
            },
        )
    ]


def test_detach_only_removes_the_transaction_file_association():
    client = FakeClient()
    assert TransactionsResource(client).detach_transaction_file("1968", "42") is None
    assert client.calls == [
        (
            "DELETE",
            "/transactions/1968/files/42",
            {"json": None, "data": None, "params": None, "headers": None},
        )
    ]
