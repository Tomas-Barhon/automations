from email_connector.interfaces.polling_service import PollingServiceInterface
from email_connector.interfaces.connector import EmailConnector
from email_connector.interfaces.models import EmailMessage
from typing import Dict, Any


class EmailPollingServiceInterface(PollingServiceInterface):
    """Outlook-specific implementation of the email polling service."""

    def __init__(self, connector: EmailConnector):
        self.connector = connector

    def poll_emails(self) -> list[EmailMessage] | None:
        """Poll for new emails from Outlook."""
        emails_list = []

        if self.connector.connect():
            try:
                # TODO: implement email polling logic
                emails_list = self.connector.get_messages(
                    folder_id="inbox", limit=10
                )
                pass
            finally:
                self.connector.disconnect()

        if len(emails_list) == 0:
            return None
        return emails_list

    def _load_state(self):
        """Load the polling state specific to Outlook."""
        # Implementation for loading state
        pass

    def _save_state(self, state: Dict[str, Any]):
        """Save the polling state specific to Outlook."""
        # Implementation for saving state
        pass
