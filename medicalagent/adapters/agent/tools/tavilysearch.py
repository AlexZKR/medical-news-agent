from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

from medicalagent.config import settings


class TavilySearchInput(BaseModel):
    query: str = Field(description="The search query to look up medical news.")


def get_tavily() -> TavilySearch:
    tavily_search_tool = TavilySearch(
        tavily_api_key=settings.AI_SETTINGS.tavily_api_key.get_secret_value(),
        max_results=5,
        topic="news",
        include_answer=True,
        search_depth="basic",
        include_raw_content=False,
        time_range="month",
    )
    tavily_search_tool.args_schema = TavilySearchInput
    tavily_search_tool.description = "Search for recent medical news and studies."
    return tavily_search_tool
