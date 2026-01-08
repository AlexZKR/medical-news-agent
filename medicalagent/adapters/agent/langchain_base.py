from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph.state import CompiledStateGraph

from medicalagent.adapters.agent.system_prompt import SYSTEM_PROMPT
from medicalagent.config import settings
from medicalagent.ports.agent import AgentService


class LangChainAgentService(AgentService):
    """LangChain-based implementation of the AgentService."""

    def __init__(self):
        """Initialize the agent service with the LangChain agent."""
        self._agent = self._create_agent()

    def _create_agent(self) -> CompiledStateGraph:
        """Create and configure the LangChain agent."""
        chat_model = ChatGroq(
            model_name="qwen/qwen3-32b",
            temperature=0,
            max_tokens=None,
            reasoning_format="hidden",
            timeout=None,
            max_retries=2,
            api_key=settings.AI_SETTINGS.groq_api_key.get_secret_value(),
        )

        agent: CompiledStateGraph = create_agent(
            system_prompt=SystemMessage(SYSTEM_PROMPT), model=chat_model
        )
        return agent

    def call_agent(self, prompt: str) -> list[AIMessage]:
        """Call the agent with a prompt and return the cleaned response."""
        try:
            message = HumanMessage(prompt)
            result = self._agent.invoke(message)
            messages = [msg for msg in result["messages"]]
            return messages

        except Exception as e:
            error_message = (
                f"Sorry, I encountered an error while researching your query: {str(e)}"
            )
            return [AIMessage(content=error_message)]
