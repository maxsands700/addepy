"""Ownership namespace containing ownership-related resources."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...client import AddeparClient
    from .entities import EntitiesResource


class OwnershipNamespace:
    """
    Namespace for ownership-related API resources.

    Resources:
        - entities: Manage entities and query entity types
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client
        self._entities: Optional["EntitiesResource"] = None

    @property
    def entities(self) -> "EntitiesResource":
        """Access the Entities resource."""
        if self._entities is None:
            from .entities import EntitiesResource

            self._entities = EntitiesResource(self._client)
        return self._entities


__all__ = ["OwnershipNamespace", "EntitiesResource"]
