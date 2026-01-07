import streamlit as st

from medicalagent.data.mock_data import get_dialogs

from .dialog_item import render_dialog_item


def render_dialog_list():
    """Renders the complete dialog list with all dialogs."""
    current_dialog_id = st.session_state.get("active_dialog_id", 1)
    dialogs = get_dialogs()

    # Render each dialog item
    for dialog in dialogs:
        is_selected = dialog.id == current_dialog_id
        render_dialog_item(dialog, is_selected)
