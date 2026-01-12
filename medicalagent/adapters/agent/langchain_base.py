from logging import getLogger
from typing import TYPE_CHECKING

from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from langgraph.graph.state import CompiledStateGraph

from medicalagent.adapters.agent.schemas import AgentContext
from medicalagent.adapters.agent.system_prompt import SYSTEM_PROMPT
from medicalagent.adapters.agent.tools.openalex_search_tool import openalex_search_tool
from medicalagent.adapters.agent.tools.save_finding_tool import save_finding_tool
from medicalagent.adapters.agent.tools.semantic_scholar_search import (
    semantic_scholar_tool,
)
from medicalagent.adapters.agent.tools.tavilysearch import get_tavily
from medicalagent.config import settings
from medicalagent.domain.dialog import ChatMessage
from medicalagent.ports.agent import AgentService

if TYPE_CHECKING:
    from medicalagent.drivers.di import DIContainer
logger = getLogger(__name__)


class LangChainAgentService(AgentService):
    """LangChain-based implementation of the AgentService."""

    def __init__(self, container: "DIContainer"):
        """Initialize the agent service with the LangChain agent."""
        self._agent = self._create_agent()
        self._container = container

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
            model_name=settings.AI_SETTINGS.main_model,
            temperature=0,
            max_tokens=None,
            # reasoning_format="hidden",
            timeout=None,
            # model_kwargs={"include_reasoning": False},
            max_retries=2,
            api_key=settings.AI_SETTINGS.groq_api_key.get_secret_value(),
        )

        agent: CompiledStateGraph = create_agent(
            system_prompt=SystemMessage(SYSTEM_PROMPT),
            model=chat_model,
            tools=[
                get_tavily(),
                save_finding_tool,
                duckducksearch_tool,
                semantic_scholar_tool,
                openalex_search_tool,
            ],
            context_schema=AgentContext,
        )
        return agent

    def call_agent(
        self, prompt: str, chat_history: list[ChatMessage], dialog_id: int
    ) -> list[AIMessage]:
        try:
            # 1. GENERATE CONTEXT FROM FINDINGS # TODO: MAKE A MIDDLEWARE
            from medicalagent.drivers.di import di_container
            from medicalagent.drivers.st_state import session_state

            findings_context = ""
            if session_state.active_dialog_id:
                # Fetch findings
                findings = di_container.findings_repository.get_by_dialog_id(
                    session_state.active_dialog_id
                )

                # A. Blacklist Context (Items marked non-relevant)
                blacklist = [f for f in findings if f.non_relevance_mark]
                if blacklist:
                    findings_context += "\n\n🚫 EXCLUSION LIST (User marked these as IRRELEVANT - Do NOT suggest similar):"
                    for f in blacklist:
                        findings_context += (
                            f"\n- {f.title} (Reason: {f.relevance_reason})"
                        )

                # B. Recap Context (Items already found)
                existing = [f for f in findings if not f.non_relevance_mark]
                if existing:
                    findings_context += (
                        "\n\n✅ EXISTING FINDINGS (Already found - Do not duplicate):"
                    )
                    for f in existing:
                        findings_context += f"\n- {f.title}"

            # 2. PREPARE MESSAGES
            messages_payload = self._map_history_to_langchain(chat_history)

            # Inject context if we have it
            if findings_context:
                # Add as a System Message at the very end to ensure high attention
                messages_payload.append(
                    SystemMessage(content=f"SYSTEM CONTEXT UPDATE:{findings_context}")
                )

            messages_payload.append(HumanMessage(content=prompt))

            # 3. INVOKE
            result = self._agent.invoke(
                {"messages": messages_payload},
                context=AgentContext(container=self.container, dialog_id=dialog_id),
            )
            return [result["messages"][-1]]

        except Exception as e:
            return [AIMessage(content=f"Error: {str(e)}")]
