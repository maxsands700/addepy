"""View Sets resource for the Addepar API."""
import logging
from typing import Any, Dict, Generator, List, Optional

from ...constants import DEFAULT_LIST_LIMIT, DEFAULT_PAGE_LIMIT
from ..base import BaseResource

logger = logging.getLogger("addepy")


class ViewSetsResource(BaseResource):
    """
    Resource for Addepar View Sets API.

    View sets are groups of views that determine what contacts see in the
    Client Portal. This is a read-only API.

    Methods:
        - get_view_set() - Get a single view set
        - list_view_sets() - List all view sets
    """

    def get_view_set(self, view_set_id: str) -> Dict[str, Any]:
        """
        Get a view set by ID.

        Args:
            view_set_id: The ID of the view set.

        Returns:
            View set resource object containing id, type, and attributes
            (name, views). The views attribute is a list of view objects
            with id, name, and type.

        Example:
            view_set = client.admin.view_sets.get_view_set(view_set_id="2000")
            print(view_set["attributes"]["name"])
            for view in view_set["attributes"]["views"]:
                print(f"  {view['name']} ({view['type']})")
        """
        response = self._get(f"/view_sets/{view_set_id}")
        data = response.json()
        view_set = data.get("data", {})
        logger.debug(f"Retrieved view set {view_set_id}")
        return view_set

    def iter_view_sets(
        self,
        *,
        limit: Optional[int] = None,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Iterate over view sets lazily.

        Args:
            limit: Maximum number of items to yield. None means no limit.
            page_limit: Results per page (default: 500, max: 2000).

        Yields:
            Individual view set resource objects.
        """
        return self._paginate("/view_sets", page_limit=page_limit, max_items=limit)

    def list_view_sets(
        self,
        *,
        limit: int = DEFAULT_LIST_LIMIT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        """
        List all view sets.

        Args:
            limit: Maximum number of items to return (default: 10,000).
                Use iter_view_sets() for unbounded iteration.
            page_limit: Results per page (default: 500, max: 2000).

        Returns:
            List of view set resource objects containing id, type, and
            attributes (name, views).

        Example:
            view_sets = client.admin.view_sets.list_view_sets()
            for vs in view_sets:
                print(f"{vs['id']}: {vs['attributes']['name']}")
        """
        view_sets = list(self.iter_view_sets(limit=limit, page_limit=page_limit))
        if len(view_sets) == limit:
            logger.warning(
                f"list_view_sets() returned {limit} items (limit reached). "
                f"Use iter_view_sets() for full results or pass a higher limit."
            )
        logger.debug(f"Listed {len(view_sets)} view sets")
        return view_sets
