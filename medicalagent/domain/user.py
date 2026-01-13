"""User domain models for the Medical News Agent."""

from pydantic import AnyHttpUrl, BaseModel, Field


class UserProfile(BaseModel):
    """User profile model."""

    email: str
    picture: AnyHttpUrl | None = None
    name: str | None = None
    trusted_sites: list[str] = Field(default_factory=list)
    created_at: str | None = None
    last_login_at: str | None = None

    @property
    def display_name(self) -> str:
        """Get display name (name or email)."""
        return self.name or self.email.split("@")[0]


class UserData(BaseModel):
    """Complete user data including profile and dialogs."""

    id: int
    profile: UserProfile
