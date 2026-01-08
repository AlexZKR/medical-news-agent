from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from medicalagent.config import settings


class ConversationTitle(BaseModel):
    """Schema for the conversation title."""

    title: str = Field(
        ..., description="A concise, 3-5 word title for the conversation. No quotes."
    )


def generate_conversation_title(first_user_message: str) -> str:
    """
    Generates a concise title using the fastest available Groq model.
    """

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=settings.AI_SETTINGS.groq_api_key.get_secret_value(),
        temperature=0.3,
        max_tokens=25,
        max_retries=2,
    ).with_structured_output(ConversationTitle)

    messages = [
        SystemMessage(
            content=(
                "You are a summarization tool. "
                "Generate a static, 3-5 word title for the following user query. "
                "Do not use quotes. Do not be chatty. Just the title."
            )
        ),
        HumanMessage(content=first_user_message),
    ]

    try:
        response = llm.invoke(messages)
        return response.title
    except Exception as e:
        print(f"Failed to generate conversation title {e}")
        return "New Research"
