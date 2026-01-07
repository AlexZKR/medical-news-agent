
import streamlit as st


def render_right_sidebar():
    """Renders the research findings board in the right column."""

    # -- Toggle Button (To Hide Panel) --
    # We place this at the top so user can close the panel
    col_head, col_btn = st.columns([0.8, 0.2])
    with col_head:
        st.subheader("📋 Findings")
    with col_btn:
        if st.button("❌", help="Close Panel", key="close_right_panel"):
            st.session_state.right_sidebar_visible = False
            st.rerun()

    # -- Content Area --
    if (
        "research_results" not in st.session_state
        or not st.session_state.research_results
    ):
        st.info("No findings yet. Start a chat to search.")
        st.caption("Results from your research will appear here.")
        return

    # Filter for active results (new first)
    active_results = [
        r
        for r in reversed(st.session_state.research_results)
        if r.get("status") != "dismissed"
    ]

    # -- Render Cards --
    for item in active_results:
        # Using st.container with border to create a native card look
        with st.container(border=True):
            st.markdown(f"#### {item['title']}")
            st.caption(f"Source: {item['source']}")
            st.markdown(f"**Paper:** [{item['paper_title']}]({item['paper_link']})")
            st.info(f"{item['relevance_reason']}")

            # Card Actions
            if item.get("status") != "kept":
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(
                        "✅ Keep", key=f"keep_{item['id']}", use_container_width=True
                    ):
                        item["status"] = "kept"
                        st.toast("Saved to collection!")
                        st.rerun()
                with c2:
                    if st.button(
                        "❌ Dismiss",
                        key=f"dismiss_{item['id']}",
                        use_container_width=True,
                    ):
                        item["status"] = "dismissed"
                        st.rerun()
            else:
                st.success("✅ Saved to Collection")
