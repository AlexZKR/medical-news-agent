"""Dialog repository interface (port) for the Medical News Agent."""

from abc import ABC, abstractmethod

from langchain_core.messages import ChatMessage

from medicalagent.domain.dialog import Dialog


class DialogRepository(ABC):
    """Abstract repository for Dialog operations."""

    @abstractmethod
    def create(self, title: str, messages: list[ChatMessage]) -> Dialog:
        """Create new empty dialog"""
        pass

    @abstractmethod
    def get_all(self) -> list[Dialog]:
        """Get all dialogs."""
        pass

    @abstractmethod
    def get_by_id(self, dialog_id: int) -> Dialog | None:
        """Get a dialog by ID."""
        pass

    @abstractmethod
    def save(self, dialog: Dialog) -> None:
        """Save a dialog."""
        pass

    @abstractmethod
    def delete(self, dialog_id: int) -> None:
        """Delete a dialog by ID."""
        pass
