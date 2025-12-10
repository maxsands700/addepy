"""Portfolio Jobs resource for the Addepar API."""
import logging
from typing import Any, Dict, Optional

import requests

from ...constants import (
    DEFAULT_BACKOFF_FACTOR,
    DEFAULT_INITIAL_WAIT,
    DEFAULT_MAX_WAIT,
    DEFAULT_TIMEOUT,
)
from ...exceptions import AddeparError
from ..base import BaseResource

logger = logging.getLogger("addepy")


class JobsResource(BaseResource):
    """
    Resource for portfolio query jobs.

    Tier 1 (CRUD wrappers):
        - create_job() - Submit a portfolio query job
        - get_job_status() - Check job status
        - get_job_results() - Download completed job results

    Tier 2 (Orchestration):
        - execute_portfolio_query() - Submit, poll, and download in one call
    """

    # =========================================================================
    # Tier 1: CRUD Wrappers
    # =========================================================================

    def create_job(self, query_dict: Dict[str, Any]) -> str:
        """
        Submit a portfolio query job to the Addepar API.

        Args:
            query_dict: Portfolio query configuration with structure:
                       {'data': {'attributes': {...}}}

        Returns:
            The job ID string.

        Raises:
            AddeparError: If job creation fails or no job ID is returned.
        """
        job_query = {
            "data": {
                "type": "job",
                "attributes": {
                    "job_type": "PORTFOLIO_QUERY",
                    "parameters": query_dict["data"]["attributes"],
                },
            }
        }

        response = self._post("/jobs", json=job_query)
        data = response.json()

        job_id = data.get("data", {}).get("id")
        if not job_id:
            raise AddeparError(f"Failed to create job: {data}")

        logger.info(f"Created portfolio query job: {job_id}")
        return job_id

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Check the status of a portfolio query job.

        Args:
            job_id: The ID of the job to check.

        Returns:
            The job data dictionary containing status information.
            Check data['data']['attributes']['status'] for current status.
        """
        response = self._get(f"/jobs/{job_id}")
        data = response.json()
        status = data.get("data", {}).get("attributes", {}).get("status", "Unknown")
        logger.debug(f"Job {job_id} status: {status}")
        return data

    def get_job_results(self, job_id: str) -> requests.Response:
        """
        Download the results of a completed job.

        Args:
            job_id: The ID of the completed job.

        Returns:
            The requests.Response object containing the job results.
            Use response.text or response.content to access the data.
        """
        logger.debug(f"Downloading results for job {job_id}")
        return self._get(f"/jobs/{job_id}/download")

    # =========================================================================
    # Tier 2: Orchestration Methods
    # =========================================================================

    def execute_portfolio_query(
            self,
            query_dict: Dict[str, Any],
            *,
            initial_wait: float = DEFAULT_INITIAL_WAIT,
            max_wait: float = DEFAULT_MAX_WAIT,
            backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
            timeout: float = DEFAULT_TIMEOUT,
        ) -> requests.Response:
        """
        Submit a portfolio query job, poll for completion, and download results.

        This is a convenience method that combines create_job(), polling with
        get_job_status(), and get_job_results() into a single call.

        Args:
            query_dict: The portfolio query dictionary to submit.
            initial_wait: Initial polling interval in seconds (default: 30).
            max_wait: Maximum polling interval in seconds (default: 300).
            backoff_factor: Multiplier for exponential backoff (default: 1.5).
            timeout: Maximum time to wait for completion (default: 1200).

        Returns:
            Response containing the query results.

        Raises:
            AddeparError: If job creation fails or job doesn't complete successfully.
            AddeparTimeoutError: If job doesn't complete within timeout.
        """
        # Step 1: Submit the job (Tier 1)
        job_id = self.create_job(query_dict)
        logger.info(f"Polling job {job_id} for completion...")

        # Step 2: Poll for completion
        def check_status(jid: str) -> Optional[Dict[str, Any]]:
            data = self.get_job_status(jid)
            status = data.get("data", {}).get("attributes", {}).get("status")
            # Return None if still in progress, data if complete
            return None if status and status != "Completed" else data

        def is_complete(data: Optional[Dict[str, Any]]) -> bool:
            return data is not None

        job_data = self._poll_until_complete(
            job_id=job_id,
            check_status_fn=check_status,
            is_complete_fn=is_complete,
            initial_wait=initial_wait,
            max_wait=max_wait,
            backoff_factor=backoff_factor,
            timeout=timeout,
            job_type="portfolio query job",
        )

        # Step 3: Verify completion and download results
        final_status = job_data.get("data", {}).get("attributes", {}).get("status")
        if final_status != "Completed":
            raise AddeparError(f"Job {job_id} finished with status: {final_status}")

        logger.info(f"Job {job_id} completed, downloading results")
        return self.get_job_results(job_id)
