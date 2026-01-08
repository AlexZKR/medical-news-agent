"""In-memory implementation of DialogRepository."""

from langchain_core.messages import ChatMessage

from medicalagent.domain.dialog import Dialog
from medicalagent.ports.dialog_repository import DialogRepository


class InMemoryDialogRepository(DialogRepository):
    """In-memory implementation of DialogRepository using mock data."""

    def __init__(self) -> None:
        self._dialogs: list[Dialog] = []

    def create(self, title: str, messages: list[ChatMessage]) -> Dialog:
        last_id = -1
        if self._dialogs:
            last_id = self._dialogs[-1].id
        d = Dialog(id=last_id + 1)
        self._dialogs.append(d)
        return d

    def get_all(self) -> list[Dialog]:
        """Get all dialogs."""
        return self._dialogs.copy()  # type: ignore

    def get_by_id(self, dialog_id: int) -> Dialog | None:
        """Get a dialog by ID."""
        return next((d for d in self._dialogs if d.id == dialog_id), None)  # type: ignore

    def save(self, dialog: Dialog) -> None:
        """Save a dialog."""
        # Check if dialog already exists
        existing = self.get_by_id(dialog.id)
        if existing:
            # Update existing dialog
            idx = self._dialogs.index(existing)  # type: ignore
            self._dialogs[idx] = dialog  # type: ignore
        else:
            # Add new dialog
            self._dialogs.append(dialog)  # type: ignore

    def delete(self, dialog_id: int) -> None:
        """Delete a dialog by ID."""
        self._dialogs = [d for d in self._dialogs if d.id != dialog_id]  # type: ignore
