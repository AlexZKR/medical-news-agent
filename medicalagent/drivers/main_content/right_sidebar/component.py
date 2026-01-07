import streamlit as st

from .result_list import render_result_list

# Right Sidebar UI Constants
BUTTON_CLOSE_PANEL = "❌"

# Help Text
HELP_CLOSE_PANEL = "Close Panel"


def render_right_sidebar_header():
    """Renders the header of the right sidebar."""
    col_head, col_btn = st.columns([0.8, 0.2])
    with col_head:
        st.subheader("📋 Findings")
    with col_btn:
        if st.button(
            BUTTON_CLOSE_PANEL, help=HELP_CLOSE_PANEL, key="close_right_panel"
        ):
            st.session_state.right_sidebar_visible = False
            st.rerun()


def render_right_sidebar():
    """Renders the research findings board in the right column."""

    render_right_sidebar_header()
    render_result_list()
