from typing import Iterable, Optional
from langchain_core.tools import Tool
from langchain_community.document_loaders import (
    NotionDBLoader,
    WeatherDataLoader,
)
import os


def create_notion_tool(name: str = "NotionDB") -> Tool:
    loader = NotionDBLoader(
        integration_token=os.getenv("NOTION_TOKEN", ""),
        database_id=os.getenv("NOTION_DATABASE_ID", ""),
    )

    def notion_fetch(query: str) -> str:
        """Simple fetch function: returns all matching documents as string."""
        docs = loader.load()
        # Optional: filter by query substring in title or content
        matching_docs = [
            doc.page_content
            for doc in docs
            if query.lower() in doc.page_content.lower()
        ]
        return (
            "\n".join(matching_docs)
            if matching_docs
            else "No matching documents found."
        )

    return Tool(
        name=name,
        func=notion_fetch,
        description="Fetch documents from Notion DB matching a query string",
    )


def create_weather_tool(
    name: str = "Weather", location: Optional[Iterable[str]] = None
) -> Tool:
    if location is None:
        location = ["Prague"]
    location = list(location)
    loader = WeatherDataLoader.from_params(
        location,
        openweathermap_api_key=os.getenv("OPENWEATHERMAP_API_KEY", ""),
    )

    def weather_fetch() -> str:
        """Fetch current weather info for a location."""
        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])

    return Tool(
        name=name,
        func=weather_fetch,
        description="Fetches current weather information for a given location",
    )
