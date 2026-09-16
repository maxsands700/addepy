"""Lossless normalization of queries copied from Addepar."""

from collections.abc import Mapping
from copy import deepcopy
import json
from typing import Any, TypeAlias

from ..exceptions import ValidationError


QueryInput: TypeAlias = Mapping[str, Any] | str


def query_parameters(query: QueryInput) -> dict[str, Any]:
    """Copy raw parameters or a JSON:API query's ``data.attributes``.

    Only the outer query shape is validated. Attribute keys, query options,
    identifiers and their values are passed through without coercion or a
    field allowlist, so a query copied from Addepar remains usable as-is.
    """
    if isinstance(query, str):
        try:
            query = json.loads(query)
        except (ValueError, TypeError) as exc:
            raise ValidationError("Query must contain a valid JSON object.") from exc

    if not isinstance(query, Mapping):
        raise ValidationError("Query must be a mapping or a JSON object string.")

    if "data" in query:
        data = query["data"]
        if not isinstance(data, Mapping) or not isinstance(
            data.get("attributes"), Mapping
        ):
            raise ValidationError(
                "Query envelope must contain a data.attributes object."
            )
        query = data["attributes"]

    return deepcopy(dict(query))
