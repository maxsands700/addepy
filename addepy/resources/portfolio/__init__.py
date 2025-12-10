"""Portfolio namespace containing portfolio-related resources."""
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...client import AddeparClient

from .jobs import JobsResource


class PortfolioNamespace:
    """
    Namespace for portfolio-related API resources.

    Usage:
        client.portfolio.jobs.create_job(...)
        client.portfolio.jobs.execute_portfolio_query(...)
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client
        self._jobs: Optional[JobsResource] = None

    @property
    def jobs(self) -> JobsResource:
        """Access portfolio jobs resource."""
        if self._jobs is None:
            self._jobs = JobsResource(self._client)
        return self._jobs


__all__ = ["PortfolioNamespace", "JobsResource"]
