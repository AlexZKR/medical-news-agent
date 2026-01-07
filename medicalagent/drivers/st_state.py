import streamlit as st

from .di import di


def init_state():
    """Initialize the session state."""
    if "init" not in st.session_state:
        st.session_state.init = True

        # Get all dialogs and set the first one as active
        dialogs = di.dialog_repository.get_all()
        if dialogs:
            st.session_state.active_dialog_id = dialogs[0].id
            st.session_state.chat_history = dialogs[0].chat_history
        else:
            st.session_state.active_dialog_id = None
            st.session_state.chat_history = []
