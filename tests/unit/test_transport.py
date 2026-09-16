"""Transport regressions: credentials, retry policy, errors and streamed downloads."""

import base64
import io
import json
from unittest.mock import Mock

import pytest
import requests

from addepy import AddePy, AddePyError, AuthenticationError, RateLimitError, TransportError, ValidationError
from addepy.exceptions import ProtocolError, RequestTimeoutError
from addepy.transport import retry_after


def response(status=200, body=None, headers=None, content=None):
    result = requests.Response()
    result.status_code = status
    result.headers.update(headers or {})
    result._content = content if content is not None else json.dumps(body if body is not None else {"data": []}).encode()
    result._content_consumed = True
    return result


def client_with(*replies, **kwargs):
    session = Mock(spec=requests.Session)
    session.request.side_effect = replies
    return AddePy("example", "1", "encoded", load_env=False, session=session, **kwargs), session


@pytest.mark.parametrize("environment,host", [
    ("production", "example.addepar.com"),
    ("development", "example.clientdev.addepar.com"),
    ("sandbox", "example.sandbox.addepar.com"),
])
def test_environment_urls_and_basic_headers(environment, host):
    client, session = client_with(response(), environment=environment)
    client.request("GET", "/entities")
    args, kwargs = session.request.call_args
    assert args == ("GET", f"https://{host}/api/v1/entities")
    assert kwargs["headers"]["Authorization"] == "Basic encoded"
    assert kwargs["headers"]["Addepar-Firm"] == "1"
    assert kwargs["headers"]["Accept"] == "application/vnd.api+json"
    assert kwargs["timeout"] == (10, 60)


def test_explicit_bearer_overrides_environment_basic(monkeypatch):
    monkeypatch.setenv("ADDEPAR_API_KEY", "old")
    session = Mock(spec=requests.Session)
    session.request.return_value = response()
    with AddePy("example", "1", access_token="fresh", session=session, load_env=False) as client:
        client.request("GET", "/entities")
    assert session.request.call_args.kwargs["headers"]["Authorization"] == "Bearer fresh"
    session.close.assert_not_called()


def test_key_pair_encoding():
    session = Mock(spec=requests.Session)
    session.request.return_value = response()
    client = AddePy("example", "1", key_id="key", key_secret="secret", session=session, load_env=False)
    client.request("GET", "/entities")
    assert session.request.call_args.kwargs["headers"]["Authorization"] == "Basic " + base64.b64encode(b"key:secret").decode()


@pytest.mark.parametrize("kwargs", [
    {"api_key": "x", "access_token": "y"}, {"key_id": "x"}, {"access_token": ""},
    {"api_key": "x", "environment": "test"}, {"api_key": "x", "base_url": "http://example.com/api/v1"},
    {"api_key": "x", "base_url": "https://user:secret@example.com/api/v1"},
])
def test_invalid_configuration(kwargs):
    with pytest.raises(ValueError):
        AddePy("example", "1", load_env=False, **kwargs)


@pytest.mark.parametrize("endpoint,url", [
    ("/entities", "https://example.addepar.com/api/v1/entities"),
    ("/v1/entities?page[after]=1", "https://example.addepar.com/api/v1/entities?page[after]=1"),
    ("/api/v1/entities", "https://example.addepar.com/api/v1/entities"),
    ("https://example.addepar.com/api/v1/entities", "https://example.addepar.com/api/v1/entities"),
])
def test_absolute_and_relative_links(endpoint, url):
    client, session = client_with(response())
    client.request("GET", endpoint)
    assert session.request.call_args.args[1] == url


def test_global_api_url():
    client, session = client_with(response(), base_url="https://api.addepar.com/v1")
    client.request("GET", "/v1/entities")
    assert session.request.call_args.args[1] == "https://api.addepar.com/v1/entities"


@pytest.mark.parametrize("url", ["https://evil.example/entities", "//evil.example/entities", "http://example.addepar.com/api/v1/entities"])
def test_cross_host_request_rejected(url):
    client, session = client_with()
    with pytest.raises(ValueError):
        client.request("GET", url)
    session.request.assert_not_called()


def test_http_errors_keep_falsey_response_metadata_and_body():
    reply = response(400, {"errors": [{"detail": "invalid field", "source": {"pointer": "/data"}}]}, {"X-Request-ID": "abc"})
    client, _ = client_with(reply)
    with pytest.raises(ValidationError) as caught:
        client.request("POST", "/entities", json={})
    error = caught.value
    assert error.status_code == 400
    assert error.response is reply
    assert error.request_id == "abc"
    assert error.errors[0]["source"]["pointer"] == "/data"
    assert "invalid field" not in str(error)


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_reads_retry_transient_statuses(status, monkeypatch):
    sleep = Mock()
    monkeypatch.setattr("addepy.transport.time.sleep", sleep)
    client, session = client_with(response(status, headers={"X-RateLimit-Retry-After": "2"}), response())
    assert client.request("GET", "/entities").status_code == 200
    assert session.request.call_count == 2
    sleep.assert_called_once_with(2)


@pytest.mark.parametrize("method", ["POST", "PATCH", "PUT", "DELETE"])
def test_writes_are_not_retried(method, monkeypatch):
    monkeypatch.setattr("addepy.transport.time.sleep", lambda _: pytest.fail("must not retry"))
    client, session = client_with(response(429, headers={"X-RateLimit-Retry-After": "1"}))
    with pytest.raises(RateLimitError):
        client.request(method, "/jobs", json={})
    assert session.request.call_count == 1


def test_explicit_retry_and_no_replay_of_stream_body(monkeypatch):
    monkeypatch.setattr("addepy.transport.time.sleep", lambda _: None)
    client, session = client_with(response(503), response())
    client.request("POST", "/jobs", json={}, retry=True)
    assert session.request.call_count == 2
    client, session = client_with(response(503))
    with pytest.raises(AddePyError):
        client.request("POST", "/imports", data=io.StringIO("csv"), retry=True)
    assert session.request.call_count == 1


def test_long_server_delay_is_not_shortened():
    client, session = client_with(response(429, headers={"X-RateLimit-Retry-After": "900"}), max_retry_wait=30)
    with pytest.raises(RateLimitError) as caught:
        client.request("GET", "/entities")
    assert caught.value.retry_after == 900
    assert session.request.call_count == 1


@pytest.mark.parametrize("value", ["bad", "NaN", "inf"])
def test_malformed_retry_header_does_not_hide_error(value):
    client, _ = client_with(response(429, headers={"X-RateLimit-Retry-After": value}), max_retries=0)
    with pytest.raises(RateLimitError) as caught:
        client.request("GET", "/entities")
    assert caught.value.retry_after is None


def test_standard_retry_after_http_date():
    assert retry_after(response(429, headers={"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"})) == 0


def test_connection_failure_is_wrapped(monkeypatch):
    monkeypatch.setattr("addepy.transport.time.sleep", lambda _: None)
    client, session = client_with(requests.ConnectionError("secret URL"), requests.ConnectionError("secret URL"), max_retries=1)
    with pytest.raises(TransportError) as caught:
        client.request("GET", "/entities")
    assert session.request.call_count == 2
    assert "secret" not in str(caught.value)


def test_post_timeout_not_replayed():
    client, session = client_with(requests.Timeout())
    with pytest.raises(RequestTimeoutError):
        client.request("POST", "/jobs", json={})
    assert session.request.call_count == 1


def test_get_redirect_strips_credentials_and_query_params():
    download_session = Mock(spec=requests.Session)
    download_session.send.return_value = response(content=b"csv")
    client, session = client_with(response(303, headers={"Location": "https://storage.example/file?signature=xyz"}), download_session=download_session)
    assert client.request("GET", "/jobs/id/download", params={"private": "value"}).content == b"csv"
    call = download_session.send.call_args
    assert call.args[0].method == "GET"
    assert call.args[0].url == "https://storage.example/file?signature=xyz"
    assert "Authorization" not in call.args[0].headers
    assert "Addepar-Firm" not in call.args[0].headers
    assert "params" not in call.kwargs
    assert session.request.call_count == 1


def test_write_redirect_is_not_replayed():
    client, session = client_with(response(307, headers={"Location": "/api/v1/other"}))
    with pytest.raises(ProtocolError):
        client.request("POST", "/jobs", json={})
    assert session.request.call_count == 1


def test_unauthorized_is_not_retried():
    client, session = client_with(response(401), max_retries=10)
    with pytest.raises(AuthenticationError):
        client.request("GET", "/entities")
    assert session.request.call_count == 1


def test_per_request_and_deadline_timeout(monkeypatch):
    monkeypatch.setattr("addepy.transport.time.monotonic", lambda: 100)
    client, session = client_with(response(), response())
    client.request("GET", "/entities", timeout=(1, 2))
    assert session.request.call_args.kwargs["timeout"] == (1, 2)
    with client.request_deadline(103):
        client.request("GET", "/entities")
        assert session.request.call_args.kwargs["timeout"].total == 3
    with client.request_deadline(99), pytest.raises(RequestTimeoutError):
        client.request("GET", "/entities")


def test_download_and_existing_file_protection(tmp_path):
    reply = response(content=b"a,b\n1,2\n")
    client, session = client_with(reply)
    target = tmp_path / "result.csv"
    assert client.download("/jobs/id/download", target) == target
    assert target.read_bytes() == b"a,b\n1,2\n"
    assert session.request.call_args.kwargs["stream"] is True
    with pytest.raises(FileExistsError):
        client.download("/jobs/id/download", target)
    assert session.request.call_count == 1
    assert list(tmp_path.iterdir()) == [target]


def test_failed_download_removes_partial_file(tmp_path):
    reply = response()
    def chunks(**kwargs):
        yield b"first"
        raise requests.ConnectionError("disconnected")
    reply.iter_content = chunks
    client, _ = client_with(reply)
    with pytest.raises(requests.ConnectionError):
        client.download("/jobs/id/download", tmp_path / "result.csv")
    assert list(tmp_path.iterdir()) == []


def test_real_download_session_cannot_merge_credentials(tmp_path):
    class RecordingAdapter(requests.adapters.BaseAdapter):
        def send(self, prepared, **kwargs):
            assert "Authorization" not in prepared.headers
            assert "Addepar-Firm" not in prepared.headers
            assert "Cookie" not in prepared.headers
            assert kwargs["cert"] is None
            assert kwargs["proxies"] == {}
            return response(content=b"data")
        def close(self):
            pass
    downloads = requests.Session()
    downloads.headers.update({"Authorization": "Bearer secret", "Addepar-Firm": "secret"})
    downloads.auth = ("username", "password")
    downloads.cookies.set("session", "secret", domain="storage.example")
    downloads.cert = "private.pem"
    downloads.mount("https://", RecordingAdapter())
    client, _ = client_with(response(303, headers={"Location": "https://storage.example/file"}), download_session=downloads)
    assert client.download("/jobs/id/download", tmp_path / "result").read_bytes() == b"data"


def test_multipart_303_becomes_bodyless_get():
    client, session = client_with(response(303, headers={"Location": "/api/v1/files/1"}), response())
    client.request("POST", "/files", files={"file": ("input.csv", b"csv")})
    call = session.request.call_args
    assert call.args[0] == "GET"
    assert "files" not in call.kwargs
    assert "Content-Type" not in call.kwargs["headers"]


def test_generator_body_is_not_retried():
    client, session = client_with(response(503))
    with pytest.raises(AddePyError):
        client.request("POST", "/imports", data=iter([b"one", b"two"]), retry=True)
    assert session.request.call_count == 1
