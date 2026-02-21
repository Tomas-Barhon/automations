from typing import Generator
from automations.jarvis.server.base_event_listener import BaseEventListener


class REPLInputListener(BaseEventListener):
    """
    Listens for user input from the command line (REPL).
    """

    def listen_for_input(self) -> str:
        user_input = input("You: ")
        return user_input
