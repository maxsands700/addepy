"""Fees and fee schedules. Replacement methods use PUT, including relationships.

Single methods return resource dictionaries; bulk methods return lists. Attribute
and relationship mappings are passed through so new server fields remain usable.
"""

from copy import deepcopy
from typing import Any, Dict, Generator, List, Mapping, Optional, Sequence

from ...constants import DEFAULT_LIST_LIMIT, DEFAULT_PAGE_LIMIT
from ..base import BaseResource


def _resource(
    kind: str,
    attributes: Mapping[str, Any],
    resource_id: Optional[str] = None,
    relationships: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    data: Dict[str, Any] = {"type": kind, "attributes": deepcopy(dict(attributes))}
    if resource_id is not None:
        data["id"] = str(resource_id)
    if relationships is not None:
        data["relationships"] = deepcopy(dict(relationships))
    return data


def _single_data(response: Any) -> Dict[str, Any]:
    """Billing may return a one-item array even for a single-resource request."""
    data = response.json()["data"]
    if isinstance(data, list):
        if len(data) != 1:
            raise ValueError("Expected one resource in the billing response")
        return data[0]
    return data


def _bulk_data(
    resources: Sequence[Mapping[str, Any]],
    kind: str,
    *,
    require_id: bool = False,
    max_items: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Copy complete JSON:API resources, allowing the type to be omitted."""
    if not resources:
        raise ValueError("At least one resource is required")
    if max_items is not None and len(resources) > max_items:
        raise ValueError(f"At most {max_items} resources are allowed per request")
    result = deepcopy([dict(item) for item in resources])
    for item in result:
        if item.setdefault("type", kind) != kind:
            raise ValueError(f"Resource type must be {kind!r}")
        if require_id and "id" not in item:
            raise ValueError("Each resource must include an id")
    return result


class FeesResource(BaseResource):
    """Manage /fees; server validates the fee structure and required fields."""

    def get_fee(self, fee_id: str) -> Dict[str, Any]:
        return _single_data(self._get(f"/fees/{fee_id}"))

    def iter_fees(
        self, *, limit: Optional[int] = None, page_limit: int = DEFAULT_PAGE_LIMIT
    ) -> Generator[Dict[str, Any], None, None]:
        return self._paginate("/fees", page_limit=min(page_limit, 500), max_items=limit)

    def list_fees(
        self, *, limit: int = DEFAULT_LIST_LIMIT, page_limit: int = DEFAULT_PAGE_LIMIT
    ) -> List[Dict[str, Any]]:
        return list(self.iter_fees(limit=limit, page_limit=page_limit))

    def create_fee(
        self,
        attributes: Mapping[str, Any],
        *,
        relationships: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create one fee; the API requires an array for fee creation."""
        return _single_data(
            self._post(
                "/fees",
                json={
                    "data": [_resource("fees", attributes, relationships=relationships)]
                },
            )
        )

    def create_fees(self, fees: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
        """Create JSON:API resource objects with attributes and optional relationships."""
        return self._post("/fees", json={"data": _bulk_data(fees, "fees")}).json()[
            "data"
        ]

    def replace_fee(
        self,
        fee_id: str,
        attributes: Mapping[str, Any],
        *,
        relationships: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Fully replace a fee, including relationships; omitted fields are not retained."""
        return _single_data(
            self._put(
                f"/fees/{fee_id}",
                json={"data": _resource("fees", attributes, fee_id, relationships)},
            )
        )

    def replace_fees(self, fees: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
        """Fully replace up to 500 complete resource objects, each including its id."""
        return self._put(
            "/fees",
            json={"data": _bulk_data(fees, "fees", require_id=True, max_items=500)},
        ).json()["data"]

    def delete_fee(self, fee_id: str) -> None:
        self._delete(f"/fees/{fee_id}")

    def delete_fees(self, fee_ids: Sequence[str]) -> None:
        self._delete(
            "/fees",
            json={
                "data": _bulk_data([{"id": str(value)} for value in fee_ids], "fees")
            },
        )

    def get_fee_schedules(self, fee_id: str) -> List[Dict[str, Any]]:
        return self._get(f"/fees/{fee_id}/fee_schedules").json()["data"]

    def get_fee_schedule_relationships(self, fee_id: str) -> List[Dict[str, Any]]:
        return self._get(f"/fees/{fee_id}/relationships/fee_schedules").json()["data"]


class FeeSchedulesResource(BaseResource):
    """Manage /fee_schedules and their fee relationships."""

    def get_fee_schedule(self, schedule_id: str) -> Dict[str, Any]:
        return _single_data(self._get(f"/fee_schedules/{schedule_id}"))

    def iter_fee_schedules(
        self, *, limit: Optional[int] = None, page_limit: int = DEFAULT_PAGE_LIMIT
    ) -> Generator[Dict[str, Any], None, None]:
        return self._paginate(
            "/fee_schedules", page_limit=min(page_limit, 500), max_items=limit
        )

    def list_fee_schedules(
        self, *, limit: int = DEFAULT_LIST_LIMIT, page_limit: int = DEFAULT_PAGE_LIMIT
    ) -> List[Dict[str, Any]]:
        return list(self.iter_fee_schedules(limit=limit, page_limit=page_limit))

    @staticmethod
    def _fees(fee_ids: Sequence[str]) -> Dict[str, Any]:
        return {
            "fees": {"data": [{"type": "fees", "id": str(value)} for value in fee_ids]}
        }

    def create_fee_schedule(
        self, attributes: Mapping[str, Any], fee_ids: Sequence[str]
    ) -> Dict[str, Any]:
        """Create a schedule with its required fee associations."""
        return _single_data(
            self._post(
                "/fee_schedules",
                json={
                    "data": _resource(
                        "fee_schedules", attributes, relationships=self._fees(fee_ids)
                    )
                },
            )
        )

    def create_fee_schedules(
        self, schedules: Sequence[Mapping[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create complete JSON:API resources, including attributes and fee relationships."""
        return self._post(
            "/fee_schedules", json={"data": _bulk_data(schedules, "fee_schedules")}
        ).json()["data"]

    def replace_fee_schedule(
        self, schedule_id: str, attributes: Mapping[str, Any], fee_ids: Sequence[str]
    ) -> Dict[str, Any]:
        """PUT all attributes and fee associations; this is a full replacement."""
        return _single_data(
            self._put(
                f"/fee_schedules/{schedule_id}",
                json={
                    "data": _resource(
                        "fee_schedules", attributes, schedule_id, self._fees(fee_ids)
                    )
                },
            )
        )

    def replace_fee_schedules(
        self, schedules: Sequence[Mapping[str, Any]]
    ) -> List[Dict[str, Any]]:
        """PUT complete JSON:API resources with id, attributes and fee relationships."""
        return self._put(
            "/fee_schedules",
            json={"data": _bulk_data(schedules, "fee_schedules", require_id=True)},
        ).json()["data"]

    def delete_fee_schedule(self, schedule_id: str) -> None:
        self._delete(f"/fee_schedules/{schedule_id}")

    def delete_fee_schedules(self, schedule_ids: Sequence[str]) -> None:
        self._delete(
            "/fee_schedules",
            json={
                "data": _bulk_data(
                    [{"id": str(value)} for value in schedule_ids], "fee_schedules"
                )
            },
        )

    def get_fees(self, schedule_id: str) -> List[Dict[str, Any]]:
        return self._get(f"/fee_schedules/{schedule_id}/fees").json()["data"]

    def get_fee_relationships(self, schedule_id: str) -> List[Dict[str, Any]]:
        return self._get(f"/fee_schedules/{schedule_id}/relationships/fees").json()[
            "data"
        ]

    def add_fees(self, schedule_id: str, fee_ids: Sequence[str]) -> None:
        self._post(
            f"/fee_schedules/{schedule_id}/relationships/fees",
            json=self._fees(fee_ids)["fees"],
        )

    def replace_fees(self, schedule_id: str, fee_ids: Sequence[str]) -> None:
        self._put(
            f"/fee_schedules/{schedule_id}/relationships/fees",
            json=self._fees(fee_ids)["fees"],
        )

    def remove_fees(self, schedule_id: str) -> None:
        """Remove all fee associations, as specified by this endpoint."""
        self._delete(f"/fee_schedules/{schedule_id}/relationships/fees")
