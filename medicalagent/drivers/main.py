import streamlit as st

from medicalagent.drivers.central_chat.component import render_central_chat
from medicalagent.drivers.left_sidebar.component import render_left_sidebar
from medicalagent.drivers.right_sidebar.component import render_right_sidebar

# --- Page Config ---
st.set_page_config(
    page_title="Medical News Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Session State Initialization ---
if "init" not in st.session_state:
    st.session_state.trusted_sources = [
        "nakedscience.ru",
        "statnews.com",
        "medscape.com",
        "medicalnewstoday.com",
    ]
    st.session_state.settings = {"date_range": "Last Month", "strict_mode": True}
    st.session_state.init = True


# --- Render UI Components ---
def main():
    """Main application entry point."""

    # Render left sidebar
    render_left_sidebar()

    # Render central chat interface
    render_central_chat()

    # Render right sidebar (togglable)
    render_right_sidebar()


if __name__ == "__main__":
    main()
