from logging import getLogger

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ClearToolUsesEdit,
    ContextEditingMiddleware,
    ModelFallbackMiddleware,
    SummarizationMiddleware,
)
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel.main import RunnableConfig

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

logger = getLogger(__name__)


class LangChainAgentService(AgentService):
    """LangChain-based implementation of the AgentService."""

    def __init__(self, container):
        """Initialize the agent service with the LangChain agent."""
        self._agent = self._create_agent()
        self.container = container

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

        primary_model = ChatGroq(
            model_name=settings.AI_SETTINGS.primary_model,
            temperature=0,
            max_tokens=settings.AI_SETTINGS.primary_model_max_tokens,
            timeout=None,
            max_retries=3,
            api_key=settings.AI_SETTINGS.groq_api_key.get_secret_value(),
        )

        fallback_model = ChatGroq(
            model_name=settings.AI_SETTINGS.fallback_model,
            temperature=0,
            max_tokens=settings.AI_SETTINGS.fallback_model_max_tokens,
            timeout=None,
            max_retries=3,
            api_key=settings.AI_SETTINGS.groq_api_key.get_secret_value(),
        )

        summarization_model = ChatGroq(
            model_name=settings.AI_SETTINGS.summarization_model,
            temperature=0,
            max_tokens=settings.AI_SETTINGS.summarization_model_max_tokens,
            timeout=None,
            max_retries=3,
            api_key=settings.AI_SETTINGS.groq_api_key.get_secret_value(),
        )

        agent: CompiledStateGraph = create_agent(
            system_prompt=SystemMessage(SYSTEM_PROMPT),
            model=primary_model,
            tools=[
                get_tavily(),
                save_finding_tool,
                duckducksearch_tool,
                semantic_scholar_tool,
                openalex_search_tool,
            ],
            context_schema=AgentContext,
            middleware=[
                ModelFallbackMiddleware(first_model=fallback_model),
                ContextEditingMiddleware(
                    edits=[
                        ClearToolUsesEdit(
                            trigger=4000,
                            keep=4,
                            clear_tool_inputs=False,
                            exclude_tools=[],
                        ),
                    ],
                ),
                SummarizationMiddleware(
                    model=summarization_model,
                    trigger=[
                        ("tokens", 6000),
                        ("messages", 6),
                    ],
                    keep=("messages", 20),
                ),
            ],
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
            config = RunnableConfig(
                tags=[settings.APP_SETTINGS.ENV],
                metadata={
                    "env": settings.APP_SETTINGS.ENV,
                    "dialog_id": dialog_id,
                },
            )

            # 3. INVOKE
            result = self._agent.invoke(
                {"messages": messages_payload},
                context=AgentContext(container=self.container, dialog_id=dialog_id),
                config=config,
            )
            return [result["messages"][-1]]

        except Exception as e:
            logger.error(
                f"CRITICAL AGENT FAILURE | Dialog ID: {dialog_id} | Error: {str(e)}",
                exc_info=True,
            )

            error_message = (
                f"⚠️ **An internal error occurred.**\n\n"
                f"Please share this **Dialog ID** with support so we can fix it:\n"
                f"**`{dialog_id}`**"
            )
            return [AIMessage(content=error_message)]
