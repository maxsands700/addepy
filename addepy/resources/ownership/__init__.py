"""Ownership namespace containing ownership-related resources (placeholder)."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...client import AddeparClient


class OwnershipNamespace:
    """
    Namespace for ownership-related API resources.

    Currently a placeholder for future implementation.

    Future resources:
        - entities
        - external_ids
        - groups
        - positions
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client


__all__ = ["OwnershipNamespace"]
