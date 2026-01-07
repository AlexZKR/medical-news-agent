import streamlit as st

from ..domain.dialog import Dialog
from .user_service import initialize_user_session


def init_state():
    """Initialize the session state."""
    if "init" not in st.session_state:
        st.session_state.init = True

        # Initialize user-specific session data
        initialize_user_session()

        # Ensure chat_history is always initialized
        if "chat_history" not in st.session_state:
            # Use the default welcome message from Dialog model
            default_dialog = Dialog(id=1, title="Default")
            st.session_state.chat_history = default_dialog.chat_history
