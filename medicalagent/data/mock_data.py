"""Mock data for the Medical News Agent application."""

import random
import uuid

from medicalagent.domain.dialog import Finding, Link

# Citation and Website Ranges
CITATION_MOCK_RANGE = (10, 500)
WEBSITE_MOCK_RANGE = (3, 25)


def get_initial_research_results(dialog_id: int = 1):
    """Returns the initial research results for demonstration."""
    return [
        Finding(
            id="initial_finding_1",
            dialog_id=1,
            title="Example: New GLP-1 Agonist Study",
            source="StatNews",
            relevance_reason="High impact study relevant to metabolic diseases.",
            citations=245,
            websites=12,
            status="new",
            news_links=[
                Link(title="New Diabetes Drug Shows Promise", url="#"),
                Link(title="GLP-1 Agonist Breakthrough Study", url="#"),
            ],
            paper_links=[
                Link(title="Efficacy of Retatrutide in Type 2 Diabetes", url="#"),
                Link(
                    title="Long-term Safety Profile of GLP-1 Receptor Agonists", url="#"
                ),
            ],
        )
    ]


def generate_mock_finding(prompt, dialog_id):
    """Generates a mock research finding based on user prompt."""
    return Finding(
        id=str(uuid.uuid4()),
        dialog_id=dialog_id,
        title=f"New Finding for: {prompt}",
        source="Medscape",
        relevance_reason="Matches your interest in clinical outcomes.",
        citations=random.randint(*CITATION_MOCK_RANGE),  # nosec B311
        websites=random.randint(*WEBSITE_MOCK_RANGE),  # nosec B311
        status="new",
        news_links=[
            Link(title=f"Latest Research on {prompt}", url="#"),
            Link(title=f"Medical Breakthrough: {prompt}", url="#"),
        ],
        paper_links=[
            Link(title=f"Clinical Study Results: {prompt}", url="#"),
            Link(title=f"Research Paper: {prompt} Analysis", url="#"),
        ],
    )
