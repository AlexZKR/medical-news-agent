"""In-memory implementation of UserRepository."""

from medicalagent.domain.user import UserData, UserProfile
from medicalagent.ports import UserRepository


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository using mock data."""

    def __init__(self):
        """Initialize the repository."""
        self._users: dict[int, UserData] = {}

    def get_by_id(self, id: int) -> UserData | None:
        return self._users.get(id, None)

    def get_by_email(self, email: str) -> UserData | None:
        """Get user data by email."""
        return next((u for u in self._users.values() if u.profile.email == email), None)

    def save(self, user_data: UserData) -> None:
        """Save user data."""
        self._users[user_data.id] = user_data

    def create_user(
        self, email: str, name: str | None = None, picture: str | None = None
    ):
        """Create a new user with default data."""
        last_id = -1
        if self._users:
            last_id = self._users[-1].id

        profile = UserProfile(email=email, name=name, picture=picture)
        user_data = UserData(profile=profile, id=last_id + 1)

        self.save(user_data)
        return user_data
