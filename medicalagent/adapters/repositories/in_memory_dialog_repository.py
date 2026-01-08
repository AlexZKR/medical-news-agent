"""In-memory implementation of DialogRepository."""

from medicalagent.domain.dialog import DEFAULT_DIALOG_TITLE, ChatMessage, Dialog
from medicalagent.ports.dialog_repository import DialogRepository


class InMemoryDialogRepository(DialogRepository):
    """In-memory implementation of DialogRepository using mock data."""

    def __init__(self) -> None:
        self._dialogs: list[Dialog] = []

    def create(
        self, messages: list[ChatMessage], user_id: int, title: str | None = None
    ) -> Dialog:
        last_id = -1
        if self._dialogs:
            last_id = self._dialogs[-1].id
        d = Dialog(
            id=last_id + 1,
            title=title if title else DEFAULT_DIALOG_TITLE,
            chat_history=messages,
            user_id=user_id,
        )
        self._dialogs.append(d)
        return d

    def get_all(self) -> list[Dialog]:
        """Get all dialogs."""
        return self._dialogs.copy()

    def get_by_user_id(self, user_id: int) -> list[Dialog]:
        return [d for d in self._dialogs if d.user_id == user_id]

    def get_by_id(self, dialog_id: int) -> Dialog | None:
        """Get a dialog by ID."""
        return next((d for d in self._dialogs if d.id == dialog_id), None)

    def save(self, dialog: Dialog) -> None:
        """Save a dialog."""  # Check if dialog already exists
        existing = self.get_by_id(dialog.id)
        if existing:
            # Update existing dialog
            idx = self._dialogs.index(existing)
            self._dialogs[idx] = dialog

    def delete(self, dialog_id: int) -> None:
        """Delete a dialog by ID."""
        self._dialogs = [d for d in self._dialogs if d.id != dialog_id]
