'''
Generic tooling functions to asist the actions.py classes.
'''

from tools.api import CFBAPIConnector

def build_current_team_database(team: str, season: str) -> dict:
    '''
    Build an in memory database of the current team. Data is sourced from
    api.collegefootballdata.com, which provides free data for college football
    games and statistics.

    NOTE: This function is written with async in mind, to prevent any blocking.

    :params team: String identifying the team we want to build a database on.
    :params season: String identifying which season we want to check.
    :returns DB: Returns an in memory database implemented as a dict.
    '''

    # Retrieve data from API.
    client = CFBAPIConnector()
    games = client.get_teams_games(team, season)

    # Create in memory database.
    DB = {}
    DB['games'] = []
    DB['record'] = {'wins' : 0, 'losses' : 0}
    DB['last_game'] = {}
    DB['next_game'] = {}

    # Iterate through response and populate database.
    for idx, game in enumerate(games):
        team_key = 'home_' if game['home_team'] == team else 'away_'
        opponent_key = 'home_' if game['away_team'] == team else 'away_'

        # Update tables.
        # Update next and last game table.
        # Determine previous games to replicate state between weeks.
        if game['home_points'] is None:
            prev = games[idx - 1]
            prev_team_key = 'home_' if prev['home_team'] == team else 'away_'
            prev_opponent_key = 'home_' if prev['away_team'] == team else 'away_'

            DB['next_game'] = {'opponent' : game[opponent_key + 'team'], 'date' : game['start_date'].split('T')[0]}
            DB['last_game'] = {
                'date'                           : prev['start_date'].split('T')[0],
                'win'                            : True if prev[prev_team_key + 'points'] > prev[prev_opponent_key + 'points'] else False,
                'opponent'                       : prev[prev_opponent_key + 'team'],
                prev[prev_team_key + 'team']     : prev[prev_team_key + 'points'],
                'opponent_score'                 : prev[prev_opponent_key + 'points']
            }

            break

        # Update complet games table.
        DB['games'].append({
            'week'                      : game['week'],
            team                        : game[team_key + 'points'],
            game[opponent_key + 'team'] : game[opponent_key + 'points']
        })

        # Update records table.
        if game[team_key + 'points'] > game[opponent_key + 'points']:
            DB['record']['wins'] += 1

        else:
            DB['record']['losses'] += 1

    return DB
