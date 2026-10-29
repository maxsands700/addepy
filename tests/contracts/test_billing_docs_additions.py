"""Contracts for Billing namespace ownership, expansions, and documented writes."""

import importlib
import json
from copy import deepcopy
from unittest.mock import Mock

import pytest
import requests

from addepy import AddePy
from addepy.resources import BillingNamespace
from addepy.resources.billing import (
    BillablePortfoliosResource,
    FeeSchedulesResource,
    FeesResource,
    PayoutRecipientsResource,
    PayoutRulesResource,
)


def make_client(document):
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(document).encode()
    session = Mock(spec=requests.Session)
    session.headers = {}
    session.request.return_value = response
    return AddePy(
        firm_name="examplefirm", firm_id="1", api_key="encoded", session=session
    ), session


@pytest.mark.parametrize(
    ("name", "resource_class"),
    [
        ("fees", FeesResource),
        ("fee_schedules", FeeSchedulesResource),
        ("billable_portfolios", BillablePortfoliosResource),
        ("payout_recipients", PayoutRecipientsResource),
        ("payout_rules", PayoutRulesResource),
    ],
)
def test_billing_namespace_owns_lazy_resources(name, resource_class):
    client, session = make_client({})
    assert isinstance(client.billing, BillingNamespace)
    assert client.billing is client.billing
    resource = getattr(client.billing, name)
    assert isinstance(resource, resource_class)
    assert resource._client is client
    assert client._admin is None
    assert not hasattr(client.admin, name)
    assert not hasattr(client.admin, f"_{name}")
    assert client.admin._client is client
    assert resource is getattr(client.billing, name)
    session.request.assert_not_called()


@pytest.mark.parametrize(
    ("resource_name", "method", "endpoint", "kind"),
    [
        ("fees", "get_fee", "/fees/7", "fees"),
        ("fee_schedules", "get_fee_schedule", "/fee_schedules/7", "fee_schedules"),
        (
            "billable_portfolios",
            "get_billable_portfolio",
            "/billable_portfolios/7",
            "billable_portfolios",
        ),
    ],
)
def test_billing_access_uses_existing_routes_and_preserves_server_fields(
    resource_name, method, endpoint, kind
):
    resource = {
        "id": "7",
        "type": kind,
        "attributes": {"future_server_field": {"enabled": True}},
        "relationships": {"future_relationship": {"data": []}},
    }
    client, session = make_client({"data": resource})
    assert getattr(getattr(client.billing, resource_name), method)("7") == resource
    assert session.request.call_args.args == (
        "GET",
        f"https://examplefirm.addepar.com/api/v1{endpoint}",
    )


def test_billing_package_exports_are_importable():
    import addepy.resources.billing as billing

    imported = {}
    exec("from addepy.resources.billing import *", imported)
    assert all(imported[name] is getattr(billing, name) for name in billing.__all__)


@pytest.mark.parametrize("module", ["billing", "billable_portfolios", "payouts"])
def test_old_admin_billing_module_paths_are_removed(module):
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(f"addepy.resources.admin.{module}")


def test_admin_does_not_export_billing_classes():
    import addepy.resources.admin as admin

    for cls in (
        FeesResource,
        FeeSchedulesResource,
        BillablePortfoliosResource,
        PayoutRecipientsResource,
        PayoutRulesResource,
    ):
        assert cls.__name__ not in admin.__all__
        assert not hasattr(admin, cls.__name__)


class FakeClient:
    def __init__(self, *documents):
        self.documents = list(documents)
        self.calls = []

    def _request(self, method, endpoint, **kwargs):
        self.calls.append((method, endpoint, deepcopy(kwargs)))
        document = self.documents.pop(0) if self.documents else None
        response = requests.Response()
        response.status_code = 204 if document is None else 200
        response._content = b"" if document is None else json.dumps(document).encode()
        return response


@pytest.mark.parametrize(
    "resource,method,endpoint,include,kind",
    [
        (FeesResource, "get_fee", "/fees/7", "fee_schedules", "fees"),
        (
            FeeSchedulesResource,
            "get_fee_schedule",
            "/fee_schedules/7",
            "fees",
            "fee_schedules",
        ),
    ],
)
@pytest.mark.parametrize("array_data", [False, True])
def test_expanded_single_reads_can_preserve_complete_documents(
    resource, method, endpoint, include, kind, array_data
):
    item = {"id": "7", "type": kind, "attributes": {"future": None}}
    document = {
        "data": [item] if array_data else item,
        "included": [{"id": "9", "type": include, "attributes": {"future": False}}],
        "meta": {"future": {"count": 1}},
        "links": {"self": endpoint},
    }
    client = FakeClient(document, document)
    api = resource(client)
    assert getattr(api, method)("7", include=include, full_document=True) == document
    assert getattr(api, method)("7", include=include) == item
    assert all(
        call == ("GET", endpoint, {"params": {"include": include}})
        for call in client.calls
    )


@pytest.mark.parametrize(
    "resource,method,endpoint,include",
    [
        (FeesResource, "iter_fee_pages", "/fees", "fee_schedules"),
        (FeeSchedulesResource, "iter_fee_schedule_pages", "/fee_schedules", "fees"),
    ],
)
def test_expanded_page_reads_follow_links_preserving_includes_and_metadata(
    resource, method, endpoint, include
):
    first = {
        "data": [{"id": "1"}],
        "included": [{"id": "11", "type": include}],
        "links": {"next": f"/v1{endpoint}?page[cursor]=cursor-2"},
        "meta": {"page": {"total": 2}},
    }
    second = {
        "data": [{"id": "2"}],
        "included": [{"id": "12", "type": include}],
        "links": {"next": None},
        "meta": {"page": {"total": 2}},
    }
    client = FakeClient(first, second)
    pages = getattr(resource(client), method)(include=include, page_limit=2000)
    assert client.calls == []
    assert list(pages) == [first, second]
    assert client.calls == [
        ("GET", endpoint, {"params": {"include": include, "page[limit]": 500}}),
        (
            "GET",
            f"/v1{endpoint}",
            {
                "params": {
                    "include": include,
                    "page[limit]": 500,
                    "page[cursor]": "cursor-2",
                },
            },
        ),
    ]


@pytest.mark.parametrize(
    "resource,method,include",
    [
        (FeesResource, "iter_fee_pages", "fee_schedules"),
        (FeeSchedulesResource, "iter_fee_schedule_pages", "fees"),
    ],
)
def test_expanded_page_reads_honor_max_pages(resource, method, include):
    document = {"data": [], "links": {"next": "?page[cursor]=next"}}
    client = FakeClient(document)
    assert list(getattr(resource(client), method)(include=include, max_pages=1)) == [
        document
    ]
    assert len(client.calls) == 1


@pytest.mark.parametrize(
    "resource,method,include",
    [
        (FeesResource, "list_fees", "fee_schedules"),
        (FeesResource, "iter_fees", "fee_schedules"),
        (FeeSchedulesResource, "list_fee_schedules", "fees"),
        (FeeSchedulesResource, "iter_fee_schedules", "fees"),
    ],
)
def test_collection_helpers_keep_resource_shapes_and_accept_include(
    resource, method, include
):
    item = {"id": "1", "attributes": {"unknown": False}}
    client = FakeClient(
        {"data": [item], "included": [{"id": "9"}], "links": {"next": None}}
    )
    assert list(getattr(resource(client), method)(include=include)) == [item]
    assert client.calls[0][2]["params"]["include"] == include


def test_singular_schedule_create_uses_array_and_retains_return_resource():
    attributes = {"name": "Quarterly", "future_field": {"enabled": False}}
    before = deepcopy(attributes)
    result = {"id": "10", "type": "fee_schedules"}
    client = FakeClient({"data": [result]})
    assert FeeSchedulesResource(client).create_fee_schedule(attributes, ["1"]) == result
    assert client.calls[0][:2] == ("POST", "/fee_schedules")
    assert client.calls[0][2]["json"] == {
        "data": [
            {
                "type": "fee_schedules",
                "attributes": before,
                "relationships": {"fees": {"data": [{"id": "1", "type": "fees"}]}},
            }
        ]
    }
    assert attributes == before


@pytest.mark.parametrize("method", ["create_fees", "replace_fees"])
def test_fee_bulk_limit_rejects_501_without_sending(method):
    client = FakeClient()
    fees = [{"id": str(index), "attributes": {"name": "Fee"}} for index in range(501)]
    before = deepcopy(fees)
    with pytest.raises(ValueError, match="500"):
        getattr(FeesResource(client), method)(fees)
    assert client.calls == []
    assert fees == before


@pytest.mark.parametrize(
    "method,http", [("create_fees", "POST"), ("replace_fees", "PUT")]
)
def test_fee_bulk_limit_allows_exactly_500(method, http):
    client = FakeClient({"data": []})
    fees = [
        {"id": str(index), "attributes": {"future_field": None}} for index in range(500)
    ]
    before = deepcopy(fees)
    assert getattr(FeesResource(client), method)(fees) == []
    assert client.calls[0][:2] == (http, "/fees")
    assert len(client.calls[0][2]["json"]["data"]) == 500
    assert fees == before


@pytest.mark.parametrize(
    "method", ["create_fee", "replace_fee", "create_fees", "replace_fees"]
)
def test_fee_schedule_relationship_writes_are_rejected_before_request(method):
    client = FakeClient()
    api = FeesResource(client)
    relationships = {"fee_schedules": {"data": [{"type": "fee_schedules", "id": "1"}]}}
    before = deepcopy(relationships)
    with pytest.raises(ValueError, match="read-only"):
        if method == "create_fee":
            api.create_fee({"name": "Fee"}, relationships=relationships)
        elif method == "replace_fee":
            api.replace_fee("1", {"name": "Fee"}, relationships=relationships)
        else:
            getattr(api, method)(
                [{"id": "1", "attributes": {}, "relationships": relationships}]
            )
    assert client.calls == []
    assert relationships == before


@pytest.mark.parametrize("bulk", [False, True])
def test_rate_asset_valuation_is_rejected_on_creation_only(bulk):
    client = FakeClient()
    api = FeesResource(client)
    attributes = {"name": "Fee", "rate_asset_valuation": "BILLABLE_ASSETS"}
    with pytest.raises(ValueError, match="rate_asset_valuation"):
        if bulk:
            api.create_fees([{"attributes": attributes}])
        else:
            api.create_fee(attributes)
    assert client.calls == []
    result = {"id": "1", "type": "fees"}
    client.documents.append({"data": [result]})
    assert api.replace_fee("1", attributes) == result
    assert client.calls[0][2]["json"]["data"]["attributes"] == attributes


@pytest.mark.parametrize(
    "method,args",
    [
        ("create_fee_schedule", ({"name": "Quarterly"}, [])),
        ("replace_fee_schedule", ("1", {"name": "Quarterly"}, [])),
        ("add_fees", ("1", [])),
        ("replace_fees", ("1", [])),
    ],
)
def test_schedule_single_mutations_require_fees(method, args):
    client = FakeClient()
    with pytest.raises(ValueError, match="fee association"):
        getattr(FeeSchedulesResource(client), method)(*args)
    assert client.calls == []


@pytest.mark.parametrize("method", ["create_fee_schedules", "replace_fee_schedules"])
@pytest.mark.parametrize(
    "relationships",
    [None, {}, {"fees": {"data": []}}, {"fees": {"data": [{"type": "fees"}]}}],
)
def test_schedule_bulk_mutations_require_fee_associations(method, relationships):
    client = FakeClient()
    resource = {"id": "1", "attributes": {"name": "Quarterly"}}
    if relationships is not None:
        resource["relationships"] = relationships
    before = deepcopy(resource)
    with pytest.raises(ValueError, match="fee association|Fee associations"):
        getattr(FeeSchedulesResource(client), method)([resource])
    assert client.calls == []
    assert resource == before


@pytest.mark.parametrize(
    "method,http", [("create_fee_schedules", "POST"), ("replace_fee_schedules", "PUT")]
)
def test_bulk_schedules_preserve_unknown_fields_and_caller_inputs(method, http):
    resources = [
        {
            "id": "1",
            "attributes": {"name": "Quarterly", "future_option": False},
            "relationships": {"fees": {"data": [{"id": "9", "type": "fees"}]}},
        }
    ]
    before = deepcopy(resources)
    client = FakeClient({"data": [{"id": "1"}]})
    assert getattr(FeeSchedulesResource(client), method)(resources) == [{"id": "1"}]
    assert client.calls[0][:2] == (http, "/fee_schedules")
    assert (
        client.calls[0][2]["json"]["data"][0]["attributes"] == before[0]["attributes"]
    )
    assert resources == before
