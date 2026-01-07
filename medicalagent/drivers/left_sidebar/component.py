import streamlit as st

from medicalagent.domain.dialog import Dialog
from medicalagent.drivers.di import di

from .dialog_list import render_dialog_list


def render_sidebar_header():
    col_title, col_new = st.columns([0.8, 0.2])

    with col_title:
        st.header("Dialogs")

    with col_new:
        if st.button("", help="Start new dialog", icon="➕"):
            # Create new dialog
            # Generate next ID from existing dialogs
            existing_dialogs = di.dialog_repository.get_all()
            next_id = max((d.id for d in existing_dialogs), default=0) + 1
            new_dialog = Dialog(id=next_id, title="New Dialog", chat_history=[])

            di.dialog_repository.save(new_dialog)
            st.session_state.active_dialog_id = new_dialog.id
            st.session_state.chat_history = new_dialog.chat_history
            st.rerun()


def render_left_sidebar():
    """Renders the left sidebar layout with dialog list."""
    with st.sidebar:
        render_sidebar_header()
        st.divider()

        render_dialog_list()
