"""User service for authentication and session management."""

import streamlit as st

from ..domain.user import UserData
from .di import di_container


def get_current_user_email() -> str | None:
    """Get the current user's email from Streamlit authentication.

    Uses the modern st.user API for authentication.
    Requires OIDC configuration in secrets.toml.
    """
    if st.user:
        email = st.user.get("email")
        return str(email) if email else None
    return None


def get_current_user() -> UserData | None:
    """Get the current user's data, creating it if it doesn't exist."""
    email = get_current_user_email()
    if not email:
        return None

    user_repo = di_container.user_repository
    user_data = user_repo.get_by_email(email)

    if not user_data:
        # Create new user with default data
        user_data = user_repo.create_default_user(email)

    return user_data


def save_current_user(user_data: UserData) -> None:
    """Save the current user's data."""
    user_repo = di_container.user_repository
    user_repo.save(user_data)


def initialize_user_session():
    """Initialize user-specific session data."""
    user = get_current_user()
    if user:
        # Store user data in session for quick access
        st.session_state.user_email = user.profile.email
        st.session_state.user_name = user.profile.display_name

        # Initialize user-specific dialogs
        if user.get_dialogs():
            first_dialog = user.get_dialogs()[0]
            st.session_state.active_dialog_id = first_dialog.id
            st.session_state.chat_history = first_dialog.chat_history
        else:
            st.session_state.active_dialog_id = None
            st.session_state.chat_history = []
    else:
        # Fallback for anonymous users or authentication issues
        st.session_state.user_email = None
        st.session_state.user_name = "Anonymous"
