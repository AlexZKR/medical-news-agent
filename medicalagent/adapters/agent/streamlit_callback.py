from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from streamlit.delta_generator import DeltaGenerator


class StreamlitStatusCallback(BaseCallbackHandler):
    """
    Updates a Streamlit placeholder with the agent's current activity.
    """

    def __init__(self, status_placeholder: DeltaGenerator):
        self.status_placeholder = status_placeholder

    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> Any:
        """Runs when the LLM starts generating."""
        self.status_placeholder.markdown("🧠 *Analyzing & Reasoning...*")

    def on_tool_start(
        self, serialized: dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Runs when a tool is triggered."""
        tool_name = serialized.get("name", "")

        if "tavily" in tool_name or "duckduck" in tool_name:
            msg = f"🌍 *Searching the web for: {input_str[:50]}...*"
        elif "openalex" in tool_name or "scholar" in tool_name:
            msg = "🎓 *Verifying with academic sources...*"
        elif "save_finding" in tool_name:
            msg = "💾 *Saving relevant finding...*"
        else:
            msg = f"🛠️ *Using tool: {tool_name}...*"

        self.status_placeholder.markdown(msg)

    def on_agent_finish(self, finish: Any, **kwargs: Any) -> Any:
        """Runs when the agent finishes."""
        self.status_placeholder.empty()
