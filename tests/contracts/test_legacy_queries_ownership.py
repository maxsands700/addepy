"""Representative offline contracts from the linked ownership and query guides.

Fixtures exercise documented wire shapes, not an available Addepar tenant.
Documentation sources and known ambiguities are in API_NOTES_INVESTMENT.md.
"""

from copy import deepcopy
import json

import pytest
import requests

from addepy.exceptions import ValidationError
from addepy.resources.ownership.external_ids import ExternalIdsResource
from addepy.resources.ownership.groups import GroupsResource
from addepy.resources.ownership.positions import PositionsResource
from addepy.resources.portfolio.analysis import AnalysisResource
from addepy.resources.portfolio.transactions import TransactionsResource


class FakeClient:
    def __init__(self, *documents):
        self.documents = list(documents)
        self.calls = []

    def _request(self, method, endpoint, **kwargs):
        self.calls.append((method, endpoint, deepcopy(kwargs)))
        assert self.documents, "Unexpected extra request"
        document = self.documents.pop(0)
        if isinstance(document, requests.Response):
            return document
        response = requests.Response()
        response.status_code = 204 if document is None else 200
        response._content = b"" if document is None else json.dumps(document).encode()
        return response


GROUP = {"id": "100", "type": "groups", "attributes": {"name": "Smith Family"}}
POSITION = {
    "id": "338",
    "type": "positions",
    "relationships": {
        "owner": {"data": {"type": "entities", "id": "27"}},
        "owned": {"data": {"type": "entities", "id": "29"}},
    },
}
PORTFOLIO_RESULT = {
    "meta": {
        "columns": [{"key": "value", "display_name": "Value (USD)"}],
        "groupings": [{"key": "asset_class"}],
    },
    "data": {
        "type": "portfolio_views",
        "attributes": {
            "total": {
                "name": "Total",
                "columns": {"value": 100.0},
                "children": [],
            }
        },
    },
    "included": [],
}
TRANSACTION_RESULT = {
    "meta": {"columns": ["trade_date", "value"]},
    "data": [
        {
            "id": "7",
            "type": "transaction_query",
            "attributes": {"trade_date": "2024-01-15", "value": None},
        }
    ],
    "links": {"next": None},
}


def test_group_filters_are_preserved_across_documented_cursor_links():
    client = FakeClient(
        {"data": [GROUP], "links": {"next": "/v1/groups?page[cursor]=abc123"}},
        {"data": [], "links": {"next": None}},
    )
    result = GroupsResource(client).list_groups(
        group_types="HH_GROUPS",
        ids="100,101",
        created_after="2024-01-01",
        modified_before="2024-06-30",
        page_limit=25,
    )
    assert result == [GROUP]
    assert client.calls[0][:2] == ("GET", "/groups")
    expected = {
        "filter[group_types]": "HH_GROUPS",
        "filter[ids]": "100,101",
        "filter[created_after]": "2024-01-01",
        "filter[modified_before]": "2024-06-30",
        "page[limit]": 25,
    }
    assert client.calls[0][2]["params"] == expected
    assert client.calls[1][2]["params"] == {**expected, "page[cursor]": "abc123"}


def test_single_group_creation_preserves_custom_attributes_and_entity_members():
    client = FakeClient({"data": GROUP})
    attributes = {
        "external_id_salesforce": "sf_123",
        "_custom_label": [{"value": "Family"}],
    }
    before = deepcopy(attributes)
    assert (
        GroupsResource(client).create_group(
            "Smith Family",
            "HH_GROUPS",
            member_ids=["200", "204"],
            attributes=attributes,
        )
        == GROUP
    )
    assert client.calls[0][:2] == ("POST", "/groups")
    assert client.calls[0][2]["json"] == {
        "data": {
            "type": "groups",
            "attributes": {"name": "Smith Family", **before},
            "relationships": {
                "group_type": {"data": {"type": "group_types", "id": "HH_GROUPS"}},
                "members": {
                    "data": [
                        {"type": "entities", "id": "200"},
                        {"type": "entities", "id": "204"},
                    ]
                },
            },
        }
    }
    assert attributes == before


def test_bulk_group_patch_can_clear_both_relationships_and_remove_attribute_values():
    updates = [
        {
            "id": "100",
            "attributes": {"external_id_salesforce": None},
            "member_ids": [],
            "child_group_ids": [],
        }
    ]
    before = deepcopy(updates)
    client = FakeClient({"data": [GROUP]})
    assert GroupsResource(client).update_groups(updates) == [GROUP]
    assert client.calls[0][:2] == ("PATCH", "/groups")
    assert client.calls[0][2]["json"] == {
        "data": [
            {
                "id": "100",
                "type": "groups",
                "attributes": {"external_id_salesforce": None},
                "relationships": {
                    "members": {"data": []},
                    "child_groups": {"data": []},
                },
            }
        ]
    }
    assert updates == before


def test_group_search_uses_external_id_type_key_from_group_search_contract():
    external_ids = [{"external_id_type": "salesforce", "external_id": "sf_12345"}]
    client = FakeClient({"data": [GROUP]})
    assert GroupsResource(client).search_groups(
        display_names=["Smith Family"],
        group_types=["HH_GROUPS"],
        external_ids=external_ids,
    ) == [GROUP]
    assert client.calls[0][:2] == ("POST", "/groups/query")
    assert client.calls[0][2]["json"] == {
        "data": {
            "type": "group_search",
            "attributes": {
                "display_names": ["Smith Family"],
                "group_types": ["HH_GROUPS"],
                "external_ids": external_ids,
            },
        }
    }


@pytest.mark.parametrize(
    "method,verb,relationship,resource_type",
    [
        ("add_members", "POST", "members", "entities"),
        ("replace_members", "PATCH", "members", "entities"),
        ("remove_members", "DELETE", "members", "entities"),
        ("add_child_groups", "POST", "child_groups", "groups"),
        ("replace_child_groups", "PATCH", "child_groups", "groups"),
    ],
)
def test_group_relationship_writes_use_linkage_and_accept_204(
    method, verb, relationship, resource_type
):
    client = FakeClient(None)
    assert getattr(GroupsResource(client), method)("100", ["200"]) is None
    assert client.calls[0][:2] == (verb, f"/groups/100/relationships/{relationship}")
    assert client.calls[0][2]["json"] == {
        "data": [{"type": resource_type, "id": "200"}]
    }


def test_group_member_linkage_is_distinct_from_paginated_entity_details():
    linkage = {"type": "entities", "id": "200"}
    entity = {**linkage, "attributes": {"original_name": "Client"}}
    client = FakeClient(
        {"data": [linkage]}, {"data": [entity], "links": {"next": None}}
    )
    resource = GroupsResource(client)
    assert resource.get_members("100") == [linkage]
    assert resource.get_member_details("100") == [entity]
    assert [call[1] for call in client.calls] == [
        "/groups/100/relationships/members",
        "/groups/100/members",
    ]


def test_group_type_false_permission_filter_is_sent_without_pagination():
    group_type = {
        "id": "HH_GROUPS",
        "type": "group_types",
        "attributes": {"is_permissioned_resource": False},
    }
    client = FakeClient({"data": [group_type]})
    assert GroupsResource(client).list_group_types(is_permissioned_resource=False) == [
        group_type
    ]
    assert client.calls[0][:2] == ("GET", "/group_types")
    assert client.calls[0][2]["params"] == {"is_permissioned_resource": "false"}


def test_position_filters_and_empty_fieldset_follow_documented_parameter_names():
    client = FakeClient({"data": [POSITION], "links": {"next": None}})
    assert PositionsResource(client).list_positions(
        fields=[],
        owner_model_types=["PERSON_NODE", "TRUST"],
        owned_model_types=["STOCK", "BOND"],
        owner_entity_id=["24", "26"],
        owned_entity_id=["23", "25"],
        modified_after="2024-01-01",
        page_limit=25,
    ) == [POSITION]
    assert client.calls[0][2]["params"] == {
        "fields[positions]": "[]",
        "filter[owner_model_types]": "PERSON_NODE,TRUST",
        "filter[owned_model_types]": "STOCK,BOND",
        "filter[owner_entity_id]": "24,26",
        "filter[owned_entity_id]": "23,25",
        "filter[modified_after]": "2024-01-01",
        "page[limit]": 25,
    }


def test_single_position_create_can_have_empty_attributes():
    client = FakeClient({"data": POSITION})
    assert PositionsResource(client).create_position("27", "29") == POSITION
    assert client.calls[0][:2] == ("POST", "/positions")
    assert client.calls[0][2]["json"] == {
        "data": {
            "type": "positions",
            "attributes": {},
            "relationships": POSITION["relationships"],
        }
    }


def test_bulk_position_create_retains_zero_percentage_and_additional_attributes():
    positions = [
        {
            "owner_id": "27",
            "owned_id": "29",
            "incepting_open_position_date": "2024-01-01",
            "incepting_open_position_ownership_percentage": 0.0,
            "attributes": {
                "incepting_open_position_value": 5,
                "_custom_status": [{"value": "Open"}],
            },
        }
    ]
    before = deepcopy(positions)
    client = FakeClient({"data": [POSITION]})
    assert PositionsResource(client).create_positions(positions) == [POSITION]
    assert positions == before
    assert client.calls[0][2]["json"] == {
        "data": [
            {
                "type": "positions",
                "relationships": POSITION["relationships"],
                "attributes": {
                    "incepting_open_position_date": "2024-01-01",
                    "incepting_open_position_ownership_percentage": 0.0,
                    "incepting_open_position_value": 5,
                    "_custom_status": [{"value": "Open"}],
                },
            }
        ]
    }


def test_bulk_position_patch_preserves_null_values_and_input_ids():
    updates = [{"id": "338", "display_name": None, "incepting_open_position_value": 5}]
    before = deepcopy(updates)
    client = FakeClient({"data": [POSITION]})
    assert PositionsResource(client).update_positions(updates) == [POSITION]
    assert updates == before
    assert client.calls[0][:2] == ("PATCH", "/positions")
    assert client.calls[0][2]["json"] == {
        "data": [
            {
                "id": "338",
                "type": "positions",
                "attributes": {
                    "display_name": None,
                    "incepting_open_position_value": 5,
                },
            }
        ]
    }


@pytest.mark.parametrize(
    "method,suffix",
    [
        ("get_position_owner", "owner"),
        ("get_position_owned", "owned"),
        ("get_position_owner_relationship", "relationships/owner"),
        ("get_position_owned_relationship", "relationships/owned"),
    ],
)
def test_position_relationship_routes_unwrap_data(method, suffix):
    entity = {"type": "entities", "id": "27"}
    client = FakeClient({"data": entity})
    assert getattr(PositionsResource(client), method)("338") == entity
    assert client.calls[0][:2] == ("GET", f"/positions/338/{suffix}")


@pytest.mark.parametrize(
    "resource_class,method,resource_type,path",
    [
        (GroupsResource, "delete_groups", "groups", "/groups"),
        (PositionsResource, "delete_positions", "positions", "/positions"),
    ],
)
def test_bulk_ownership_delete_uses_typed_identifier_array(
    resource_class, method, resource_type, path
):
    client = FakeClient(None)
    assert getattr(resource_class(client), method)(["100", "101"]) is None
    assert client.calls[0][:2] == ("DELETE", path)
    assert client.calls[0][2]["json"] == {
        "data": [
            {"type": resource_type, "id": "100"},
            {"type": resource_type, "id": "101"},
        ]
    }


def test_external_id_type_crud_uses_key_as_id_and_only_display_name_on_update():
    item = {
        "id": "dynamics",
        "type": "external_id_types",
        "attributes": {"external_type_key": "dynamics", "display_name": "Dynamics"},
    }
    client = FakeClient(
        {"data": [item]}, {"data": item}, {"data": item}, {"data": item}, None
    )
    resource = ExternalIdsResource(client)
    assert resource.list_external_id_types() == [item]
    assert resource.get_external_id_type("dynamics") == item
    assert resource.create_external_id_type("dynamics", "Dynamics") == item
    assert resource.update_external_id_type("dynamics", "Microsoft Dynamics") == item
    assert resource.delete_external_id_type("dynamics") is None
    assert [(method, endpoint) for method, endpoint, _ in client.calls] == [
        ("GET", "/external_id_types"),
        ("GET", "/external_id_types/dynamics"),
        ("POST", "/external_id_types"),
        ("PATCH", "/external_id_types/dynamics"),
        ("DELETE", "/external_id_types/dynamics"),
    ]
    assert client.calls[0][2]["params"] is None
    assert client.calls[2][2]["json"] == {
        "data": {
            "type": "external_id_types",
            "attributes": item["attributes"],
        }
    }
    assert client.calls[3][2]["json"] == {
        "data": {
            "id": "dynamics",
            "type": "external_id_types",
            "attributes": {"display_name": "Microsoft Dynamics"},
        }
    }


@pytest.mark.parametrize(
    "resource_class,query_type,path,result",
    [
        (AnalysisResource, "portfolio_query", "/portfolio/query", PORTFOLIO_RESULT),
        (
            TransactionsResource,
            "transaction_query",
            "/transactions/query",
            TRANSACTION_RESULT,
        ),
    ],
)
@pytest.mark.parametrize("form", ["parameters", "envelope", "text"])
def test_raw_sync_queries_preserve_copied_fields_and_complete_response(
    resource_class, query_type, path, result, form
):
    parameters = {
        "columns": [{"key": "value"}] if query_type == "portfolio_query" else ["value"],
        "portfolio_type": "ENTITY",
        "external_ids": [{"external_type_key": "crm", "external_id": "client-1"}],
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "filters": [],
        "future_option": {"enabled": False, "value": None},
    }
    if query_type == "portfolio_query":
        parameters["groupings"] = ["asset_class"]
    envelope = {"data": {"type": query_type, "attributes": parameters}}
    query = (
        parameters
        if form == "parameters"
        else envelope
        if form == "envelope"
        else json.dumps(envelope)
    )
    before = deepcopy(query)
    client = FakeClient(result)
    assert resource_class(client).query_raw(query) == result
    assert query == before
    assert client.calls[0][:2] == ("POST", path)
    assert client.calls[0][2]["json"] == envelope
    assert "portfolio_id" not in client.calls[0][2]["json"]["data"]["attributes"]


@pytest.mark.parametrize("resource_class", [AnalysisResource, TransactionsResource])
@pytest.mark.parametrize("query", ["not JSON", {"data": []}])
def test_raw_sync_queries_reject_malformed_envelopes_before_sending(
    resource_class, query
):
    client = FakeClient()
    with pytest.raises(ValidationError):
        resource_class(client).query_raw(query)
    assert not client.calls


def test_portfolio_query_helper_keeps_argument_filters_false_flags_and_metadata():
    columns = [{"key": "value", "arguments": {"currency": "USD"}}]
    filters = [
        {
            "attribute": "value",
            "type": "number",
            "operator": "range",
            "ranges": [{"from": 0, "to": 100}],
        }
    ]
    client = FakeClient(PORTFOLIO_RESULT)
    result = AnalysisResource(client).query(
        columns,
        ["asset_class"],
        "entity",
        [329263],
        "2024-01-01",
        "2024-06-30",
        filters=filters,
        hide_previous_holdings=False,
        look_through_constituent_holdings={"type": "top", "threshold": 10},
    )
    assert result == PORTFOLIO_RESULT
    assert client.calls[0][2]["json"] == {
        "data": {
            "type": "portfolio_query",
            "attributes": {
                "columns": columns,
                "groupings": ["asset_class"],
                "portfolio_type": "ENTITY",
                "portfolio_id": [329263],
                "start_date": "2024-01-01",
                "end_date": "2024-06-30",
                "filters": filters,
                "hide_previous_holdings": False,
                "look_through_constituent_holdings": {"type": "top", "threshold": 10},
            },
        }
    }


def test_transaction_query_helper_preserves_date_filters_and_documented_sorting_example():
    filters = [
        {
            "attribute": "trade_date",
            "operator": "include",
            "type": "date",
            "period": {
                "type": "static_time_period",
                "start": "2024-01-01",
                "end": "2024-06-30",
            },
        }
    ]
    sorting = [{"attribute": "trade_date", "ascending": False}]
    client = FakeClient(TRANSACTION_RESULT)
    result = TransactionsResource(client).query_transactions(
        ["trade_date", "value"],
        "entity",
        "123",
        "2024-01-01",
        "2024-06-30",
        filters=filters,
        sorting=sorting,
        limit=10,
        include_deleted=True,
    )
    assert result == TRANSACTION_RESULT
    assert client.calls[0][2]["json"] == {
        "data": {
            "type": "transaction_query",
            "attributes": {
                "columns": ["trade_date", "value"],
                "portfolio_type": "ENTITY",
                "portfolio_id": ["123"],
                "start_date": "2024-01-01",
                "end_date": "2024-06-30",
                "filters": filters,
                "sorting": sorting,
                "limit": 10,
                "include_online_valuations": False,
                "include_unverified": False,
                "include_deleted": True,
            },
        }
    }


def test_saved_portfolio_view_definition_keeps_reusable_query_parameters():
    view = {
        "id": "19",
        "type": "portfolio_views",
        "attributes": {
            "display_name": "Value",
            "parameters": {"columns": [{"key": "value"}], "groupings": ["asset_class"]},
        },
    }
    client = FakeClient({"data": [view]}, {"data": view})
    resource = AnalysisResource(client)
    assert resource.list_views() == [view]
    assert resource.get_view("19") == view
    assert [call[:2] for call in client.calls] == [
        ("GET", "/portfolio/views"),
        ("GET", "/portfolio/views/19"),
    ]


def test_saved_portfolio_view_json_returns_full_analytics_envelope():
    client = FakeClient(PORTFOLIO_RESULT)
    result = AnalysisResource(client).get_view_results(
        "19", 10, "entity", "2024-01-01", "2024-06-30", "json"
    )
    assert result == PORTFOLIO_RESULT
    assert client.calls[0][:2] == ("GET", "/portfolio/views/19/results")
    assert client.calls[0][2]["params"] == {
        "portfolio_id": 10,
        "portfolio_type": "ENTITY",
        "output_type": "JSON",
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
    }


@pytest.mark.parametrize("output_type", ["CSV", "TSV", "XLSX"])
def test_saved_portfolio_view_file_formats_return_exact_bytes(output_type):
    response = requests.Response()
    response.status_code = 200
    response._content = b"\x00exact export bytes\xff"
    client = FakeClient(response)
    assert (
        AnalysisResource(client).get_view_results(
            "19", 10, "ENTITY", "2024-01-01", "2024-06-30", output_type
        )
        == response.content
    )
    assert client.calls[0][2]["params"]["output_type"] == output_type


def test_transaction_saved_view_keeps_response_return_type_for_compatibility():
    response = requests.Response()
    response.status_code = 200
    response._content = b"Trade Date,Value\n2024-01-15,100\n"
    client = FakeClient(response)
    result = TransactionsResource(client).get_view_results(
        "19", "10", "entity", "2024-01-01", "2024-06-30", "csv"
    )
    assert result is response
    assert client.calls[0][:2] == ("GET", "/transactions/views/19/results")
    assert client.calls[0][2]["params"]["output_type"] == "CSV"
