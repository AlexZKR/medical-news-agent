import time

import streamlit as st

from medicalagent.data.mock_data import (
    add_finding,
    generate_mock_finding,
    get_dialog,
    get_initial_chat_history,
)


def render_chat_header(active_dialog):
    """Renders the chat interface header."""
    if active_dialog:
        st.subheader(f"💬 {active_dialog.title}")
    else:
        st.subheader("💬 No dialog selected")


def initialize_chat_state():
    """Initializes chat history if they don't exist."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = get_initial_chat_history()


def render_chat_messages():
    """Renders all chat messages in the conversation."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def generate_assistant_response(prompt):
    """Generates and displays the assistant's response to user input."""
    with st.chat_message("assistant"):
        msg_ph = st.empty()
        msg_ph.markdown("🔍 *Scanning trusted sources...*")
        time.sleep(1.0)  # Latency simulation

        resp = f"I've searched for **'{prompt}'**. Here are some findings."
        msg_ph.markdown(resp)
        st.session_state.chat_history.append({"role": "assistant", "content": resp})

        # Mock Finding - create new research result
        active_dialog_id = st.session_state.get("active_dialog_id", 1)
        new_finding = generate_mock_finding(prompt, active_dialog_id)
        # Add to findings store
        add_finding(new_finding)

        # Force a rerun so the Right Sidebar updates immediately
        st.rerun()


def handle_chat_input():
    """Handles user chat input and generates responses."""
    if prompt := st.chat_input("Type a topic (e.g., 'Alzheimers biomarkers')..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        generate_assistant_response(prompt)


def render_central_chat():
    """Renders the central chat interface with research capabilities."""
    active_dialog = get_dialog(st.session_state.get("active_dialog_id"))

    render_chat_header(active_dialog)
    initialize_chat_state()
    render_chat_messages()
    handle_chat_input()
