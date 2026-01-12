import streamlit as st

from medicalagent.domain.finding import Finding
from medicalagent.drivers.di import di_container

# Card Layout Constants
CARD_TITLE_RATIO = 0.85
CARD_TOGGLE_RATIO = 0.15

# Card UI Constants
BUTTON_DELETE = "🗑️ Delete"
BUTTON_NON_RELEVANT = "👎 Non-relevant"
BUTTON_NON_RELEVANT_UNDO = "👍 Mark as relevant"
BUTTON_TOGGLE_EXPAND = "▶️"
BUTTON_TOGGLE_COLLAPSE = "🔽"
CARD_SAVED_MESSAGE = "✅ Saved to Collection"

# Help Text
HELP_DELETE = "Permanently delete this finding"
HELP_NON_RELEVANT = (
    "Mark as non-relevant to improve future searches in the current dialog"
)
HELP_TOGGLE_DETAILS = "Toggle card details"


def render_card_header(finding: Finding):
    """Renders the card header with title and toggle button."""

    if f"card_expanded_{finding.id}" not in st.session_state:
        st.session_state[f"card_expanded_{finding.id}"] = True

    col_title, col_toggle = st.columns([CARD_TITLE_RATIO, CARD_TOGGLE_RATIO])

    with col_title:
        # Add warning icon if finding is marked as non-relevant
        warning_icon = " ⚠️" if getattr(finding, "non_relevance_mark", False) else ""
        title_text = f"**{finding.title}{warning_icon}**"

        if getattr(finding, "non_relevance_mark", False):
            st.markdown(
                title_text,
                help="This finding has been marked as non-relevant and will be excluded from the context of future searches in this dialog",
            )
        else:
            st.markdown(title_text)

        with col_toggle:
            toggle_icon = (
                BUTTON_TOGGLE_COLLAPSE
                if st.session_state[f"card_expanded_{finding.id}"]
                else BUTTON_TOGGLE_EXPAND
            )
            if st.button(
                "",
                icon=toggle_icon,
                key=f"toggle_{finding.id}",
                help=HELP_TOGGLE_DETAILS,
                use_container_width=True,
            ):
                st.session_state[f"card_expanded_{finding.id}"] = not st.session_state[
                    f"card_expanded_{finding.id}"
                ]
                st.rerun()

    return st.session_state[f"card_expanded_{finding.id}"]


def render_card_links(item):
    """Renders the links section with news and paper sources."""
    # Links section - expandable for multiple sources
    if item.news_links:
        with st.expander("📰 News Sources", expanded=False):
            for i, link in enumerate(item.news_links, 1):
                st.markdown(f"{i}. [{link.title}]({link.url})")

    if item.paper_links:
        with st.expander("🔬 Scientific Papers", expanded=False):
            for i, link in enumerate(item.paper_links, 1):
                st.markdown(f"{i}. [{link.title}]({link.url})")


def render_card_popularity(item):
    """Renders the popularity information."""
    citations = item.citations
    websites = item.websites
    st.caption(f"📊 {citations} citations • 🌐 {websites} sources")


def render_card_actions(item):
    """Renders the card action buttons."""
    card_id = item.id
    is_non_relevant = getattr(item, "non_relevance_mark", False)

    # Create two columns for the buttons
    col_delete, col_relevance = st.columns(2)

    with col_delete:
        if st.button(
            BUTTON_DELETE,
            key=f"delete_{card_id}",
            use_container_width=True,
            help=HELP_DELETE,
        ):
            di_container.findings_repository.delete(item.id)
            st.rerun()

    with col_relevance:
        if is_non_relevant:
            # Show button to mark as relevant
            if st.button(
                BUTTON_NON_RELEVANT_UNDO,
                key=f"relevant_{card_id}",
                use_container_width=True,
                help="Mark this finding as relevant again",
            ):
                di_container.findings_repository.mark_relevant(item.id)
                st.rerun()
        # Show button to mark as non-relevant
        elif st.button(
            BUTTON_NON_RELEVANT,
            key=f"non_relevant_{card_id}",
            use_container_width=True,
            help=HELP_NON_RELEVANT,
        ):
            di_container.findings_repository.mark_non_relevant(item.id)
            st.rerun()


def render_card_content(item):
    """Renders the expanded card content."""
    st.caption(item.relevance_reason)
    render_card_links(item)
    render_card_popularity(item)
    render_card_actions(item)


def render_result_card(finding: Finding):
    """Renders a single research finding as a collapsible card."""
    with st.container(border=True):
        is_expanded = render_card_header(finding)
        if is_expanded:
            render_card_content(finding)
