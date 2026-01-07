import streamlit as st

from medicalagent.domain.dialog import Dialog
from medicalagent.drivers.di import di


def handle_title_click(dialog):
    """Handles title button click logic."""
    st.session_state.active_dialog_id = dialog.id

    active_dialog = di.dialog_repository.get_by_id(dialog.id)
    if active_dialog:
        st.session_state.chat_history = active_dialog.chat_history
    else:
        repo_dialog = di.dialog_repository.get_by_id(dialog.id)
        if repo_dialog:
            st.session_state.chat_history = repo_dialog.chat_history
        else:
            default_dialog = Dialog(id=dialog.id, title=dialog.title, chat_history=[])
            st.session_state.chat_history = default_dialog.chat_history

    st.rerun()


def handle_delete_click(dialog):
    """Handles delete button click logic."""
    # Delete the dialog from repository
    di.dialog_repository.delete(dialog.id)

    st.session_state.active_dialog_id = None
    st.session_state.chat_history = []

    st.rerun()


def render_title_button(dialog, is_selected):
    """Renders the title button and handles clicks."""
    title_clicked = st.button(
        dialog.title,
        key=f"select_{dialog.id}",
        use_container_width=True,
        type="secondary" if is_selected else "tertiary",
    )

    if title_clicked:
        handle_title_click(dialog)


def render_delete_button(dialog):
    """Renders the delete button and handles clicks."""
    delete_clicked = st.button(
        "",
        icon="🗑️",
        key=f"delete_{dialog.id}",
        type="secondary",
    )

    if delete_clicked:
        handle_delete_click(dialog)


def render_dialog_item(dialog, is_selected=False):
    """Renders a single dialog item with Streamlit buttons."""
    col_title, col_delete = st.columns([0.8, 0.2])

    with col_title:
        render_title_button(dialog, is_selected)

    with col_delete:
        render_delete_button(dialog)
