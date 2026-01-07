import streamlit as st

from medicalagent.data.mock_data import get_findings

from .result_list import render_result_list


def render_right_sidebar_header():
    """Renders the header of the right sidebar."""
    st.subheader("📋 Findings")


def render_right_sidebar():
    """Renders the research findings board in the right column."""
    # Get findings for the current active dialog
    active_dialog_id = st.session_state.get("active_dialog_id", 1)

    current_findings = get_findings(active_dialog_id)

    render_right_sidebar_header()
    render_result_list(current_findings)
