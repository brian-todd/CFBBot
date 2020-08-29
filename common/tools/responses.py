"""
Class for rendering text to the end user.
"""


class ChatBotResponseHandler:
    """
    This class is broadly responsible for handling two things:
        1- Defining the domain of chatbot responses.
        2- Providing a set of tools to operate on those responses.
    """

    def __init__(self):
        self.general_prompt = "What else can I tell you?"
        self.no_team_slot = "I'm sorry, I couldn't figure out which team you're interested in. Would you rephrase that?"

        # action_return_team_greeting
        self.team_acknowledge_init = "I can tell you all about {team}!"
        self.team_acknowledge_roulette = [
            "For example, it looks like {team} is {wins}-{losses} this year.",
            "For example, last year {team} was {wins}-{losses}.",
            "For example, {team} plays in the {conference} conference.",
            "For example, {team} plays in the {division} division in the {conference}."
            "For example, {team} is coached by {coach}.",
            "For example, {team}'s recruiting class was ranked #{recruiting_rank} in {years}.",
        ]

        # action_return_record
