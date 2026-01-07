import streamlit as st


def render_right_sidebar():
    """Renders the togglable right sidebar with placeholder content."""

    # Initialize toggle state
    if "right_sidebar_visible" not in st.session_state:
        st.session_state.right_sidebar_visible = False

    # Toggle button (placed outside the sidebar)
    col_toggle, col_spacer = st.columns([0.1, 0.9])
    with col_toggle:
        if st.button("📊", help="Toggle Analysis Panel"):
            st.session_state.right_sidebar_visible = (
                not st.session_state.right_sidebar_visible
            )
            st.rerun()

    # Render sidebar only if visible
    if st.session_state.right_sidebar_visible:
        with st.sidebar:
            st.header("📊 Analysis Panel")
            st.info("Right sidebar placeholder - future analysis features")

            st.divider()

            # Analysis tools placeholder
            st.subheader("Tools")
            if st.button("📈 Statistics", use_container_width=True):
                st.info("Statistical analysis - coming soon")

            if st.button("🔗 References", use_container_width=True):
                st.info("Reference management - coming soon")

            if st.button("💾 Export", use_container_width=True):
                st.info("Export features - coming soon")

            st.divider()

            # Session info
            st.subheader("Session Info")
            if "research_results" in st.session_state:
                new_count = len(
                    [
                        r
                        for r in st.session_state.research_results
                        if r["status"] == "new"
                    ]
                )
                saved_count = len(
                    [
                        r
                        for r in st.session_state.research_results
                        if r["status"] == "kept"
                    ]
                )

                st.metric("Active Findings", new_count)
                st.metric("Saved Items", saved_count)
            else:
                st.caption("No session data yet")
