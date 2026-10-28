"""Audit queries use a POST first page and transport-backed GET pagination."""

import json
from unittest.mock import Mock

import pytest
import requests

from addepy import AddePy, ForbiddenError
from addepy.exceptions import ProtocolError


AUDIT_URL = "https://example.addepar.com/api/v1/audit_trail"


def response(document, status=200, headers=None):
    result = requests.Response()
    result.status_code = status
    result.headers.update(headers or {})
    result._content = json.dumps(document).encode()
    result._content_consumed = True
    return result


def page(entry_id, next_link=None):
    return response(
        {
            "data": [{"id": entry_id, "type": "audit_trail"}],
            "links": {"next": next_link},
        }
    )


def client_with(*replies, token_provider=None):
    session = Mock(spec=requests.Session)
    session.request.side_effect = replies
    auth = (
        {"token_provider": token_provider}
        if token_provider is not None
        else {"api_key": "encoded"}
    )
    return AddePy("example", "1", session=session, **auth), session


@pytest.mark.parametrize(
    "method,object_type",
    [
        ("query_login_attempts", "login_attempt"),
        ("query_attribute_changes", "attribute"),
        ("query_transaction_changes", "transaction"),
        ("query_permission_changes", "permission"),
    ],
)
def test_all_audit_queries_post_once_then_get_pages(method, object_type):
    client, session = client_with(
        page("first", "/api/v1/audit_trail?page[cursor]=next"), page("second")
    )
    filters = {"user_type": "custom", "users": ["17"]}
    if object_type != "login_attempt":
        filters["actions"] = ["Modify"]
    result = getattr(client.admin.audit, method)(
        "2026-10-27", "2026-10-28", page_limit=1, **filters
    )
    assert [entry["id"] for entry in result] == ["first", "second"]
    assert session.request.call_count == 2
    first, second = session.request.call_args_list
    assert first.args == ("POST", AUDIT_URL)
    assert first.kwargs["json"] == {
        "data": {
            "type": "audit_trail",
            "attributes": {
                "object_type": object_type,
                "start_date": "2026-10-27",
                "end_date": "2026-10-28",
                **filters,
            },
        }
    }
    assert first.kwargs["params"] == {"page[limit]": 1}
    assert second.args == ("GET", AUDIT_URL)
    assert second.kwargs["params"] == {"page[limit]": 1, "page[cursor]": "next"}
    assert "json" not in second.kwargs
    assert second.kwargs["headers"]["Authorization"] == "Basic encoded"
    assert second.kwargs["headers"]["Addepar-Firm"] == "1"
    assert second.kwargs["headers"]["Accept"] == "application/vnd.api+json"
    assert second.kwargs["timeout"] == (10, 60)
    session.get.assert_not_called()


@pytest.mark.parametrize(
    "next_link",
    [
        "/audit_trail?page[cursor]=next",
        "/v1/audit_trail?page[cursor]=next",
        "/api/v1/audit_trail?page[cursor]=next",
        AUDIT_URL + "?page[cursor]=next",
        "?page[cursor]=next",
        {"href": "?page[cursor]=next"},
        {"href": AUDIT_URL + "?page[cursor]=next"},
    ],
)
def test_audit_follows_next_link_forms(next_link):
    client, session = client_with(page("first", next_link), page("second"))
    result = client.admin.audit.query_attribute_changes("2026-10-27", "2026-10-27")
    assert [entry["id"] for entry in result] == ["first", "second"]
    assert session.request.call_args.args == ("GET", AUDIT_URL)
    assert session.request.call_args.kwargs["params"]["page[cursor]"] == "next"


def test_audit_repeated_next_link_raises_before_another_request():
    next_link = "?page[cursor]=same"
    client, session = client_with(page("first", next_link), page("second", next_link))
    with pytest.raises(ProtocolError, match="repeated"):
        client.admin.audit.query_attribute_changes("2026-10-27", "2026-10-27")
    assert session.request.call_count == 2


def test_audit_next_page_uses_current_token():
    provider = Mock(side_effect=["first-token", "second-token"])
    client, session = client_with(
        page("first", "?page[cursor]=next"),
        page("second"),
        token_provider=provider,
    )
    client.admin.audit.query_attribute_changes("2026-10-27", "2026-10-27")
    assert [
        call.kwargs["headers"]["Authorization"]
        for call in session.request.call_args_list
    ] == ["Bearer first-token", "Bearer second-token"]
    assert provider.call_count == 2


@pytest.mark.parametrize("status", [429, 503])
def test_audit_next_page_retries_transient_errors(status, monkeypatch):
    sleep = Mock()
    monkeypatch.setattr("addepy.transport.time.sleep", sleep)
    client, session = client_with(
        page("first", "?page[cursor]=next"),
        response({"errors": []}, status, {"Retry-After": "2"}),
        page("second"),
    )
    result = client.admin.audit.query_attribute_changes("2026-10-27", "2026-10-27")
    assert [entry["id"] for entry in result] == ["first", "second"]
    assert [call.args[0] for call in session.request.call_args_list] == [
        "POST",
        "GET",
        "GET",
    ]
    sleep.assert_called_once_with(2)


def test_audit_next_page_raises_sdk_error_with_response_details():
    denied = response(
        {"errors": [{"detail": "Permission denied"}]},
        403,
        {"X-Request-ID": "audit-request"},
    )
    client, session = client_with(page("first", "?page[cursor]=next"), denied)
    with pytest.raises(ForbiddenError) as caught:
        client.admin.audit.query_attribute_changes("2026-10-27", "2026-10-27")
    assert caught.value.response is denied
    assert caught.value.status_code == 403
    assert caught.value.request_id == "audit-request"
    assert session.request.call_count == 2


def test_audit_external_next_link_is_rejected():
    client, session = client_with(
        page("first", "https://other.example/api/v1/audit_trail?page[cursor]=next")
    )
    with pytest.raises(ValueError, match="configured host"):
        client.admin.audit.query_attribute_changes("2026-10-27", "2026-10-27")
    assert session.request.call_count == 1


@pytest.mark.parametrize("first_page", [True, False])
def test_audit_rejects_malformed_collection_on_any_page(first_page):
    replies = [] if first_page else [page("first", "?page[cursor]=next")]
    client, _ = client_with(*replies, response({"data": {"id": "not-an-array"}}))
    with pytest.raises(ProtocolError, match="data as an array"):
        client.admin.audit.query_attribute_changes("2026-10-27", "2026-10-27")
