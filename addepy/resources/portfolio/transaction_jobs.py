"""Transaction query and saved-view export jobs."""

from typing import Any

import requests

from ...constants import (
    DEFAULT_BACKOFF_FACTOR,
    DEFAULT_INITIAL_WAIT,
    DEFAULT_MAX_WAIT,
    DEFAULT_TIMEOUT,
    PortfolioType,
    TransactionOutputType,
)
from ..job import (
    JOB_FAILURE_STATUSES,
    JOB_IN_PROGRESS_STATUSES,
    JOB_SUCCESS_STATUSES,
    JOB_TERMINAL_STATUSES,
    JobResource,
)


# Retain the existing constants for callers that import them directly.
TRANSACTION_JOB_IN_PROGRESS_STATUSES = JOB_IN_PROGRESS_STATUSES
TRANSACTION_JOB_SUCCESS_STATUSES = JOB_SUCCESS_STATUSES
TRANSACTION_JOB_FAILURE_STATUSES = JOB_FAILURE_STATUSES
TRANSACTION_JOB_TERMINAL_STATUSES = JOB_TERMINAL_STATUSES


class TransactionJobsResource(JobResource):
    """Transaction exports with the same raw-query lifecycle as portfolio jobs.

    ``create_job(raw_query)`` submits a dictionary or copied JSON string.
    ``execute_job(raw_query)`` also waits and downloads. Argument-based helpers
    remain available for query and saved-view exports.
    """

    _endpoint = "/transaction_jobs"
    _resource_type = "transaction_jobs"
    _query_job_type = "transaction_query"
    _job_label = "transaction job"
    _success_statuses = TRANSACTION_JOB_SUCCESS_STATUSES
    _failure_statuses = TRANSACTION_JOB_FAILURE_STATUSES

    def create_view_job(
        self,
        view_id: str,
        portfolio_id: str,
        portfolio_type: PortfolioType,
        start_date: str,
        end_date: str,
        output_type: TransactionOutputType = "CSV",
    ) -> str:
        """Export a saved transaction view as CSV, TSV or XLSX; return its ID."""
        return self._submit_job(
            "transaction_view_results",
            {
                "view_id": view_id,
                "portfolio_id": portfolio_id,
                "portfolio_type": portfolio_type.lower(),
                "output_type": output_type.lower(),
                "start_date": start_date,
                "end_date": end_date,
            },
        )

    def create_query_job(
        self,
        columns: list[str],
        portfolio_type: PortfolioType,
        portfolio_id: str | list[str],
        start_date: str,
        end_date: str,
        *,
        filters: list[dict[str, Any]] | None = None,
        sorting: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        include_online_valuations: bool = False,
        include_unverified: bool = False,
        include_deleted: bool = False,
    ) -> str:
        """Build and submit a transaction query; use ``create_job`` for raw JSON.

        ``sorting`` follows the request example in the transaction-jobs guide;
        the guide's parameter table instead says ``sortings``. A raw query can
        pass either field unchanged if the firm's API requires that spelling.
        """
        parameters: dict[str, Any] = {
            "columns": columns,
            "portfolio_type": portfolio_type.lower(),
            "portfolio_id": [portfolio_id]
            if isinstance(portfolio_id, str)
            else portfolio_id,
            "start_date": start_date,
            "end_date": end_date,
            "include_online_valuations": include_online_valuations,
            "include_unverified": include_unverified,
            "include_deleted": include_deleted,
        }
        if filters is not None:
            parameters["filters"] = filters
        if sorting is not None:
            parameters["sorting"] = sorting
        if limit is not None:
            parameters["limit"] = limit
        return self.create_job(parameters)

    def execute_view_job(
        self,
        view_id: str,
        portfolio_id: str,
        portfolio_type: PortfolioType,
        start_date: str,
        end_date: str,
        output_type: TransactionOutputType = "CSV",
        *,
        initial_wait: float = DEFAULT_INITIAL_WAIT,
        max_wait: float = DEFAULT_MAX_WAIT,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        """Submit a saved-view export, wait, and return the file response."""
        return self.resume_job(
            self.create_view_job(
                view_id=view_id,
                portfolio_id=portfolio_id,
                portfolio_type=portfolio_type,
                start_date=start_date,
                end_date=end_date,
                output_type=output_type,
            ),
            initial_wait=initial_wait,
            max_wait=max_wait,
            backoff_factor=backoff_factor,
            timeout=timeout,
        )

    def execute_query_job(
        self,
        columns: list[str],
        portfolio_type: PortfolioType,
        portfolio_id: str | list[str],
        start_date: str,
        end_date: str,
        *,
        filters: list[dict[str, Any]] | None = None,
        sorting: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        include_online_valuations: bool = False,
        include_unverified: bool = False,
        include_deleted: bool = False,
        initial_wait: float = DEFAULT_INITIAL_WAIT,
        max_wait: float = DEFAULT_MAX_WAIT,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        """Build a query, wait, and return JSON results as a response.

        Use ``execute_job(raw_query)`` to run copied Addepar query JSON instead.
        """
        return self.resume_job(
            self.create_query_job(
                columns=columns,
                portfolio_type=portfolio_type,
                portfolio_id=portfolio_id,
                start_date=start_date,
                end_date=end_date,
                filters=filters,
                sorting=sorting,
                limit=limit,
                include_online_valuations=include_online_valuations,
                include_unverified=include_unverified,
                include_deleted=include_deleted,
            ),
            initial_wait=initial_wait,
            max_wait=max_wait,
            backoff_factor=backoff_factor,
            timeout=timeout,
        )

    execute_transaction_query = JobResource.execute_job
    execute_transaction_query_job = JobResource.execute_job
