"""Offline request contracts transcribed from the linked Addepar guides.

These check SDK behavior against documentation, not server availability.
See docs/resources.md for investment resource conventions.
"""

from collections import deque
from copy import deepcopy

import pytest

from addepy.exceptions import AddePyError
from addepy.resources.ownership.entities import EntitiesResource
from addepy.resources.portfolio import PortfolioNamespace
from addepy.resources.portfolio.benchmarks import BenchmarksResource
from addepy.resources.portfolio.estimated_returns import EstimatedReturnsResource
from addepy.resources.portfolio.underlying_assets import UnderlyingAssetsResource


class FakeResponse:
    def __init__(self, document):
        self.document = document

    def json(self):
        return deepcopy(self.document)


class FakeClient:
    def __init__(self, *documents):
        self.documents = deque(documents)
        self.calls = []

    def _request(self, method, endpoint, **kwargs):
        self.calls.append((method, endpoint, deepcopy(kwargs)))
        assert self.documents, "Unexpected extra HTTP request"
        return FakeResponse(self.documents.popleft())


ESTIMATED_RETURN = {
    "id": "123_2024-01-15",
    "type": "estimated_returns",
    "attributes": {"entity_id": 123, "date": "2024-01-15", "return_value": 0.05},
}
PROXY = {
    "id": "116_2025-12-31",
    "type": "benchmark_proxies",
    "attributes": {
        "as_of_date": "2025-12-31",
        "entity_id": 116,
        "benchmark_id": 734,
        "benchmark_name": "Imported Benchmark 1",
    },
}
ASSET = {
    "id": "1234",
    "type": "derivatives_underlying_assets",
    "attributes": {
        "entity_name": "corporate bond",
        "entity_type": "SECURITY",
        "underlying_type": "PRICE",
        "base_currency": "USD",
    },
}


def test_new_resources_available_and_cached_in_portfolio_namespace():
    namespace = PortfolioNamespace(FakeClient())
    assert isinstance(namespace.estimated_returns, EstimatedReturnsResource)
    assert namespace.estimated_returns is namespace.estimated_returns
    assert isinstance(namespace.underlying_assets, UnderlyingAssetsResource)
    assert namespace.underlying_assets is namespace.underlying_assets


def test_estimated_returns_required_entity_filter_and_composite_cursor():
    second = {**ESTIMATED_RETURN, "id": "124_2024-01-15"}
    client = FakeClient(
        {
            "data": [ESTIMATED_RETURN],
            "links": {"next": "/v1/estimated_returns?page[after]=123_2024-01-15"},
        },
        {"data": [second], "links": {"next": None}},
    )
    result = EstimatedReturnsResource(client).list_estimated_returns(
        [123, "124"], page_limit=1
    )
    assert result == [ESTIMATED_RETURN, second]
    assert client.calls[0][:2] == ("GET", "/estimated_returns")
    assert client.calls[0][2]["params"] == {
        "filter[entity_id]": "123,124",
        "page[limit]": 1,
    }
    assert client.calls[1][2]["params"]["page[after]"] == "123_2024-01-15"


@pytest.mark.parametrize("entity_ids", [[], "123"])
def test_estimated_returns_reject_missing_or_ambiguous_filter(entity_ids):
    client = FakeClient()
    with pytest.raises(ValueError, match="entity_ids"):
        EstimatedReturnsResource(client).list_estimated_returns(entity_ids)
    assert not client.calls


@pytest.mark.parametrize("response_data", [[ESTIMATED_RETURN], ESTIMATED_RETURN])
def test_estimated_return_single_upsert_handles_documented_array_response(
    response_data,
):
    client = FakeClient({"data": response_data})
    result = EstimatedReturnsResource(client).upsert_estimated_return(
        123, "2024-01-15", 0.05
    )
    assert result == ESTIMATED_RETURN
    assert client.calls[0][:2] == ("POST", "/estimated_returns")
    assert client.calls[0][2]["json"] == {
        "data": {
            "type": "estimated_returns",
            "attributes": ESTIMATED_RETURN["attributes"],
        }
    }


def test_single_estimated_return_rejects_empty_success_response():
    resource = EstimatedReturnsResource(FakeClient({"data": []}))
    with pytest.raises(AddePyError, match="Expected one"):
        resource.create_estimated_return(123, "2024-01-15", 0.05)


def test_estimated_returns_bulk_upsert_preserves_attributes_and_input():
    attributes = [deepcopy(ESTIMATED_RETURN["attributes"])]
    original = deepcopy(attributes)
    client = FakeClient({"data": [ESTIMATED_RETURN]})
    assert EstimatedReturnsResource(client).create_estimated_returns(attributes) == [
        ESTIMATED_RETURN
    ]
    assert attributes == original
    assert client.calls[0][2]["json"] == {
        "data": [
            {"type": "estimated_returns", "attributes": original[0]},
        ]
    }


def test_estimated_return_patch_only_changes_value_and_preserves_zero():
    client = FakeClient({"data": ESTIMATED_RETURN})
    EstimatedReturnsResource(client).update_estimated_return("123_2024-01-15", 0.0)
    assert client.calls[0][:2] == ("PATCH", "/estimated_returns/123_2024-01-15")
    assert client.calls[0][2]["json"] == {
        "data": {
            "id": "123_2024-01-15",
            "type": "estimated_returns",
            "attributes": {"return_value": 0.0},
        }
    }


@pytest.mark.parametrize(
    "resource_class,method,arg,path,document",
    [
        (
            EstimatedReturnsResource,
            "get_estimated_return",
            "123_2024-01-15",
            "/estimated_returns/123_2024-01-15",
            ESTIMATED_RETURN,
        ),
        (
            BenchmarksResource,
            "get_benchmark_proxy",
            "116_2025-12-31",
            "/benchmark_proxies/116_2025-12-31",
            PROXY,
        ),
    ],
)
def test_composite_id_reads(resource_class, method, arg, path, document):
    client = FakeClient({"data": document})
    assert getattr(resource_class(client), method)(arg) == document
    assert client.calls[0][:2] == ("GET", path)


@pytest.mark.parametrize(
    "resource_class,method,arg,path",
    [
        (
            EstimatedReturnsResource,
            "delete_estimated_return",
            "123_2024-01-15",
            "/estimated_returns/123_2024-01-15",
        ),
        (
            EstimatedReturnsResource,
            "delete_entity_estimated_returns",
            123,
            "/estimated_returns/entity/123",
        ),
        (
            BenchmarksResource,
            "delete_benchmark_proxy",
            "116_2025-12-31",
            "/benchmark_proxies/116_2025-12-31",
        ),
        (
            BenchmarksResource,
            "delete_entity_benchmark_proxies",
            116,
            "/benchmark_proxies/entity/116",
        ),
        (
            UnderlyingAssetsResource,
            "delete_underlying_asset",
            "1234",
            "/derivatives/underlying_assets/1234",
        ),
    ],
)
def test_deletes_do_not_parse_empty_204_body(resource_class, method, arg, path):
    client = FakeClient(None)
    assert getattr(resource_class(client), method)(arg) is None
    assert client.calls[0][:2] == ("DELETE", path)


def test_benchmark_proxy_list_follows_reference_cursor():
    client = FakeClient(
        {
            "data": [PROXY],
            "links": {"next": "/v1/benchmark_proxies?page[cursor]=next-proxy"},
        },
        {"data": [], "links": {"next": None}},
    )
    assert BenchmarksResource(client).list_benchmark_proxies(entity_ids=[116]) == [
        PROXY
    ]
    assert len(client.calls) == 2
    assert client.calls[1][2]["params"]["page[cursor]"] == "next-proxy"
    assert client.calls[0][2]["params"]["filter[entity_id]"] == "116"


def test_bulk_benchmark_updates_do_not_pop_callers_ids():
    updates = [
        {"id": "739", "name": "New name", "fixed_return": {"fixed_return": 0.17}}
    ]
    original = deepcopy(updates)
    client = FakeClient({"data": []})
    BenchmarksResource(client).update_benchmarks(updates)
    assert updates == original
    assert client.calls[0][2]["json"] == {
        "data": [
            {
                "id": "739",
                "type": "benchmarks",
                "attributes": {
                    "name": "New name",
                    "fixed_return": {"fixed_return": 0.17},
                },
            }
        ]
    }


def test_underlying_asset_get_includes_metric_window():
    client = FakeClient({"data": ASSET})
    result = UnderlyingAssetsResource(client).get_underlying_asset(
        "1234", metric_date_from="2025-01-01", metric_date_to="2025-01-31"
    )
    assert result == ASSET
    assert client.calls[0][:2] == ("GET", "/derivatives/underlying_assets/1234")
    assert client.calls[0][2]["params"] == {
        "metric_date_from": "2025-01-01",
        "metric_date_to": "2025-01-31",
    }


def test_underlying_assets_paginate_numeric_offset_without_links_or_known_server_cap():
    other = {**ASSET, "id": "1235"}
    client = FakeClient({"data": [ASSET]}, {"data": [other]}, {"data": []})
    result = UnderlyingAssetsResource(client).list_underlying_assets(page_limit=50)
    assert result == [ASSET, other]
    assert [call[2]["params"]["page[after]"] for call in client.calls] == [0, 1, 2]


def test_underlying_assets_limit_avoids_additional_requests():
    client = FakeClient({"data": [ASSET, {**ASSET, "id": "1235"}]})
    assert UnderlyingAssetsResource(client).list_underlying_assets(limit=1) == [ASSET]
    assert len(client.calls) == 1
    assert UnderlyingAssetsResource(FakeClient()).list_underlying_assets(limit=0) == []


def test_underlying_assets_reject_repeated_pages_instead_of_looping():
    client = FakeClient({"data": [ASSET]}, {"data": [ASSET]})
    with pytest.raises(AddePyError, match="did not advance"):
        UnderlyingAssetsResource(client).list_underlying_assets()


@pytest.mark.parametrize("kwargs", [{"limit": -1}, {"page_limit": 0}])
def test_underlying_assets_reject_invalid_pagination(kwargs):
    with pytest.raises(ValueError):
        UnderlyingAssetsResource(FakeClient()).list_underlying_assets(**kwargs)


def test_underlying_asset_create_has_resource_type_and_no_client_assigned_id():
    client = FakeClient({"data": ASSET})
    assert (
        UnderlyingAssetsResource(client).create_underlying_asset(**ASSET["attributes"])
        == ASSET
    )
    assert client.calls[0][:2] == ("POST", "/derivatives/underlying_assets")
    assert client.calls[0][2]["json"] == {
        "data": {
            "type": "derivatives_underlying_assets",
            "attributes": ASSET["attributes"],
        }
    }


def test_underlying_asset_patch_preserves_null_spot_deletion():
    client = FakeClient({"data": ASSET})
    spots = {"2025-01-01": 7.0, "2025-01-02": None}
    UnderlyingAssetsResource(client).update_underlying_asset(1234, metric_values=spots)
    assert client.calls[0][:2] == ("PATCH", "/derivatives/underlying_assets/1234")
    assert client.calls[0][2]["json"] == {
        "data": {
            "id": "1234",
            "type": "derivatives_underlying_assets",
            "attributes": {"metric_values": spots},
        }
    }


def test_bulk_underlying_asset_operations_use_collection_and_preserve_inputs():
    client = FakeClient({"data": [ASSET]}, {"data": [ASSET]}, None)
    resource = UnderlyingAssetsResource(client)
    attributes = deepcopy(ASSET["attributes"])
    updates = [{"id": 1234, "metric_values": {"2025-01-02": None}}]
    original = deepcopy(updates)
    assert resource.create_underlying_assets([attributes]) == [ASSET]
    assert resource.update_underlying_assets(updates) == [ASSET]
    resource.delete_underlying_assets([1234, "1235"])
    assert updates == original
    assert client.calls[0][2]["json"]["data"] == [
        {"type": ASSET["type"], "attributes": attributes}
    ]
    assert client.calls[1][2]["json"]["data"] == [
        {
            "id": "1234",
            "type": ASSET["type"],
            "attributes": {"metric_values": {"2025-01-02": None}},
        }
    ]
    assert client.calls[2][2]["json"]["data"] == [
        {"id": "1234", "type": ASSET["type"]},
        {"id": "1235", "type": ASSET["type"]},
    ]
    assert [call[:2] for call in client.calls] == [
        (method, "/derivatives/underlying_assets")
        for method in ("POST", "PATCH", "DELETE")
    ]


def test_model_type_changes_use_dedicated_bulk_route_not_entity_attribute_patch():
    data = [
        {
            "type": "entity_type_updates",
            "id": 1111,
            "attributes": {"new_model_type": "hedge_fund"},
        }
    ]
    client = FakeClient({"data": data})
    updates = [{"id": 1111, "new_model_type": "hedge_fund"}]
    original = deepcopy(updates)
    assert EntitiesResource(client).change_model_types(updates) == data
    assert updates == original
    assert client.calls[0][:2] == ("PATCH", "/entity_types")
    assert client.calls[0][2]["json"] == {"data": data}


def test_single_model_type_change_unwraps_bulk_response():
    item = {
        "type": "entity_type_updates",
        "id": "1111",
        "attributes": {"new_model_type": "etf"},
    }
    client = FakeClient({"data": [item]})
    assert EntitiesResource(client).change_model_type("1111", "etf") == item
    assert client.calls[0][2]["json"] == {"data": [item]}


def test_entity_type_discovery_remains_unpaginated():
    model_type = {
        "id": "stock",
        "type": "entity_types",
        "attributes": {"entity_attributes": []},
    }
    client = FakeClient({"data": [model_type]}, {"data": model_type})
    resource = EntitiesResource(client)
    assert resource.list_entity_types() == [model_type]
    assert resource.get_entity_type("stock") == model_type
    assert [call[:2] for call in client.calls] == [
        ("GET", "/entity_types"),
        ("GET", "/entity_types/stock"),
    ]
    assert client.calls[0][2]["params"] is None
