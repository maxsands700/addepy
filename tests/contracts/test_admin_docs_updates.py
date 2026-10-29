"""Offline requests for Admin behavior in the current Addepar guides."""

from copy import deepcopy
import json

import pytest
import requests

from addepy.exceptions import ProtocolError
from addepy.resources.admin.audit import AuditResource
from addepy.resources.admin.files import FilesResource
from addepy.resources.admin.reports import ReportsResource


class FakeClient:
    def __init__(self, *documents):
        self.documents = list(documents)
        self.calls = []

    def _request(self, method, endpoint, **kwargs):
        self.calls.append((method, endpoint, deepcopy(kwargs)))
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps(self.documents.pop(0)).encode()
        return response


@pytest.mark.parametrize(
    "method,kind",
    [
        ("query_login_attempts", "login_attempt"),
        ("query_attribute_changes", "attribute"),
        ("query_transaction_changes", "transaction"),
        ("query_permission_changes", "permission"),
    ],
)
@pytest.mark.parametrize(
    "dates",
    [{}, {"start_date": "2026-10-01"}, {"end_date": "2026-10-02"}],
)
def test_audit_leaves_missing_date_defaults_to_server(method, kind, dates):
    client = FakeClient({"data": []})
    assert getattr(AuditResource(client), method)(**dates) == []
    assert client.calls[0][:2] == ("POST", "/audit_trail")
    assert client.calls[0][2]["json"] == {
        "data": {"type": "audit_trail", "attributes": {"object_type": kind, **dates}}
    }


@pytest.mark.parametrize("actions", [["Add"], []])
def test_login_action_filter_is_sent_with_user_filters(actions):
    client = FakeClient({"data": [{"id": "entry", "type": "audit_trail"}]})
    entries = AuditResource(client).query_login_attempts(
        actions=actions, user_type="custom", users=["17"]
    )
    assert entries == [{"id": "entry", "type": "audit_trail"}]
    assert client.calls[0][2]["json"]["data"]["attributes"] == {
        "object_type": "login_attempt",
        "actions": actions,
        "user_type": "custom",
        "users": ["17"],
    }


def test_file_item_supports_documented_filters_and_preserves_resource_fields():
    item = {"id": "123", "type": "files", "attributes": {"future_attribute": False}}
    client = FakeClient({"data": item})
    assert FilesResource(client).get_file(
        "123",
        created_after="2026-10-01",
        created_before="2026-10-02",
        entity_id="1",
        group_id="2",
        included_objects="FILES_AND_FOLDERS",
        parent_folder_id="0",
    ) == item
    assert client.calls == [
        (
            "GET",
            "/files/123",
            {
                "params": {
                    "filter[files][createdAfter]": "2026-10-01",
                    "filter[files][createdBefore]": "2026-10-02",
                    "filter[files][entityId]": "1",
                    "filter[files][groupId]": "2",
                    "filter[files][includedObjects]": "FILES_AND_FOLDERS",
                    "filter[files][parentFolderId]": "0",
                }
            },
        )
    ]


def test_file_item_without_filters_retains_original_request():
    client = FakeClient({"data": {"id": "123", "type": "files"}})
    FilesResource(client).get_file("123")
    assert client.calls == [("GET", "/files/123", {"params": None})]


@pytest.mark.parametrize("method", ["iter_archived_files", "list_archived_files"])
def test_archive_portfolio_filters_survive_pagination(method):
    client = FakeClient(
        {
            "data": [{"id": "1", "type": "files"}],
            "links": {"next": "/v1/archive/files?page[after]=1&page[limit]=1"},
        },
        {"data": [{"id": "2", "type": "files"}], "links": {"next": None}},
    )
    result = list(
        getattr(FilesResource(client), method)(entity_id="4", group_id="5", page_limit=1)
    )
    assert [item["id"] for item in result] == ["1", "2"]
    for _, _, kwargs in client.calls:
        assert kwargs["params"]["filter[files][entityId]"] == "4"
        assert kwargs["params"]["filter[files][groupId]"] == "5"
    assert client.calls[1][2]["params"]["page[after]"] == "1"


@pytest.mark.parametrize("method", ["iter_reports", "list_reports"])
def test_report_list_caps_pages_and_resumes_after_id_with_filters(method):
    client = FakeClient(
        {
            "data": [{"id": "8", "type": "reports"}],
            "links": {"next": "/v1/reports?page[after]=8&page[limit]=500"},
        },
        {"data": [{"id": "9", "type": "reports"}], "links": {"next": None}},
    )
    reports = list(
        getattr(ReportsResource(client), method)(
            name="Quarterly", page_after=7, page_limit=2000
        )
    )
    assert [item["id"] for item in reports] == ["8", "9"]
    assert client.calls[0] == (
        "GET",
        "/reports",
        {"params": {"filter[name]": "Quarterly", "page[after]": 7, "page[limit]": 500}},
    )
    assert client.calls[1][2]["params"] == {
        "filter[name]": "Quarterly",
        "page[after]": "8",
        "page[limit]": "500",
    }


def test_report_metadata_cursor_uses_after_and_preserves_zero_starting_id():
    client = FakeClient(
        {"data": [{"id": "1", "type": "reports"}], "meta": {"page": {"next_cursor": 1}}},
        {"data": [], "links": {"next": None}},
    )
    ReportsResource(client).list_reports(page_after=0, page_limit=1)
    assert client.calls[0][2]["params"] == {"page[after]": 0, "page[limit]": 1}
    assert client.calls[1][2]["params"] == {"page[after]": 1, "page[limit]": 1}


def test_report_list_still_requires_a_collection_response():
    client = FakeClient({"data": {"id": "1", "type": "reports"}})
    with pytest.raises(ProtocolError, match="data as an array"):
        ReportsResource(client).list_reports()


def test_report_page_cap_does_not_change_general_file_page_limits():
    client = FakeClient({"data": []})
    FilesResource(client).list_files(page_limit=2000)
    assert client.calls[0][2]["params"]["page[limit]"] == 2000
