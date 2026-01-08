import streamlit as st

from medicalagent.adapters.agent.dialog_title_generator import (
    generate_conversation_title,
)
from medicalagent.domain.dialog import DEFAULT_DIALOG_TITLE, ChatMessage
from medicalagent.drivers.di import di_container
from medicalagent.drivers.st_state import session_state
from medicalagent.drivers.user_service import get_current_user


def render_chat_header(active_dialog):
    """Renders the chat interface header."""
    if active_dialog:
        st.subheader(f"💬 {active_dialog.title}")
    else:
        st.subheader("💬 No dialog selected")


def render_chat_messages(chat_history: list[ChatMessage]):
    """Renders all chat messages in the conversation."""
    for message in chat_history:
        with st.chat_message(message.role):
            st.markdown(message.content)


def handle_chat_input():
    """Handles user chat input and generates responses."""

    if prompt := st.chat_input("Submit a request", max_chars=1500):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            msg_ph = st.empty()
            msg_ph.markdown("🔍 *Generating response...*")

            response = di_container.agent_service.call_agent(prompt)
            response_text = (
                response[0].content if isinstance(response, list) else response.content
            )

            msg_ph.markdown(response_text, text_alignment="justify")

        user_msg = ChatMessage(role="user", content=prompt)
        ai_msg = ChatMessage(role="assistant", content=response_text)

        active_dialog_id = session_state.active_dialog_id
        user = get_current_user()

        # --- SCENARIO 1: Create New Dialog ---
        if not active_dialog_id:
            conversation_title = generate_conversation_title(prompt)

            new_dialog = di_container.dialog_repository.create(
                title=conversation_title, messages=[user_msg, ai_msg], user_id=user.id
            )
            session_state.set_active_dialog(new_dialog)
            st.rerun()

        # --- SCENARIO 2 & 3: Update Existing Dialog ---
        else:
            dialog = di_container.dialog_repository.get_by_id(active_dialog_id)

            if dialog:
                dialog.chat_history.extend([user_msg, ai_msg])

                # Check for Rename (Scenario 2: Dialog exists but has default name)
                if dialog.title == DEFAULT_DIALOG_TITLE:
                    new_title = generate_conversation_title(prompt)
                    dialog.title = new_title

                # Save changes
                session_state.set_active_dialog(dialog)
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
