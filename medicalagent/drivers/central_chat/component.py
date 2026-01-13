from logging import getLogger

import streamlit as st

from medicalagent.adapters.agent.dialog_title_generator import (
    generate_conversation_title,
)
from medicalagent.domain.dialog import DEFAULT_DIALOG_TITLE, ChatMessage, Dialog
from medicalagent.drivers.di import di_container
from medicalagent.drivers.st_state import session_state
from medicalagent.drivers.user_service import get_current_user

logger = getLogger(__name__)


def render_chat_header(active_dialog: Dialog) -> None:
    """Renders the chat interface header."""
    if active_dialog:
        st.subheader(f"💬 {active_dialog.title}")
    else:
        st.subheader("💬 New Conversation")


def render_chat_messages(chat_history: list[ChatMessage]) -> None:
    """Renders all chat messages in the conversation."""
    for message in chat_history:
        with st.chat_message(message.role):
            st.markdown(message.content)


def handle_chat_input() -> None:
    """Handles user chat input and generates responses."""

    if prompt := st.chat_input("Submit a request", max_chars=1500):
        # 1. Render User Message Immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        user = get_current_user()
        active_dialog_id = session_state.active_dialog_id

        # ---------------------------------------------------------
        # CRITICAL FIX: Pre-Create Dialog if one doesn't exist
        # ---------------------------------------------------------
        # The agent needs a valid dialog_id for the 'save_finding' tool
        # to work. We create an empty container first.
        if active_dialog_id is None:
            new_dialog = di_container.dialog_repository.create(
                title=DEFAULT_DIALOG_TITLE,
                messages=[],  # Start empty
                user_id=user.id,
            )
            # Set state IMMEDIATELY so the tool sees it
            session_state.set_active_dialog(new_dialog)
            active_dialog_id = new_dialog.id

        # 2. Fetch Context (Now guaranteed to exist)
        dialog = di_container.dialog_repository.get_by_id(active_dialog_id)
        chat_history = dialog.chat_history if dialog else []

        # 3. Call Agent
        with st.chat_message("assistant"):
            msg_ph = st.empty()
            msg_ph.markdown("🔍 *Researching & verifying...*")

            try:
                # Agent can now safely call 'save_finding_tool'
                # because session_state.active_dialog_id is set.
                response = di_container.agent_service.call_agent(
                    prompt, chat_history=chat_history, dialog_id=active_dialog_id
                )
                response_text = (
                    response[0].content
                    if isinstance(response, list)
                    else response.content
                )

                msg_ph.markdown(response_text, text_alignment="justify")

            except Exception as e:
                logger.error(f"Agent failed: {e}", exc_info=True)
                msg_ph.error(f"An error occurred: {str(e)}")
                return

        # 4. Save Interaction
        user_msg = ChatMessage(role="user", content=prompt)
        ai_msg = ChatMessage(role="assistant", content=response_text)

        # We append to the existing object we retrieved/created above
        dialog.chat_history.extend([user_msg, ai_msg])

        # 5. Smart Renaming (Lazy)
        # If this was a new dialog (still has default title), give it a real name
        if dialog.title == DEFAULT_DIALOG_TITLE:
            try:
                new_title = generate_conversation_title(prompt)
                dialog.title = new_title
            except Exception:
                pass  # Fallback to default if generator fails

        # 6. Persist & Refresh
        di_container.dialog_repository.save(dialog)
        st.rerun()


def render_central_chat():
    """Renders the central chat interface with research capabilities."""
    user = get_current_user()
    active_dialog_id = session_state.active_dialog_id
    active_dialog = None
    active_dialog_chat_hist: list[ChatMessage] = []

    if user and active_dialog_id is not None:
        active_dialog = di_container.dialog_repository.get_by_id(active_dialog_id)
        if active_dialog:
            active_dialog_chat_hist = active_dialog.chat_history

    render_chat_header(active_dialog)
    render_chat_messages(active_dialog_chat_hist)
    handle_chat_input()
