import streamlit as st

from .defaults import DEFAULT_SETTINGS, DEFAULT_TRUSTED_SOURCES, DEFAULT_UI_STATE


def init_state():
    """Initialize the session state."""
    if "init" not in st.session_state:
        st.session_state.trusted_sources = DEFAULT_TRUSTED_SOURCES.copy()
        st.session_state.settings = DEFAULT_SETTINGS.copy()
        st.session_state.init = DEFAULT_UI_STATE["init"]
        st.session_state.active_dialog_id = DEFAULT_UI_STATE["active_dialog_id"]
