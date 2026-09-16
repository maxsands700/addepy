"""Recurring report schedules and their execution relationships."""

from copy import deepcopy
from typing import Any, Dict, Generator, List, Mapping, Optional

from ...constants import DEFAULT_LIST_LIMIT, DEFAULT_PAGE_LIMIT
from ..base import BaseResource
from .billing import _resource


class ReportSchedulesResource(BaseResource):
    """Manage /report_schedule. The resource type is plural: report_schedules.

    Attribute/filter dictionaries remain open so firm-specific options can pass
    through. Dates and scheduled times follow the firm's timezone, per the API.
    """

    def get_schedule(self, schedule_id: str) -> Dict[str, Any]:
        return self._get(f"/report_schedule/{schedule_id}").json()["data"]

    def iter_schedules(
        self,
        *,
        params: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        """Iterate schedules; params accepts API query parameter names verbatim."""
        return self._paginate(
            "/report_schedule", params=params, page_limit=page_limit, max_items=limit
        )

    def list_schedules(
        self,
        *,
        params: Optional[Dict[str, Any]] = None,
        limit: int = DEFAULT_LIST_LIMIT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        return list(
            self.iter_schedules(params=params, limit=limit, page_limit=page_limit)
        )

    def create_schedule(self, attributes: Mapping[str, Any]) -> Dict[str, Any]:
        """Create from report_id, portfolio_id, frequency, start_date, time and options."""
        return self._post(
            "/report_schedule", json={"data": _resource("report_schedules", attributes)}
        ).json()["data"]

    def update_schedule(
        self, schedule_id: str, attributes: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """PATCH only supplied attributes, including explicit nulls."""
        return self._patch(
            f"/report_schedule/{schedule_id}",
            json={"data": _resource("report_schedules", attributes, schedule_id)},
        ).json()["data"]

    def delete_schedule(self, schedule_id: str) -> None:
        self._delete(f"/report_schedule/{schedule_id}")

    def execute_schedule(
        self, schedule_id: str, payload: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """Execute with an explicit raw JSON:API request; return the entire response.

        The API reference does not define execution attributes or a concrete
        resource type. This method therefore forwards a caller-supplied payload.
        """
        return self._post(
            f"/report_schedule/{schedule_id}/execute", json=deepcopy(dict(payload))
        ).json()

    def iter_executions(
        self,
        schedule_id: str,
        *,
        limit: Optional[int] = None,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        """Yield execution relationship identifiers, not expanded job resources."""
        return self._paginate(
            f"/report_schedule/{schedule_id}/relationships/executions",
            page_limit=page_limit,
            max_items=limit,
        )

    def list_executions(
        self,
        schedule_id: str,
        *,
        limit: int = DEFAULT_LIST_LIMIT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        return list(
            self.iter_executions(schedule_id, limit=limit, page_limit=page_limit)
        )
