import streamlit as st

from medicalagent.domain.dialog import Dialog
from medicalagent.drivers.di import di_container
from medicalagent.drivers.st_state import session_state
from medicalagent.drivers.user_service import get_current_user


def handle_title_click(dialog: Dialog):
    """Handles title button click logic."""
    user = get_current_user()
    if user:
        user_dialog = di_container.dialog_repository.get_by_id(dialog.id)
        if user_dialog:
            session_state.set_active_dialog(user_dialog)
        else:
            session_state.active_dialog_id = None
            session_state.reset_dialog_state()
    st.rerun()


def handle_delete_click(dialog: Dialog):
    """Handles delete button click logic."""

    user = get_current_user()
    if user:
        di_container.dialog_repository.delete(dialog.id)
        session_state.reset_dialog_state()
    st.rerun()


def render_title_button(dialog: Dialog, is_selected: bool):
    """Renders the title button and handles clicks."""
    title_clicked = st.button(
        dialog.title,
        key=f"select_{dialog.id}",
        use_container_width=True,
        type="secondary" if is_selected else "tertiary",
    )

    if title_clicked:
        handle_title_click(dialog)


def render_delete_button(dialog: Dialog):
    """Renders the delete button and handles clicks."""
    delete_clicked = st.button(
        "",
        icon="🗑️",
        key=f"delete_{dialog.id}",
        type="secondary",
    )

    if delete_clicked:
        handle_delete_click(dialog)


def render_dialog_item(dialog: Dialog, is_selected: bool = False):
    """Renders a single dialog item with Streamlit buttons."""
    col_title, col_delete = st.columns([0.8, 0.2])

    with col_title:
        render_title_button(dialog, is_selected)

    with col_delete:
        render_delete_button(dialog)
