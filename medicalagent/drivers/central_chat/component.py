import streamlit as st

from medicalagent.adapters.agent.dialog_title_generator import (
    generate_conversation_title,
)
from medicalagent.drivers.di import di_container
from medicalagent.drivers.st_state import ChatMessage, session_state
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
            user_msg = st.empty()
            user_msg.markdown(prompt)
            user_msg = session_state.add_chat_message("user", prompt)

        with st.chat_message("assistant"):
            msg_ph = st.empty()
            msg_ph.markdown("🔍 *Generating response...*")
            response = di_container.agent_service.call_agent(prompt)
            response_text = response[0].content
            msg_ph.markdown(response_text, text_alignment="justify")

            ai_response = session_state.add_chat_message("assistant", response_text)

        if not session_state.active_dialog_id:
            converstation_title = generate_conversation_title(prompt)
            new_dialog = di_container.dialog_repository.create(
                converstation_title, [user_msg, ai_response]
            )
            session_state.set_active_dialog(new_dialog)
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
