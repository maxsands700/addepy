"""Group Types resource for the Addepar API."""
import logging
from typing import Any, Dict, List, Optional

from ..base import BaseResource

logger = logging.getLogger("addepy")


class GroupTypesResource(BaseResource):
    """
    Resource for Addepar Group Types API.

    Group types categorize groups and control access permissions.
    By default, firms have one group type called "GROUPS".

    Tier 1 (CRUD):
        - get_group_type() - Get a single group type
        - list_group_types() - List all group types
        - create_group_type() - Create a new group type
        - update_group_type() - Update a group type
        - delete_group_type() - Delete a group type
    """

    # =========================================================================
    # Tier 1: CRUD Methods
    # =========================================================================

    def get_group_type(self, group_type_id: str) -> Dict[str, Any]:
        """
        Get a single group type by ID.

        Args:
            group_type_id: The ID (group_type_key) of the group type to retrieve.

        Returns:
            The group type resource object containing id, type, and attributes.
        """
        response = self._get(f"/group_types/{group_type_id}")
        data = response.json()
        group_type = data.get("data", {})
        logger.debug(f"Retrieved group type {group_type_id}")
        return group_type

    def list_group_types(
        self,
        *,
        is_permissioned_resource: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        List all group types.

        Note: This endpoint does not support pagination.

        Args:
            is_permissioned_resource: If True, filter to explicit access types.
                If False, filter to implicit access types.

        Returns:
            List of group type resource objects.
        """
        params: Dict[str, Any] = {}

        if is_permissioned_resource is not None:
            params["is_permissioned_resource"] = str(is_permissioned_resource).lower()

        response = self._get("/group_types", params=params if params else None)
        data = response.json()
        group_types = data.get("data", [])
        logger.debug(f"Listed {len(group_types)} group types")
        return group_types

    def create_group_type(
        self,
        group_type_key: str,
        display_name: str,
        *,
        is_permissioned_resource: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a new group type.

        Args:
            group_type_key: The unique ID/key for the group type.
            display_name: The user-facing name for the group type.
            is_permissioned_resource: If True (default), users need explicit access
                to groups of this type. If False, users need access to each
                individual member to access groups of this type.

        Returns:
            The created group type resource object.

        Raises:
            ConflictError: If group_type_key already exists.
        """
        payload = {
            "data": {
                "type": "group_types",
                "attributes": {
                    "group_type_key": group_type_key,
                    "display_name": display_name,
                    "is_permissioned_resource": is_permissioned_resource,
                },
            }
        }

        response = self._post("/group_types", json=payload)
        data = response.json()
        group_type = data.get("data", {})
        logger.info(f"Created group type: {group_type.get('id')}")
        return group_type

    def update_group_type(
        self,
        group_type_id: str,
        *,
        display_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a group type.

        Only the display_name can be updated. The default "GROUPS" type
        cannot be modified.

        Args:
            group_type_id: The ID of the group type to update.
            display_name: The new user-facing name for the group type.

        Returns:
            The updated group type resource object.
        """
        attributes: Dict[str, Any] = {}

        if display_name is not None:
            attributes["display_name"] = display_name

        payload = {
            "data": {
                "type": "group_types",
                "id": group_type_id,
                "attributes": attributes,
            }
        }

        response = self._patch(f"/group_types/{group_type_id}", json=payload)
        data = response.json()
        group_type = data.get("data", {})
        logger.info(f"Updated group type: {group_type_id}")
        return group_type

    def delete_group_type(self, group_type_id: str) -> None:
        """
        Delete a group type.

        The default "GROUPS" type cannot be deleted.

        Args:
            group_type_id: The ID of the group type to delete.
        """
        self._delete(f"/group_types/{group_type_id}")
        logger.info(f"Deleted group type: {group_type_id}")
