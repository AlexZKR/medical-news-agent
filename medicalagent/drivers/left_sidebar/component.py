import streamlit as st

from medicalagent.data.mock_data import create_dialog

from .dialog_list import render_dialog_list


def render_sidebar_header():
    col_title, col_new = st.columns([0.8, 0.2])

    with col_title:
        st.header("Dialogs")

    with col_new:
        if st.button("", help="Start new dialog", icon="➕"):
            # Create new dialog
            new_dialog = create_dialog()

            st.session_state.active_dialog_id = new_dialog.id
            st.session_state.chat_history = new_dialog.chat_history
            st.rerun()


def render_left_sidebar():
    """Renders the left sidebar layout with dialog list."""
    with st.sidebar:
        render_sidebar_header()
        st.divider()

        render_dialog_list()
