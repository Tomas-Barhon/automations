from dataclasses import dataclass
from typing import Optional


# TODO Refactor to smth real
@dataclass
class AgentOutput:
    """
    Represents the output of an agent's action.

    Attributes:
        success (bool): Indicates whether the action was successful.
        message (str): A message describing the result of the action.
        data (dict): Additional data related to the action's output.
    """

    success: bool
    message: str
    data: Optional[dict] = None
