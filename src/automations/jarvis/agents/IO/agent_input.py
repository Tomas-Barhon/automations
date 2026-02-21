from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentInput:
    """
    Represents an input event for an agent.
    """

    role: str
    content: str
    config: Optional[dict] = None
    thread_id: Optional[str] = None
    metadata: Optional[dict] = None
