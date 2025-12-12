"""Portfolio namespace containing portfolio-related resources."""
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...client import AddeparClient

from .benchmarks import BenchmarksResource
from .jobs import JobsResource
from .snapshots import SnapshotsResource
from .transactions import TransactionsResource
from .transaction_jobs import TransactionJobsResource


class PortfolioNamespace:
    """
    Namespace for portfolio-related API resources.

    Usage:
        client.portfolio.benchmarks.list_benchmarks()
        client.portfolio.benchmarks.create_benchmark(...)
        client.portfolio.jobs.create_job(...)
        client.portfolio.jobs.execute_portfolio_query(...)
        client.portfolio.snapshots.create_snapshot(...)
        client.portfolio.snapshots.get_snapshot(...)
        client.portfolio.transactions.create_transaction(...)
        client.portfolio.transaction_jobs.execute_view_job(...)
    """

    def __init__(self, client: "AddeparClient") -> None:
        self._client = client
        self._benchmarks: Optional[BenchmarksResource] = None
        self._jobs: Optional[JobsResource] = None
        self._snapshots: Optional[SnapshotsResource] = None
        self._transactions: Optional[TransactionsResource] = None
        self._transaction_jobs: Optional[TransactionJobsResource] = None

    @property
    def benchmarks(self) -> BenchmarksResource:
        """Access benchmarks resource."""
        if self._benchmarks is None:
            self._benchmarks = BenchmarksResource(self._client)
        return self._benchmarks

    @property
    def jobs(self) -> JobsResource:
        """Access portfolio jobs resource."""
        if self._jobs is None:
            self._jobs = JobsResource(self._client)
        return self._jobs

    @property
    def snapshots(self) -> SnapshotsResource:
        """Access snapshots resource."""
        if self._snapshots is None:
            self._snapshots = SnapshotsResource(self._client)
        return self._snapshots

    @property
    def transactions(self) -> TransactionsResource:
        """Access transactions resource."""
        if self._transactions is None:
            self._transactions = TransactionsResource(self._client)
        return self._transactions

    @property
    def transaction_jobs(self) -> TransactionJobsResource:
        """Access transaction jobs resource."""
        if self._transaction_jobs is None:
            self._transaction_jobs = TransactionJobsResource(self._client)
        return self._transaction_jobs


__all__ = [
    "PortfolioNamespace",
    "BenchmarksResource",
    "JobsResource",
    "SnapshotsResource",
    "TransactionsResource",
    "TransactionJobsResource",
]
