import streamlit as st

from medicalagent.drivers.central_chat.component import render_central_chat
from medicalagent.drivers.left_sidebar.component import render_left_sidebar
from medicalagent.drivers.right_sidebar.component import render_right_sidebar
from medicalagent.drivers.st_state import init_state

st.set_page_config(
    page_title="Medical News Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_auth_ui():
    """Render authentication UI when user is not logged in."""
    st.title("🧬 Medical News Agent")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        ### Welcome to Medical News Agent

        Get personalized medical research findings and stay updated with the latest developments
        in healthcare and medicine.

        **Features:**
        - 🔍 Intelligent research queries
        - 📋 Personalized findings
        - 💬 Conversation history
        - 🔒 Secure authentication
        """)

        if st.button("🔐 Log in", type="primary", use_container_width=True):
            st.login()


def main():
    """Main application entry point."""
    if not st.user.is_logged_in:
        render_auth_ui()
        return

    init_state()

    render_left_sidebar()
    col_chat, col_right = st.columns([2, 1.1], gap="medium")

    with col_chat:
        render_central_chat()

    with col_right:
        render_right_sidebar()


if __name__ == "__main__":
    main()
