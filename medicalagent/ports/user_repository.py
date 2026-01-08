"""User repository interface (port) for the Medical News Agent."""

from abc import ABC, abstractmethod

from medicalagent.domain.user import UserData


class UserRepository(ABC):
    """Abstract repository for User operations."""

    @abstractmethod
    def get_by_email(self, email: str) -> UserData | None:
        """Get user data by email."""
        pass

    @abstractmethod
    def save(self, user_data: UserData) -> None:
        """Save user data."""
        pass

    @abstractmethod
    def create_user(
        self, email: str, name: str | None = None, picture: str | None = None
    ) -> UserData:
        """Create a new user with default data."""
        pass
