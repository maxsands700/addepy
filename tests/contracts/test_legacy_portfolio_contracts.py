"""Regression contracts for existing transaction and historical-price wrappers."""

from copy import deepcopy
import json

import pytest
import requests

from addepy.exceptions import ProtocolError
from addepy.resources.portfolio.historical_prices import HistoricalPricesResource
from addepy.resources.portfolio.transactions import TransactionsResource


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


def test_bulk_transaction_creation_preserves_relationship_ids_for_reuse():
    transactions = [
        {
            "type": "buy",
            "currency": "USD",
            "trade_date": "2024-01-15",
            "owner_id": "123",
            "owned_id": "456",
            "cash_position_id": "789",
            "amount": 10000,
            "units": 100,
            "fee_breakdown": [{"name": "brokerage", "amount": 10}],
        }
    ]
    before = deepcopy(transactions)
    client = FakeClient({"data": [{"id": "1"}]}, {"data": [{"id": "2"}]})
    resource = TransactionsResource(client)
    assert resource.create_transactions(transactions) == [{"id": "1"}]
    assert transactions == before
    assert resource.create_transactions(transactions) == [{"id": "2"}]
    assert transactions == before
    assert client.calls[0][:2] == ("POST", "/transactions")
    data = client.calls[0][2]["json"]["data"][0]
    assert data["type"] == "transactions"
    assert data["relationships"] == {
        "owner": {"data": {"type": "entities", "id": "123"}},
        "owned": {"data": {"type": "entities", "id": "456"}},
        "cash_position": {"data": {"type": "positions", "id": "789"}},
    }
    assert data["attributes"] == {
        key: value
        for key, value in before[0].items()
        if key not in {"owner_id", "owned_id", "cash_position_id"}
    }


def test_invalid_bulk_transaction_input_remains_unchanged():
    transactions = [{"owner_id": "123", "currency": "USD"}]
    before = deepcopy(transactions)
    client = FakeClient()
    with pytest.raises(KeyError, match="owned_id"):
        TransactionsResource(client).create_transactions(transactions)
    assert transactions == before
    assert not client.calls


def test_historical_price_async_responses_are_not_portfolio_job_resources():
    client = FakeClient({"async_price_save_id": 10}, {"async_price_delete_id": 11})
    resource = HistoricalPricesResource(client)
    prices = [{"date": "2012-06-29", "nodeId": 60, "value": 101.0}]
    assert resource.create_prices("60", prices) == 10
    assert resource.delete_price("60", "2012-06-29") == 11
    assert client.calls[0][:2] == ("POST", "/entities/60/prices")
    assert client.calls[0][2]["json"] == {
        "data": [
            {"type": "historical_prices", "attributes": prices[0]},
        ]
    }
    assert client.calls[1][:2] == ("DELETE", "/entities/60/prices/2012-06-29")


@pytest.mark.parametrize("document", [{}, {"async_price_save_id": None}, []])
def test_historical_price_creation_rejects_missing_job_id(document):
    resource = HistoricalPricesResource(FakeClient(document))
    with pytest.raises(ProtocolError, match="async_price_save_id") as error:
        resource.create_prices(
            "60", [{"date": "2012-06-29", "nodeId": 60, "value": 101.0}]
        )
    assert error.value.status_code == 200


def test_historical_price_deletion_rejects_missing_job_id():
    resource = HistoricalPricesResource(FakeClient({}))
    with pytest.raises(ProtocolError, match="async_price_delete_id"):
        resource.delete_price("60", "2012-06-29")
