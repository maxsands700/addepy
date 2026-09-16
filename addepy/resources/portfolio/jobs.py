"""Portfolio query and saved-view export jobs.

LIVE API COMPATIBILITY NOTE FOR MAINTAINERS:
Addepar's online job-status documentation is incorrect for the completion path
confirmed by a user against their live firm: GET /jobs/{id} can return the
completed portfolio result itself (meta, data, included), without
data.attributes.status. Its data.attributes.total contains columns and/or
children. Requiring status="Completed" rejects these successful responses.

Recognize this result structure as completion, preserving the original document.
Do not restore the old blanket "missing status means success" fallback: empty,
malformed, error, and job-status documents are not portfolio results. Explicit
statuses still take precedence. This behavior is specific to portfolio jobs;
transaction jobs retain their status-based lifecycle.
"""

from typing import Any

import requests

from ...constants import (
    DEFAULT_BACKOFF_FACTOR,
    DEFAULT_INITIAL_WAIT,
    DEFAULT_MAX_WAIT,
    DEFAULT_TIMEOUT,
    OutputType,
    PortfolioType,
)
from ..job import (
    JOB_FAILURE_STATUSES,
    JOB_IN_PROGRESS_STATUSES as JOB_IN_PROGRESS_STATUSES,
    JOB_SUCCESS_STATUSES,
    JOB_TERMINAL_STATUSES as JOB_TERMINAL_STATUSES,
    JobResource,
)
from ..query import QueryInput, query_parameters


def _is_portfolio_result(document: Any) -> bool:
    """Recognize the result envelope observed on completed portfolio jobs."""
    if not isinstance(document, dict) or document.get("errors"):
        return False
    data = document.get("data")
    if not isinstance(data, dict) or data.get("errors"):
        return False
    if data.get("type") in ("jobs", "job", "transaction_jobs"):
        return False
    attributes = data.get("attributes")
    if (
        not isinstance(attributes, dict)
        or "status" in attributes
        or "job_type" in attributes
        or attributes.get("errors")
    ):
        return False
    total = attributes.get("total")
    return isinstance(total, dict) and (
        isinstance(total.get("columns"), dict)
        or isinstance(total.get("children"), list)
    )


class JobsResource(JobResource):
    """Portfolio exports with raw queries, optional builders, and resumable jobs.

    ``batch=True`` opts into Addepar's beta batched computation. It requires
    compatible views/attributes; advanced tables, pivot tables and summary
    table-row data are unsupported. Unsupported attributes cause a job error.
    See https://developers.addepar.com/docs/batched-jobs for current restrictions.
    """

    _endpoint = "/jobs"
    _resource_type = "jobs"
    _query_job_type = "PORTFOLIO_QUERY"
    _job_label = "portfolio job"
    _success_statuses = JOB_SUCCESS_STATUSES
    _failure_statuses = JOB_FAILURE_STATUSES

    def _status(self, job_id: str, document: dict[str, Any]) -> str:
        if _is_portfolio_result(document):
            return "Completed"
        return super()._status(job_id, document)

    def create_job(
        self,
        query_dict: QueryInput,
        *,
        batch: bool = False,
        job_type: str | None = None,
    ) -> str:
        """Submit raw query parameters or exported ``data.attributes`` JSON.

        A mapping or JSON string is accepted. All query fields and values are
        preserved without modifying the input. ``batch=True`` adds only the
        documented ``Addepar-Compute-Type: BATCH`` header.

        The standard query type remains ``PORTFOLIO_QUERY``. The beta guide
        also names ``portfolio_query_results``; ``job_type`` lets a caller use
        that explicit value if required for their environment.
        """
        return self._submit_job(
            job_type or self._query_job_type,
            query_parameters(query_dict),
            headers={"Addepar-Compute-Type": "BATCH"} if batch else None,
        )

    def create_query_job(
        self,
        portfolio_type: PortfolioType,
        portfolio_id: str,
        start_date: str,
        end_date: str,
        columns: list[dict[str, Any]],
        groupings: list[dict[str, Any]],
        *,
        filters: list[dict[str, Any]] | None = None,
        hide_previous_holdings: bool = False,
        batch: bool = False,
    ) -> str:
        """Build and submit a portfolio query; use ``create_job`` for raw JSON."""
        parameters: dict[str, Any] = {
            "portfolio_type": portfolio_type.lower(),
            "portfolio_id": portfolio_id,
            "start_date": start_date,
            "end_date": end_date,
            "columns": columns,
            "groupings": groupings,
            "hide_previous_holdings": hide_previous_holdings,
        }
        if filters is not None:
            parameters["filters"] = filters
        return self.create_job(parameters, batch=batch)

    def create_view_job(
        self,
        view_id: str,
        portfolio_type: PortfolioType,
        portfolio_id: str,
        start_date: str,
        end_date: str,
        output_type: OutputType = "JSON",
        *,
        batch: bool = False,
    ) -> str:
        """Export a saved view as JSON, CSV, TSV or XLSX; return the job ID."""
        return self._submit_job(
            "portfolio_view_results",
            {
                "view_id": view_id,
                "portfolio_type": portfolio_type.lower(),
                "portfolio_id": portfolio_id,
                "output_type": output_type.lower(),
                "start_date": start_date,
                "end_date": end_date,
            },
            headers={"Addepar-Compute-Type": "BATCH"} if batch else None,
        )

    def execute_job(
        self,
        query_dict: QueryInput,
        *,
        batch: bool = False,
        job_type: str | None = None,
        initial_wait: float = DEFAULT_INITIAL_WAIT,
        max_wait: float = DEFAULT_MAX_WAIT,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        """Submit raw query JSON, wait, and return results as a response.

        To resume after a local timeout, call ``resume_job(error.job_id)``.
        For streaming output, call ``create_job``, ``wait_for_job`` and
        ``download_job_results`` separately.
        """
        return self.resume_job(
            self.create_job(query_dict, batch=batch, job_type=job_type),
            initial_wait=initial_wait,
            max_wait=max_wait,
            backoff_factor=backoff_factor,
            timeout=timeout,
        )

    # Existing names and the names documented by earlier README versions.
    execute_portfolio_query_job = execute_job
    execute_portfolio_query = execute_job

    def execute_view_job(
        self,
        view_id: str,
        portfolio_type: PortfolioType,
        portfolio_id: str,
        start_date: str,
        end_date: str,
        output_type: OutputType = "JSON",
        *,
        batch: bool = False,
        initial_wait: float = DEFAULT_INITIAL_WAIT,
        max_wait: float = DEFAULT_MAX_WAIT,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        """Submit a saved-view export, wait, and return its JSON or file response."""
        return self.resume_job(
            self.create_view_job(
                view_id=view_id,
                portfolio_type=portfolio_type,
                portfolio_id=portfolio_id,
                start_date=start_date,
                end_date=end_date,
                output_type=output_type,
                batch=batch,
            ),
            initial_wait=initial_wait,
            max_wait=max_wait,
            backoff_factor=backoff_factor,
            timeout=timeout,
        )

    execute_portfolio_view = execute_view_job
