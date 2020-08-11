"""
Connector library for async calls https://api.collegefootballdata.com
"""

import aiohttp
import asyncio

from typing import Optional, Union, List, Dict, Any

from common.errors import CFBBotTypeMismatchError, CFBBotAPIStatusCodeError


class CFBAPIBase:
    """
    API connection class.
    """

    def __init__(self):
        self.API_BASE_URL = "https://api.collegefootballdata.com"
        self.headers = {"accept": "application/json"}

    async def _make_and_validate_request(
        self,
        session: aiohttp.ClientSession,
        semaphore: asyncio.Semaphore,
        endpoint: str,
        payload: Optional[dict] = {},
    ) -> List[Dict[str, Any]]:
        """
        Make an async request on an endpoint and payload pair.

        :params session: Session context manager for aiohttp.
        :params semaphore: Async Semaphore for managing number of conccurent connections.
        :params endpoint: Path to API endpoint.
        :params payload: Optional dictionary containing payload data.
        :returns response: Requests Response object containing data recieved from the API.
        """

        full_path_to_resource = self.API_BASE_URL + endpoint
        async with semaphore:
            async with session.get(
                full_path_to_resource, params=payload, headers=self.headers
            ) as response:
                if response.status == 200:
                    return await response.json()

                else:
                    raise CFBBotAPIStatusCodeError(
                        "Invalid status code {code}. Error: {error}",
                        {"code": resp.status, "error": resp.text()},
                    )

    async def _get(
        self,
        endpoint: Union[str, List[str]],
        payload: Union[dict, List[dict]],
        concurrent_tasks: Optional[int] = 10,
        sort: Optional[str] = None,
    ) -> Union[List[Dict[str, Any]], List[List[Dict[str, Any]]]]:
        """
        Make one or more async GET requests to the API.

        :params endpoint: String or list of strings indicating the relevant resource endpoint.
        :params payload: Dictionary or list of dictionaries containing payload for endpoint.
        :params concurrent_tasks: Maximum number of tasks to be run concurrently.
        :params sort: Optionally provide a sorting key.
        :returns response: JSON response for single or multiple API calls.
        """

        # Semaphore to limimt number of concurrent tasks.
        semaphore = asyncio.Semaphore(concurrent_tasks)

        # There are two paths here:
        # 1- If there are multiple tuples, then perform multiple concurrent requests.
        # 2- If there is one tuple, then perform a single async request.
        # However if none of those paths are matched then throw an error.
        async with aiohttp.ClientSession() as session:
            if isinstance(endpoint, list) and isinstance(payload, list):
                tasks = []
                for _endpoint, _payload in zip(endpoint, payload):
                    task = asyncio.ensure_future(
                        self._make_and_validate_request(
                            session, semaphore, _endpoint, _payload
                        )
                    )
                    tasks.append(task)

                return await asyncio.gather(*tasks)

            elif isinstance(endpoint, str) and isinstance(payload, dict):
                return await self._make_and_validate_request(
                    session, semaphore, endpoint, payload
                )

            else:
                raise CFBBotTypeMismatchError(
                    "endpoint[{endpoint_t}] and payload[{payload_t}] are not compatible.",
                    {"endpoint_t": type(endpoint), "payload_t": {type(payload)}},
                )
