import requests
import time
from typing import Optional, Tuple, Dict, List, Literal
from dotenv import load_dotenv
import os
import io
import pandas as pd

load_dotenv()

# --- GLOBAL DEFAULT HEADERS ---
DEFAULT_HEADERS = {
    "Content-Type": "application/vnd.api+json", 
    "Addepar-Firm": os.getenv("ADDEPAR_FIRM_ID"),
    "Authorization": f"Basic {os.getenv("ADDEPAR_API_KEY")}"
}

# ==============================================================================
# 1. PORTFOLIO QUERY JOB HELPERS
# ==============================================================================
def submit_portfolio_query_job(query_dict: Dict):
    """Submit a portfolio query job to Addepar API."""
    job_query = {
        "data": {
            "type": "job",
            "attributes": {
                "job_type": "PORTFOLIO_QUERY",
                "parameters": None
            }
        }
    }
    job_query['data']['attributes']['parameters'] = query_dict['data']['attributes']
    
    response = requests.post(
        url="https://choate.addepar.com/api/v1/jobs",
        headers=DEFAULT_HEADERS,
        json=job_query
    )
    
    print("Status Code:", response.status_code)
    data = response.json()
    
    if response.ok:
        job_id = data.get('data', {}).get('id', {})
        print("Job ID:", job_id)
        return job_id, data
    else:
        return None, data


def get_job_status(job_id: str):
    response = requests.get(url=f"https://choate.addepar.com/api/v1/jobs/{job_id}", headers=DEFAULT_HEADERS)
    data = response.json()
    if data.get('data', {}).get('attributes', {}).get('status', {}):
        print('Job in Progress')
        return None
    else:
        print("Job Completed, data is returned")
        return data


def download_job_results(job_id: str):
    """Download the results of a completed job."""
    response = requests.get(
        url=f"https://choate.addepar.com/api/v1/jobs/{job_id}/download",
        headers=DEFAULT_HEADERS
    )
    
    print('Response Status:', response.status_code)
    return response

# ==============================================================================
# 2. IMPORT JOB HELPERS
# ==============================================================================
IMPORT_COMPLETED_STATUSES = {
    'ERRORS_READY_FOR_REVIEW', 
    'WARNINGS_READY_FOR_REVIEW',
    'ERRORS_AND_WARNINGS_READY_FOR_REVIEW',
    'DRY_RUN_SUCCESSFUL', 
    'IMPORT_SUCCESSFUL',
    'VALIDATION_FAILED', 
    'IMPORT_FAILED'
}

VALID_POST_IMPORT_TYPES = {
    'ATTRIBUTES', 
    'BENCHMARKS', 
    'BENCHMARK_ASSOCIATIONS', 
    'CONTACTS', 
    'COST_BASIS', 
    'ESTIMATED_RETURNS',
    'GROUPS', 
    'HISTORICAL_PRICES', 
    'MANAGE_INVESTMENTS', 
    'MANAGE_OWNERSHIP', 
    'MANUAL_ADJUSTMENTS', 
    'CONSTITUENTS', 
    'POSITION_VALUATIONS', 
    'SUMMARY_DATA', 
    'TARGET_ALLOCATIONS', 
    'TOTAL_OUTSTANDING_SHARES', 
    'TRANSACTIONS',
    'DELETE_TRANSACTIONS',
    'VALUES_AND_FLOWS'
}

VALID_DELETE_IMPORT_TYPES = {
    'DELETE_TRANSACTIONS'
}

ALL_VALID_IMPORT_TYPES = VALID_POST_IMPORT_TYPES.union(VALID_DELETE_IMPORT_TYPES)

AddeparImportType = Literal[
    'ATTRIBUTES', 
    'BENCHMARKS', 
    'BENCHMARK_ASSOCIATIONS', 
    'CONTACTS', 
    'COST_BASIS', 
    'ESTIMATED_RETURNS',
    'GROUPS', 
    'HISTORICAL_PRICES', 
    'MANAGE_INVESTMENTS', 
    'MANAGE_OWNERSHIP', 
    'MANUAL_ADJUSTMENTS', 
    'CONSTITUENTS', 
    'POSITION_VALUATIONS', 
    'SUMMARY_DATA', 
    'TARGET_ALLOCATIONS', 
    'TOTAL_OUTSTANDING_SHARES', 
    'TRANSACTIONS',
    'DELETE_TRANSACTIONS' 
    'VALUES_AND_FLOWS'
]

def import_addepar_data(
    import_dataframe: pd.DataFrame, 
    import_type: AddeparImportType, 
    is_dry_run: bool, 
    ignore_warnings: bool
) -> Tuple[requests.Response, Optional[str]]:
    """
    Submit an import job to the Addepar Imports API endpoint, selecting HTTP method 
    based on the import type (POST or DELETE).

    Args:
        import_dataframe: Pandas DataFrame containing the data to be imported/deleted.
        import_type: The type of data being imported/deleted (must be one of AddeparImportType).
        is_dry_run: If True, performs a dry run without saving data.
        ignore_warnings: If True, allows the import to proceed despite warnings.

    Returns:
        A tuple of (response, import_id).
        - response: The raw requests.Response object from the submission.
        - import_id: The ID of the submitted import job (str) if successful, otherwise None.
    
    Raises:
        ValueError: If the provided import_type is invalid or not mapped to a method.
    """
    normalized_import_type = import_type.upper()
    
    # 1. Validation: Check if the type is globally supported
    if normalized_import_type not in ALL_VALID_IMPORT_TYPES:
        error_msg = (
            f"Invalid import_type '{import_type}'. "
            f"Must be one of: {', '.join(sorted(ALL_VALID_IMPORT_TYPES))}"
        )
        print(f"Error: {error_msg}")
        raise ValueError(error_msg)

    # 2. Determine HTTP Method
    if normalized_import_type in VALID_DELETE_IMPORT_TYPES:
        http_method = requests.delete
        print(f"Submitting {normalized_import_type} using DELETE method.")
    elif normalized_import_type in VALID_POST_IMPORT_TYPES:
        http_method = requests.post
        print(f"Submitting {normalized_import_type} using POST method.")
    else:
        # Fallback for types defined in ALL_VALID_IMPORT_TYPES but not categorized
        raise ValueError(f"Import type '{import_type}' is valid but not mapped to a submission method.")


    # 3. Request Preparation
    url = f"https://choate.addepar.com/api/v1/imports?import_type={normalized_import_type}&is_dry_run={is_dry_run}&ignore_warnings={ignore_warnings}"

    # Convert dataframe to csv format for request payload
    csv_buffer = io.StringIO()
    import_dataframe.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_payload = csv_buffer.getvalue()

    # Create a local header copy and set Content-Type to 'text/plain'
    import_headers = DEFAULT_HEADERS.copy()
    import_headers['Content-Type'] = 'text/plain'

    # 4. Execute Request
    resp = http_method(
        url=url,
        headers=import_headers,
        data=csv_payload
    )

    # 5. Process Response
    if resp.ok:
        try:
            import_id = resp.json().get('data', {}).get('id')
            return resp, import_id
        except requests.exceptions.JSONDecodeError:
            print("Error: Could not decode JSON from successful import submission.")
            return resp, None
    
    return resp, None


def get_import_status(import_id: str) -> Optional[str]:
    """
    Check the status of an import job (using Import API statuses).

    Args:
        import_id: The ID of the import job to check.

    Returns:
        The status string (str) of the import (e.g., 'IN_QUEUE', 'IMPORT_SUCCESSFUL').
        
    Raises:
        requests.HTTPError: If the API request returns a 4xx or 5xx status code.
    """
    url = f"https://choate.addepar.com/api/v1/imports/{import_id}"
    resp = requests.get(url=url, headers=DEFAULT_HEADERS)

    if resp.ok:
        try:
            data = resp.json()
            status = data.get('data', {}).get('attributes', {}).get('status', 'UNKNOWN_STATUS')
            return status
        except requests.exceptions.JSONDecodeError:
            print("Error: Could not decode JSON from successful status check.")
            return 'API_PARSE_ERROR'
    else:
        print(f"Error retrieving import status: {resp.status_code}")
        resp.raise_for_status()
        return None


def get_import_results(import_id: str) -> Dict:
    """
    Get the results (digests, warnings, errors) of a completed import job.

    Args:
        import_id: The ID of the completed import job.

    Returns:
        A dictionary containing the import results structure: 
        {'digests': Dict, 'warnings': Dict, 'errors': Dict}.
        Returns a dictionary with an 'error' key on API or JSON decode failure.
    """
    url = f"https://choate.addepar.com/api/v1/import_results/{import_id}"
    resp = requests.get(url=url, headers=DEFAULT_HEADERS)

    if resp.ok:
        try:
            data = resp.json()
            attributes = data.get('data', {}).get('attributes', {})
            
            digests = attributes.get('digests', {})
            warnings = attributes.get('warnings', {})
            errors = attributes.get('errors', {})
            
            return {"digests": digests, "warnings": warnings, "errors": errors}
        except requests.exceptions.JSONDecodeError:
            print("Error: Could not decode JSON from successful results fetch.")
            return {"error": "JSON_DECODE_ERROR"}
    else:
        print(f"Error retrieving import results: {resp.status_code}")
        return resp.json()

# ==============================================================================
# 3. Main Execution Functions
# ==============================================================================

def execute_portfolio_query_job(
    query_dict: Dict,
    initial_wait: float = 30,
    max_wait: float = 60*5,
    backoff_factor: float = 1.5,
    timeout: float = 60*20
) -> Tuple[Optional[requests.Response], Optional[Dict]]:
    """
    Submit a portfolio query job, poll for completion using exponential backoff, and download results.
    
    Args:
        query_dict: The portfolio query dictionary to submit.
        initial_wait: Initial polling interval in seconds (default: 30).
        max_wait: Maximum polling interval in seconds (default: 300 / 5 min).
        backoff_factor: Multiplier for exponential backoff (default: 1.5).
        timeout: Maximum time to wait for job completion in seconds (default: 1200 / 20 min).
    
    Returns:
        Tuple of (download_response, job_data).
        - download_response: The requests.Response object with job results if successful, None otherwise.
        - job_data: Final job status data (Dict).
    
    Raises:
        Exception: If job submission fails.
        TimeoutError: If job doesn't complete within timeout period.
    """
    print("=" * 60)
    print("Submitting portfolio query job...")
    print("=" * 60)
    
    job_id, submission_data = submit_portfolio_query_job(query_dict)
    
    if job_id is None:
        error_msg = f"Failed to submit job: {submission_data}"
        print(error_msg)
        raise Exception(error_msg)
    
    print(f"\nPolling for job completion (Job ID: {job_id})...")
    print(f"Initial wait: {initial_wait}s, Max wait: {max_wait}s, Timeout: {timeout}s")
    print("-" * 60)
    
    start_time = time.time()
    wait_time = initial_wait
    attempt = 1
    job_data = None
    
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(
                f"Job {job_id} did not complete within {timeout} seconds. "
                f"You may want to check the job status manually."
            )
        
        print(f"Attempt {attempt}: Waiting {wait_time:.1f}s before checking status... (Elapsed: {elapsed_time:.1f}s)")
        time.sleep(wait_time)
        
        # get_job_status returns None if in progress, data if completed
        job_data = get_job_status(job_id)
        
        if job_data is not None:
            # Check if the status is actually 'Completed' before downloading
            final_status = job_data.get('data', {}).get('attributes', {}).get('status')
            if final_status == 'Completed':
                print("\n" + "=" * 60)
                print("Job completed successfully! Downloading results...")
                print("=" * 60)
                download_response = download_job_results(job_id)
                return download_response, job_data
            else:
                print(f"\nJob finished with status: {final_status}. No download attempted.")
                return None, job_data
        
        wait_time = min(wait_time * backoff_factor, max_wait)
        attempt += 1

def execute_addepar_import_job(
    import_dataframe: pd.DataFrame,
    import_type: AddeparImportType,
    is_dry_run: bool,
    ignore_warnings: bool,
    initial_wait: float = 30,
    max_wait: float = 60*5,
    backoff_factor: float = 1.5,
    timeout: float = 60*20
) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Submit an Addepar import job and wait for completion with exponential backoff polling 
    (using Import API statuses).
    
    Args:
        import_dataframe: Pandas DataFrame containing the data to import.
        import_type: The type of data being imported (e.g., 'ATTRIBUTES').
        is_dry_run: If True, performs a dry run without saving data.
        ignore_warnings: If True, allows the import to proceed despite warnings.
        initial_wait: Initial polling interval in seconds (default: 30).
        max_wait: Maximum polling interval in seconds (default: 300 / 5 min).
        backoff_factor: Multiplier for exponential backoff (default: 1.5).
        timeout: Maximum time to wait for job completion in seconds (default: 1200 / 20 min).
    
    Returns:
        Tuple of (results_data, final_status).
        - results_data: Dictionary with 'digests', 'warnings', 'errors' if completed/ready, 
                        None otherwise.
        - final_status: The final status string (e.g., 'IMPORT_SUCCESSFUL') or an error message.
    
    Raises:
        Exception: If import submission or status check fails.
        TimeoutError: If job doesn't complete within timeout period.
    """
    print("=" * 60)
    print("Submitting Addepar import job...")
    print("=" * 60)
    
    # Define the final statuses where results are ready or the process has definitively failed
    FINAL_RESULT_READY_STATUSES = {
        'ERRORS_READY_FOR_REVIEW', 
        'WARNINGS_READY_FOR_REVIEW',
        'ERRORS_AND_WARNINGS_READY_FOR_REVIEW',
        'DRY_RUN_SUCCESSFUL', 
        'IMPORT_SUCCESSFUL'
    }
    # Define all statuses that stop the polling loop (ready OR failed)
    STOP_POLLING_STATUSES = FINAL_RESULT_READY_STATUSES.union({'VALIDATION_FAILED', 'IMPORT_FAILED'})

    # Submit the job
    submission_resp, import_id = import_addepar_data(
        import_dataframe, import_type, is_dry_run, ignore_warnings
    )
    
    if import_id is None or not submission_resp.ok:
        error_msg = f"Failed to submit import job (Status: {submission_resp.status_code}): {submission_resp.json()}"
        print(error_msg)
        raise Exception(error_msg)
    
    # Poll for completion with exponential backoff
    print(f"\nPolling for import completion (Import ID: {import_id})...")
    print(f"Initial wait: {initial_wait}s, Max wait: {max_wait}s, Timeout: {timeout}s")
    print("-" * 60)
    
    start_time = time.time()
    wait_time = initial_wait
    attempt = 1
    current_status = None
    
    while current_status not in STOP_POLLING_STATUSES:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(
                f"Import {import_id} did not complete within {timeout} seconds. "
                f"Last known status: {current_status}. You may want to check the status manually."
            )
        
        print(f"Attempt {attempt}: Waiting {wait_time:.1f}s before checking status... (Elapsed: {elapsed_time:.1f}s)")
        time.sleep(wait_time)
        
        status_result = get_import_status(import_id)
        
        if isinstance(status_result, str):
            current_status = status_result
            print(f"Import Status: **{current_status}**")
        else:
            error_msg = f"Failed to retrieve status for Import ID {import_id}."
            print(error_msg)
            raise Exception(error_msg) 
            
        # Check if a final status has been reached
        if current_status in STOP_POLLING_STATUSES:
            print("\n" + "=" * 60)
            print(f"Import finished with status: **{current_status}**")
            print("=" * 60)

            # Only fetch results if the status indicates results are available (success or reviewable errors/warnings)
            if current_status in FINAL_RESULT_READY_STATUSES:
                print("Fetching import results...")
                results_data = get_import_results(import_id)
                
                if isinstance(results_data, dict) and 'error' not in results_data:
                    print(f"Results fetched successfully.")
                    print(f"Digests: {len(results_data.get('digests', {}))} sections")
                    print(f"Warnings: {len(results_data.get('warnings', {}))} sections")
                    print(f"Errors: {len(results_data.get('errors', {}))} sections")
                    return results_data, current_status
                else:
                    error_msg = f"Failed to fetch final import results: {results_data}"
                    print(error_msg)
                    return None, f"Results fetch failed: {error_msg}"
            
            # If status is VALIDATION_FAILED or IMPORT_FAILED, return None results
            print("Job failed and does not have structured results to fetch.")
            return None, current_status
        
        # Job still in progress, increase wait time with exponential backoff
        wait_time = min(wait_time * backoff_factor, max_wait)
        attempt += 1

    return None, current_status