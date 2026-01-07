"""Dependency injection container for the Medical News Agent."""

from medicalagent.adapters.repositories import (
    InMemoryDialogRepository,
    InMemoryFindingsRepository,
    InMemoryUserRepository,
)
from medicalagent.data.mock_data import get_initial_research_results
from medicalagent.ports import DialogRepository, FindingsRepository, UserRepository


class DIContainer:
    """Dependency injection container that provides access to all repositories."""

    def __init__(self):
        """Initialize the DI container with concrete implementations."""
        self._dialog_repository = InMemoryDialogRepository()
        self._findings_repository = InMemoryFindingsRepository()
        self._user_repository = InMemoryUserRepository()

        # Initialize findings repository with default data for dialog 1
        initial_findings = get_initial_research_results(1)
        for finding in initial_findings:
            self._findings_repository.save(finding)

    @property
    def dialog_repository(self) -> DialogRepository:
        """Get the dialog repository instance."""
        return self._dialog_repository

    @property
    def findings_repository(self) -> FindingsRepository:
        """Get the findings repository instance."""
        return self._findings_repository

    @property
    def user_repository(self) -> UserRepository:
        """Get the user repository instance."""
        return self._user_repository


# Global DI container instance
di = DIContainer()
