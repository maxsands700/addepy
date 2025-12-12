"""Admin namespace containing admin-related resources."""
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...client import AddeparClient

from .audit import AuditResource
from .billable_portfolios import BillablePortfoliosResource
from .contacts import ContactsResource
from .import_tool import ImportToolResource
from .roles import RolesResource
from .teams import TeamsResource
from .users import UsersResource


class AdminNamespace:
    """
    Namespace for admin-related API resources.

    Usage:
        client.admin.audit.query_login_attempts(...)
        client.admin.audit.query_attribute_changes(...)
        client.admin.billable_portfolios.create_billable_portfolio(...)
        client.admin.contacts.get_contact(...)
        client.admin.contacts.list_contacts()
        client.admin.import_tool.create_import(...)
        client.admin.import_tool.execute_import(...)
        client.admin.roles.get_role(...)
        client.admin.roles.list_roles()
        client.admin.teams.create_team(...)
        client.admin.teams.list_teams()
        client.admin.users.get_user(...)
        client.admin.users.list_users()
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client
        self._audit: Optional[AuditResource] = None
        self._billable_portfolios: Optional[BillablePortfoliosResource] = None
        self._contacts: Optional[ContactsResource] = None
        self._import_tool: Optional[ImportToolResource] = None
        self._roles: Optional[RolesResource] = None
        self._teams: Optional[TeamsResource] = None
        self._users: Optional[UsersResource] = None

    @property
    def audit(self) -> AuditResource:
        """Access audit resource."""
        if self._audit is None:
            self._audit = AuditResource(self._client)
        return self._audit

    @property
    def billable_portfolios(self) -> BillablePortfoliosResource:
        """Access billable portfolios resource."""
        if self._billable_portfolios is None:
            self._billable_portfolios = BillablePortfoliosResource(self._client)
        return self._billable_portfolios

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
    def roles(self) -> RolesResource:
        """Access roles resource."""
        if self._roles is None:
            self._roles = RolesResource(self._client)
        return self._roles

    @property
    def teams(self) -> TeamsResource:
        """Access teams resource."""
        if self._teams is None:
            self._teams = TeamsResource(self._client)
        return self._teams

    @property
    def users(self) -> UsersResource:
        """Access users resource."""
        if self._users is None:
            self._users = UsersResource(self._client)
        return self._users


__all__ = [
    "AdminNamespace",
    "AuditResource",
    "BillablePortfoliosResource",
    "ContactsResource",
    "ImportToolResource",
    "RolesResource",
    "TeamsResource",
    "UsersResource",
]
