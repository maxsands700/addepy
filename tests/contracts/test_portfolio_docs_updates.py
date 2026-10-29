"""Current documentation contracts for approved portfolio behavior updates."""

from copy import deepcopy
import json

import pytest
import requests

from addepy.resources.portfolio.analysis import AnalysisResource
from addepy.resources.portfolio.benchmarks import BenchmarksResource
from addepy.resources.portfolio.snapshots import SnapshotsResource
from addepy.resources.portfolio.transaction_jobs import TransactionJobsResource
from addepy.resources.portfolio.transactions import TRANSACTION_TYPES, TransactionsResource


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


SNAPSHOT = {
    "snapshot_type": "snapshot",
    "currency": "USD",
    "trade_date": "2026-03-31",
    "amount": 1000,
    "owner_id": "1",
    "owned_id": "2",
    "knowledge_date": "2026-04-15",
}


def test_snapshot_creation_preserves_knowledge_date_and_allows_percent_based_assets():
    resource = {"id": "123_2026-04-15", "type": "snapshots"}
    client = FakeClient({"data": [resource]})
    assert SnapshotsResource(client).create_snapshot(**SNAPSHOT) == resource
    attributes = client.calls[0][2]["json"]["data"][0]["attributes"]
    assert attributes == {
        "type": "snapshot",
        "currency": "USD",
        "trade_date": "2026-03-31",
        "amount": 1000,
        "knowledge_date": "2026-04-15",
    }


def test_bulk_snapshot_creation_keeps_distinct_knowledge_dates_without_mutation():
    snapshots = [deepcopy(SNAPSHOT), {**SNAPSHOT, "knowledge_date": "2026-04-30", "units": 0}]
    before = deepcopy(snapshots)
    client = FakeClient({"data": []})
    SnapshotsResource(client).create_snapshots(snapshots)
    assert snapshots == before
    data = client.calls[0][2]["json"]["data"]
    assert [item["attributes"]["knowledge_date"] for item in data] == ["2026-04-15", "2026-04-30"]
    assert data[1]["attributes"]["units"] == 0


@pytest.mark.parametrize("attribute", ["amount", "currency", "units", "comment", "price_factor", "accrued_income_per_unit"])
def test_single_snapshot_update_distinguishes_null_from_omitted_fields(attribute):
    client = FakeClient({"data": {}}, {"data": {}})
    resource = SnapshotsResource(client)
    resource.update_snapshot("123_2026-04-15", **{attribute: None})
    resource.update_snapshot("123_2026-04-15")
    assert client.calls[0][2]["json"]["data"]["attributes"] == {attribute: None}
    assert client.calls[1][2]["json"]["data"]["attributes"] == {}
    assert client.calls[0][:2] == ("PATCH", "/snapshots/123_2026-04-15")


@pytest.mark.parametrize("transaction_type", ["transfer", "corporate_action"])
def test_single_transaction_destination_ids_are_relationships(transaction_type):
    client = FakeClient({"data": {"id": "30"}})
    TransactionsResource(client).create_transaction(
        transaction_type, "USD", "2026-03-31", "1", "2",
        new_owner_id="3", new_owned_id="4", amount=0, other_units=10,
    )
    data = client.calls[0][2]["json"]["data"]
    assert data["relationships"] == {
        "owner": {"data": {"type": "entities", "id": "1"}},
        "owned": {"data": {"type": "entities", "id": "2"}},
        "new_owner": {"data": {"type": "entities", "id": "3"}},
        "new_owned": {"data": {"type": "entities", "id": "4"}},
    }
    assert data["attributes"]["other_units"] == 10
    assert data["attributes"]["amount"] == 0
    assert "new_owner_id" not in data["attributes"]
    assert "new_owned_id" not in data["attributes"]


def test_bulk_transaction_destinations_and_ownerless_fee_are_serialized_without_mutation():
    transactions = [
        {"type": "transfer", "owner_id": "1", "owned_id": "2", "new_owner_id": "3", "new_owned_id": "4", "other_units": 5},
        {"type": "node_fee", "owned_id": "12345", "amount": 50},
    ]
    before = deepcopy(transactions)
    client = FakeClient({"data": []})
    TransactionsResource(client).create_transactions(transactions)
    assert transactions == before
    transfer, fee = client.calls[0][2]["json"]["data"]
    assert transfer["relationships"]["new_owner"] == {"data": {"type": "entities", "id": "3"}}
    assert transfer["relationships"]["new_owned"] == {"data": {"type": "entities", "id": "4"}}
    assert transfer["attributes"] == {"type": "transfer", "other_units": 5}
    assert fee["relationships"] == {"owned": {"data": {"type": "entities", "id": "12345"}}}


@pytest.mark.parametrize("transaction_type", ["node_fee", "account_fee", "account_fee_custodian"])
def test_account_fee_with_unknown_owner_omits_the_owner_relationship(transaction_type):
    client = FakeClient({"data": {}})
    TransactionsResource(client).create_transaction(
        transaction_type, "USD", "2026-03-31", owned_id="12345", amount=50,
    )
    relationships = client.calls[0][2]["json"]["data"]["relationships"]
    assert relationships == {"owned": {"data": {"type": "entities", "id": "12345"}}}
    assert "node_fee" in TRANSACTION_TYPES


@pytest.mark.parametrize("bulk", [False, True])
def test_other_transactions_still_require_an_owner_before_sending(bulk):
    client = FakeClient()
    resource = TransactionsResource(client)
    with pytest.raises(ValueError, match="owner_id"):
        if bulk:
            resource.create_transactions([{"type": "buy", "owned_id": "2"}])
        else:
            resource.create_transaction("buy", "USD", "2026-03-31", owned_id="2")
    assert client.calls == []


QUERY_SCOPES = [
    (AnalysisResource, "query", {"columns": [{"key": "value"}], "groupings": ["asset_class"]}),
    (TransactionsResource, "query_transactions", {"columns": ["value"]}),
    (TransactionJobsResource, "create_query_job", {"columns": ["value"]}),
]


@pytest.mark.parametrize("resource_class,method,query", QUERY_SCOPES)
def test_query_builders_accept_external_ids_without_a_portfolio_id(resource_class, method, query):
    external_ids = [{"external_type_key": "crm", "external_id": "client-1"}]
    before = deepcopy(external_ids)
    client = FakeClient({"data": {"id": "job-1"}})
    getattr(resource_class(client), method)(
        **query, portfolio_type="ENTITY", start_date="2026-01-01", end_date="2026-03-31", external_ids=external_ids,
    )
    attributes = client.calls[0][2]["json"]["data"]["attributes"]
    if resource_class is TransactionJobsResource:
        attributes = attributes["parameters"]
    assert attributes["external_ids"] == external_ids
    assert "portfolio_id" not in attributes
    assert external_ids == before


@pytest.mark.parametrize("resource_class,method,query", QUERY_SCOPES)
def test_query_builders_accept_documented_empty_portfolio_placeholder_with_external_ids(resource_class, method, query):
    scope = {"portfolio_id": [], "external_ids": [{"external_type_key": "crm", "external_id": "client-1"}]}
    before = deepcopy(scope)
    client = FakeClient({"data": {"id": "job-1"}})
    getattr(resource_class(client), method)(
        **query, portfolio_type="ENTITY", start_date="2026-01-01", end_date="2026-03-31", **scope,
    )
    attributes = client.calls[0][2]["json"]["data"]["attributes"]
    if resource_class is TransactionJobsResource:
        attributes = attributes["parameters"]
    assert attributes["external_ids"] == scope["external_ids"]
    assert "portfolio_id" not in attributes
    assert scope == before


@pytest.mark.parametrize("resource_class,method,query", QUERY_SCOPES)
def test_zero_portfolio_id_remains_an_explicit_scope(resource_class, method, query):
    client = FakeClient()
    with pytest.raises(ValueError, match="exactly one"):
        getattr(resource_class(client), method)(
            **query, portfolio_type="ENTITY", portfolio_id=0,
            start_date="2026-01-01", end_date="2026-03-31",
            external_ids=[{"external_type_key": "crm", "external_id": "client-1"}],
        )
    assert client.calls == []


@pytest.mark.parametrize(
    "resource_class,method",
    [(AnalysisResource, "query_raw"), (TransactionsResource, "query_raw"), (TransactionJobsResource, "create_job")],
)
def test_raw_queries_preserve_empty_portfolio_placeholder(resource_class, method):
    query = {
        "portfolio_id": [],
        "external_ids": [{"external_type_key": "crm", "external_id": "client-1"}],
        "future_option": {"enabled": False},
    }
    before = deepcopy(query)
    client = FakeClient({"data": {"id": "job-1"}})
    getattr(resource_class(client), method)(query)
    attributes = client.calls[0][2]["json"]["data"]["attributes"]
    if resource_class is TransactionJobsResource:
        attributes = attributes["parameters"]
    assert attributes == before
    assert query == before


@pytest.mark.parametrize("resource_class,method,query", QUERY_SCOPES)
@pytest.mark.parametrize("scope", [{}, {"portfolio_id": "1", "external_ids": [{"external_type_key": "crm", "external_id": "client-1"}]}])
def test_query_builders_require_exactly_one_scope(resource_class, method, query, scope):
    client = FakeClient()
    with pytest.raises(ValueError, match="exactly one"):
        getattr(resource_class(client), method)(
            **query, portfolio_type="ENTITY", start_date="2026-01-01", end_date="2026-03-31", **scope,
        )
    assert client.calls == []


@pytest.mark.parametrize("resource_class,method,query", QUERY_SCOPES)
def test_query_dates_remain_required_with_external_ids(resource_class, method, query):
    client = FakeClient()
    with pytest.raises(ValueError, match="start_date and end_date"):
        getattr(resource_class(client), method)(
            **query, portfolio_type="ENTITY", external_ids=[{"external_type_key": "crm", "external_id": "client-1"}],
        )
    assert client.calls == []


def test_portfolio_query_normalizes_only_string_groupings_without_mutation():
    groupings = ["asset_class", {"key": "security", "arguments": {"show_ticker": False}}]
    before = deepcopy(groupings)
    client = FakeClient({"data": {}})
    AnalysisResource(client).query(
        [{"key": "value"}], groupings, "ENTITY", 1, "2026-01-01", "2026-03-31",
    )
    assert client.calls[0][2]["json"]["data"]["attributes"]["groupings"] == [{"key": "asset_class"}, before[1]]
    assert groupings == before


def test_execute_transaction_query_job_passes_external_ids_to_submission(monkeypatch):
    client = FakeClient({"data": {"id": "job-1"}})
    resource = TransactionJobsResource(client)
    expected = requests.Response()
    monkeypatch.setattr(resource, "resume_job", lambda job_id, **kwargs: expected)
    result = resource.execute_query_job(
        ["value"], "ENTITY", start_date="2026-01-01", end_date="2026-03-31",
        external_ids=[{"external_type_key": "crm", "external_id": "client-1"}],
    )
    assert result is expected
    parameters = client.calls[0][2]["json"]["data"]["attributes"]["parameters"]
    assert parameters["external_ids"][0]["external_id"] == "client-1"
    assert "portfolio_id" not in parameters


@pytest.mark.parametrize("method,endpoint", [("list_benchmarks", "/benchmarks"), ("list_benchmark_association_strategies", "/benchmark_associations_strategies")])
def test_benchmark_page_ceiling_retains_the_callers_total_limit_and_cursor(method, endpoint):
    client = FakeClient(
        {"data": [{"id": "1"}], "links": {"next": f"/v1{endpoint}?page[after]=1"}},
        {"data": [{"id": "2"}], "links": {"next": None}},
    )
    assert getattr(BenchmarksResource(client), method)(page_limit=2000, limit=2) == [{"id": "1"}, {"id": "2"}]
    assert client.calls[0][2]["params"] == {"page[limit]": 500}
    assert client.calls[1][2]["params"] == {"page[limit]": 500, "page[after]": "1"}


@pytest.mark.parametrize("resource_class,method", [(SnapshotsResource, "create_snapshots"), (SnapshotsResource, "update_snapshots"), (SnapshotsResource, "delete_snapshots"), (TransactionsResource, "create_transactions"), (TransactionsResource, "update_transactions"), (TransactionsResource, "delete_transactions")])
@pytest.mark.parametrize("size", [0, 501])
def test_bulk_snapshot_and_transaction_limits_fail_before_sending(resource_class, method, size):
    client = FakeClient()
    values = [{} for _ in range(size)]
    with pytest.raises(ValueError, match="between 1 and 500"):
        getattr(resource_class(client), method)(values)
    assert client.calls == []
