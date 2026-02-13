"""Attributes resource for the Addepar API."""
import logging
from typing import Any, Dict, Generator, List, Optional

from ...constants import AttributeOutputType, AttributeUsage, DEFAULT_LIST_LIMIT, DEFAULT_PAGE_LIMIT
from ..base import BaseResource

logger = logging.getLogger("addepy")


class AttributesResource(BaseResource):
    """
    Resource for Addepar Attributes API.

    Attributes are qualitative and quantitative details used to organize
    and analyze data in Addepar. Use this API to discover available
    attributes and their arguments.

    Methods:
        - get_attribute() - Get a single attribute
        - list_attributes() - List all attributes with optional filters
        - query_attributes() - Query multiple attributes by keys
        - get_argument_ids() - Get argument IDs for an attribute
        - get_arguments() - Get full argument objects for an attribute
    """

    def get_attribute(self, attribute_id: str) -> Dict[str, Any]:
        """
        Get an attribute by ID.

        Args:
            attribute_id: The attribute key (e.g., "time_weighted_return").

        Returns:
            Attribute resource object containing id, type, attributes
            (output_type, usage, display_name, category, created_at,
            modified_at), and relationships (arguments).

        Example:
            attr = client.portfolio.attributes.get_attribute("time_weighted_return")
            print(f"{attr['attributes']['display_name']}: {attr['attributes']['category']}")
        """
        response = self._get(f"/attributes/{attribute_id}")
        data = response.json()
        result = data.get("data", {})
        logger.debug(f"Retrieved attribute: {attribute_id}")
        return result

    def iter_attributes(
        self,
        *,
        category: Optional[str] = None,
        usage: Optional[AttributeUsage] = None,
        output_type: Optional[AttributeOutputType] = None,
        limit: Optional[int] = None,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Iterate over attributes lazily with optional filters.

        Args:
            category: Filter by category (e.g., "Cash Flows", "Security Details").
            usage: Filter by usage.
            output_type: Filter by output type.
            limit: Maximum number of items to yield. None means no limit.
            page_limit: Results per page (default: 500, max: 2000).

        Yields:
            Individual attribute resource objects.
        """
        params: Dict[str, Any] = {}

        if category is not None:
            params["filter[category]"] = category
        if usage is not None:
            params["filter[usage]"] = usage
        if output_type is not None:
            params["filter[output_type]"] = output_type

        return self._paginate(
            "/attributes",
            page_limit=page_limit,
            params=params if params else None,
            max_items=limit,
        )

    def list_attributes(
        self,
        *,
        category: Optional[str] = None,
        usage: Optional[AttributeUsage] = None,
        output_type: Optional[AttributeOutputType] = None,
        limit: int = DEFAULT_LIST_LIMIT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
    ) -> List[Dict[str, Any]]:
        """
        List all attributes with optional filters.

        Args:
            category: Filter by category (e.g., "Cash Flows", "Security Details",
                "Holding Details", "Performance Metrics").
            usage: Filter by usage. One of: "columns", "groupings", "filters",
                "position_custom_attributes", "entity_custom_attributes",
                "entity_attributes".
            output_type: Filter by output type. One of: "Word", "Boolean",
                "Percent", "Date", "Currency", "List", "Number".
            limit: Maximum number of items to return (default: 10,000).
                Use iter_attributes() for unbounded iteration.
            page_limit: Results per page (default: 500, max: 2000).

        Returns:
            List of attribute resource objects.

        Example:
            # List all performance metrics
            attrs = client.portfolio.attributes.list_attributes(
                category="Performance Metrics"
            )

            # List attributes usable as columns
            attrs = client.portfolio.attributes.list_attributes(
                usage="columns"
            )
        """
        attributes = list(self.iter_attributes(
            category=category,
            usage=usage,
            output_type=output_type,
            limit=limit,
            page_limit=page_limit,
        ))
        if len(attributes) == limit:
            logger.warning(
                f"list_attributes() returned {limit} items (limit reached). "
                f"Use iter_attributes() for full results or pass a higher limit."
            )
        logger.debug(f"Listed {len(attributes)} attributes")
        return attributes

    def query_attributes(self, attribute_keys: List[str]) -> List[Dict[str, Any]]:
        """
        Query multiple attributes by their keys.

        Args:
            attribute_keys: List of attribute keys to retrieve.

        Returns:
            List of attribute resource objects matching the keys.

        Example:
            attrs = client.portfolio.attributes.query_attributes([
                "account_fees",
                "account_number",
                "_custom_automatic_conversion_minimum_amount_406"
            ])
        """
        payload = {
            "data": {
                "type": "attribute_search",
                "attributes": {
                    "attribute_keys": attribute_keys,
                },
            }
        }

        response = self._post("/attributes/query", json=payload)
        data = response.json()
        results = data.get("data", [])
        logger.debug(f"Queried {len(results)} attributes")
        return results

    def get_argument_ids(self, attribute_id: str) -> List[Dict[str, str]]:
        """
        Get the list of argument IDs for an attribute.

        Args:
            attribute_id: The attribute key.

        Returns:
            List of argument reference objects with 'id' and 'type' keys.

        Example:
            arg_ids = client.portfolio.attributes.get_argument_ids(
                "time_weighted_return"
            )
            for arg in arg_ids:
                print(arg["id"])  # e.g., "period", "currency"
        """
        response = self._get(f"/attributes/{attribute_id}/relationships/arguments")
        data = response.json()
        results = data.get("data", [])
        logger.debug(f"Retrieved {len(results)} argument IDs for attribute {attribute_id}")
        return results

    def get_arguments(self, attribute_id: str) -> List[Dict[str, Any]]:
        """
        Get full argument objects for an attribute.

        Args:
            attribute_id: The attribute key.

        Returns:
            List of argument resource objects with id, type, and attributes
            (values, default_value, arg_type).

        Example:
            args = client.portfolio.attributes.get_arguments("cost_basis")
            for arg in args:
                print(f"{arg['id']}: {arg['attributes']['default_value']}")
        """
        response = self._get(f"/attributes/{attribute_id}/arguments")
        data = response.json()
        results = data.get("data", [])
        logger.debug(f"Retrieved {len(results)} arguments for attribute {attribute_id}")
        return results
