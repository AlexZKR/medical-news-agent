import re

import streamlit as st

from medicalagent.drivers.di import di_container
from medicalagent.drivers.user_service import get_current_user

# Constants
MAX_RESPONSE_LENGTH = 2000


def render_chat_header(active_dialog):
    """Renders the chat interface header."""
    if active_dialog:
        st.subheader(f"💬 {active_dialog.title}")
    else:
        st.subheader("💬 No dialog selected")


def render_chat_messages():
    """Renders all chat messages in the conversation."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def generate_assistant_response(prompt):
    """Generates and displays the assistant's response to user input."""
    with st.chat_message("assistant"):
        msg_ph = st.empty()
        msg_ph.markdown("🔍 *Scanning trusted medical sources...*")

        try:
            # Invoke the LangGraph agent with proper input format
            result = di_container.agent.invoke({"input": prompt})

            # Extract the response from the agent result
            # LangGraph agents typically return a dict with messages
            if isinstance(result, dict) and "messages" in result:
                # Get the last AI message
                messages = result["messages"]
                for msg in reversed(messages):
                    if hasattr(msg, "type") and msg.type == "ai":
                        response_text = msg.content
                        break
                    elif hasattr(msg, "content"):
                        response_text = msg.content
                        break
                else:
                    response_text = str(result)
            elif hasattr(result, "content"):
                response_text = result.content
            else:
                # Fallback: try to convert to string
                response_text = str(result)

            # Remove thinking tags from the response
            response_text = re.sub(
                r"<think>.*?</think>", "", response_text, flags=re.DOTALL
            ).strip()

            # Clean up the response if it's too verbose
            if len(response_text) > MAX_RESPONSE_LENGTH:
                response_text = (
                    response_text[:MAX_RESPONSE_LENGTH]
                    + "...\n\n*Response truncated for readability*"
                )

            msg_ph.markdown(response_text)
            st.session_state.chat_history.append(
                {"role": "assistant", "content": response_text}
            )

        except Exception as e:
            error_msg = (
                f"Sorry, I encountered an error while researching your query: {str(e)}"
            )
            msg_ph.markdown(error_msg)
            st.session_state.chat_history.append(
                {"role": "assistant", "content": error_msg}
            )


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
    user = get_current_user()
    active_dialog_id = st.session_state.get("active_dialog_id")
    active_dialog = None

    if user and active_dialog_id:
        active_dialog = next(
            (d for d in user.get_dialogs() if d.id == active_dialog_id), None
        )

    render_chat_header(active_dialog)
    render_chat_messages()
    handle_chat_input()
