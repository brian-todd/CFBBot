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
    validate_input,
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
        recruiting = tracker.get_slot("recruiting")
        stats = tracker.get_slot("stats")

        # Validate basic inputs.
        if team is None:
            dispatcher.utter_message(text.no_team_slot)

        if year is None:
            year = determine_current_season()

        if not all([games, record, coach, recruiting, stats]):
            DB = await build_initial_database(team, year)
            record = DB["record"]

        if team != record[0]["team"]:
            DB = await build_initial_database(team, year)

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
            SlotSet("recruiting", DB["recruiting"]),
            SlotSet("stats", DB["stats"]),
        ]


class ActionReturnRecord(Action):
    """
    Report back the score of the requested game.
    """

    def name(self) -> Text:
        return "action_return_record"

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
        record = tracker.get_slot("record")

        # Validate basic inputs.
        if team is None:
            dispatcher.utter_message(text.no_team_slot)

        if year is None:
            year = determine_current_season()

        # If the record is not present, refresh the database
        _slots_to_be_set = []
        if not all([record]):
            DB = await build_initial_database(team, year)
            record = DB["record"]
            _slots_to_be_set = [
                SlotSet("games", DB["games"]),
                SlotSet("record", record),
                SlotSet("coach", DB["coach"]),
                SlotSet("recruiting", DB["recruiting"]),
                SlotSet("stats", DB["stats"]),
            ]

        wins = record[0]["total"]["wins"]
        losses = record[0]["total"]["losses"]
        dispatcher.utter_message(f"{team} was {wins}-{losses} during {year}")

        return _slots_to_be_set
