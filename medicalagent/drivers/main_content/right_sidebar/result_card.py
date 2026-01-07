import streamlit as st

# Card Layout Constants
CARD_TITLE_RATIO = 0.85
CARD_TOGGLE_RATIO = 0.15

# Card UI Constants
BUTTON_DISMISS = "❌ Dismiss"
BUTTON_TOGGLE_EXPAND = "▶️"
BUTTON_TOGGLE_COLLAPSE = "🔽"
CARD_SAVED_MESSAGE = "✅ Saved to Collection"

# Help Text
HELP_DISMISS = "Remove this finding"
HELP_TOGGLE_DETAILS = "Toggle card details"


def render_card_header(item):
    """Renders the card header with title and toggle button."""
    card_id = item["id"]

    if f"card_expanded_{card_id}" not in st.session_state:
        st.session_state[f"card_expanded_{card_id}"] = True

    col_title, col_toggle = st.columns([CARD_TITLE_RATIO, CARD_TOGGLE_RATIO])

    with col_title:
        st.markdown(f"**{item['title']}**")

        with col_toggle:
            toggle_icon = (
                BUTTON_TOGGLE_COLLAPSE
                if st.session_state[f"card_expanded_{card_id}"]
                else BUTTON_TOGGLE_EXPAND
            )
            if st.button(
                "",
                icon=toggle_icon,
                key=f"toggle_{card_id}",
                help=HELP_TOGGLE_DETAILS,
                use_container_width=True,
            ):
                st.session_state[f"card_expanded_{card_id}"] = not st.session_state[
                    f"card_expanded_{card_id}"
                ]
                st.rerun()

    return st.session_state[f"card_expanded_{card_id}"]


def render_card_links(item):
    """Renders the links section with news and paper sources."""
    # Links section - expandable for multiple sources
    if "news_links" in item and item["news_links"]:
        with st.expander("📰 News Sources", expanded=False):
            for i, link in enumerate(item["news_links"], 1):
                st.markdown(
                    f"{i}. [{link.get('title', 'News Article')}]({link['url']})"
                )
    else:
        # Fallback for single link
        st.markdown(f"[📰 News]({item.get('link', '#')})")

    if "paper_links" in item and item["paper_links"]:
        with st.expander("🔬 Scientific Papers", expanded=False):
            for i, link in enumerate(item["paper_links"], 1):
                st.markdown(
                    f"{i}. [{link.get('title', 'Research Paper')}]({link['url']})"
                )
    else:
        # Fallback for single link
        st.markdown(f"[🔬 Paper]({item.get('paper_link', '#')})")


def render_card_popularity(item):
    """Renders the popularity information."""
    citations = item.get("citations", 0)
    websites = item.get("websites", 0)
    st.caption(f"📊 {citations} citations • 🌐 {websites} sources")


def render_card_actions(item):
    """Renders the card action buttons."""
    card_id = item["id"]

    # Dismiss button only
    if item.get("status") != "dismissed":
        if st.button(
            BUTTON_DISMISS,
            key=f"dismiss_{card_id}",
            use_container_width=True,
            help=HELP_DISMISS,
        ):
            item["status"] = "dismissed"
            st.rerun()


def render_card_content(item):
    """Renders the expanded card content."""
    # Description
    st.caption(item.get("relevance_reason", "Research finding"))

    # Links
    render_card_links(item)

    # Popularity info
    render_card_popularity(item)

    # Actions
    render_card_actions(item)


def render_result_card(item):
    """Renders a single research finding as a collapsible card."""
    with st.container(border=True):
        is_expanded = render_card_header(item)
        if is_expanded:
            render_card_content(item)
