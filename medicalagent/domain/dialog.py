"""Domain models for the Medical News Agent."""

from pydantic import BaseModel, Field

DEFAULT_DIALOG_TITLE = "New Dialog"


class Link(BaseModel):
    """Link domain model."""

    title: str
    url: str


class ChatMessage(BaseModel):
    """Type definition for chat message in session state."""

    role: str
    content: str


class Dialog(BaseModel):
    """Dialog domain model."""

    id: int
    user_id: int
    title: str = Field(DEFAULT_DIALOG_TITLE)
    chat_history: list[ChatMessage] = Field(
        default_factory=lambda: [
            ChatMessage(
                role="assistant",
                content="Hello! I'm your Medical Research Agent. What would you like to research today?",
            ),
        ]
    )
