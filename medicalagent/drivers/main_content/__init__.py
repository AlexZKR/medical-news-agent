import streamlit as st

from medicalagent.drivers.main_content.central_chat.component import render_central_chat
from medicalagent.drivers.main_content.right_sidebar.component import (
    render_right_sidebar,
)


def render_main_content():
    """Renders the main content area with optional right sidebar."""

    if st.session_state.right_sidebar_visible:
        col_chat, col_right = st.columns([2, 1.1], gap="medium")

        with col_chat:
            render_central_chat()

        with col_right:
            render_right_sidebar()
    else:
        render_central_chat()
