import time
import uuid

import streamlit as st


def render_central_chat():
    """Renders the central chat interface with research capabilities."""

    # Initialize chat history if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hello! I'm your Medical Research Agent. Try 'Find latest diabetes news'.",
            }
        ]

    # Initialize research results if not exists
    if "research_results" not in st.session_state:
        st.session_state.research_results = [
            {
                "id": "init_1",
                "title": "Example: New GLP-1 Agonist Study",
                "source": "StatNews",
                "link": "#",
                "paper_title": "Efficacy of Retatrutide",
                "paper_link": "#",
                "relevance_reason": "High impact study relevant to metabolic diseases.",
                "status": "new",
            }
        ]

    st.title("🧬 Medical Research Agent")

    # Chat Interface
    st.subheader("💬 Discussion")

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
            new_finding = {
                "id": str(uuid.uuid4()),
                "title": f"New Finding for: {prompt}",
                "source": "Medscape",
                "link": "#",
                "paper_title": "Clinical Trial Results Phase III",
                "paper_link": "#",
                "relevance_reason": "Matches your interest in clinical outcomes.",
                "status": "new",
            }
            st.session_state.research_results.append(new_finding)
            st.rerun()
