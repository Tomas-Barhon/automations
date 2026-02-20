"""Class encapsulating different tools for AI reactive agents."""

from dataclasses import dataclass, Field
from langchain_core.tools import Tool


@dataclass
class Toolkit:
    tools: list[Tool]

    def __post_init__(self):
        if self.tools is None:
            raise ValueError("Tools must be provided to the Toolkit.")
        if not all(isinstance(tool, Tool) for tool in self.tools):
            raise ValueError("All items in tools must be instances of Tool.")
        self.tool_calls = {tool.name: tool for tool in self.tools}

    def __repr__(self):
        return f"Toolkit(tools={self.tools})"
