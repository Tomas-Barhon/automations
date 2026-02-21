from automations.jarvis.server.base_event_listener import BaseEventListener


class OutputPrinter(BaseEventListener):
    """
    Listens for agent output events and prints them to the console.
    """

    def listen_for_input(self):
        # This listener doesn't listen for input, so we can just pass here.
        pass

    def print_output(self, message: str):
        print(f"Agent: {message}")
