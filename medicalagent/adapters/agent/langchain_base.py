from logging import getLogger

from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from langgraph.graph.state import CompiledStateGraph

from medicalagent.adapters.agent.system_prompt import SYSTEM_PROMPT
from medicalagent.adapters.agent.tools.semantic_scholar_search import (
    semantic_scholar_tool,
)
from medicalagent.adapters.agent.tools.tavilysearch import get_tavily
from medicalagent.config import settings
from medicalagent.domain.dialog import ChatMessage
from medicalagent.ports.agent import AgentService

logger = getLogger(__name__)


class LangChainAgentService(AgentService):
    """LangChain-based implementation of the AgentService."""

    def __init__(self):
        """Initialize the agent service with the LangChain agent."""
        self._agent = self._create_agent()

    def _map_history_to_langchain(self, history: list[ChatMessage]) -> list:
        """Converts internal chat history to LangChain format."""
        lc_messages: list[HumanMessage | AIMessage] = []
        for msg in history:
            if msg.role == "user":
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                lc_messages.append(AIMessage(content=msg.content))
        return lc_messages

    def _create_agent(self) -> CompiledStateGraph:
        """Create and configure the LangChain agent."""
        duckducksearch_tool = DuckDuckGoSearchRun()

        chat_model = ChatGroq(
            model_name="qwen/qwen3-32b",
            temperature=0,
            max_tokens=None,
            # reasoning_format="hidden",
            timeout=None,
            model_kwargs={"include_reasoning": False},
            max_retries=2,
            api_key=settings.AI_SETTINGS.groq_api_key.get_secret_value(),
        )

        agent: CompiledStateGraph = create_agent(
            system_prompt=SystemMessage(SYSTEM_PROMPT),
            model=chat_model,
            tools=[
                get_tavily(),
                duckducksearch_tool,
                semantic_scholar_tool,
            ],
        )
        return agent

    def call_agent(
        self, prompt: str, chat_history: list[ChatMessage]
    ) -> list[AIMessage]:
        """Call the agent with a prompt and return the cleaned response."""
        try:
            messages_payload = self._map_history_to_langchain(chat_history)
            messages_payload.append(HumanMessage(prompt))
            result = self._agent.invoke({"messages": messages_payload})
            return [result["messages"][-1]]

        except Exception as e:
            return [AIMessage(content=f"Error: {str(e)}")]
