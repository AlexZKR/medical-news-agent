from abc import ABC, abstractmethod

from langchain_core.messages import AIMessage

from medicalagent.domain.dialog import ChatMessage


class AgentService(ABC):
    """Abstract interface for AI agent services."""

    @abstractmethod
    def call_agent(
        self, prompt: str, chat_history: list[ChatMessage], dialog_id: int
    ) -> list[AIMessage]:
        """Call the agent with a prompt and return the response.

        Args:
            prompt: The user's query or prompt

        Returns:
            The agent's response as a list of AIMessages
        """
        pass
