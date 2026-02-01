from abc import ABC, abstractmethod
from typing import Dict, Any


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
    def _save_state(self, state: Dict[str, Any]):
        """Save the polling state."""
        pass
