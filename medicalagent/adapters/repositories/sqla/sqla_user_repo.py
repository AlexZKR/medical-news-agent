from datetime import datetime

from sqlalchemy.orm import Session

from medicalagent.adapters.repositories.sqla.models import UserModel
from medicalagent.domain.user import UserData, UserProfile
from medicalagent.infra.db import get_session
from medicalagent.ports.user_repository import UserRepository


class SQLAUserRepository(UserRepository):
    """SQLAlchemy implementation of the UserRepository."""

    def get_by_email(self, email: str) -> UserData | None:
        session: Session = get_session()
        try:
            db_user = session.query(UserModel).filter(UserModel.email == email).first()
            if not db_user:
                return None
            return self._to_domain(db_user)
        finally:
            session.close()

    def create_user(
        self, email: str, name: str | None = None, picture: str | None = None
    ) -> UserData:
        session: Session = get_session()
        try:
            # Check if exists first to be safe, though usage usually implies new
            existing = session.query(UserModel).filter(UserModel.email == email).first()
            if existing:
                return self._to_domain(existing)

            new_user = UserModel(
                email=email,
                name=name,
                picture=picture,
                trusted_sites=[],
                last_login_at=datetime.now(),
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return self._to_domain(new_user)
        finally:
            session.close()

    def save(self, user_data: UserData) -> None:
        """Updates an existing user."""
        session: Session = get_session()
        try:
            db_user = (
                session.query(UserModel).filter(UserModel.id == user_data.id).first()
            )
            if db_user:
                profile = user_data.profile
                db_user.name = profile.name
                db_user.picture = str(profile.picture) if profile.picture else None
                db_user.trusted_sites = profile.trusted_sites

                # Update login timestamp if provided in domain
                if profile.last_login_at:
                    try:
                        db_user.last_login_at = datetime.fromisoformat(
                            profile.last_login_at
                        )
                    except ValueError:
                        pass  # Keep existing if parse fails

                session.commit()
        finally:
            session.close()

    # --- Helper Method ---

    def _to_domain(self, db_user: UserModel) -> UserData:
        """Converts ORM model to Pydantic Domain model."""

        # Convert DB datetime to ISO string for domain
        created_at_str = db_user.created_at.isoformat() if db_user.created_at else None
        last_login_str = (
            db_user.last_login_at.isoformat() if db_user.last_login_at else None
        )

        profile = UserProfile(
            email=db_user.email,
            name=db_user.name,
            picture=db_user.picture,
            trusted_sites=db_user.trusted_sites,
            created_at=created_at_str,
            last_login_at=last_login_str,
        )

        return UserData(id=db_user.id, profile=profile)
