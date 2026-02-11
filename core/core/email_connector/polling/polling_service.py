import json
from datetime import datetime
from typing import Any, Dict

from email_connector.interfaces.connector import EmailConnector
from email_connector.interfaces.models import EmailMessage
from email_connector.interfaces.polling import PollingServiceInterface


class EmailPollingServiceInterface(PollingServiceInterface):
    """Outlook-specific implementation of the email polling service."""

    STATE_FILE = "outlook_polling_state.json"

    def __init__(self, connector: EmailConnector):
        self._connector = connector
        self._state: datetime | None = None
        self._new_state: datetime | None = None

    def poll_emails(self) -> list[EmailMessage] | None:
        """Poll for new emails from Outlook."""
        emails_list = []

        if self._connector.connect():
            try:
                # TODO: implement email polling logic
                emails_list = self._connector.get_messages(
                    folder_id="inbox", limit=10
                )
            finally:
                self._connector.disconnect()

        if len(emails_list) == 0:
            return None
        return emails_list

    def _load_state(self) -> datetime | None:
        """Load the last polling date"""
        if self._state is None:
            try:
                with open(self.STATE_FILE, "r") as state_file:
                    self._state = self._parse_state(json.load(state_file))

            except FileNotFoundError:
                # TODO: implement better fallback when no state
                return None
            return self._state

    def _save_state(self) -> datetime | None:
        """Save the current polling date to statefile"""
        self._new_state = datetime.utcnow()

        with open(self.STATE_FILE, "w") as state_file:
            json.dump({"state": self._new_state.isoformat()}, state_file)
        return self._new_state

    def _parse_state(self, state_data: Dict[str, Any]) -> datetime | None:
        """Parse the polling state data from JSON."""
        state_str = state_data.get("state")
        if state_str:
            return datetime.fromisoformat(state_str)
        return None
