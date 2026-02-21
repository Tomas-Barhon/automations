from enum import Enum
from dataclasses import dataclass
from langchain_core.tools import Tool
from langchain_community.agent_toolkits import SlackToolkit, O365Toolkit
from langchain_community.document_loaders import (
    NotionDBLoader,
    WeatherDataLoader,
)
from langchain_google_community import CalendarToolkit
from dotenv import load_dotenv
from automations.jarvis.tools.tool_wrappers import (
    create_notion_tool,
    create_weather_tool,
)


class AvailableToolkits(Enum):
    SLACK = SlackToolkit
    CALENDAR = CalendarToolkit
    OUTLOOK = O365Toolkit


TOOL_REGISTRY = {
    "NOTION_DB": create_notion_tool,
    "WEATHER": create_weather_tool,
}


class AvailableLoaders(Enum):
    NOTION_DB = NotionDBLoader
    WEATHER = WeatherDataLoader


@dataclass
class AgentTools:
    tools: list[Tool]

    def __post_init__(self):
        if self.tools is None:
            raise ValueError("Tools must be provided to the Toolkit.")
        if not all(isinstance(tool, Tool) for tool in self.tools):
            raise ValueError("All items in tools must be instances of Tool.")
        self.tool_calls = {tool.name: tool for tool in self.tools}

    def __repr__(self):
        return f"Toolkit(tools={self.tools})"

    # NOTE: Consider tool specific kwargs
    @classmethod
    def from_tool_names(
        cls, tool_names: list[str], **tool_kwargs
    ) -> "AgentTools":
        load_dotenv()
        tools = []
        # TODO: add kwargs support for tools that require it
        for name in tool_names:
            if name in AvailableToolkits.__members__:
                toolkit_class = AvailableToolkits[name].value
                tools.extend(toolkit_class(**tool_kwargs).get_tools())
            elif name in TOOL_REGISTRY:
                tool_func = TOOL_REGISTRY[name]
                tool = tool_func(name=name, **tool_kwargs)
                tools.append(tool)
            else:
                raise ValueError(f"Unsupported tool class or func: {name}")
        return cls(tools=tools)
