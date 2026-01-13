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


def create_user() -> UserData:
    """Creates a new user with verified types for MyPy."""
    email = str(st.user.email) if st.user.email else ""
    name = str(st.user.name) if isinstance(st.user.name, str) else None
    picture_val = st.user.get("picture")
    picture = str(picture_val) if isinstance(picture_val, str) else None

    return di_container.user_repository.create_user(
        email,
        name,
        picture,
    )


def get_current_user() -> UserData:
    """Get the current user's data, creating it if it doesn't exist."""
    email = get_current_user_email()
    if not email:
        st.logout()
        return  # type: ignore

    user_repo = di_container.user_repository
    user_data = user_repo.get_by_email(email)

    if not user_data:
        st.logout()
        return  # type: ignore

    return user_data
