"""In-memory implementation of FindingsRepository."""

from medicalagent.domain.finding import Finding
from medicalagent.ports.findings_repository import FindingsRepository


class InMemoryFindingsRepository(FindingsRepository):
    """In-memory implementation of FindingsRepository using mock data."""

    def __init__(self) -> None:
        """Initialize the repository."""
        self._findings: list[Finding] = []

    def get_all(self) -> list[Finding]:
        """Get all findings."""
        return self._findings.copy()

    def get_by_dialog_id(self, dialog_id: int) -> list[Finding]:
        """Get all findings for a specific dialog."""
        return [f for f in self._findings if f.dialog_id == dialog_id]

    def get_by_id(self, finding_id: int) -> Finding | None:
        """Get a finding by ID."""
        return next((f for f in self._findings if f.id == finding_id), None)

    def save(self, finding: Finding) -> None:
        """Save a finding."""
        # Check if finding already exists
        existing = self.get_by_id(finding.id)
        if existing:
            # Update existing finding
            idx = self._findings.index(existing)
            self._findings[idx] = finding
        else:
            # Add new finding
            self._findings.append(finding)

    def delete(self, finding_id: int) -> None:
        """Delete a finding by ID."""
        self._findings = [f for f in self._findings if f.id != finding_id]

    def mark_non_relevant(self, finding_id: int) -> None:
        """Mark a finding as non-relevant."""
        finding = self.get_by_id(finding_id)
        if finding:
            finding.non_relevance_mark = True

    def mark_relevant(self, finding_id: int) -> None:
        """Mark a finding as relevant (removes non-relevance mark)."""
        finding = self.get_by_id(finding_id)
        if finding:
            finding.non_relevance_mark = False
