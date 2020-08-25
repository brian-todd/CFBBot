"""
Script that pulls all available teams and prepares a file for lookups/synonyms.
"""

import argparse
import asyncio

from common.logger import logger
from common.api.teams import CFBAPITeams

LOG = logger()


async def main():
    """
    Pull data from /teams endpoint, and parse.
    """

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--path", help="Path for file writes.", type=str)
    args = arg_parser.parse_args()

    LOG.info("Fetching all teams at api.collegefootballdata.com")
    teams = CFBAPITeams()
    all_teams = await teams.get_teams({})

    LOG.info("Creating list of valid teams lookups")
    all_teams_names = []
    for team in all_teams:
        for key in ["school", "alt_name1", "alt_name2", "alt_name3"]:
            if team[key] is not None:
                all_teams_names.append(team[key])

    LOG.info(f"Writing all team names to {args.path}")
    with open(args.path, "w") as outs:
        for team in all_teams_names:
            outs.write(team + "\n")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
