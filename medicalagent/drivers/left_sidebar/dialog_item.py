import streamlit as st

from medicalagent.drivers.st_state import session_state
from medicalagent.drivers.user_service import get_current_user, save_current_user


def handle_title_click(dialog):
    """Handles title button click logic."""
    # Load dialog-specific chat history from user data
    user = get_current_user()
    if user:
        user_dialog = next((d for d in user.get_dialogs() if d.id == dialog.id), None)
        if user_dialog:
            session_state.set_active_dialog(dialog.id, user_dialog.chat_history)
        else:
            # Fallback for dialogs not found in user data
            session_state.active_dialog_id = dialog.id
            session_state.clear_chat_history()

    st.rerun()


def handle_delete_click(dialog):
    """Handles delete button click logic."""
    # Delete the dialog from user data
    user = get_current_user()
    if user:
        user.remove_dialog(dialog.id)

        # If this was the active dialog, switch to another dialog or clear
        if session_state.active_dialog_id == dialog.id:
            remaining_dialogs = user.get_dialogs()
            if remaining_dialogs:
                # Switch to the first remaining dialog
                new_active_dialog = remaining_dialogs[0]
                session_state.set_active_dialog(
                    new_active_dialog.id, new_active_dialog.chat_history
                )
            else:
                # No dialogs left
                session_state.reset_session()

        # Save updated user data
        save_current_user(user)

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
