"""Billing resources, grouped as in the Addepar Developer Portal."""

from typing import TYPE_CHECKING, Optional

from .billable_portfolios import BillablePortfoliosResource
from .fees import FeeSchedulesResource, FeesResource
from .payouts import PayoutRecipientsResource, PayoutRulesResource

if TYPE_CHECKING:
    from ...client import AddePy


class BillingNamespace:
    """Access fees, fee schedules, billable portfolios, and payouts.

    Usage::

        client.billing.fees.list_fees()
        client.billing.fee_schedules.list_fee_schedules()
        client.billing.billable_portfolios.list_billable_portfolios()

    """

    def __init__(self, client: "AddePy") -> None:
        self._client = client
        self._fees: Optional[FeesResource] = None
        self._fee_schedules: Optional[FeeSchedulesResource] = None
        self._billable_portfolios: Optional[BillablePortfoliosResource] = None
        self._payout_recipients: Optional[PayoutRecipientsResource] = None
        self._payout_rules: Optional[PayoutRulesResource] = None

    @property
    def fees(self) -> FeesResource:
        """Manage fee definitions and read their fee schedule associations."""
        if self._fees is None:
            self._fees = FeesResource(self._client)
        return self._fees

    @property
    def fee_schedules(self) -> FeeSchedulesResource:
        """Manage fee schedules and their fee associations."""
        if self._fee_schedules is None:
            self._fee_schedules = FeeSchedulesResource(self._client)
        return self._fee_schedules

    @property
    def billable_portfolios(self) -> BillablePortfoliosResource:
        """Manage portfolios associated with fee schedules."""
        if self._billable_portfolios is None:
            self._billable_portfolios = BillablePortfoliosResource(self._client)
        return self._billable_portfolios

    @property
    def payout_recipients(self) -> PayoutRecipientsResource:
        """Manage the existing payout recipient API."""
        if self._payout_recipients is None:
            self._payout_recipients = PayoutRecipientsResource(self._client)
        return self._payout_recipients

    @property
    def payout_rules(self) -> PayoutRulesResource:
        """Manage the existing payout rules API."""
        if self._payout_rules is None:
            self._payout_rules = PayoutRulesResource(self._client)
        return self._payout_rules


__all__ = [
    "BillingNamespace",
    "FeesResource",
    "FeeSchedulesResource",
    "BillablePortfoliosResource",
    "PayoutRecipientsResource",
    "PayoutRulesResource",
]
