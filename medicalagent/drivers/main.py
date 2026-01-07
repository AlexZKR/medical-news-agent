import streamlit as st

from medicalagent.drivers.left_sidebar.component import render_left_sidebar
from medicalagent.drivers.main_content import render_main_content
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
    render_main_content()


if __name__ == "__main__":
    main()
