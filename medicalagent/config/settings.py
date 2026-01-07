from urllib import parse

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AI_SETTINGS__", env_file=".env", extra="ignore"
    )
    groq_api_key: SecretStr = SecretStr("XXX")
    main_model: str = "moonshotai/kimi-k2-instruct-0905"


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


class Settings(BaseSettings):
    AI_SETTINGS: AISettings = AISettings()
    POSTGRESQL: PostgreSQLSettings = PostgreSQLSettings()
