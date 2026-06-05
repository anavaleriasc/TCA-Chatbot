from functools import lru_cache
from pathlib import Path
from dotenv import find_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from enum import StrEnum


from pydantic import (
    BeforeValidator,
    Field,
    HttpUrl,
    SecretStr,
    TypeAdapter,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict



BASE_DIR = Path(__file__).resolve().parents[2]



class Settings(BaseSettings):
    app_name: str = "TCA CHATBOT API"
    api_prefix: str = "/api"

    api_gateway_timeout: int = 10
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    environment: str = "local"
    database_host: str = "localhost"
    database_port: int = 5433
    database_name: str = "tca_chatbot"
    database_user: str = "admin"
    database_password: str = "admin_tca"
    database_socket: str = ""


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @computed_field
    @property
    def async_database_url(self) -> str:
        if self.environment == "local":
            print("Using local database connection")
            return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
                self.database_user,
                self.database_password,
                self.database_host,
                self.database_port,
                self.database_name,
            )
       

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

class DatabaseType(StrEnum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"
    MONGO = "mongo"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def to_logging_level(self) -> int:
        """Convert to Python logging level constant."""
        import logging

        mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
        }
        return mapping[self]


def check_str_is_http(x: str) -> str:
    http_url_adapter = TypeAdapter(HttpUrl)
    return str(http_url_adapter.validate_python(x))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        validate_default=False,
    )
    MODE: str | None = None

    # Core API settings used by app modules.
    app_name: str = "TCA CHATBOT API"
    api_prefix: str = "/api"
    environment: str = "local"
    database_host: str = "localhost"
    database_port: int = 5433
    database_name: str = "tca_chatbot"
    database_user: str = "admin"
    database_password: str = "admin_tca"
    database_socket: str = ""
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    HOST: str = "0.0.0.0"
    PORT: int = 8080
    GRACEFUL_SHUTDOWN_TIMEOUT: int = 30
    LOG_LEVEL: LogLevel = LogLevel.WARNING

    AUTH_SECRET: SecretStr | None = None

    OPENAI_API_KEY: SecretStr | None = None
    GOOGLE_API_KEY: SecretStr | None = None

    USE_FAKE_MODEL: bool = False
    OPENROUTER_API_KEY: str | None = None

   

    # Database Configuration
    DATABASE_TYPE: DatabaseType = (
        DatabaseType.SQLITE
    )  # Options: DatabaseType.SQLITE or DatabaseType.POSTGRES
    SQLITE_DB_PATH: str = "checkpoints.db"

    # PostgreSQL Configuration
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: SecretStr | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_APPLICATION_NAME: str = "chatbot_api"
    POSTGRES_MIN_CONNECTIONS_PER_POOL: int = 1
    POSTGRES_MAX_CONNECTIONS_PER_POOL: int = 1



    @computed_field  # type: ignore[prop-decorator]
    @property
    def BASE_URL(self) -> str:
        return f"http://{self.HOST}:{self.PORT}"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def async_database_url(self) -> str:
        if self.environment == "local":
            return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
                self.database_user,
                self.database_password,
                self.database_host,
                self.database_port,
                self.database_name,
            )

        return "postgresql://{}:{}@/{}?host={}".format(
            self.database_user,
            self.database_password,
            self.database_name,
            self.database_socket,
        )

    def is_dev(self) -> bool:
        return self.MODE == "dev"


settings = Settings()
