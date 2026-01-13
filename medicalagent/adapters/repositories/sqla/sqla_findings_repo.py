from sqlalchemy.orm import Session

from medicalagent.adapters.repositories.sqla.models import FindingModel
from medicalagent.domain.dialog import Link
from medicalagent.domain.finding import Finding
from medicalagent.infra.db import get_session
from medicalagent.ports.findings_repository import FindingsRepository


class SQLAFindingsRepository(FindingsRepository):
    """SQLAlchemy implementation of the FindingsRepository."""

    def get_all(self) -> list[Finding]:
        session: Session = get_session()
        try:
            db_findings = session.query(FindingModel).all()
            return [self._to_domain(f) for f in db_findings]
        finally:
            session.close()

    def get_by_dialog_id(self, dialog_id: int) -> list[Finding]:
        session: Session = get_session()
        try:
            db_findings = (
                session.query(FindingModel)
                .filter(FindingModel.dialog_id == dialog_id)
                # Order by creation time (implicitly via ID or explicit created_at if strictly needed)
                # Ideally we order by created_at, but base model has it.
                .order_by(FindingModel.created_at.desc())
                .all()
            )
            return [self._to_domain(f) for f in db_findings]
        finally:
            session.close()

    def get_by_id(self, finding_id: int) -> Finding | None:
        session: Session = get_session()
        try:
            db_finding = (
                session.query(FindingModel)
                .filter(FindingModel.id == finding_id)
                .first()
            )
            if not db_finding:
                return None
            return self._to_domain(db_finding)
        finally:
            session.close()

    def save(self, finding: Finding) -> None:
        """Saves a finding (Insert or Update)."""
        session: Session = get_session()
        try:
            # Check if it exists
            existing = (
                session.query(FindingModel)
                .filter(FindingModel.id == finding.id)
                .first()
            )

            # Convert nested Pydantic objects to dicts for JSONB
            news_data = [link.model_dump() for link in finding.news_links]
            paper_data = [link.model_dump() for link in finding.paper_links]

            if existing:
                # UPDATE
                existing.title = finding.title
                existing.source = finding.source
                existing.relevance_reason = finding.relevance_reason
                existing.citations = finding.citations
                existing.websites = finding.websites
                existing.status = finding.status
                existing.non_relevance_mark = finding.non_relevance_mark
                existing.news_links = news_data
                existing.paper_links = paper_data
            else:
                # INSERT
                new_finding = FindingModel(
                    id=finding.id,
                    dialog_id=finding.dialog_id,
                    title=finding.title,
                    source=finding.source,
                    relevance_reason=finding.relevance_reason,
                    citations=finding.citations,
                    websites=finding.websites,
                    status=finding.status,
                    non_relevance_mark=finding.non_relevance_mark,
                    news_links=news_data,
                    paper_links=paper_data,
                )
                session.add(new_finding)

            session.commit()
        finally:
            session.close()

    def delete(self, finding_id: int) -> None:
        session: Session = get_session()
        try:
            db_finding = (
                session.query(FindingModel)
                .filter(FindingModel.id == finding_id)
                .first()
            )
            if db_finding:
                session.delete(db_finding)
                session.commit()
        finally:
            session.close()

    def mark_non_relevant(self, finding_id: int) -> None:
        session: Session = get_session()
        try:
            db_finding = (
                session.query(FindingModel)
                .filter(FindingModel.id == finding_id)
                .first()
            )
            if db_finding:
                db_finding.non_relevance_mark = True
                session.commit()
        finally:
            session.close()

    def mark_relevant(self, finding_id: int) -> None:
        session: Session = get_session()
        try:
            db_finding = (
                session.query(FindingModel)
                .filter(FindingModel.id == finding_id)
                .first()
            )
            if db_finding:
                db_finding.non_relevance_mark = False
                session.commit()
        finally:
            session.close()

    def _to_domain(self, db_finding: FindingModel) -> Finding:
        """Converts ORM model to Pydantic Domain model."""
        # Convert list of dicts back to list of Link objects
        news = [Link(**link) for link in db_finding.news_links]
        papers = [Link(**link) for link in db_finding.paper_links]

        return Finding(
            id=db_finding.id,
            dialog_id=db_finding.dialog_id,
            title=db_finding.title,
            source=db_finding.source,
            relevance_reason=db_finding.relevance_reason,
            citations=db_finding.citations,
            websites=db_finding.websites,
            status=db_finding.status,
            non_relevance_mark=db_finding.non_relevance_mark,
            news_links=news,
            paper_links=papers,
        )
