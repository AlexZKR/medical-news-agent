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


def main():
    """Main application entry point."""
    init_state()

    render_left_sidebar()
    col_chat, col_right = st.columns([2, 1.1], gap="medium")

    with col_chat:
        render_central_chat()

    with col_right:
        render_right_sidebar()


if __name__ == "__main__":
    main()
