"""Admin namespace containing admin-related resources."""
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...client import AddeparClient

from .contacts import ContactsResource
from .import_tool import ImportToolResource
from .users import UsersResource


class AdminNamespace:
    """
    Namespace for admin-related API resources.

    Usage:
        client.admin.contacts.get_contact(...)
        client.admin.contacts.list_contacts()
        client.admin.import_tool.create_import(...)
        client.admin.import_tool.execute_import(...)
        client.admin.users.get_user(...)
        client.admin.users.list_users()
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client
        self._contacts: Optional[ContactsResource] = None
        self._import_tool: Optional[ImportToolResource] = None
        self._users: Optional[UsersResource] = None

    @property
    def contacts(self) -> ContactsResource:
        """Access contacts resource."""
        if self._contacts is None:
            self._contacts = ContactsResource(self._client)
        return self._contacts

    @property
    def import_tool(self) -> ImportToolResource:
        """Access import tool resource."""
        if self._import_tool is None:
            self._import_tool = ImportToolResource(self._client)
        return self._import_tool

    @property
    def users(self) -> UsersResource:
        """Access users resource."""
        if self._users is None:
            self._users = UsersResource(self._client)
        return self._users


__all__ = ["AdminNamespace", "ContactsResource", "ImportToolResource", "UsersResource"]
