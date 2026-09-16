"""Billing payout recipients and rules, using their plain offset/limit paging."""

from typing import Any, Dict, Generator, List, Mapping, Optional, Sequence

from ...constants import DEFAULT_LIST_LIMIT, DEFAULT_PAGE_LIMIT
from ..base import BaseResource
from .billing import _bulk_data, _resource, _single_data


class _PayoutResource(BaseResource):
    endpoint: str
    resource_type: str

    def _iter_payouts(
        self,
        *,
        limit: Optional[int],
        page_limit: int,
        params: Optional[Dict[str, Any]] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """These routes use offset/limit and meta.page.total, not JSON:API cursors."""
        if page_limit <= 0 or (limit is not None and limit < 0):
            raise ValueError(
                "page_limit must be positive and limit must be nonnegative"
            )
        if limit == 0:
            return
        query = dict(params or {})
        offset = 0
        previous_items = None
        while True:
            query.update(
                offset=offset,
                limit=min(page_limit, limit - offset)
                if limit is not None
                else page_limit,
            )
            document = self._get(self.endpoint, params=query.copy()).json()
            items = document["data"]
            if not items:
                return
            if items == previous_items:
                raise ValueError("Payout pagination returned a repeated page")
            previous_items = items
            for item in items:
                yield item
                offset += 1
                if limit is not None and offset >= limit:
                    return
            total = document.get("meta", {}).get("page", {}).get("total")
            if total is not None and offset >= int(total):
                return
            # If metadata is absent, continue until an empty page: the server
            # may impose a smaller page size than the caller requested.

    def _create(self, attributes: Mapping[str, Any]) -> Dict[str, Any]:
        return _single_data(
            self._post(
                self.endpoint, json={"data": _resource(self.resource_type, attributes)}
            )
        )

    def _create_many(
        self, resources: Sequence[Mapping[str, Any]]
    ) -> List[Dict[str, Any]]:
        return self._post(
            self.endpoint, json={"data": _bulk_data(resources, self.resource_type)}
        ).json()["data"]

    def _replace(
        self,
        resource_id: str,
        attributes: Mapping[str, Any],
        *,
        include_id: bool = True,
    ) -> Dict[str, Any]:
        return _single_data(
            self._put(
                f"{self.endpoint}/{resource_id}",
                json={
                    "data": _resource(
                        self.resource_type,
                        attributes,
                        resource_id if include_id else None,
                    )
                },
            )
        )

    def _delete_many(self, resource_ids: Sequence[str]) -> None:
        self._delete(
            self.endpoint,
            json={
                "data": _bulk_data(
                    [{"id": str(value)} for value in resource_ids], self.resource_type
                )
            },
        )


class PayoutRecipientsResource(_PayoutResource):
    """Manage recipients; mutation methods accept attribute dictionaries."""

    endpoint = "/billing/payout/recipients"
    resource_type = "payout_recipient"

    def get_payout_recipient(self, recipient_id: str) -> Dict[str, Any]:
        return _single_data(self._get(f"{self.endpoint}/{recipient_id}"))

    def iter_payout_recipients(
        self,
        *,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        return self._iter_payouts(
            limit=limit,
            page_limit=page_limit,
            params={"search": search} if search is not None else None,
        )

    def list_payout_recipients(
        self,
        *,
        search: Optional[str] = None,
        limit: int = DEFAULT_LIST_LIMIT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        return list(
            self.iter_payout_recipients(
                search=search, limit=limit, page_limit=page_limit
            )
        )

    def create_payout_recipient(self, attributes: Mapping[str, Any]) -> Dict[str, Any]:
        """Create a recipient from attributes such as name and type."""
        return self._create(attributes)

    def create_payout_recipients(
        self, recipients: Sequence[Mapping[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create a list of JSON:API resources, each containing attributes."""
        return self._create_many(recipients)

    def replace_payout_recipient(
        self, recipient_id: str, attributes: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """Replace a recipient using PUT and its complete attribute mapping."""
        return self._replace(recipient_id, attributes, include_id=False)

    def delete_payout_recipient(self, recipient_id: str) -> None:
        self._delete(f"{self.endpoint}/{recipient_id}")

    def delete_payout_recipients(self, recipient_ids: Sequence[str]) -> None:
        self._delete_many(recipient_ids)


class PayoutRulesResource(_PayoutResource):
    """Manage payout rules; split structures remain raw dictionaries."""

    endpoint = "/billing/payout/rules"
    resource_type = "payout_rule"

    def get_payout_rule(self, rule_id: str) -> Dict[str, Any]:
        return _single_data(self._get(f"{self.endpoint}/{rule_id}"))

    def iter_payout_rules(
        self,
        *,
        search: Optional[str] = None,
        recipient_ids: Optional[Sequence[str]] = None,
        limit: Optional[int] = None,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        params: Dict[str, Any] = {}
        if search is not None:
            params["search"] = search
        if recipient_ids is not None:
            # requests encodes a list as repeated recipient_ids query parameters.
            params["recipient_ids"] = list(recipient_ids)
        return self._iter_payouts(limit=limit, page_limit=page_limit, params=params)

    def list_payout_rules(
        self,
        *,
        search: Optional[str] = None,
        recipient_ids: Optional[Sequence[str]] = None,
        limit: int = DEFAULT_LIST_LIMIT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        return list(
            self.iter_payout_rules(
                search=search,
                recipient_ids=recipient_ids,
                limit=limit,
                page_limit=page_limit,
            )
        )

    def create_payout_rule(self, attributes: Mapping[str, Any]) -> Dict[str, Any]:
        """Create a rule. Within splits, supply recipient IDs, not expanded recipients."""
        return self._create(attributes)

    def create_payout_rules(
        self, rules: Sequence[Mapping[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create complete JSON:API resource objects containing attributes."""
        return self._create_many(rules)

    def replace_payout_rule(
        self, rule_id: str, attributes: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """PUT a complete rule, including its split structure."""
        return self._replace(rule_id, attributes)

    def delete_payout_rule(self, rule_id: str) -> None:
        self._delete(f"{self.endpoint}/{rule_id}")

    def delete_payout_rules(self, rule_ids: Sequence[str]) -> None:
        self._delete_many(rule_ids)
