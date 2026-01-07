import streamlit as st

from medicalagent.data.mock_data import create_dialog, get_dialog


def handle_title_click(dialog):
    """Handles title button click logic."""
    st.session_state.active_dialog_id = dialog.id

    # Load dialog-specific chat history
    # For now, use mock dialog data or create defaults
    active_dialog = get_dialog(dialog.id)
    if active_dialog:
        st.session_state.chat_history = active_dialog.chat_history
    else:
        # Fallback for newly created dialogs
        new_dialog = create_dialog()
        new_dialog.id = dialog.id
        st.session_state.chat_history = new_dialog.chat_history

    st.rerun()


def handle_delete_click(dialog):
    """Handles delete button click logic."""
    # Remove this dialog from session state if it's active
    if st.session_state.active_dialog_id == dialog.id:
        st.session_state.active_dialog_id = 1
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
        help=f"Delete {dialog.title}",
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
