"""Ownership namespace containing ownership-related resources."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...client import AddeparClient
    from .entities import EntitiesResource
    from .groups import GroupsResource
    from .group_types import GroupTypesResource


class OwnershipNamespace:
    """
    Namespace for ownership-related API resources.

    Resources:
        - entities: Manage entities and query entity types
        - groups: Manage groups and group members
        - group_types: Manage group types
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client
        self._entities: Optional["EntitiesResource"] = None
        self._groups: Optional["GroupsResource"] = None
        self._group_types: Optional["GroupTypesResource"] = None

    @property
    def entities(self) -> "EntitiesResource":
        """Access the Entities resource."""
        if self._entities is None:
            from .entities import EntitiesResource

            self._entities = EntitiesResource(self._client)
        return self._entities

    @property
    def groups(self) -> "GroupsResource":
        """Access the Groups resource."""
        if self._groups is None:
            from .groups import GroupsResource

            self._groups = GroupsResource(self._client)
        return self._groups

    @property
    def group_types(self) -> "GroupTypesResource":
        """Access the Group Types resource."""
        if self._group_types is None:
            from .group_types import GroupTypesResource

            self._group_types = GroupTypesResource(self._client)
        return self._group_types


__all__ = ["OwnershipNamespace", "EntitiesResource", "GroupsResource", "GroupTypesResource"]
