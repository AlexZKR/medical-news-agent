from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx


class StreamlitStatusCallback(BaseCallbackHandler):
    """
    Updates a Streamlit placeholder with the agent's current activity.
    """

    THINKING_PROMPTS = [
        "🧠 Analyzing clinical data",
        "🧬 Synthesizing medical insights",
        "🔬 Connecting research dots",
        "🛰️ Navigating the medical knowledge graph",
        "🧪 Evaluating scientific evidence",
        "📖 Cross-referencing journals",
        "🔍 Reframing the research strategy",
        "🤖 Processing complex correlations",
    ]

    def __init__(self, status_placeholder: DeltaGenerator):
        self.status_placeholder = status_placeholder
        self.ctx = get_script_run_ctx()

    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> Any:
        """Runs when the LLM starts generating."""
        if self.ctx:
            add_script_run_ctx(ctx=self.ctx)

        # Safely extract the step number
        metadata = kwargs.get("metadata") or {}
        step = metadata.get("langgraph_step", 0)

        # Select a prompt based on the step number to ensure variety
        # but consistency if the same step is re-run
        prompt_index = step % len(self.THINKING_PROMPTS)
        selected_prompt = self.THINKING_PROMPTS[prompt_index]

        self.status_placeholder.markdown(f"{selected_prompt}... **(Step {step})**")

    def on_tool_start(
        self, serialized: dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Runs when a tool is triggered."""
        if self.ctx:
            add_script_run_ctx(ctx=self.ctx)
        tool_name = serialized.get("name", "")

        if "tavily" in tool_name or "duckduck" in tool_name:
            # Try to get the specific query from inputs if available
            inputs = kwargs.get("inputs") or {}
            query_msg = inputs.get("query") or input_str[:100]
            msg = f"🌍 *Searching the web for: {query_msg}*"
        elif "openalex" in tool_name or "scholar" in tool_name:
            msg = "🎓 *Verifying evidence with academic databases...*"
        elif "save_finding" in tool_name:
            msg = "💾 *Archiving verified finding to sidebar...*"
        else:
            msg = f"🛠️ *Executing {tool_name}...*"

        self.status_placeholder.markdown(msg)

    def on_agent_finish(self, finish: Any, **kwargs: Any) -> Any:
        """Runs when the agent finishes."""
        if self.ctx:
            add_script_run_ctx(ctx=self.ctx)
        self.status_placeholder.empty()
