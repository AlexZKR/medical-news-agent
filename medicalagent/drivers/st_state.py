import streamlit as st

from ..domain.dialog import ChatMessage, Dialog
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
            dialogs = user.get_dialogs()
            if dialogs:
                first_dialog = dialogs[0]
                self.dialogs = dialogs
                self.active_dialog_id = first_dialog.id
                self.chat_history = first_dialog.chat_history
            else:
                self.dialogs = []
                self.active_dialog_id = None
                self.chat_history = []

    # Getters and setters
    @property
    def dialogs(self) -> list[Dialog]:
        """Get the list of dialogs."""
        return st.session_state.get("dialogs", [])

    @dialogs.setter
    def dialogs(self, value: list[Dialog]) -> None:
        """Set the list of dialogs."""
        st.session_state.dialogs = value

    @property
    def active_dialog_id(self) -> int | None:
        """Get the active dialog ID."""
        return st.session_state.get("active_dialog_id")

    @active_dialog_id.setter
    def active_dialog_id(self, value: int | None) -> None:
        """Set the active dialog ID."""
        st.session_state.active_dialog_id = value

    @property
    def chat_history(self) -> list[ChatMessage]:
        """Get the chat history."""
        return st.session_state.get("chat_history", [])

    @chat_history.setter
    def chat_history(self, value: list[ChatMessage]) -> None:
        """Set the chat history."""
        st.session_state.chat_history = value

    @property
    def is_initialized(self) -> bool:
        """Check if session state is initialized."""
        return st.session_state.get("init", False)

    def add_chat_message(self, role: str, content: str | list[str | dict]) -> None:
        """Add a message to the chat history."""
        new_message = ChatMessage(role=role, content=content)
        current_history = self.chat_history
        current_history.append(new_message)
        self.chat_history = current_history

    def clear_chat_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []

    def set_active_dialog(
        self, dialog_id: int, chat_history: list[ChatMessage]
    ) -> None:
        """Set the active dialog and its chat history."""
        self.active_dialog_id = dialog_id
        self.chat_history = chat_history

    def reset_session(self) -> None:
        """Reset the session to initial state."""
        self.dialogs = []
        self.active_dialog_id = None
        self.chat_history = []


# Global instance
session_state = SessionStateManager()
