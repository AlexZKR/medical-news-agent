import streamlit as st

from medicalagent.drivers.di import di_container
from medicalagent.drivers.st_state import session_state

from .result_list import render_result_list


def render_right_sidebar_header():
    """Renders the header of the right sidebar."""
    st.subheader("📋 Findings")


def render_right_sidebar():
    """Renders the research findings board in the right column."""
    # Get findings for the current active dialog
    active_dialog_id = session_state.active_dialog_id

    if active_dialog_id is not None:
        current_findings = di_container.findings_repository.get_by_dialog_id(
            active_dialog_id
        )
    else:
        current_findings = []

    render_right_sidebar_header()
    render_result_list(current_findings)
