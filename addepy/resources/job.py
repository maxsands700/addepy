"""Shared lifecycle for portfolio and transaction export jobs."""

from collections.abc import Mapping
from copy import deepcopy
import logging
from os import PathLike
from pathlib import Path
from typing import Any, Generator

import requests

from ..constants import (
    DEFAULT_BACKOFF_FACTOR,
    DEFAULT_INITIAL_WAIT,
    DEFAULT_LIST_LIMIT,
    DEFAULT_MAX_WAIT,
    DEFAULT_PAGE_LIMIT,
    DEFAULT_TIMEOUT,
)
from ..exceptions import AddePyError, JobError
from .base import BaseResource
from .query import QueryInput, query_parameters


logger = logging.getLogger("addepy")

JOB_IN_PROGRESS_STATUSES = frozenset(
    {
        "Queued",
        "In Progress",
        "In Progress - Waiting For Capacity",
        "Picked Up By Job Runner",
        "Cancel Requested",
    }
)
JOB_SUCCESS_STATUSES = frozenset({"Completed"})
JOB_FAILURE_STATUSES = frozenset(
    {
        "Canceled",
        "Timed Out",
        "Failed",
        "Rejected",
        "Error",
        "Error Cancelled",
        "User Cancelled",
    }
)
JOB_TERMINAL_STATUSES = JOB_SUCCESS_STATUSES | JOB_FAILURE_STATUSES


def _normalized_status(status: str) -> str:
    # Addepar documents both display names and underscore forms for canceling.
    return status.casefold().replace("_", " ").replace("cancelled", "canceled").strip()


class JobResource(BaseResource):
    """Common job methods; subclasses supply routes and documented states."""

    _endpoint: str
    _resource_type: str
    _query_job_type: str
    _job_label = "job"
    _success_statuses = JOB_SUCCESS_STATUSES
    _failure_statuses = JOB_FAILURE_STATUSES

    def _submit_job(
        self,
        job_type: str,
        parameters: Mapping[str, Any],
        *,
        headers: dict[str, str] | None = None,
    ) -> str:
        payload = {
            "data": {
                "type": self._resource_type,
                "attributes": {
                    "job_type": job_type,
                    "parameters": deepcopy(dict(parameters)),
                },
            }
        }
        response = self._post(self._endpoint, json=payload, headers=headers)
        try:
            document = response.json()
        except ValueError as exc:
            raise AddePyError(
                "Job creation returned an invalid JSON response.", response
            ) from exc
        data = document.get("data") if isinstance(document, Mapping) else None
        job_id = data.get("id") if isinstance(data, Mapping) else None
        if (
            not isinstance(job_id, (str, int))
            or isinstance(job_id, bool)
            or not str(job_id)
        ):
            raise AddePyError("Job creation returned no job ID.", response)
        logger.info("Created %s: %s", self._job_label, job_id)
        return str(job_id)

    def create_job(self, query_dict: QueryInput) -> str:
        """Submit a copied query (mapping or JSON string) and return its job ID.

        Accepts either query parameters directly or the ``data.attributes``
        envelope exported by Addepar. Unknown fields are retained and the input
        is never modified. Use ``create_query_job`` for the argument helper.
        """
        return self._submit_job(self._query_job_type, query_parameters(query_dict))

    def get_job_status(self, job_id: str) -> dict[str, Any]:
        """Return the complete JSON:API status document, including error details."""
        response = self._get(f"{self._endpoint}/{job_id}")
        try:
            document = response.json()
        except ValueError as exc:
            raise JobError(
                "Job status returned an invalid JSON response.",
                job_id=job_id,
                response=response,
            ) from exc
        if not isinstance(document, dict):
            raise JobError(
                "Job status must be a JSON object.",
                job_id=job_id,
                response=response,
                job_data=document,
            )
        return document

    def _status(self, job_id: str, document: dict[str, Any]) -> str:
        data = document.get("data")
        attributes = data.get("attributes") if isinstance(data, Mapping) else None
        status = attributes.get("status") if isinstance(attributes, Mapping) else None
        if not isinstance(status, str) or not status.strip():
            raise JobError(
                f"{self._job_label.capitalize()} {job_id} returned no valid status.",
                job_id=job_id,
                errors=attributes.get("errors")
                if isinstance(attributes, Mapping)
                else None,
                job_data=document,
            )
        return status

    def wait_for_job(
        self,
        job_id: str,
        *,
        initial_wait: float = DEFAULT_INITIAL_WAIT,
        max_wait: float = DEFAULT_MAX_WAIT,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> dict[str, Any]:
        """Wait for an existing job and return its complete successful status.

        Failures raise ``JobError`` with ``job_id``, ``status``, ``errors`` and
        ``job_data``. Missing status is an invalid response, never success.
        Unrecognized states are polled until a known terminal state or timeout.
        A local timeout leaves the server job running for later resumption.
        """
        success = {_normalized_status(value) for value in self._success_statuses}
        terminal = success | {
            _normalized_status(value) for value in self._failure_statuses
        }
        document = self._poll_until_complete(
            job_id=job_id,
            check_status_fn=self.get_job_status,
            is_complete_fn=lambda value: (
                _normalized_status(self._status(job_id, value)) in terminal
            ),
            initial_wait=initial_wait,
            max_wait=max_wait,
            backoff_factor=backoff_factor,
            timeout=timeout,
            job_type=self._job_label,
        )
        status = self._status(job_id, document)
        if _normalized_status(status) not in success:
            raise JobError(
                f"{self._job_label.capitalize()} {job_id} failed with status: {status}",
                job_id=job_id,
                status=status,
                errors=document["data"]["attributes"].get("errors"),
                job_data=document,
            )
        return document

    def get_job_results(
        self, job_id: str, *, stream: bool = False
    ) -> requests.Response:
        """Fetch results as a response; opt into streaming for manual consumption.

        Use ``response.json()`` for JSON, ``response.text`` for CSV/TSV, or
        ``response.content`` for XLSX. With ``stream=True``, close the response
        after reading. Addepar removes results 24 hours after job creation.
        """
        return self._get(f"{self._endpoint}/{job_id}/download", stream=stream)

    def download_job_results(self, job_id: str, path: str | PathLike[str]) -> Path:
        """Stream completed results to a file without buffering the entire export."""
        return self._client.download(f"{self._endpoint}/{job_id}/download", path)

    def resume_job(
        self,
        job_id: str,
        *,
        initial_wait: float = DEFAULT_INITIAL_WAIT,
        max_wait: float = DEFAULT_MAX_WAIT,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        """Wait for an existing job and fetch results without submitting again."""
        self.wait_for_job(
            job_id,
            initial_wait=initial_wait,
            max_wait=max_wait,
            backoff_factor=backoff_factor,
            timeout=timeout,
        )
        return self.get_job_results(job_id)

    def execute_job(
        self,
        query_dict: QueryInput,
        *,
        initial_wait: float = DEFAULT_INITIAL_WAIT,
        max_wait: float = DEFAULT_MAX_WAIT,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        """Submit raw query JSON, wait for completion, and fetch its results."""
        return self.resume_job(
            self.create_job(query_dict),
            initial_wait=initial_wait,
            max_wait=max_wait,
            backoff_factor=backoff_factor,
            timeout=timeout,
        )

    def iter_jobs(
        self, *, limit: int | None = None, page_limit: int = DEFAULT_PAGE_LIMIT
    ) -> Generator[dict[str, Any], None, None]:
        """Iterate job resource objects lazily across all result pages."""
        return self._paginate(self._endpoint, page_limit=page_limit, max_items=limit)

    def list_jobs(
        self, *, limit: int = DEFAULT_LIST_LIMIT, page_limit: int = DEFAULT_PAGE_LIMIT
    ) -> list[dict[str, Any]]:
        """Collect jobs up to ``limit``; use ``iter_jobs`` for unbounded iteration."""
        jobs = list(self.iter_jobs(limit=limit, page_limit=page_limit))
        if len(jobs) == limit:
            logger.warning(
                "list_jobs() reached %s items; use iter_jobs() for all jobs.", limit
            )
        return jobs

    def cancel_job(self, job_id: str) -> None:
        """Request cancellation, or archive results if the job already completed."""
        self._delete(f"{self._endpoint}/{job_id}")
        logger.info("Canceled %s: %s", self._job_label, job_id)

    # Preserve the helper used by existing resource convenience methods.
    _poll_and_download = resume_job
