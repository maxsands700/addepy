"""Pagination and deadline behavior using independent server-shaped responses."""

from collections import deque
import json

import pytest
import requests

from addepy import AddePy
from addepy.exceptions import AddePyTimeoutError, ProtocolError
from addepy.resources.base import BaseResource


class Client:
    def __init__(self, documents):
        self.documents = deque(documents)
        self.calls = []

    def _request(self, method, endpoint, **kwargs):
        self.calls.append((method, endpoint, kwargs))
        result = requests.Response()
        result.status_code = 200
        result._content = json.dumps(self.documents.popleft()).encode()
        return result


def page(ids, next_url=None):
    return {
        "data": [{"id": str(i), "type": "entities"} for i in ids],
        "links": {"next": next_url},
    }


@pytest.mark.parametrize("key", ["page[after]", "page[cursor]"])
def test_cursor_spelling_and_filters_are_preserved(key):
    client = Client([page([1], f"/v1/entities?{key}=two&page[limit]=1"), page([2])])
    params = {"filter[model_types]": "PERSON_NODE"}
    assert [
        x["id"]
        for x in BaseResource(client)._paginate(
            "/entities", params=params, page_limit=1
        )
    ] == ["1", "2"]
    assert client.calls[1][2]["params"][key] == "two"
    assert client.calls[1][2]["params"]["filter[model_types]"] == "PERSON_NODE"
    assert params == {"filter[model_types]": "PERSON_NODE"}


def test_metadata_cursor_and_full_page_retention():
    first = {
        "data": [{"id": "1"}],
        "included": [{"id": "related"}],
        "meta": {"page": {"next_cursor": "abc"}},
    }
    client = Client([first, {"data": [], "meta": {"page": {"next_cursor": None}}}])
    pages = list(BaseResource(client).iter_pages("/billable_portfolios", page_limit=1))
    assert pages[0] == first
    assert client.calls[1][2]["params"]["page[cursor]"] == "abc"


def test_next_null_takes_precedence_over_stale_metadata():
    first = {
        "data": [],
        "links": {"next": None},
        "meta": {"page": {"next_cursor": "abc"}},
    }
    client = Client([first])
    assert list(BaseResource(client).iter_pages("/entities")) == [first]
    assert len(client.calls) == 1


def test_offset_uses_returned_page_number_not_increment():
    client = Client(
        [page([1], "/v1/generated_reports?page[number]=7&page[size]=2"), page([2])]
    )
    assert (
        len(
            list(
                BaseResource(client)._paginate_offset("/generated_reports", page_size=2)
            )
        )
        == 2
    )
    assert client.calls[1][2]["params"]["page[number]"] == "7"


def test_zero_limit_does_not_send_request():
    client = Client([])
    assert list(BaseResource(client)._paginate("/entities", max_items=0)) == []
    assert client.calls == []


def test_limit_stops_without_fetching_next_page():
    client = Client([page([1, 2], "/v1/entities?page[after]=2")])
    assert len(list(BaseResource(client)._paginate("/entities", max_items=1))) == 1
    assert len(client.calls) == 1


def test_query_only_links_and_multi_valued_filters():
    client = Client(
        [page([1], {"href": "?page[cursor]=c&filter[x]=a&filter[x]=b"}), page([2])]
    )
    assert len(list(BaseResource(client)._paginate("/entities"))) == 2
    assert client.calls[1][1] == "/entities"
    assert client.calls[1][2]["params"]["filter[x]"] == ["a", "b"]


def test_repeated_next_page_is_an_error():
    client = Client([page([1], "?page[cursor]=a"), page([2], "?page[cursor]=a")])
    with pytest.raises(ProtocolError, match="repeated"):
        list(BaseResource(client)._paginate("/entities"))
    assert len(client.calls) == 2


@pytest.mark.parametrize("doc", [{}, [], {"data": {}}, {"data": ["bad"]}])
def test_malformed_collection_is_not_silently_empty(doc):
    client = Client([doc])
    with pytest.raises(ProtocolError):
        list(BaseResource(client)._paginate("/entities"))


def test_external_pagination_link_is_rejected():
    class Session:
        def request(self, *args, **kwargs):
            return Client([page([1], "https://external.example/steal")])._request(
                "GET", "/entities"
            )

    client = AddePy("example", "1", "encoded", session=Session())
    with pytest.raises(ValueError):
        list(client.iter_pages("/entities"))


class Clock:
    def __init__(self):
        self.now = 0
        self.sleeps = []

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


@pytest.fixture
def clock(monkeypatch):
    result = Clock()
    monkeypatch.setattr("addepy.resources.base.time.monotonic", lambda: result.now)
    monkeypatch.setattr("addepy.resources.base.time.sleep", result.sleep)
    return result


def test_poll_checks_immediately(clock):
    resource = BaseResource(Client([]))
    assert (
        resource._poll_until_complete(
            "id", lambda _: "Completed", lambda s: s == "Completed"
        )
        == "Completed"
    )
    assert clock.sleeps == []


def test_polling_sleeps_are_capped_at_deadline(clock):
    resource = BaseResource(Client([]))
    with pytest.raises(AddePyTimeoutError) as caught:
        resource._poll_until_complete(
            "id",
            lambda _: "Queued",
            lambda _: False,
            initial_wait=3,
            max_wait=10,
            timeout=5,
        )
    assert clock.sleeps == [3, 2]
    assert clock.now == 5
    assert caught.value.job_id == "id"
    assert caught.value.last_status == "Queued"


def test_slow_status_response_cannot_succeed_after_deadline(clock):
    def check(_):
        clock.now += 6
        return "Completed"

    with pytest.raises(AddePyTimeoutError):
        BaseResource(Client([]))._poll_until_complete(
            "id", check, lambda _: True, timeout=5
        )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"timeout": 0},
        {"initial_wait": -1},
        {"max_wait": 0},
        {"backoff_factor": 0.5},
        {"timeout": float("nan")},
    ],
)
def test_invalid_polling_configuration_fails_before_request(kwargs):
    with pytest.raises(ValueError):
        BaseResource(Client([]))._poll_until_complete(
            "id", lambda _: pytest.fail("no requests"), lambda _: False, **kwargs
        )
