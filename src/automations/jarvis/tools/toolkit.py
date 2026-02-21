from enum import Enum
from dataclasses import dataclass
from langchain_core.tools import Tool
from langchain_community.agent_toolkits import SlackToolkit
from langchain_community.document_loaders import (
    NotionDirectoryLoader,
    NotionDBLoader,
)
from dotenv import load_dotenv
import os


class AvailableTools(Enum):
    SLACK = SlackToolkit
    NOTION_DB = NotionDBLoader
    NOTION_DIR = NotionDirectoryLoader


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


filter_object = {
    "property": "Name",  # change if your title property has a different name
    "title": {"equals": "Graduation photos"},
}
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
loader = NotionDBLoader(
    integration_token=NOTION_TOKEN,
    database_id=NOTION_DATABASE_ID,
    request_timeout_sec=30,
    filter_object=filter_object,
)
docks = loader.load()
print(docks)
