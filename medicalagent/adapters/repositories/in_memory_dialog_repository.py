"""In-memory implementation of DialogRepository."""

from medicalagent.domain.dialog import Dialog
from medicalagent.ports.dialog_repository import DialogRepository


class InMemoryDialogRepository(DialogRepository):
    """In-memory implementation of DialogRepository using mock data."""

    def __init__(self):
        """Initialize the repository."""
        self._dialogs = self._get_mock_dialogs()

    def _get_mock_dialogs(self) -> list[Dialog]:
        """Returns mock dialog data."""
        return [
            Dialog(id=1, title="Diabetes Research"),
            Dialog(id=2, title="Cancer Biomarkers"),
            Dialog(id=3, title="AI in Medical Diagnosis"),
            Dialog(id=4, title="COVID-19 Variants"),
        ]

    def get_all(self) -> list[Dialog]:
        """Get all dialogs."""
        return self._dialogs.copy()

    def get_by_id(self, dialog_id: int) -> Dialog | None:
        """Get a dialog by ID."""
        return next((d for d in self._dialogs if d.id == dialog_id), None)

    def save(self, dialog: Dialog) -> None:
        """Save a dialog."""
        # Check if dialog already exists
        existing = self.get_by_id(dialog.id)
        if existing:
            # Update existing dialog
            idx = self._dialogs.index(existing)
            self._dialogs[idx] = dialog
        else:
            # Add new dialog
            self._dialogs.append(dialog)

    def delete(self, dialog_id: int) -> None:
        """Delete a dialog by ID."""
        self._dialogs = [d for d in self._dialogs if d.id != dialog_id]
