import streamlit as st

from medicalagent.drivers.user_service import get_current_user

from .dialog_item import render_dialog_item


def render_dialog_list():
    """Renders the complete dialog list with all dialogs."""
    current_dialog_id = st.session_state.get("active_dialog_id")
    user = get_current_user()
    dialogs = user.get_dialogs() if user else []

    # Render each dialog item
    for dialog in dialogs:
        is_selected = dialog.id == current_dialog_id
        render_dialog_item(dialog, is_selected)
