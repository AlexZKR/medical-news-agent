"""In-memory implementation of UserRepository."""

from medicalagent.domain.dialog import Dialog
from medicalagent.domain.user import UserData, UserProfile


class InMemoryUserRepository:
    """In-memory implementation of UserRepository using mock data."""

    def __init__(self):
        """Initialize the repository."""
        self._users: dict[str, UserData] = {}

    def get_by_email(self, email: str) -> UserData | None:
        """Get user data by email."""
        return self._users.get(email)

    def save(self, user_data: UserData) -> None:
        """Save user data."""
        self._users[user_data.profile.email] = user_data

    def delete(self, email: str) -> None:
        """Delete user data by email."""
        if email in self._users:
            del self._users[email]

    def exists(self, email: str) -> bool:
        """Check if user exists."""
        return email in self._users

    def get_all_users(self) -> list[str]:
        """Get all user emails."""
        return list(self._users.keys())

    def create_default_user(self, email: str, name: str | None = None):
        """Create a new user with default data."""
        profile = UserProfile(email=email, name=name)

        # Create default dialogs for new users
        default_dialogs = [
            Dialog(id=1, title="Diabetes Research"),
            Dialog(id=2, title="Cancer Biomarkers"),
            Dialog(id=3, title="AI in Medical Diagnosis"),
            Dialog(id=4, title="COVID-19 Variants"),
        ]

        user_data = UserData(profile=profile, dialogs=default_dialogs)

        self.save(user_data)
        return user_data
