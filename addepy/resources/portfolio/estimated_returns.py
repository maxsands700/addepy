"""Estimated returns for entities, using Addepar's documented JSON:API routes."""

from copy import deepcopy
from typing import Any, Dict, Generator, List, Optional, Sequence, Union

from ...constants import DEFAULT_LIST_LIMIT, DEFAULT_PAGE_LIMIT
from ...exceptions import AddePyError
from ..base import BaseResource


class EstimatedReturnsResource(BaseResource):
    """Read and maintain estimated returns (POST has upsert semantics)."""

    def get_estimated_return(self, estimated_return_id: str) -> Dict[str, Any]:
        """Get a return by composite ID, for example ``123_2024-01-15``."""
        return self._get(f"/estimated_returns/{estimated_return_id}").json()["data"]

    def iter_estimated_returns(
        self,
        entity_ids: Sequence[Union[str, int]],
        *,
        limit: Optional[int] = None,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        """Iterate returns for one or more entities; the entity filter is required."""
        if isinstance(entity_ids, (str, bytes)) or not entity_ids:
            raise ValueError("entity_ids must be a nonempty sequence of entity IDs")
        return self._paginate(
            "/estimated_returns",
            params={"filter[entity_id]": ",".join(str(value) for value in entity_ids)},
            page_limit=page_limit,
            max_items=limit,
        )

    def list_estimated_returns(
        self,
        entity_ids: Sequence[Union[str, int]],
        *,
        limit: int = DEFAULT_LIST_LIMIT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        """List returns for the given entities, up to ``limit`` records."""
        return list(
            self.iter_estimated_returns(entity_ids, limit=limit, page_limit=page_limit)
        )

    def create_estimated_return(
        self, entity_id: int, date: str, return_value: float
    ) -> Dict[str, Any]:
        """Create or replace the return for an entity/date pair (YYYY-MM-DD)."""
        payload = {
            "data": {
                "type": "estimated_returns",
                "attributes": {
                    "entity_id": entity_id,
                    "date": date,
                    "return_value": return_value,
                },
            }
        }
        data = self._post("/estimated_returns", json=payload).json()["data"]
        # The guide shows an array even for a single POST request.
        if isinstance(data, list):
            if len(data) != 1:
                raise AddePyError(
                    "Expected one estimated return from a single create request"
                )
            return data[0]
        return data

    def create_estimated_returns(
        self, estimated_returns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Upsert attribute dictionaries containing entity_id, date and return_value."""
        payload = {
            "data": [
                {"type": "estimated_returns", "attributes": deepcopy(attributes)}
                for attributes in estimated_returns
            ]
        }
        return self._post("/estimated_returns", json=payload).json()["data"]

    upsert_estimated_return = create_estimated_return
    upsert_estimated_returns = create_estimated_returns

    def update_estimated_return(
        self, estimated_return_id: str, return_value: float
    ) -> Dict[str, Any]:
        """Update only the return value; the entity and date are immutable."""
        payload = {
            "data": {
                "id": estimated_return_id,
                "type": "estimated_returns",
                "attributes": {"return_value": return_value},
            }
        }
        return self._patch(
            f"/estimated_returns/{estimated_return_id}", json=payload
        ).json()["data"]

    def delete_estimated_return(self, estimated_return_id: str) -> None:
        """Delete one return by its composite ID."""
        self._delete(f"/estimated_returns/{estimated_return_id}")

    def delete_entity_estimated_returns(self, entity_id: Union[str, int]) -> None:
        """Delete ALL estimated returns for the entity."""
        self._delete(f"/estimated_returns/entity/{entity_id}")
