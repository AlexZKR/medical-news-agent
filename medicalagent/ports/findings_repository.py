"""Findings repository interface (port) for the Medical News Agent."""

from abc import ABC, abstractmethod

from medicalagent.domain.dialog import Finding


class FindingsRepository(ABC):
    """Abstract repository for Finding operations."""

    @abstractmethod
    def get_all(self) -> list[Finding]:
        """Get all findings."""
        pass

    @abstractmethod
    def get_by_dialog_id(self, dialog_id: int) -> list[Finding]:
        """Get all findings for a specific dialog."""
        pass

    @abstractmethod
    def get_by_id(self, finding_id: str) -> Finding | None:
        """Get a finding by ID."""
        pass

    @abstractmethod
    def save(self, finding: Finding) -> None:
        """Save a finding."""
        pass

    @abstractmethod
    def delete(self, finding_id: str) -> None:
        """Delete a finding by ID."""
        pass

    @abstractmethod
    def mark_non_relevant(self, finding_id: str) -> None:
        """Mark a finding as non-relevant."""
        pass

    @abstractmethod
    def mark_relevant(self, finding_id: str) -> None:
        """Mark a finding as relevant."""
        pass
