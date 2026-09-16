"""Billable Portfolios resource for the Addepar API."""
import logging
from typing import Any, Dict, Generator, List, Mapping, Optional, Sequence

from ...constants import DEFAULT_LIST_LIMIT, DEFAULT_PAGE_LIMIT
from ..base import BaseResource
from .billing import _bulk_data, _resource

logger = logging.getLogger("addepy")


class BillablePortfoliosResource(BaseResource):
    """
    Resource for Addepar Billable Portfolios API.

    A billable portfolio is a portfolio (entity or group) associated with
    a fee schedule for billing purposes.

    Methods:
        - create_billable_portfolio() - Add a portfolio for billing
        - update_fee_schedule() - Update fee schedule or restore archived portfolio
        - archive_billable_portfolio() - Archive a billable portfolio
    """

    def create_billable_portfolio(
        self,
        schedule_id: str,
        *,
        entity_id: Optional[str] = None,
        group_id: Optional[str] = None,
        payout_rule_id: Optional[str] = None,
    ) -> str:
        """
        Add a portfolio for billing with a specified fee schedule.

        You must provide either entity_id OR group_id, but not both.

        Args:
            schedule_id: The ID of the fee schedule to associate.
            entity_id: The ID of the entity to set up for billing.
                Use this OR group_id, not both.
            group_id: The ID of the group to set up for billing.
                Use this OR entity_id, not both.
            payout_rule_id: Optional payout rule to associate.

        Returns:
            The ID of the created billable portfolio.

        Raises:
            ValueError: If both entity_id and group_id are provided,
                or if neither is provided.
        """
        if entity_id and group_id:
            raise ValueError("Provide either entity_id or group_id, not both")
        if not entity_id and not group_id:
            raise ValueError("Must provide either entity_id or group_id")

        attributes = {"schedule_id": schedule_id}
        if entity_id:
            attributes["entity_id"] = entity_id
        if group_id:
            attributes["group_id"] = group_id
        if payout_rule_id is not None:
            attributes["payout_rule_id"] = payout_rule_id

        payload = {
            "data": {
                "type": "create_billable_portfolio",
                "attributes": attributes,
            }
        }

        response = self._post("/billable_portfolios", json=payload)
        data = response.json()
        billable_portfolio_id = str(data.get("id", ""))
        logger.info(f"Created billable portfolio: {billable_portfolio_id}")
        return billable_portfolio_id

    def update_fee_schedule(
        self,
        billable_portfolio_id: str,
        fee_schedule_id: str,
    ) -> None:
        """
        Update a billable portfolio's fee schedule.

        This can also be used to restore an archived billable portfolio
        by assigning it a new fee schedule.

        Args:
            billable_portfolio_id: The ID of the billable portfolio.
            fee_schedule_id: The ID of the fee schedule to assign.
        """
        payload = {
            "data": {
                "id": fee_schedule_id,
                "type": "fee_schedules",
            }
        }

        self._patch(
            f"/billable_portfolios/{billable_portfolio_id}/relationships/fee_schedules",
            json=payload,
        )
        logger.info(
            f"Updated fee schedule for billable portfolio {billable_portfolio_id} "
            f"to {fee_schedule_id}"
        )

    def archive_billable_portfolio(self, billable_portfolio_id: str) -> None:
        """
        Archive a billable portfolio.

        Archived portfolios will no longer be billed. Previous bills
        are not affected.

        Args:
            billable_portfolio_id: The ID of the billable portfolio to archive.

        Raises:
            ConflictError: If the billable portfolio is already archived.
        """
        self._delete(
            f"/billable_portfolios/{billable_portfolio_id}/relationships/fee_schedules"
        )
        logger.info(f"Archived billable portfolio: {billable_portfolio_id}")

    def get_billable_portfolio(self, portfolio_id: str) -> Dict[str, Any]:
        """Return one billable portfolio resource, including archive state."""
        return self._get(f"/billable_portfolios/{portfolio_id}").json()["data"]

    def iter_billable_portfolios(
        self, *, limit: Optional[int] = None, page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        return self._paginate("/billable_portfolios", page_limit=page_limit, max_items=limit)

    def list_billable_portfolios(
        self, *, limit: int = DEFAULT_LIST_LIMIT, page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        return list(self.iter_billable_portfolios(limit=limit, page_limit=page_limit))

    def create_billable_portfolios(
        self, portfolios: Sequence[Mapping[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Create from attribute mappings containing schedule_id and entity_id or group_id."""
        resources = []
        for attributes in portfolios:
            if bool(attributes.get("entity_id")) == bool(attributes.get("group_id")):
                raise ValueError("Each portfolio requires either entity_id or group_id")
            resources.append(_resource("create_billable_portfolio", attributes))
        return self._post("/billable_portfolios", json={"data": _bulk_data(
            resources, "create_billable_portfolio")}).json()["data"]

    def update_fee_schedules(self, schedules: Mapping[str, str]) -> None:
        """Assign fee schedules using {billable_portfolio_id: schedule_id}, up to 500."""
        resources = [_resource("create_billable_portfolio", {"schedule_id": schedule_id}, portfolio_id)
                     for portfolio_id, schedule_id in schedules.items()]
        self._patch("/billable_portfolios/relationships/fee_schedules", json={"data":
            _bulk_data(resources, "create_billable_portfolio", max_items=500)})

    def archive_billable_portfolios(self, portfolio_ids: Sequence[str]) -> None:
        """Archive up to 500 portfolios in a single API request."""
        self._delete("/billable_portfolios/relationships/fee_schedules", json={"data":
            _bulk_data([{"id": str(value)} for value in portfolio_ids],
                       "billable_portfolios", max_items=500)})

    def update_payout_rule(self, portfolio_id: str, rule_id: str) -> None:
        self._patch(f"/billable_portfolios/{portfolio_id}/relationships/payout_rule",
                    json={"data": {"id": str(rule_id), "type": "payout_rule"}})

    def remove_payout_rule(self, portfolio_id: str) -> None:
        self._delete(f"/billable_portfolios/{portfolio_id}/relationships/payout_rule")
