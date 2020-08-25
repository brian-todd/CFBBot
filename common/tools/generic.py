"""
Generic tooling functions to asist the actions.py classes.
"""

from datetime import datetime

from common.api.base import CFBAPIBase


def determine_current_season() -> str:
    """
    Determine which season should be considered the current, default season.

    :returns year: The year for the current season.
    """

    today = datetime.now()
    if today.month > 1 and today.month < 9:
        return today.year - 1

    return today.year


async def build_initial_database(team: str, year: str) -> dict:
    """
    Build an in memory database of the current team. Data is sourced from
    api.collegefootballdata.com, which provides free data for college football
    games and statistics.

    :params team: String identifying the team we want to build a database on.
    :params year: String identifying which season we want to check.
    :returns DB: In memory database containing basic season information.
    """

    api = CFBAPIBase()

    # Populate database with API data.
    endpoints = ["/games", "/records", "/coaches", "/recruiting/teams", "/stats/season"]
    payload = {"team": team, "year": year}
    response = await api.get(endpoints, payload)

    return {
        "team": team,
        "games": response["/games"],
        "record": response["/records"],
        "coach": response["/coaches"],
        "recruiting": response["/recruiting/teams"],
        "stats": response["/stats/season"],
    }


def build_roulette_data(DB: dict) -> dict:
    """
    Build dictionary of data used in initial roulette dialogue.

    :params DB: In memory database containing basic season information.
    :returns roulette_data: Dictionary containig data about the roulette text.
    """

    return {
        "team": DB["team"],
        "wins": DB["record"][0]["total"]["wins"],
        "losses": DB["record"][0]["total"]["losses"],
        "coach": DB["coach"][0]["first_name"] + " " + DB["coach"][0]["last_name"],
        "conference": DB["record"][0]["conference"],
        "division": DB["record"][0]["division"],
        "recruiting_rank": DB["recruiting"][0]["rank"],
    }
