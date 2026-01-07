from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.graph.state import CompiledStateGraph

from medicalagent.adapters.agent.system_prompt import SYSTEM_PROMPT
from medicalagent.config import settings


def agent_init() -> CompiledStateGraph:
    chat_model = init_chat_model(
        model="qwen/qwen3-32b",
        model_provider="groq",
        api_key=settings.AI_SETTINGS.groq_api_key.get_secret_value(),
    )
    agent: CompiledStateGraph = create_agent(
        system_prompt=SYSTEM_PROMPT, model=chat_model
    )
    return agent
