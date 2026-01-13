import streamlit as st

from medicalagent.domain.finding import Finding
from medicalagent.drivers.right_sidebar.result_card import render_result_card

# Container Heights
RESULT_LIST_HEIGHT = 800  # pixels

# Empty State Messages
EMPTY_FINDINGS_MESSAGE = "No findings yet. Start a chat to search."
EMPTY_FINDINGS_CAPTION = "Results from your research will appear here."


def render_result_list_empty() -> None:
    """Renders the empty state of the result list."""
    st.info(EMPTY_FINDINGS_MESSAGE)
    st.caption(EMPTY_FINDINGS_CAPTION)


def render_result_list(research_results: list[Finding]) -> None:
    """Renders the list of research findings."""

    if not research_results:
        render_result_list_empty()
        return

    with st.container(border=False, height=RESULT_LIST_HEIGHT):
        for i, item in enumerate(reversed(research_results)):
            render_result_card(item, key_suffix=str(i))
