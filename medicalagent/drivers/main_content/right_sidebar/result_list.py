import streamlit as st

from medicalagent.drivers.main_content.right_sidebar.result_card import (
    render_result_card,
)

# Container Heights
RESULT_LIST_HEIGHT = 800  # pixels

# Empty State Messages
EMPTY_FINDINGS_MESSAGE = "No findings yet. Start a chat to search."
EMPTY_FINDINGS_CAPTION = "Results from your research will appear here."


def render_result_list_empty():
    """Renders the empty state of the result list."""
    st.info(EMPTY_FINDINGS_MESSAGE)
    st.caption(EMPTY_FINDINGS_CAPTION)


def render_result_list():
    """Renders the list of research findings."""

    if (
        "research_results" not in st.session_state
        or not st.session_state.research_results
    ):
        render_result_list_empty()
        return

    active_results = [
        r
        for r in reversed(st.session_state.research_results)
        if r.get("status") != "dismissed"
    ]
    with st.container(border=False, height=RESULT_LIST_HEIGHT):
        for item in active_results:
            render_result_card(item)
