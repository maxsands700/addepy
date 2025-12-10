"""Ownership namespace containing ownership-related resources."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...client import AddeparClient
    from .entities import EntitiesResource, EntityTypesResource


class OwnershipNamespace:
    """
    Namespace for ownership-related API resources.

    Resources:
        - entities: Manage entities (people, trusts, accounts, securities, etc.)
        - entity_types: Query available model types and their attributes
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client
        self._entities: Optional["EntitiesResource"] = None
        self._entity_types: Optional["EntityTypesResource"] = None

    @property
    def entities(self) -> "EntitiesResource":
        """Access the Entities resource."""
        if self._entities is None:
            from .entities import EntitiesResource

            self._entities = EntitiesResource(self._client)
        return self._entities

    @property
    def entity_types(self) -> "EntityTypesResource":
        """Access the Entity Types resource."""
        if self._entity_types is None:
            from .entities import EntityTypesResource

            self._entity_types = EntityTypesResource(self._client)
        return self._entity_types


__all__ = ["OwnershipNamespace", "EntitiesResource", "EntityTypesResource"]
