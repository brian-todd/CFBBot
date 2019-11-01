'''
Connector for CFB API.
'''

import requests

from typing import Optional

class CFBAPIConnector:
    '''
    API connection class.
    '''

    def __init__(self):
        self.API_BASE_URL = 'https://api.collegefootballdata.com'

    def _make_and_validate_request(self, endpoint: str, payload: Optional[dict] = {}) -> requests.Response:
        '''
        Make a request to a particular endpoint. If this method determines that
        it is a bad request, then a Requests exception will be raised.

        :params endpoint: Path to API endpoint.
        :params payload: Optional dictionary containing payload data.
        :returns resp: Requests Response object containing data recieved from the API.
        '''

        # Create custom headers.
        headers = {'accept': 'application/json'}

        # Request data from API.
        resp = requests.get(endpoint, params=payload, headers=headers)
        if not resp.status_code == requests.codes.ok:
            resp.raise_for_status()

        return resp

    def get_game(self, home_team: str, away_team: str, season: str, season_type: Optional[str] = 'regular') -> dict:
        '''
        Get an individual game based on the home team and away team.

        :params home_team: String indicating the home team for the game.
        :params home_team: String indicating the away team for the game.
        :params season: String indicating the year of the season (ex: 2019)
        :params season_type: Indicate whether it is the regular season or the post season.
        :returns resp: Dictionary containing response data for a particular game.
        '''

        # Create URL endpoint for resource.
        request_url = self.API_BASE_URL + '/games'

        # Create JSON payload.
        payload = {
        'home'          : home_team,
        'away'          : away_team,
        'year'          : season,
        'seasonType'    : season_type
        }

        resp = self._make_and_validate_request(request_url, payload)
        return resp.json()

    def get_teams_games(self, team: str, season: str, season_type: Optional[str] = 'regular') -> dict:
        '''
        Retrieve all games a team has participated in.

        :params team: String indicating the team name.
        :params season: String indicating the year of the season (ex: 2019)
        :params season_type: Indicate whether it is the regular season or the post season.
        :returns resp: Dictionary containing response data for each game in a team's season.
        '''

        # Create URL endpoint for resource.
        request_url = self.API_BASE_URL + '/games'

        # Create JSON payload.
        payload = {
        'team'          : team,
        'year'          : season,
        'seasonType'    : season_type
        }

        resp = self._make_and_validate_request(request_url, payload)
        resp = resp.json()

        # Sort data to ensure season order.
        return sorted(resp, key=lambda d: d['week'])
