import httpx
from typing import Any, Dict, Optional


async def fetch_with_retry(
    url: str,
    method: str = "GET",
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    retries: int = 3,
    timeout: int = 10,
) -> Any:
    """
    Fetch data from an API with optional retries.

    Args:
        url (str): API URL to fetch data from.
        method (str): HTTP method (GET, POST, etc.). Defaults to "GET".
        params (Optional[Dict]): Query parameters. Defaults to None.
        headers (Optional[Dict]): HTTP headers. Defaults to None.
        retries (int): Number of retries for failed requests. Defaults to 3.
        timeout (int): Timeout for the request in seconds. Defaults to 10.

    Returns:
        Any: JSON response from the API.

    Raises:
        httpx.RequestError: If the request fails after all retries.
    """
    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                response = await client.request(
                    method=method, url=url, params=params, headers=headers, timeout=timeout
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                if attempt < retries - 1:
                    continue 
                raise e
