"""Derivative underlying assets, including optional dated spot values."""

from copy import deepcopy
from typing import Any, Dict, Generator, List, Optional, Sequence, Union

from ...constants import DEFAULT_LIST_LIMIT, DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT
from ...exceptions import AddePyError
from ..base import BaseResource


class UnderlyingAssetsResource(BaseResource):
    """Manage ``/derivatives/underlying_assets`` resources."""

    _endpoint = "/derivatives/underlying_assets"
    _type = "derivatives_underlying_assets"

    @staticmethod
    def _metric_params(
        metric_date_from: Optional[str], metric_date_to: Optional[str]
    ) -> Dict[str, Any]:
        return {
            key: value
            for key, value in {
                "metric_date_from": metric_date_from,
                "metric_date_to": metric_date_to,
            }.items()
            if value is not None
        }

    def get_underlying_asset(
        self,
        asset_id: Union[str, int],
        *,
        metric_date_from: Optional[str] = None,
        metric_date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get an asset; supply both ISO date bounds to include its spot values."""
        return self._get(
            f"{self._endpoint}/{asset_id}",
            params=self._metric_params(metric_date_from, metric_date_to),
        ).json()["data"]

    def iter_underlying_assets(
        self,
        *,
        metric_date_from: Optional[str] = None,
        metric_date_to: Optional[str] = None,
        limit: Optional[int] = None,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        """Iterate using this endpoint's numeric ``page[after]`` offset.

        The documented response has no pagination links. Fetch subsequent pages
        until an empty page so a server-side page cap cannot truncate results.
        """
        if page_limit <= 0 or (limit is not None and limit < 0):
            raise ValueError(
                "page_limit must be positive and limit must be nonnegative"
            )
        if limit == 0:
            return
        params = self._metric_params(metric_date_from, metric_date_to)
        params["page[limit]"] = min(page_limit, MAX_PAGE_LIMIT)
        offset = 0
        previous_ids = None
        while True:
            params["page[after]"] = offset
            document = self._get(self._endpoint, params=params).json()
            items = document["data"]
            if not isinstance(items, list):
                raise AddePyError("Expected an array of underlying assets")
            if not items:
                return
            current_ids = tuple(item.get("id") for item in items)
            if previous_ids == current_ids:
                raise AddePyError("Underlying asset pagination did not advance")
            previous_ids = current_ids
            for item in items:
                yield item
                offset += 1
                if limit is not None and offset >= limit:
                    return
            # Respect an explicit terminal link when supplied by the server.
            if "next" in document.get("links", {}) and not document["links"]["next"]:
                return

    def list_underlying_assets(
        self,
        *,
        metric_date_from: Optional[str] = None,
        metric_date_to: Optional[str] = None,
        limit: int = DEFAULT_LIST_LIMIT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        """List underlying assets, optionally including spot values in a date range."""
        return list(
            self.iter_underlying_assets(
                metric_date_from=metric_date_from,
                metric_date_to=metric_date_to,
                limit=limit,
                page_limit=page_limit,
            )
        )

    def create_underlying_asset(self, **attributes: Any) -> Dict[str, Any]:
        """Create an asset from attributes; the server assigns its ID.

        Attributes include entity_name, entity_type, underlying_type,
        base_currency, optional financial_graph_node_id and metric_values.
        """
        payload = {"data": {"type": self._type, "attributes": deepcopy(attributes)}}
        return self._post(self._endpoint, json=payload).json()["data"]

    def create_underlying_assets(
        self, assets: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create assets from a list of attribute dictionaries."""
        payload = {
            "data": [
                {"type": self._type, "attributes": deepcopy(attributes)}
                for attributes in assets
            ]
        }
        return self._post(self._endpoint, json=payload).json()["data"]

    def update_underlying_asset(
        self, asset_id: Union[str, int], **attributes: Any
    ) -> Dict[str, Any]:
        """Patch attributes; a null metric value deletes that date's spot value.

        Omitted metric_values leave all spots unchanged. Dates outside the
        supplied metric interval remain unchanged.
        """
        payload = {
            "data": {
                "id": str(asset_id),
                "type": self._type,
                "attributes": deepcopy(attributes),
            }
        }
        return self._patch(f"{self._endpoint}/{asset_id}", json=payload).json()["data"]

    def update_underlying_assets(
        self, assets: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Patch dictionaries containing an id and the attributes to change."""
        payload = {
            "data": [
                {
                    "id": str(asset["id"]),
                    "type": self._type,
                    "attributes": deepcopy(
                        {key: value for key, value in asset.items() if key != "id"}
                    ),
                }
                for asset in assets
            ]
        }
        return self._patch(self._endpoint, json=payload).json()["data"]

    def delete_underlying_asset(self, asset_id: Union[str, int]) -> None:
        """Delete one underlying asset."""
        self._delete(f"{self._endpoint}/{asset_id}")

    def delete_underlying_assets(self, asset_ids: Sequence[Union[str, int]]) -> None:
        """Delete assets by ID; the API ignores IDs unavailable to the requester."""
        self._delete(
            self._endpoint,
            json={
                "data": [
                    {"id": str(asset_id), "type": self._type} for asset_id in asset_ids
                ]
            },
        )
