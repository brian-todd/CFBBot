'''
Custom actions for handling response.
'''

from tools.tools import build_current_team_database

from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionReturnTeamGreeting(Action):
    '''
    Determine which team we want to know about.
    '''

    def name(self) -> Text:
        return 'action_return_team_greeting'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        '''
        Determine which score to use and return the game data.
        '''

        # Pull out the team from our current state.
        team = tracker.get_slot('team')

        # Pull the relevant team data and construct DB.
        DB = build_current_team_database(team, 2019)

        # Construct response.
        response = {
            'Michigan'          : 'Go Blue!',
            'Ohio State'        : 'Go Bucks!',
            'Michigan State'    : 'Go Green! Go White!'
        }
        dispatcher.utter_message(f'I can tell you all about how {team} is doing this season!')
        dispatcher.utter_message(response[team])

        return [
            SlotSet('wins', str(DB['record']['wins'])),
            SlotSet('losses', str(DB['record']['losses'])),
            SlotSet('next_opponent', DB['next_game']['opponent']),
            SlotSet('next_opponent_date', DB['next_game']['date']),
            SlotSet('last_opponent', DB['last_game']['opponent']),
            SlotSet('last_opponent_date', DB['last_game']['date']),
            SlotSet('last_opponent_score', DB['last_game']['opponent_score']),
            SlotSet('last_team_score', DB['last_game'][team]),
            SlotSet('last_outcome', DB['last_game']['win'])
        ]

class ActionReturnRecord(Action):
    '''
    Report back the score of the requested game.
    '''

    def name(self) -> Text:
        return 'action_return_record'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        '''
        Determine which score to use and return the game data.
        '''

        team = tracker.get_slot('team')
        wins = tracker.get_slot('wins')
        losses = tracker.get_slot('losses')
        dispatcher.utter_message(f'{team} is {wins}-{losses}')

        return []

class ActionReturnLastOpponent(Action):
    '''
    Report back the score of the requested game.
    '''

    def name(self) -> Text:
        return 'action_return_last_opponent'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        '''
        Determine which score to use and return the game data.
        '''

        last_opponent = tracker.get_slot('last_opponent')
        last_opponent_date = tracker.get_slot('last_opponent_date')

        dispatcher.utter_message(f'The last game was against {last_opponent} on {last_opponent_date}')

        return []

class ActionReturnLastGame(ActionReturnLastOpponent):
    '''
    Report back the score of the requested game.
    '''

    def name(self) -> Text:
        return 'action_return_last_game'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        '''
        Determine which score to use and return the game data.
        '''

        team = tracker.get_slot('team')
        last_opponent = tracker.get_slot('last_opponent')
        last_opponent_date = tracker.get_slot('last_opponent_date')
        last_opponent_score = tracker.get_slot('last_opponent_score')
        last_team_score = tracker.get_slot('last_team_score')
        last_outcome = tracker.get_slot('last_outcome')

        if last_outcome:
            dispatcher.utter_message(f'{team} beat {last_opponent} {last_team_score}-{last_opponent_score} on {last_opponent_date}')

        else:
            dispatcher.utter_message(f'{team} lost to {last_opponent} {last_team_score}-{last_opponent_score} on {last_opponent_date}')

        return []

class ActionReturnNextOpponent(Action):
    '''
    Report back the score of the requested game.
    '''

    def name(self) -> Text:
        return 'action_return_next_opponent'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        '''
        Write text string for next opponent.
        '''

        team = tracker.get_slot('team')
        next_opponent = tracker.get_slot('next_opponent')
        next_opponent_date = tracker.get_slot('next_opponent_date')

        dispatcher.utter_message(f'{team} plays {next_opponent} on {next_opponent_date}')

        return []

