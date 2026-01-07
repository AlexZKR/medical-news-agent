import uuid

import streamlit as st

from medicalagent.drivers.defaults import (
    NEW_DIALOG_PLACEHOLDER,
    NEW_DIALOG_WELCOME_MESSAGE,
)
from medicalagent.drivers.main_content.mock_data import get_mock_dialogs

# UI Layout Constants for left sidebar
ACCENT_BAR_RATIO = 0.05  # For accent bar in active dialogs
CONTENT_RATIO = 0.95  # For content area in active dialogs

# Dialog UI Constants
BUTTON_NEW_DIALOG = "➕"

# Help Text
HELP_NEW_DIALOG = "Start new dialog"


def get_dialog_switch_message(dialog_title):
    """Generate a message when switching to a dialog."""
    return {
        "role": "assistant",
        "content": f"Switched to: **{dialog_title}**\n\nHello! I'm ready to continue our discussion about {dialog_title.lower()}.",
    }


def render_dialog_item(dialog, is_active=False):
    """Renders a single dialog item in the list."""
    if is_active:
        # Active dialog - use container with visual indicators
        with st.container():
            # Blue accent bar simulation with columns
            col_bar, col_content = st.columns([ACCENT_BAR_RATIO, CONTENT_RATIO])
            with col_bar:
                st.markdown("🔵")  # Blue indicator
            with col_content:
                st.markdown(f"**{dialog['title']}**")
                st.caption(dialog["last_message"][:50] + "...")
                st.caption(
                    f"{dialog['timestamp']} • {dialog['message_count']} messages"
                )
    elif st.button(
        f"**{dialog['title']}**\n{dialog['last_message'][:40]}...\n*{dialog['timestamp']}*",
        key=f"dialog_{dialog['id']}",
        use_container_width=True,
        help=f"Switch to {dialog['title']}",
    ):
        st.session_state.active_dialog = dialog["id"]
        # Reset chat history for new dialog
        st.session_state.chat_history = [get_dialog_switch_message(dialog["title"])]
        # Reset research results for new dialog
        st.session_state.research_results = []
        st.rerun()


def render_left_sidebar():
    """Renders the left sidebar with dialog list."""
    with st.sidebar:
        # Header with new dialog button
        col_title, col_new = st.columns([0.8, 0.2])
        with col_title:
            st.header("💬 Dialogs")
        with col_new:
            if st.button(BUTTON_NEW_DIALOG, help="Start new dialog"):
                # Create new dialog
                new_dialog_id = f"dialog_{str(uuid.uuid4())[:8]}"
                st.session_state.active_dialog = new_dialog_id
                st.session_state.chat_history = [NEW_DIALOG_WELCOME_MESSAGE.copy()]
                st.session_state.research_results = []
                st.rerun()

        st.divider()

        # Initialize active dialog if not set
        if "active_dialog" not in st.session_state:
            st.session_state.active_dialog = "dialog_1"

        # Get dialogs and render them
        dialogs = get_mock_dialogs()

        # Add current active dialog if it's a new one
        active_id = st.session_state.active_dialog
        if active_id not in [d["id"] for d in dialogs]:
            # This is a newly created dialog
            new_dialog = NEW_DIALOG_PLACEHOLDER.copy()
            new_dialog["id"] = active_id
            dialogs.insert(0, new_dialog)
        else:
            # Move active dialog to top
            active_dialog = next((d for d in dialogs if d["id"] == active_id), None)
            if active_dialog:
                dialogs.remove(active_dialog)
                dialogs.insert(0, active_dialog)

        # Render dialog list
        for dialog in dialogs:
            is_active = dialog["id"] == st.session_state.active_dialog
            render_dialog_item(dialog, is_active)

        st.divider()
        st.caption("Click on any dialog to switch to it")
