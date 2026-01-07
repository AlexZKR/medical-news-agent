import streamlit as st

from medicalagent.domain.dialog import Finding
from medicalagent.drivers.right_sidebar.result_card import render_result_card

# Container Heights
RESULT_LIST_HEIGHT = 800  # pixels

# Empty State Messages
EMPTY_FINDINGS_MESSAGE = "No findings yet. Start a chat to search."
EMPTY_FINDINGS_CAPTION = "Results from your research will appear here."


def render_result_list_empty():
    """Renders the empty state of the result list."""
    st.info(EMPTY_FINDINGS_MESSAGE)
    st.caption(EMPTY_FINDINGS_CAPTION)


def render_result_list(research_results: list[Finding]):
    """Renders the list of research findings."""

    if not research_results:
        render_result_list_empty()
        return

    with st.container(border=False, height=RESULT_LIST_HEIGHT):
        for item in reversed(research_results):
            render_result_card(item)
