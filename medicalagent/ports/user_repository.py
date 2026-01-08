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
    def delete(self, email: str) -> None:
        """Delete user data by email."""
        pass

    @abstractmethod
    def exists(self, email: str) -> bool:
        """Check if user exists."""
        pass

    @abstractmethod
    def get_all_users(self) -> list[str]:
        """Get all user emails (for admin purposes)."""
        pass

    @abstractmethod
    def create_user(self, email: str, name: str | None = None):
        """Create a new user with default data."""
        pass
