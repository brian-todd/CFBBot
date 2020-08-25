"""
Custom actions for handling response.
"""

import asyncio
import random

from common.api.games import CFBAPIGames
from common.tools.generic import (
    determine_current_season,
    build_initial_database,
    build_roulette_data,
)
from common.tools.responses import ChatBotResponseHandler

from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from pprint import pprint

text = ChatBotResponseHandler()


class ActionReturnTeamGreeting(Action):
    """
    Determine which team we want to know about.
    """

    def name(self) -> Text:
        return "action_return_team_greeting"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """
        Determine which score to use and return the game data.
        """

        # Pull the relevant team and season year.
        team = tracker.get_slot("team")
        year = tracker.get_slot("year")
        games = tracker.get_slot("games")
        record = tracker.get_slot("record")
        coach = tracker.get_slot("coach")

        if team is None:
            dispatcher.utter_message(text.no_team_slot)

        if year is None:
            year = determine_current_season()

        # Build the initial database if them team is not set.
        if not (games and record and coach):
            DB = await build_initial_database(team, year)

        # TODO: Implement logic for when the team slot differs from the in memory DB.

        # Dispatch team acknowledgement text responses.
        resp = text.team_acknowledge_init.format(**{"team": team})
        dispatcher.utter_message(resp)

        roulette_data = build_roulette_data(DB)
        resp = random.choice(text.team_acknowledge_roulette).format(**roulette_data)
        dispatcher.utter_message(resp)

        return [
            SlotSet("team", team),
            SlotSet("year", year),
            SlotSet("games", DB["games"]),
            SlotSet("record", DB["record"]),
            SlotSet("coach", DB["coach"]),
        ]


class ActionReturnRecord(Action):
    """
    Report back the score of the requested game.
    """

    def name(self) -> Text:
        return "action_return_record"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """
        Determine which score to use and return the game data.
        """

        team = tracker.get_slot("team")
        record = tracker.get_slot("record")
        dispatcher.utter_message(f"{team} is {wins}-{losses}")

        return []
