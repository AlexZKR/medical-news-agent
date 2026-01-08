import streamlit as st

from medicalagent.drivers.di import di_container

from ..domain.dialog import Dialog
from .user_service import get_current_user


class SessionStateManager:
    """Manager class for Streamlit session state with typed getters/setters."""

    def __init__(self):
        """Initialize the session state manager."""
        self._ensure_initialized()

    def _ensure_initialized(self) -> None:
        """Ensure session state is initialized."""
        if "init" not in st.session_state:
            st.session_state.init = True
            self._initialize_user_session()

    def _initialize_user_session(self) -> None:
        """Initialize user-specific session data."""
        user = get_current_user()
        if user:
            dialogs = di_container.dialog_repository.get_by_user_id(user.id)
            if dialogs:
                first_dialog = dialogs[0]
                self.active_dialog_id = first_dialog.id
                self.chat_history = first_dialog.chat_history
            else:
                self.active_dialog_id = None
                self.chat_history = []

    @property
    def active_dialog_id(self) -> int | None:
        """Get the active dialog ID."""
        return st.session_state.get("active_dialog_id")

    @active_dialog_id.setter
    def active_dialog_id(self, value: int | None) -> None:
        """Set the active dialog ID."""
        st.session_state.active_dialog_id = value

    @property
    def is_initialized(self) -> bool:
        """Check if session state is initialized."""
        return st.session_state.get("init", False)

    def reset_dialog_state(self) -> None:
        """Clear the chat history."""
        self.chat_history = []
        self.active_dialog_id = None

    def set_active_dialog(self, d: Dialog) -> None:
        """Set the active dialog and its chat history."""
        self.active_dialog_id = d.id
        self.chat_history = d.chat_history


# Global instance
session_state = SessionStateManager()
