from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from medicalagent.infra.db import Base


class DialogModel(Base):
    """SQLAlchemy model for the Dialog table."""

    __tablename__ = "dialogs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    title = Column(String, nullable=False)
    chat_history: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class FindingModel(Base):
    """SQLAlchemy model for the Findings table."""

    __tablename__ = "findings"

    # Using String for ID because domain uses UUID strings
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    dialog_id = Column(Integer, index=True, nullable=False)

    title = Column(String, nullable=False)
    source = Column(String, nullable=False)
    relevance_reason = Column(String, nullable=False)
    citations = Column(Integer, default=0)
    websites = Column(Integer, default=0)
    status = Column(String, default="new")

    # Boolean flag for relevance feedback
    non_relevance_mark = Column(Boolean, default=False)

    # Storing links as JSONB arrays of objects {title: str, url: str}
    news_links: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list)
    paper_links: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserModel(Base):
    """SQLAlchemy model for the Users table."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    picture: Mapped[str | None] = mapped_column(String, nullable=True)

    # Store trusted sites as a JSON list of strings
    trusted_sites: Mapped[list[str]] = mapped_column(JSONB, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
