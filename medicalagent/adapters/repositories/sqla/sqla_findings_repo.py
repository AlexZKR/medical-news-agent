from sqlalchemy.orm import Session

from medicalagent.adapters.repositories.sqla.models import FindingModel
from medicalagent.domain.dialog import Link
from medicalagent.domain.finding import Finding
from medicalagent.infra.db import get_session
from medicalagent.ports.findings_repository import FindingsRepository


class SQLAFindingsRepository(FindingsRepository):
    """SQLAlchemy implementation of the FindingsRepository."""

    def create(
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
        session: Session = get_session()
        try:
            # 1. Prepare JSONB data
            news_data = [link.model_dump() for link in news_links]
            paper_data = [link.model_dump() for link in paper_links]

            # 2. Create DB Model (ID is None here, DB will assign it)
            db_finding = FindingModel(
                dialog_id=dialog_id,
                title=title,
                source=source,
                relevance_reason=relevance_reason,
                citations=citations,
                websites=websites,
                status="new",
                non_relevance_mark=False,
                news_links=news_data,
                paper_links=paper_data,
            )

            session.add(db_finding)
            session.commit()
            session.refresh(db_finding)

            # 3. Return Strict Domain Object (now with ID)
            return self._to_domain(db_finding)
        finally:
            session.close()

    def update(self, finding: Finding) -> None:
        session: Session = get_session()
        try:
            db_finding = (
                session.query(FindingModel)
                .filter(FindingModel.id == finding.id)
                .first()
            )
            if db_finding:
                db_finding.title = finding.title
                db_finding.source = finding.source
                db_finding.relevance_reason = finding.relevance_reason
                db_finding.citations = finding.citations
                db_finding.websites = finding.websites
                db_finding.status = finding.status
                db_finding.non_relevance_mark = finding.non_relevance_mark

                # Update JSONB columns
                db_finding.news_links = [l.model_dump() for l in finding.news_links]
                db_finding.paper_links = [l.model_dump() for l in finding.paper_links]

                session.commit()
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
                .order_by(FindingModel.created_at.desc())
                .all()
            )
            return [self._to_domain(f) for f in db_findings]
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
        news = [Link(**link) for link in db_finding.news_links]
        papers = [Link(**link) for link in db_finding.paper_links]

        return Finding(
            id=db_finding.id,  # Guaranteed to be int now
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
