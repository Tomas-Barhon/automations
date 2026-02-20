"""Class encapsulating different tools for AI reactive agents."""

from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchResults


class Toolset:
    def __init__(self) -> None:
        # prebuilt tools from langchain
        self.search_duck_duck_go = DuckDuckGoSearchResults()
        self.tools = [
            Tool(
                name="Search",
                func=self.search_duck_duck_go.run,
                description="useful for when you need to answer questions \
                about current events",
            )
        ]

    def get_tools(self):
        return self.tools
