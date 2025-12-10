"""Admin namespace containing admin-related resources."""
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...client import AddeparClient

from .import_tool import ImportToolResource


class AdminNamespace:
    """
    Namespace for admin-related API resources.

    Usage:
        client.admin.import_tool.create_import(...)
        client.admin.import_tool.execute_import(...)
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client
        self._import_tool: Optional[ImportToolResource] = None

    @property
    def import_tool(self) -> ImportToolResource:
        """Access import tool resource."""
        if self._import_tool is None:
            self._import_tool = ImportToolResource(self._client)
        return self._import_tool


__all__ = ["AdminNamespace", "ImportToolResource"]
