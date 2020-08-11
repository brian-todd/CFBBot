"""
Connector library for async calls to /drives endpoints.
"""

from common.api.base import CFBAPIBase

from typing import Optional, Union, List, Dict, Any


class CFBAPIDrives(CFBAPIBase):
    """
    Library for connecting to /drives endpoints.
    """

    async def get_drives(
        self,
        payload: Union[dict, List[dict]],
        concurrent_tasks: Optional[int] = 10,
        sort: Optional[str] = None,
    ) -> Union[List[Dict[str, Any]], List[List[Dict[str, Any]]]]:
        """
        GET request on /drives endpoint.

        :params payload: Dictionary or list of dictionaries containing payload for endpoint.
        :params concurrent_tasks: Maximum number of tasks to be run concurrently.
        :params sort: Optionally provide a sorting key.
        :returns response: JSON response for single or multiple API calls.
        """

        return await self._get("/drives", payload, concurrent_tasks, sort)
