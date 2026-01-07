import time

import streamlit as st

from ..mock_data import (
    generate_mock_finding,
    get_initial_chat_history,
    get_initial_research_results,
)


def render_central_chat():
    """Renders the central chat interface with research capabilities."""

    # -- Toggle Button (To Show Panel if Hidden) --
    if not st.session_state.get("right_sidebar_visible", True):
        if st.button("📋 Show Findings", key="open_right_panel"):
            st.session_state.right_sidebar_visible = True
            st.rerun()

    st.subheader("💬 Research Discussion")

    # Initialize chat history if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = get_initial_chat_history()

    # Initialize research results if not exists
    if "research_results" not in st.session_state:
        st.session_state.research_results = get_initial_research_results()

    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type a topic (e.g., 'Alzheimers biomarkers')..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            msg_ph = st.empty()
            msg_ph.markdown("🔍 *Scanning trusted sources...*")
            time.sleep(1.0)  # Latency simulation

            resp = f"I've searched for **'{prompt}'**. Here are some findings."
            msg_ph.markdown(resp)
            st.session_state.chat_history.append({"role": "assistant", "content": resp})

            # Mock Finding - create new research result
            new_finding = generate_mock_finding(prompt)
            # Append to global state so Right Sidebar can see it
            st.session_state.research_results.append(new_finding)

            # Force a rerun so the Right Sidebar updates immediately
            st.rerun()
