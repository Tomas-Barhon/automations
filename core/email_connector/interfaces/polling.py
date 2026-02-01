from abc import ABC, abstractmethod


class PollingServiceInterface(ABC):
    """Interface for email polling services."""

    @abstractmethod
    def poll_emails(self):
        """Poll for new emails."""
        pass

    @abstractmethod
    def _load_state(self):
        """Load the polling state."""
        pass

    @abstractmethod
    def _save_state(self):
        """Save the polling state."""
        pass
