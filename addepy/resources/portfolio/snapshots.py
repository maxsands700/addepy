"""Snapshots resource for the Addepar API."""
import logging
from typing import Any, Dict, List, Optional

from ...constants import SnapshotType
from ..base import BaseResource

logger = logging.getLogger("addepy")

# Valid snapshot types
SNAPSHOT_TYPES = {"snapshot", "valuation"}


class _Unset:
    def __repr__(self) -> str:
        return "UNSET"


_UNSET = _Unset()


class SnapshotsResource(BaseResource):
    """
    Resource for Addepar Snapshots API.

    Snapshots record the value of share-based or percent-based assets on a single day.
    Valuations record value-based assets like real estate, hedge funds, and private equity.

    Tier 1 (CRUD):
        - get_snapshot() - Get a single snapshot/valuation
        - create_snapshot() - Create a single snapshot/valuation
        - create_snapshots() - Create multiple snapshots/valuations (up to 500)
        - update_snapshot() - Update a single snapshot
        - update_snapshots() - Update multiple snapshots (up to 500)
        - delete_snapshot() - Delete a single snapshot
        - delete_snapshots() - Delete multiple snapshots (up to 500)

    Relationship Methods:
        - get_snapshot_owner() - Get the owner entity
        - get_snapshot_owner_relationship() - Get owner relationship ID
        - get_snapshot_owned() - Get the owned entity
        - get_snapshot_owned_relationship() - Get owned relationship ID
        - get_snapshot_position() - Get the position
        - get_snapshot_position_relationship() - Get position relationship ID
    """

    # =========================================================================
    # Tier 1: CRUD Methods
    # =========================================================================

    def get_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get a single snapshot or valuation by ID.

        Args:
            snapshot_id: The ID of the snapshot to retrieve.

        Returns:
            The snapshot resource object containing id, type, attributes,
            and relationships.
        """
        response = self._get(f"/snapshots/{snapshot_id}")
        data = response.json()
        snapshot = data.get("data", {})
        logger.debug(f"Retrieved snapshot {snapshot_id}")
        return snapshot

    def create_snapshot(
        self,
        snapshot_type: SnapshotType,
        currency: str,
        trade_date: str,
        amount: float,
        owner_id: str,
        owned_id: str,
        *,
        units: Optional[float] = None,
        comment: Optional[str] = None,
        price_factor: Optional[float] = None,
        accrued_income_per_unit: Optional[float] = None,
        knowledge_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a single snapshot or valuation.

        Args:
            snapshot_type: Either "snapshot" (share/percent-based) or "valuation" (value-based).
            currency: Three-letter currency code (e.g., "USD").
            trade_date: Date string in "YYYY-MM-DD" format.
            amount: The value of the snapshot/valuation.
            owner_id: Entity ID of the owner.
            owned_id: Entity ID of the owned asset.
            units: Number of shares. Required by Addepar for share-based assets;
                omit for percent-based snapshots or valuations.
            comment: Optional description (max 4000 characters).
            price_factor: Principal factor for bonds.
            accrued_income_per_unit: Accrued income per unit.
            knowledge_date: When the value was known or reported (YYYY-MM-DD).
                Distinguishes values with the same position and trade date.

        Returns:
            The created snapshot resource object.

        Raises:
            ValueError: If snapshot_type is invalid. Addepar validates asset-specific
                requirements, including whether units are required.
        """
        if snapshot_type not in SNAPSHOT_TYPES:
            raise ValueError(f"snapshot_type must be one of: {SNAPSHOT_TYPES}")

        attributes: Dict[str, Any] = {
            "type": snapshot_type,
            "currency": currency,
            "trade_date": trade_date,
            "amount": amount,
        }

        if units is not None:
            attributes["units"] = units
        if comment is not None:
            attributes["comment"] = comment
        if price_factor is not None:
            attributes["price_factor"] = price_factor
        if accrued_income_per_unit is not None:
            attributes["accrued_income_per_unit"] = accrued_income_per_unit
        if knowledge_date is not None:
            attributes["knowledge_date"] = knowledge_date

        payload = {
            "data": [
                {
                    "type": "snapshots",
                    "attributes": attributes,
                    "relationships": {
                        "owner": {
                            "data": {"type": "entities", "id": owner_id}
                        },
                        "owned": {
                            "data": {"type": "entities", "id": owned_id}
                        },
                    },
                }
            ]
        }

        response = self._post("/snapshots", json=payload)
        data = response.json()
        snapshots = data.get("data", [])
        snapshot = snapshots[0] if snapshots else {}
        logger.info(f"Created snapshot: {snapshot.get('id')}")
        return snapshot

    def create_snapshots(self, snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple snapshots or valuations at once.

        Args:
            snapshots: List of snapshot definitions. Each should have:
                - snapshot_type (str): "snapshot" or "valuation". Required.
                - currency (str): Three-letter currency code. Required.
                - trade_date (str): Date "YYYY-MM-DD". Required.
                - amount (float): Value. Required.
                - owner_id (str): Owner entity ID. Required.
                - owned_id (str): Owned entity ID. Required.
                - units (float, optional): Required for share-based assets.
                - comment (str, optional): Description.
                - price_factor (float, optional): For bonds.
                - accrued_income_per_unit (float, optional): Accrued income.
                - knowledge_date (str, optional): When the value was known/reported.

        Returns:
            List of created snapshot resource objects.

        Example:
            snapshots = [
                {
                    "snapshot_type": "snapshot",
                    "currency": "USD",
                    "trade_date": "2023-01-31",
                    "amount": 1000.00,
                    "units": 10.0,
                    "owner_id": "22",
                    "owned_id": "34",
                },
                {
                    "snapshot_type": "valuation",
                    "currency": "USD",
                    "trade_date": "2023-01-31",
                    "amount": 500000.00,
                    "owner_id": "22",
                    "owned_id": "100",
                },
            ]
            created = client.portfolio.snapshots.create_snapshots(snapshots)
        """
        if not 1 <= len(snapshots) <= 500:
            raise ValueError("snapshots must contain between 1 and 500 items")
        data_items = []
        for snap in snapshots:
            snapshot_type = snap.get("snapshot_type", "snapshot")
            if snapshot_type not in SNAPSHOT_TYPES:
                raise ValueError(f"snapshot_type must be one of: {SNAPSHOT_TYPES}")

            attributes: Dict[str, Any] = {
                "type": snapshot_type,
                "currency": snap["currency"],
                "trade_date": snap["trade_date"],
                "amount": snap["amount"],
            }

            if "units" in snap:
                attributes["units"] = snap["units"]
            if "comment" in snap:
                attributes["comment"] = snap["comment"]
            if "price_factor" in snap:
                attributes["price_factor"] = snap["price_factor"]
            if "accrued_income_per_unit" in snap:
                attributes["accrued_income_per_unit"] = snap["accrued_income_per_unit"]
            if "knowledge_date" in snap:
                attributes["knowledge_date"] = snap["knowledge_date"]

            data_items.append({
                "type": "snapshots",
                "attributes": attributes,
                "relationships": {
                    "owner": {
                        "data": {"type": "entities", "id": snap["owner_id"]}
                    },
                    "owned": {
                        "data": {"type": "entities", "id": snap["owned_id"]}
                    },
                },
            })

        payload = {"data": data_items}

        response = self._post("/snapshots", json=payload)
        data = response.json()
        created_snapshots = data.get("data", [])
        logger.info(f"Created {len(created_snapshots)} snapshots")
        return created_snapshots

    def update_snapshot(
        self,
        snapshot_id: str,
        *,
        amount: float | None | _Unset = _UNSET,
        currency: str | None | _Unset = _UNSET,
        units: float | None | _Unset = _UNSET,
        comment: str | None | _Unset = _UNSET,
        price_factor: float | None | _Unset = _UNSET,
        accrued_income_per_unit: float | None | _Unset = _UNSET,
    ) -> Dict[str, Any]:
        """
        Update a single snapshot or valuation.

        Note: Cannot update type, trade_date, knowledge_date, owner, owned, or position.
        Omitted attributes remain unchanged. Explicit None is sent as JSON null
        to remove an editable attribute.

        Args:
            snapshot_id: The ID of the snapshot to update.
            amount: New value for the snapshot.
            currency: New currency code.
            units: New units value.
            comment: New comment (set to None to remove).
            price_factor: New price factor.
            accrued_income_per_unit: New accrued income per unit.

        Returns:
            The updated snapshot resource object.
        """
        attributes: Dict[str, Any] = {}

        if amount is not _UNSET:
            attributes["amount"] = amount
        if currency is not _UNSET:
            attributes["currency"] = currency
        if units is not _UNSET:
            attributes["units"] = units
        if comment is not _UNSET:
            attributes["comment"] = comment
        if price_factor is not _UNSET:
            attributes["price_factor"] = price_factor
        if accrued_income_per_unit is not _UNSET:
            attributes["accrued_income_per_unit"] = accrued_income_per_unit

        payload = {
            "data": {
                "id": snapshot_id,
                "type": "snapshots",
                "attributes": attributes,
            }
        }

        response = self._patch(f"/snapshots/{snapshot_id}", json=payload)
        data = response.json()
        snapshot = data.get("data", {})
        logger.info(f"Updated snapshot: {snapshot_id}")
        return snapshot

    def update_snapshots(self, snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Update multiple snapshots or valuations at once.

        Args:
            snapshots: List of snapshot updates. Each should have:
                - id (str): Snapshot ID. Required.
                - amount (float, optional): New value.
                - currency (str, optional): New currency.
                - units (float, optional): New units.
                - comment (str, optional): New comment.
                - price_factor (float, optional): New price factor.
                - accrued_income_per_unit (float, optional): New accrued income.

        Returns:
            List of updated snapshot resource objects.

        Example:
            updates = [
                {"id": "344671144892", "amount": 1500.00},
                {"id": "344671144893", "comment": None},  # Removes comment
            ]
            updated = client.portfolio.snapshots.update_snapshots(updates)
        """
        if not 1 <= len(snapshots) <= 500:
            raise ValueError("snapshots must contain between 1 and 500 items")
        data_items = []
        for snap in snapshots:
            attributes: Dict[str, Any] = {}

            if "amount" in snap:
                attributes["amount"] = snap["amount"]
            if "currency" in snap:
                attributes["currency"] = snap["currency"]
            if "units" in snap:
                attributes["units"] = snap["units"]
            if "comment" in snap:
                attributes["comment"] = snap["comment"]
            if "price_factor" in snap:
                attributes["price_factor"] = snap["price_factor"]
            if "accrued_income_per_unit" in snap:
                attributes["accrued_income_per_unit"] = snap["accrued_income_per_unit"]

            data_items.append({
                "id": snap["id"],
                "type": "snapshots",
                "attributes": attributes,
            })

        payload = {"data": data_items}

        response = self._patch("/snapshots", json=payload)
        data = response.json()
        updated_snapshots = data.get("data", [])
        logger.info(f"Updated {len(updated_snapshots)} snapshots")
        return updated_snapshots

    def delete_snapshot(self, snapshot_id: str) -> None:
        """
        Delete a single snapshot or valuation.

        Args:
            snapshot_id: The ID of the snapshot to delete.
        """
        self._delete(f"/snapshots/{snapshot_id}")
        logger.info(f"Deleted snapshot: {snapshot_id}")

    def delete_snapshots(self, snapshot_ids: List[str]) -> None:
        """
        Delete multiple snapshots or valuations at once.

        Args:
            snapshot_ids: List of snapshot IDs to delete.
        """
        if not 1 <= len(snapshot_ids) <= 500:
            raise ValueError("snapshot_ids must contain between 1 and 500 items")
        payload = {
            "data": [
                {"id": snapshot_id, "type": "snapshots"}
                for snapshot_id in snapshot_ids
            ]
        }

        self._delete("/snapshots", json=payload)
        logger.info(f"Deleted {len(snapshot_ids)} snapshots")

    # =========================================================================
    # Relationship Methods
    # =========================================================================

    def get_snapshot_owner(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get the owner entity of a snapshot.

        Args:
            snapshot_id: The ID of the snapshot.

        Returns:
            The owner entity resource object with full attributes.
        """
        response = self._get(f"/snapshots/{snapshot_id}/owner")
        data = response.json()
        owner = data.get("data", {})
        logger.debug(f"Retrieved owner for snapshot {snapshot_id}")
        return owner

    def get_snapshot_owner_relationship(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get the owner relationship of a snapshot.

        Args:
            snapshot_id: The ID of the snapshot.

        Returns:
            The owner relationship object with id and type.
        """
        response = self._get(f"/snapshots/{snapshot_id}/relationships/owner")
        data = response.json()
        relationship = data.get("data", {})
        logger.debug(f"Retrieved owner relationship for snapshot {snapshot_id}")
        return relationship

    def get_snapshot_owned(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get the owned entity of a snapshot.

        Args:
            snapshot_id: The ID of the snapshot.

        Returns:
            The owned entity resource object with full attributes.
        """
        response = self._get(f"/snapshots/{snapshot_id}/owned")
        data = response.json()
        owned = data.get("data", {})
        logger.debug(f"Retrieved owned for snapshot {snapshot_id}")
        return owned

    def get_snapshot_owned_relationship(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get the owned relationship of a snapshot.

        Args:
            snapshot_id: The ID of the snapshot.

        Returns:
            The owned relationship object with id and type.
        """
        response = self._get(f"/snapshots/{snapshot_id}/relationships/owned")
        data = response.json()
        relationship = data.get("data", {})
        logger.debug(f"Retrieved owned relationship for snapshot {snapshot_id}")
        return relationship

    def get_snapshot_position(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get the position of a snapshot.

        Args:
            snapshot_id: The ID of the snapshot.

        Returns:
            The position resource object.
        """
        response = self._get(f"/snapshots/{snapshot_id}/position")
        data = response.json()
        position = data.get("data", {})
        logger.debug(f"Retrieved position for snapshot {snapshot_id}")
        return position

    def get_snapshot_position_relationship(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get the position relationship of a snapshot.

        Args:
            snapshot_id: The ID of the snapshot.

        Returns:
            The position relationship object with id and type.
        """
        response = self._get(f"/snapshots/{snapshot_id}/relationships/position")
        data = response.json()
        relationship = data.get("data", {})
        logger.debug(f"Retrieved position relationship for snapshot {snapshot_id}")
        return relationship
