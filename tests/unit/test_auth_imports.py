"""OAuth lifecycle and dependency-free CSV imports."""

import io
import json
from unittest.mock import Mock

import pytest
import requests

from addepy import AddePy, AuthenticationError, OAuthTokenProvider
from addepy.resources.admin.import_tool import ImportToolResource


def response(body, status=200):
    result = requests.Response()
    result.status_code = status
    result._content = json.dumps(body).encode()
    result._content_consumed = True
    return result


def test_oauth_reuses_until_expiry_and_persists_rotated_refresh_token(monkeypatch):
    now = [100.0]
    monkeypatch.setattr("addepy.auth.time.monotonic", lambda: now[0])
    session = Mock(spec=requests.Session)
    session.post.side_effect = [
        response(
            {"access_token": "one", "refresh_token": "rotated", "expires_in": 100}
        ),
        response({"access_token": "two", "expires_in": 100}),
    ]
    save = Mock()
    provider = OAuthTokenProvider(
        token_url="https://api.addepar.com/public/oauth2/token",
        client_id="id",
        client_secret="secret",
        refresh_token="initial",
        session=session,
        on_token_update=save,
    )
    assert provider() == provider() == "one"
    assert session.post.call_count == 1
    now[0] += 91
    assert provider() == "two"
    assert session.post.call_args.kwargs["data"]["refresh_token"] == "rotated"
    assert session.post.call_args.kwargs["allow_redirects"] is False
    assert save.call_count == 2
    provider.close()
    session.close.assert_not_called()


@pytest.mark.parametrize(
    "body,status",
    [
        ({}, 200),
        ({"access_token": "x", "expires_in": 0}, 200),
        ({"client_secret": "sensitive"}, 401),
        ({}, 302),
    ],
)
def test_invalid_refresh_response_is_explicit_and_redacted(body, status):
    session = Mock(spec=requests.Session)
    session.post.return_value = response(body, status)
    provider = OAuthTokenProvider(
        token_url="https://api.addepar.com/public/oauth2/token",
        client_id="id",
        client_secret="secret",
        refresh_token="refresh",
        session=session,
    )
    with pytest.raises(AuthenticationError) as caught:
        provider()
    assert "sensitive" not in str(caught.value)
    assert "secret" not in str(caught.value)


def test_token_provider_is_used_by_client():
    provider = Mock(return_value="current")
    session = Mock(spec=requests.Session)
    session.request.return_value = response({"data": []})
    client = AddePy(
        "example", "1", token_provider=provider, session=session
    )
    client.request("GET", "/entities")
    provider.assert_called_once_with()
    assert (
        session.request.call_args.kwargs["headers"]["Authorization"] == "Bearer current"
    )


@pytest.mark.parametrize(
    "make_data",
    [
        lambda p: "a,b\n1,2\n",
        lambda p: b"a,b\n1,2\n",
        lambda p: io.StringIO("a,b\n1,2\n"),
        lambda p: io.BytesIO(b"a,b\n1,2\n"),
        lambda p: p,
    ],
)
def test_csv_inputs_work_without_pandas(make_data, tmp_path):
    path = tmp_path / "import.csv"
    path.write_text("a,b\n1,2\n")
    client = Mock()
    client._request.return_value = response({"data": {"id": "job"}})
    assert (
        ImportToolResource(client).create_import(make_data(path), "ATTRIBUTES") == "job"
    )
    kwargs = client._request.call_args.kwargs
    assert kwargs["data"] == "a,b\n1,2\n"
    assert kwargs["params"]["is_dry_run"] == "true"
    assert kwargs["params"]["ignore_warnings"] == "false"
    assert kwargs["headers"]["Content-Type"] == "text/plain"


def test_dataframe_adapter_does_not_mutate_or_require_pandas():
    frame = Mock()
    frame.read = None
    del frame.read
    frame.to_csv.return_value = "a\n1\n"
    client = Mock()
    client._request.return_value = response({"data": {"id": "job"}})
    ImportToolResource(client).create_import(frame, "ATTRIBUTES")
    frame.to_csv.assert_called_once_with(index=False)


@pytest.mark.parametrize("data", ["", b"", object()])
def test_invalid_import_input_never_sends(data):
    client = Mock()
    with pytest.raises((ValueError, TypeError)):
        ImportToolResource(client).create_import(data, "ATTRIBUTES")
    client._request.assert_not_called()


def test_oauth_refresh_inherits_client_deadline(monkeypatch):
    monkeypatch.setattr("addepy.auth.time.monotonic", lambda: 100)
    refresh_session = Mock(spec=requests.Session)
    refresh_session.post.return_value = response(
        {"access_token": "current", "expires_in": 240}
    )
    provider = OAuthTokenProvider(
        token_url="https://api.addepar.com/public/oauth2/token",
        client_id="id",
        client_secret="secret",
        refresh_token="refresh",
        session=refresh_session,
    )
    api_session = Mock(spec=requests.Session)
    api_session.request.return_value = response({"data": []})
    client = AddePy(
        "example", "1", token_provider=provider, session=api_session
    )
    with client.request_deadline(101):
        client.request("GET", "/entities")
    assert refresh_session.post.call_args.kwargs["timeout"].total == 1


def test_expired_oauth_deadline_never_refreshes(monkeypatch):
    from addepy import RequestTimeoutError

    monkeypatch.setattr("addepy.auth.time.monotonic", lambda: 100)
    session = Mock(spec=requests.Session)
    provider = OAuthTokenProvider(
        token_url="https://api.addepar.com/public/oauth2/token",
        client_id="id",
        client_secret="secret",
        refresh_token="refresh",
        session=session,
    )
    with pytest.raises(RequestTimeoutError):
        provider.get_token(deadline=99)
    session.post.assert_not_called()


def test_real_dataframe_with_read_column():
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame({"read": ["value"], "amount": [12]})
    client = Mock()
    client._request.return_value = response({"data": {"id": "job"}})
    ImportToolResource(client).create_import(frame, "ATTRIBUTES")
    assert client._request.call_args.kwargs["data"] == "read,amount\nvalue,12\n"
    assert frame.to_dict() == {"read": {0: "value"}, "amount": {0: 12}}
