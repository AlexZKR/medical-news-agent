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
    st.session_state.right_sidebar_visible = True
    st.session_state.init = True


# --- Render UI Components ---
def main():
    """Main application entry point."""

    # 1. Render Native Streamlit Sidebar (Left)
    render_left_sidebar()

    # 2. Define Layout Columns (Central vs Right)
    if st.session_state.right_sidebar_visible:
        # Split layout: 65% Chat, 35% Right Panel
        col_chat, col_right = st.columns([2, 1.1], gap="medium")

        with col_chat:
            render_central_chat()

        with col_right:
            render_right_sidebar()
    else:
        # Full width Chat
        render_central_chat()


if __name__ == "__main__":
    main()
