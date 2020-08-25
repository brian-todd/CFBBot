"""
Custom exception handling.
"""

from typing import Optional


class CFBBotException(Exception):
    """
    Base exception class.
    """

    def __init__(self, message: Optional[str] = None, payload: Optional[dict] = None):
        self.message = message
        self.payload = payload

    def __str__(self):
        return str(self.message.format(**self.payload))


class CFBBotTypeMismatchError(CFBBotException):
    """
    Exception encountered when types are incorrectly mixed.
    """

    pass


class CFBBotAPIStatusCodeError(CFBBotException):
    """
    Exception encountered when types are incorrectly mixed.
    """

    pass
