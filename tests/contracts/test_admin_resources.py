"""Offline contracts based on the Addepar billing/report guides, not live writes."""

from copy import deepcopy
import json

import pytest
import requests

from addepy.resources.admin import AdminNamespace
from addepy.resources.admin.billing import FeesResource, FeeSchedulesResource
from addepy.resources.admin.billable_portfolios import BillablePortfoliosResource
from addepy.resources.admin.files import FilesResource
from addepy.resources.admin.payouts import PayoutRecipientsResource, PayoutRulesResource
from addepy.resources.admin.report_schedules import ReportSchedulesResource
from addepy.resources.admin.reports import ReportsResource


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


def test_fee_creation_uses_array_and_preserves_unknown_fields():
    attributes = {
        "name": "Annual fee",
        "fee_structure": "FLAT",
        "flat_fee_amount": 2500,
        "asset_valuation": {"method": "ON_BILL_DATE"},
        "future_option": None,
    }
    before = deepcopy(attributes)
    resource = {"id": "1", "type": "fees"}
    client = FakeClient({"data": [resource]})
    assert FeesResource(client).create_fee(attributes) == resource
    assert client.calls[0][:2] == ("POST", "/fees")
    assert client.calls[0][2]["json"] == {
        "data": [{"type": "fees", "attributes": before}]
    }
    assert attributes == before


def test_fee_replacement_is_put_and_preserves_relationships():
    relationships = {"fee_schedules": {"data": [{"type": "fee_schedules", "id": "3"}]}}
    client = FakeClient({"data": [{"id": "1", "type": "fees"}]})
    FeesResource(client).replace_fee(
        "1", {"name": "Updated", "description": None}, relationships=relationships
    )
    assert client.calls[0][:2] == ("PUT", "/fees/1")
    assert client.calls[0][2]["json"] == {
        "data": {
            "id": "1",
            "type": "fees",
            "attributes": {"name": "Updated", "description": None},
            "relationships": relationships,
        }
    }


def test_fee_bulk_replacement_does_not_pop_input_ids():
    fees = [{"id": "1", "attributes": {"name": "New fee", "flat_fee_amount": 3000}}]
    before = deepcopy(fees)
    client = FakeClient({"data": [{"id": "1", "type": "fees"}]})
    assert FeesResource(client).replace_fees(fees) == [{"id": "1", "type": "fees"}]
    assert fees == before
    assert client.calls[0][:2] == ("PUT", "/fees")
    assert client.calls[0][2]["json"]["data"][0]["type"] == "fees"


@pytest.mark.parametrize(
    "fees",
    [
        [],
        [{"attributes": {}}],
        [{"id": "1", "type": "wrong"}],
        [{"id": str(i)} for i in range(501)],
    ],
)
def test_invalid_fee_bulk_request_is_not_sent(fees):
    client = FakeClient()
    with pytest.raises(ValueError):
        FeesResource(client).replace_fees(fees)
    assert client.calls == []


def test_schedule_replacement_sends_all_fee_associations():
    attributes = {
        "name": "Quarterly",
        "currency": "USD",
        "interval": "QUARTERLY",
        "timing": "IN_ADVANCE",
        "rounding": "NONE",
        "billing_period_cycle_start_month": 1,
    }
    client = FakeClient({"data": [{"id": "6", "type": "fee_schedules"}]})
    result = FeeSchedulesResource(client).replace_fee_schedule(
        "6", attributes, ["1", "2"]
    )
    assert result["id"] == "6"
    assert client.calls[0][:2] == ("PUT", "/fee_schedules/6")
    assert client.calls[0][2]["json"] == {
        "data": {
            "id": "6",
            "type": "fee_schedules",
            "attributes": attributes,
            "relationships": {
                "fees": {
                    "data": [{"type": "fees", "id": "1"}, {"type": "fees", "id": "2"}]
                }
            },
        }
    }


def test_fee_relationship_replace_and_remove_all_are_distinct():
    client = FakeClient()
    schedules = FeeSchedulesResource(client)
    schedules.add_fees("6", ["1"])
    schedules.replace_fees("6", ["2"])
    schedules.remove_fees("6")
    assert [call[0] for call in client.calls] == ["POST", "PUT", "DELETE"]
    assert all(
        call[1] == "/fee_schedules/6/relationships/fees" for call in client.calls
    )
    assert client.calls[1][2]["json"] == {"data": [{"type": "fees", "id": "2"}]}
    assert client.calls[2][2]["json"] is None


def test_billable_portfolio_legacy_scalar_id_and_new_payout_parameter():
    client = FakeClient({"id": 1234})
    result = BillablePortfoliosResource(client).create_billable_portfolio(
        "2", entity_id="1", payout_rule_id="3"
    )
    assert result == "1234"
    assert client.calls[0][2]["json"] == {
        "data": {
            "type": "create_billable_portfolio",
            "attributes": {"schedule_id": "2", "entity_id": "1", "payout_rule_id": "3"},
        }
    }


def test_billable_portfolio_bulk_create_and_restore_have_distinct_shapes():
    client = FakeClient({"data": [{"id": "1001", "type": "billable_portfolios"}]})
    portfolios = BillablePortfoliosResource(client)
    assert (
        portfolios.create_billable_portfolios([{"entity_id": 1, "schedule_id": 2}])[0][
            "id"
        ]
        == "1001"
    )
    portfolios.update_fee_schedules({"1001": "7"})
    assert client.calls[0][:2] == ("POST", "/billable_portfolios")
    assert client.calls[0][2]["json"] == {
        "data": [
            {
                "type": "create_billable_portfolio",
                "attributes": {"entity_id": 1, "schedule_id": 2},
            }
        ]
    }
    assert client.calls[1][:2] == (
        "PATCH",
        "/billable_portfolios/relationships/fee_schedules",
    )
    assert client.calls[1][2]["json"] == {
        "data": [
            {
                "id": "1001",
                "type": "create_billable_portfolio",
                "attributes": {"schedule_id": "7"},
            }
        ]
    }


def test_billable_portfolio_archive_and_payout_relationships():
    client = FakeClient()
    portfolios = BillablePortfoliosResource(client)
    portfolios.archive_billable_portfolios(["2", "5"])
    portfolios.update_payout_rule("2", "3")
    portfolios.remove_payout_rule("2")
    assert client.calls[0][:2] == (
        "DELETE",
        "/billable_portfolios/relationships/fee_schedules",
    )
    assert client.calls[0][2]["json"] == {
        "data": [
            {"id": "2", "type": "billable_portfolios"},
            {"id": "5", "type": "billable_portfolios"},
        ]
    }
    assert client.calls[1][:2] == (
        "PATCH",
        "/billable_portfolios/2/relationships/payout_rule",
    )
    assert client.calls[1][2]["json"] == {"data": {"id": "3", "type": "payout_rule"}}
    assert client.calls[2][:2] == (
        "DELETE",
        "/billable_portfolios/2/relationships/payout_rule",
    )


@pytest.mark.parametrize("attributes", [{}, {"entity_id": 1, "group_id": 2}])
def test_bulk_portfolios_reject_ambiguous_owners(attributes):
    client = FakeClient()
    with pytest.raises(ValueError):
        BillablePortfoliosResource(client).create_billable_portfolios([attributes])
    assert client.calls == []


def test_payout_pagination_uses_plain_offset_and_repeated_recipient_filters():
    client = FakeClient(
        {
            "data": [{"id": "1", "type": "payout_rule"}],
            "meta": {"page": {"total": 2, "cursor": 0}},
        },
        {
            "data": [{"id": "2", "type": "payout_rule"}],
            "meta": {"page": {"total": 2, "cursor": 1}},
        },
    )
    assert [
        item["id"]
        for item in PayoutRulesResource(client).iter_payout_rules(
            search="a", recipient_ids=["10", "11"], page_limit=500
        )
    ] == ["1", "2"]
    assert client.calls[0][2]["params"] == {
        "search": "a",
        "recipient_ids": ["10", "11"],
        "offset": 0,
        "limit": 500,
    }
    assert client.calls[1][2]["params"]["offset"] == 1
    assert (
        len(client.calls) == 2
    )  # A server-imposed smaller page must not truncate the result.


def test_payout_zero_limit_and_invalid_paging_do_not_make_requests():
    client = FakeClient()
    recipients = PayoutRecipientsResource(client)
    assert list(recipients.iter_payout_recipients(limit=0)) == []
    with pytest.raises(ValueError):
        list(recipients.iter_payout_recipients(page_limit=0))
    assert client.calls == []


def test_payout_repeated_page_cannot_loop_forever():
    page = {"data": [{"id": "1", "type": "payout_recipient"}]}
    client = FakeClient(page, page)
    with pytest.raises(ValueError, match="repeated page"):
        list(PayoutRecipientsResource(client).iter_payout_recipients())


def test_payout_recipient_put_matches_documented_body():
    resource = {
        "id": "1",
        "type": "payout_recipient",
        "attributes": {"name": "Jane", "type": "Advisor"},
    }
    client = FakeClient({"data": resource})
    assert (
        PayoutRecipientsResource(client).replace_payout_recipient(
            "1", resource["attributes"]
        )
        == resource
    )
    assert client.calls[0][:2] == ("PUT", "/billing/payout/recipients/1")
    assert client.calls[0][2]["json"] == {
        "data": {"type": "payout_recipient", "attributes": resource["attributes"]}
    }


def test_payout_replacement_retains_nested_splits_without_mutation():
    attributes = {
        "name": "Jack",
        "splits": [
            {
                "recipient": {"id": "10"},
                "distribution_type": "PERCENTAGE",
                "distribution_amount": 100.0,
                "children": [],
            }
        ],
    }
    before = deepcopy(attributes)
    client = FakeClient(
        {"data": {"id": "1", "type": "payout_rule", "attributes": attributes}}
    )
    result = PayoutRulesResource(client).replace_payout_rule("1", attributes)
    assert result["attributes"] == before
    assert client.calls[0][:2] == ("PUT", "/billing/payout/rules/1")
    assert client.calls[0][2]["json"] == {
        "data": {"id": "1", "type": "payout_rule", "attributes": before}
    }
    assert attributes == before


@pytest.mark.parametrize(
    "factory,method,endpoint,kind",
    [
        (FeesResource, "delete_fees", "/fees", "fees"),
        (
            FeeSchedulesResource,
            "delete_fee_schedules",
            "/fee_schedules",
            "fee_schedules",
        ),
        (
            PayoutRecipientsResource,
            "delete_payout_recipients",
            "/billing/payout/recipients",
            "payout_recipient",
        ),
        (
            PayoutRulesResource,
            "delete_payout_rules",
            "/billing/payout/rules",
            "payout_rule",
        ),
    ],
)
def test_bulk_delete_body_matches_resource_type(factory, method, endpoint, kind):
    client = FakeClient()
    assert getattr(factory(client), method)(["1", "2"]) is None
    assert client.calls[0][:2] == ("DELETE", endpoint)
    assert client.calls[0][2]["json"] == {
        "data": [{"type": kind, "id": "1"}, {"type": kind, "id": "2"}]
    }


def test_report_schedule_create_patch_and_raw_execution_contracts():
    attributes = {
        "report_id": 37,
        "portfolio_id": [56659],
        "frequency": "QUARTERLY",
        "start_date": "2026-10-01",
        "time": "09:00",
        "email_notification": "DO_NOT_NOTIFY",
    }
    response = {"id": "144", "type": "report_schedules", "attributes": attributes}
    client = FakeClient(
        {"data": response},
        {"data": response},
        {"data": {"id": "job-1"}, "meta": {"queued": True}},
    )
    schedules = ReportSchedulesResource(client)
    assert schedules.create_schedule(attributes) == response
    schedules.update_schedule("144", {"label": None})
    payload = {
        "data": {"type": "scheduled_job_execute", "attributes": {"custom_option": True}}
    }
    before = deepcopy(payload)
    result = schedules.execute_schedule("144", payload)
    assert client.calls[0][:2] == ("POST", "/report_schedule")
    assert client.calls[0][2]["json"] == {
        "data": {"type": "report_schedules", "attributes": attributes}
    }
    assert client.calls[1][:2] == ("PATCH", "/report_schedule/144")
    assert client.calls[1][2]["json"] == {
        "data": {"id": "144", "type": "report_schedules", "attributes": {"label": None}}
    }
    assert client.calls[2][:2] == ("POST", "/report_schedule/144/execute")
    assert client.calls[2][2]["json"] == before
    assert payload == before
    assert result["meta"]["queued"] is True


def test_report_executions_return_linkage_and_passthrough_filter_names():
    client = FakeClient(
        {"data": [{"type": "generated_reports", "id": "job-1"}]}, {"data": []}
    )
    schedules = ReportSchedulesResource(client)
    assert schedules.list_executions("144") == [
        {"type": "generated_reports", "id": "job-1"}
    ]
    assert schedules.list_schedules(params={"report_ids[]": [2, 4]}) == []
    assert client.calls[0][1] == "/report_schedule/144/relationships/executions"
    assert client.calls[1][2]["params"]["report_ids[]"] == [2, 4]


def test_report_generation_supports_brand_without_losing_legacy_options():
    client = FakeClient({"data": {"id": "job-1"}})
    ReportsResource(client).create_report_generation_job(
        "42",
        [{"portfolio_type": "entity", "portfolio_id": "22"}],
        "2026-01-01",
        "2026-03-31",
        label=[1, 2],
        brand_id="7",
        contact_notification="DO_NOT_NOTIFY",
    )
    attributes = client.calls[0][2]["json"]["data"]["attributes"]
    assert attributes["brand_id"] == "7"
    assert attributes["label"] == [1, 2]
    assert attributes["contact_notification"] == "DO_NOT_NOTIFY"


def test_admin_resources_are_discoverable_and_reuse_instances():
    admin = AdminNamespace(FakeClient())
    for name, factory in [
        ("fees", FeesResource),
        ("fee_schedules", FeeSchedulesResource),
        ("payout_recipients", PayoutRecipientsResource),
        ("payout_rules", PayoutRulesResource),
        ("report_schedules", ReportSchedulesResource),
    ]:
        assert isinstance(getattr(admin, name), factory)
        assert getattr(admin, name) is getattr(admin, name)


def test_file_upload_uses_shared_transport_and_multipart_metadata():
    client = FakeClient({"data": {"id": "10", "type": "files"}})
    result = FilesResource(client).upload_file(
        b"pdf data", "report.pdf", entity_ids=["22"]
    )
    assert result["id"] == "10"
    assert client.calls[0][:2] == ("POST", "/files")
    options = client.calls[0][2]
    assert options["headers"] == {"Content-Type": None}
    assert options["files"]["file"] == ("report.pdf", b"pdf data")
    assert json.loads(options["files"]["metadata"][1])["data"]["relationships"] == {
        "associated_entities": {"data": [{"type": "entities", "id": "22"}]}
    }


@pytest.mark.parametrize(
    "factory,method,endpoint",
    [
        (FilesResource, "download_file_to", "/files/42/download"),
        (FilesResource, "download_archived_file_to", "/archive/files/42/download"),
        (
            ReportsResource,
            "download_zipped_file_to",
            "/generated_reports/42/zipped_file/download",
        ),
    ],
)
def test_download_helpers_delegate_to_atomic_streaming(
    factory, method, endpoint, tmp_path
):
    class DownloadClient:
        def download(self, url, path, **kwargs):
            assert (url, path, kwargs) == (
                endpoint,
                tmp_path / "result",
                {"overwrite": False},
            )
            return path

    assert (
        getattr(factory(DownloadClient()), method)("42", tmp_path / "result")
        == tmp_path / "result"
    )
