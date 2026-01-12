import uuid

from langchain_core.tools import tool
from langgraph.prebuilt.tool_node import ToolRuntime
from pydantic import BaseModel, Field

from medicalagent.adapters.agent.langchain_base import AgentContext
from medicalagent.domain.dialog import Link
from medicalagent.domain.finding import Finding


class SaveFindingInput(BaseModel):
    """Input schema for saving a finding."""

    title: str = Field(description="Headline of the finding.")
    source: str = Field(description="Main source name (e.g., 'Nature', 'CNN').")
    relevance_reason: str = Field(
        description="One sentence explaining why this specifically answers the user's query."
    )
    citations: int = Field(
        default=0, description="Citation count from academic paper (if available)."
    )
    websites: int = Field(
        default=1,
        description="Number of distinct sources/websites found for this item.",
    )
    news_urls: list[str] = Field(
        default_factory=list, description="List of URLs for news articles found."
    )
    paper_urls: list[str] = Field(
        default_factory=list, description="List of URLs/DOIs for academic papers found."
    )


@tool("save_finding_tool", args_schema=SaveFindingInput)
def save_finding_tool(
    runtime: ToolRuntime[AgentContext],
    title: str,
    source: str,
    relevance_reason: str,
    citations: int = 0,
    websites: int = 1,
    news_urls: list[str] | None = None,
    paper_urls: list[str] | None = None,
) -> str:
    """
    Saves a verified medical finding to the side panel.
    Call this for EVERY relevant result you find before generating the final answer.
    """

    # 1. Validation
    dialog_id = runtime.context.dialog_id
    if dialog_id is None:
        return "Error: No active dialog. Cannot save finding."

    # 2. Convert URLs to Link Domain Objects
    # (The agent gives simple URLs, we wrap them for the UI)
    news_links_objects = [
        Link(title=f"News Source {i + 1}", url=url)
        for i, url in enumerate(news_urls or [])
    ]

    paper_links_objects = [
        Link(title=f"Paper Source {i + 1}", url=url)
        for i, url in enumerate(paper_urls or [])
    ]

    # 3. Create Domain Object
    new_finding = Finding(
        id=str(uuid.uuid4()),
        dialog_id=int(dialog_id),  # Ensure int matches your model
        title=title,
        source=source,
        relevance_reason=relevance_reason,
        citations=citations,
        websites=websites,
        status="new",
        non_relevance_mark=False,
        news_links=news_links_objects,
        paper_links=paper_links_objects,
    )

    # 4. Save
    runtime.context.container.findings_repository.save(new_finding)

    return f"Success: Saved finding '{title}' to sidebar."
