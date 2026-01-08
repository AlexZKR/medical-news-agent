import streamlit as st

from medicalagent.drivers.di import di_container
from medicalagent.drivers.st_state import session_state
from medicalagent.drivers.user_service import get_current_user

from .dialog_list import render_dialog_list


def render_sidebar_header():
    col_title, col_new = st.columns([0.8, 0.2])

    with col_title:
        st.header("Dialogs")

    with col_new:
        if st.button("", help="Start new dialog", icon="➕"):
            user = get_current_user()
            if user:
                new_dialog = di_container.dialog_repository.create(
                    messages=[], user_id=user.id
                )
                session_state.set_active_dialog(new_dialog)
            st.rerun()


def render_sidebar_footer():
    """Render sidebar footer with user info and logout."""

    if st.user:
        with st.container():
            # User profile section
            user_picture = st.user.get("picture")
            user_name = st.user.get("name") or st.user.get("email", "User")

            if user_picture:
                col_img, col_info = st.columns([0.3, 0.7])
                with col_img:
                    st.image(user_picture, width=50)  # type: ignore
                with col_info:
                    st.markdown(f"**{user_name}**")
            else:
                st.markdown(f"👤 **{user_name}**")

            if st.button("Logout", use_container_width=True, icon="🚪"):
                st.logout()


def render_left_sidebar():
    """Renders the left sidebar layout with dialog list."""
    with st.sidebar:
        render_sidebar_header()
        st.divider()

        render_dialog_list()

        render_sidebar_footer()
