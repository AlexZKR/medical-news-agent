from medicalagent.domain.dialog import Link
from pydantic import BaseModel, Field


class Finding(BaseModel):
    """Finding domain model."""

    id: int
    dialog_id: int
    title: str
    source: str
    relevance_reason: str
    citations: int
    websites: int
    status: str
    non_relevance_mark: bool = Field(
        default=False,
        description="User marks this as non_relevant, which means, that this finding must be used to narrow down the search (exclude similar results)",
    )
    news_links: list[Link]
    paper_links: list[Link]
