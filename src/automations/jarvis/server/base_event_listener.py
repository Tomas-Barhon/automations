from abc import ABC, abstractmethod
from typing import Generator


class BaseEventListener(ABC):
    """
    Abstract base listener for detecting agent inputs.
    Subclasses implement `listen_for_input` to yield input events.
    """

    @abstractmethod
    def listen_for_input(self) -> Generator[str, None, None]:
        """
        Yield AgentInput objects whenever input is detected.
        """
        ...
