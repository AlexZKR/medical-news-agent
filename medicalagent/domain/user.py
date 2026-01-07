"""User domain models for the Medical News Agent."""

from pydantic import BaseModel, Field

from .dialog import Dialog


class UserPreferences(BaseModel):
    """User preferences model."""

    theme: str = Field(default="light", description="UI theme preference")
    language: str = Field(default="en", description="Preferred language")
    notifications_enabled: bool = Field(
        default=True, description="Enable notifications"
    )
    auto_save: bool = Field(default=True, description="Auto-save user data")


class UserProfile(BaseModel):
    """User profile model."""

    email: str
    name: str | None = None
    trusted_sites: list[str] = Field(default_factory=list)
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    created_at: str | None = None
    last_login_at: str | None = None

    @property
    def display_name(self) -> str:
        """Get display name (name or email)."""
        return self.name or self.email.split("@")[0]


class UserData(BaseModel):
    """Complete user data including profile and dialogs."""

    profile: UserProfile
    dialogs: list[Dialog] = Field(default_factory=list)

    def get_dialogs(self) -> list[Dialog]:
        """Get all user dialogs."""
        return self.dialogs

    def add_dialog(self, dialog: Dialog) -> None:
        """Add a dialog to user data."""
        self.dialogs.append(dialog)

    def remove_dialog(self, dialog_id: int) -> None:
        """Remove a dialog from user data."""
        self.dialogs = [d for d in self.dialogs if d.id != dialog_id]
