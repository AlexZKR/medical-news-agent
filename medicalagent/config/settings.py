from urllib import parse

import urllib3
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPTransportSettings(BaseSettings):
    chunk_size: int = 8192
    user_agent: str = "MedicalNewsAgent/1.0 pet-project"
    default_timeout: int = 30

    @property
    def common_headers(self) -> dict[str, str]:
        return {"user-agent": self.user_agent}


class RetryBackoffSettings(BaseSettings):
    max_retries: int = 5
    backoff_factor: float = 0.2
    backoff_jitter: float = 2
    max_backoff: int = 120
    status_forcelist: list[int] = [413, 429, 502, 503, 504]
    allowed_methods: frozenset[str] = urllib3.Retry.DEFAULT_ALLOWED_METHODS


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AI_SETTINGS__", env_file=".env", extra="ignore"
    )
    groq_api_key: SecretStr = SecretStr("XXX")
    tavily_api_key: SecretStr = SecretStr("XXX")

    primary_model: str = "moonshotai/kimi-k2-instruct-0905"
    primary_model_max_tokens: int = 10_000

    fallback_model: str = "llama-3.3-70b-versatile"
    fallback_model_max_tokens: int = 10_000

    summarization_model: str = "llama-3.1-8b-instant"
    summarization_model_max_tokens: int = 10_000


class PostgreSQLSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="db__", env_file=".env", extra="ignore"
    )

    host: str = "postgres"
    port: int = 5432
    user: str = "postgres"
    password: SecretStr | None = SecretStr("pass")
    name: str = "postgres"

    @property
    def dsn(self) -> str:
        """
        Returns a PostgreSQL DSN string in the format:
        postgresql://user:password@host:port/dbname
        """
        password_part = (
            f":{parse.quote(self.password.get_secret_value())}" if self.password else ""
        )
        return f"postgresql://{self.user}{password_part}@{self.host}:{self.port}/{self.name}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="app__", env_file=".env", extra="ignore"
    )
    ENV: str = "dev"


class Settings(BaseSettings):
    AI_SETTINGS: AISettings = AISettings()
    POSTGRESQL: PostgreSQLSettings = PostgreSQLSettings()
    APP_SETTINGS: AppSettings = AppSettings()
