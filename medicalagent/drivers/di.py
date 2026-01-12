"""Dependency injection container for the Medical News Agent."""

from medicalagent.adapters.agent.langchain_base import LangChainAgentService
from medicalagent.adapters.repositories import (
    InMemoryDialogRepository,
    InMemoryFindingsRepository,
    InMemoryUserRepository,
)
from medicalagent.infra.requests_transport.base import AbstractSyncHTTPTransport
from medicalagent.infra.requests_transport.requests_transport import (
    RequestsHTTPTransport,
)
from medicalagent.ports import (
    AgentService,
    DialogRepository,
    FindingsRepository,
    UserRepository,
)


class DIContainer:
    """Dependency injection container that provides access to all repositories."""

    def __init__(self):
        """Initialize the DI container with concrete implementations."""
        self._dialog_repository = InMemoryDialogRepository()
        self._findings_repository = InMemoryFindingsRepository()
        self._user_repository = InMemoryUserRepository()
        self._http_transport = RequestsHTTPTransport()
        self._agent_service = LangChainAgentService(container=self)

    @property
    def dialog_repository(self) -> DialogRepository:
        """Get the dialog repository instance."""
        return self._dialog_repository

    @property
    def agent_service(self) -> AgentService:
        """Get the agent service instance."""
        return self._agent_service

    @property
    def findings_repository(self) -> FindingsRepository:
        """Get the findings repository instance."""
        return self._findings_repository

    @property
    def user_repository(self) -> UserRepository:
        """Get the user repository instance."""
        return self._user_repository

    @property
    def http_transport(self) -> AbstractSyncHTTPTransport:
        return self._http_transport


di_container = DIContainer()
