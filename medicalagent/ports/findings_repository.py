"""Findings repository interface (port)."""

from abc import ABC, abstractmethod

from medicalagent.domain.dialog import Link
from medicalagent.domain.finding import Finding


class FindingsRepository(ABC):
    """Abstract repository for Finding operations."""

    @abstractmethod
    def create(  # noqa: PLR0913
        self,
        dialog_id: int,
        title: str,
        source: str,
        relevance_reason: str,
        citations: int,
        websites: int,
        news_links: list[Link],
        paper_links: list[Link],
    ) -> Finding:
        """Create a new finding from raw data and return the domain object with ID."""
        pass

    @abstractmethod
    def update(self, finding: Finding) -> None:
        """Update an existing finding."""
        pass

    @abstractmethod
    def get_all(self) -> list[Finding]:
        pass

    @abstractmethod
    def get_by_dialog_id(self, dialog_id: int) -> list[Finding]:
        pass

    @abstractmethod
    def get_by_id(self, finding_id: int) -> Finding | None:
        pass

    @abstractmethod
    def delete(self, finding_id: int) -> None:
        pass

    @abstractmethod
    def mark_non_relevant(self, finding_id: int) -> None:
        pass

    @abstractmethod
    def mark_relevant(self, finding_id: int) -> None:
        pass
