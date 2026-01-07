"""Mock data for the Medical News Agent application."""

import random
import uuid

from ..defaults import DEFAULT_WELCOME_MESSAGE

# Citation and Website Ranges
CITATION_MOCK_RANGE = (10, 500)
WEBSITE_MOCK_RANGE = (3, 25)


def get_initial_chat_history():
    """Returns the initial chat history for new sessions."""
    return [DEFAULT_WELCOME_MESSAGE.copy()]


def get_initial_research_results():
    """Returns the initial research results for demonstration."""
    return [
        {
            "id": "init_1",
            "title": "Example: New GLP-1 Agonist Study",
            "source": "StatNews",
            "relevance_reason": "High impact study relevant to metabolic diseases.",
            "citations": 245,
            "websites": 12,
            "status": "new",
            "news_links": [
                {"title": "New Diabetes Drug Shows Promise", "url": "#"},
                {"title": "GLP-1 Agonist Breakthrough Study", "url": "#"},
            ],
            "paper_links": [
                {"title": "Efficacy of Retatrutide in Type 2 Diabetes", "url": "#"},
                {
                    "title": "Long-term Safety Profile of GLP-1 Receptor Agonists",
                    "url": "#",
                },
            ],
        }
    ]


def get_mock_dialogs():
    """Returns mock dialog data."""
    return [
        {
            "id": "dialog_1",
            "title": "Diabetes Research Discussion",
            "last_message": "Found several promising studies...",
            "timestamp": "2 hours ago",
            "message_count": 8,
        },
        {
            "id": "dialog_2",
            "title": "Cancer Biomarkers",
            "last_message": "Latest clinical trial results show...",
            "timestamp": "1 day ago",
            "message_count": 12,
        },
        {
            "id": "dialog_3",
            "title": "AI in Medical Diagnosis",
            "last_message": "New paper on machine learning...",
            "timestamp": "3 days ago",
            "message_count": 6,
        },
        {
            "id": "dialog_4",
            "title": "COVID-19 Variants Study",
            "last_message": "Research on omicron subvariants...",
            "timestamp": "1 week ago",
            "message_count": 15,
        },
    ]


def generate_mock_finding(prompt):
    """Generates a mock research finding based on user prompt."""
    return {
        "id": str(uuid.uuid4()),
        "title": f"New Finding for: {prompt}",
        "source": "Medscape",
        "relevance_reason": "Matches your interest in clinical outcomes.",
        "citations": random.randint(*CITATION_MOCK_RANGE),  # nosec B311
        "websites": random.randint(*WEBSITE_MOCK_RANGE),  # nosec B311
        "status": "new",
        "news_links": [
            {"title": f"Latest Research on {prompt}", "url": "#"},
            {"title": f"Medical Breakthrough: {prompt}", "url": "#"},
        ],
        "paper_links": [
            {"title": f"Clinical Study Results: {prompt}", "url": "#"},
            {"title": f"Research Paper: {prompt} Analysis", "url": "#"},
        ],
    }
