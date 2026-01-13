from sqlalchemy import nulls_last
from sqlalchemy.orm import Session

from medicalagent.adapters.repositories.sqla.models import DialogModel
from medicalagent.domain.dialog import DEFAULT_DIALOG_TITLE, ChatMessage, Dialog
from medicalagent.infra.db import get_session
from medicalagent.ports.dialog_repository import DialogRepository


class SQLADialogRepository(DialogRepository):
    """SQLAlchemy implementation of the DialogRepository."""

    def create(
        self, messages: list[ChatMessage], user_id: int, title: str | None = None
    ) -> Dialog:
        session: Session = get_session()
        try:
            final_title = title if title else DEFAULT_DIALOG_TITLE

            # 2. Convert Domain -> ORM
            messages_data = [msg.model_dump() for msg in messages]

            db_dialog = DialogModel(
                title=final_title, user_id=user_id, chat_history=messages_data
            )

            session.add(db_dialog)
            session.commit()
            session.refresh(db_dialog)

            # 3. Convert ORM -> Domain
            return self._to_domain(db_dialog)
        finally:
            session.close()

    def get_by_id(self, dialog_id: int) -> Dialog | None:
        session: Session = get_session()
        try:
            db_dialog = (
                session.query(DialogModel).filter(DialogModel.id == dialog_id).first()
            )
            if not db_dialog:
                return None
            return self._to_domain(db_dialog)
        finally:
            session.close()

    def get_by_user_id(self, user_id: int) -> list[Dialog]:
        """Get all dialogs for a specific user."""
        session: Session = get_session()
        try:
            db_dialogs = (
                session.query(DialogModel)
                .filter(DialogModel.user_id == user_id)
                .order_by(nulls_last(DialogModel.updated_at.desc()))
                .all()
            )
            return [self._to_domain(d) for d in db_dialogs]
        finally:
            session.close()

    def save(self, dialog: Dialog) -> None:
        """Updates an existing dialog."""
        session: Session = get_session()
        try:
            db_dialog = (
                session.query(DialogModel).filter(DialogModel.id == dialog.id).first()
            )

            if db_dialog:
                # Use type hints or cast if Mypy still complains about Column vs str
                db_dialog.title = dialog.title

                # Convert Pydantic objects back to simple dicts for JSONB
                history_data = [msg.model_dump() for msg in dialog.chat_history]
                db_dialog.chat_history = history_data

                session.commit()
        finally:
            session.close()

    def get_chat_history_by_id(self, dialog_id: int) -> list[ChatMessage]:
        """Optimization: Fetch only the history, though for JSONB we usually fetch the row."""
        # Re-using get_by_id for simplicity as JSONB usually loads with the row anyway.
        dialog = self.get_by_id(dialog_id)
        return dialog.chat_history if dialog else []

    def delete(self, dialog_id: int) -> None:
        session: Session = get_session()
        try:
            db_dialog = (
                session.query(DialogModel).filter(DialogModel.id == dialog_id).first()
            )
            if db_dialog:
                session.delete(db_dialog)
                session.commit()
        finally:
            session.close()

    def _to_domain(self, db_dialog: DialogModel) -> Dialog:
        """Converts an SQLAlchemy model to a Pydantic Domain model."""
        # Convert list of dicts (from JSONB) back to list of ChatMessage objects
        messages = [ChatMessage(**msg) for msg in db_dialog.chat_history]

        return Dialog(
            id=db_dialog.id,
            user_id=db_dialog.user_id,
            title=db_dialog.title,
            chat_history=messages,
        )
