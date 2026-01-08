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
        user_data = user_repo.create_user(email)

    return user_data


def save_current_user(user_data: UserData) -> None:
    """Save the current user's data."""
    user_repo = di_container.user_repository
    user_repo.save(user_data)
