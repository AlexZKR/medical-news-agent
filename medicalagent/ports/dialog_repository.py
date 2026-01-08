"""Dialog repository interface (port) for the Medical News Agent."""

from abc import ABC, abstractmethod

from medicalagent.domain.dialog import ChatMessage, Dialog


class DialogRepository(ABC):
    """Abstract repository for Dialog operations."""

    @abstractmethod
    def create(
        self, messages: list[ChatMessage], user_id: int, title: str | None = None
    ) -> Dialog:
        """Create new empty dialog"""
        pass

    @abstractmethod
    def get_all(self) -> list[Dialog]:
        """Get all dialogs."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list[Dialog]:
        """Get dialogs for user"""
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
