"""Mock data for the Medical News Agent application."""

import random
import uuid

from medicalagent.domain.dialog import Dialog, Finding, Link
from medicalagent.drivers.defaults import DEFAULT_WELCOME_MESSAGE

# In-memory storage for findings (to be replaced with database later)
_findings_store: list[Finding] = []

# Citation and Website Ranges
CITATION_MOCK_RANGE = (10, 500)
WEBSITE_MOCK_RANGE = (3, 25)


def get_initial_chat_history():
    """Returns the initial chat history for new sessions."""
    return [DEFAULT_WELCOME_MESSAGE.copy()]


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


def get_dialogs() -> list[Dialog]:
    """Returns mock dialog data."""
    return [
        Dialog(id=1, title="Diabetes Research"),
        Dialog(id=2, title="Cancer Biomarkers"),
        Dialog(id=3, title="AI in Medical Diagnosis"),
        Dialog(id=4, title="COVID-19 Variants"),
    ]


def generate_next_dialog_id():
    """Generates the next available dialog ID based on existing dialogs."""
    dialogs = get_dialogs()
    if not dialogs:
        return 1

    # Find the maximum ID from existing dialogs
    max_id = max(dialog.id for dialog in dialogs)
    return max_id + 1


def create_dialog() -> Dialog:
    """Creates a new dialog object with default values."""
    new_dialog_id = generate_next_dialog_id()
    return Dialog(id=new_dialog_id, title="New Dialog", chat_history=[])


def get_dialog(active_dialog_id):
    """Gets the active dialog from a list of dialogs based on ID."""
    dialogs = get_dialogs()
    if not active_dialog_id:
        return None
    return next((d for d in dialogs if d.id == active_dialog_id), None)


def initialize_findings_store():
    """Initialize the findings store with default data."""
    global _findings_store  # noqa: PLW0602
    if not _findings_store:  # Only initialize once
        initial_findings = get_initial_research_results(1)
        _findings_store.extend(initial_findings)


def get_findings(dialog_id: int) -> list[Finding]:
    """Gets all findings for a specific dialog."""
    initialize_findings_store()
    return [
        f
        for f in _findings_store
        if f.dialog_id == dialog_id and f.status != "dismissed"
    ]


def add_finding(finding: Finding):
    """Adds a finding to the store."""
    initialize_findings_store()
    _findings_store.append(finding)


def delete_finding(finding_id: str):
    """Deletes a finding from the store."""
    initialize_findings_store()
    global _findings_store  # noqa: PLW0602
    _findings_store[:] = [f for f in _findings_store if f.id != finding_id]


def mark_finding_non_relevant(finding_id: str):
    """Marks a finding as non-relevant."""
    initialize_findings_store()
    for finding in _findings_store:
        if finding.id == finding_id:
            finding.non_relevance_mark = True
            break


def mark_finding_relevant(finding_id: str):
    """Marks a finding as relevant (removes non-relevance mark)."""
    initialize_findings_store()
    for finding in _findings_store:
        if finding.id == finding_id:
            finding.non_relevance_mark = False
            break


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
