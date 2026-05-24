import secrets
from pathlib import Path
from typing import Literal

from fastapi_csrf_protect import CsrfProtect
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).parent.parent.parent


class AppSettings(BaseSettings):
    IS_DEBUG: bool = Field(default=True)
    IS_DOCKERIZED: bool = Field(default=False)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DBSettings(AppSettings):
    SQLITE_URL: str = "sqlite+aiosqlite:///db.sqlite3"

    POSTGRES_DB: str = "POSTGRES_DB"
    POSTGRES_USER: str = "POSTGRES_USER"
    POSTGRES_PASSWORD: str = "POSTGRES_PASSWORD"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    def get_pg_url(self) -> str:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    def model_post_init(self, __context) -> None:
        object.__setattr__(self,
            "DB_URL", self.get_pg_url() if self.IS_DOCKERIZED else self.SQLITE_URL,
        )


class SessionSettings(AppSettings):
    COOKIE_KEY: str = "csrf_token"
    SECRET_KEY: str = secrets.token_urlsafe(50)
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"
    COOKIE_SECURE: bool = True
    HTTPONLY: bool = True
    SESSION_MAX_AGE: int = 60 * 60 * 24 * 14


class RedisSettings(AppSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CONNECTION_POOL_MAXSIZE: int = 10
    EXPIRE: int = 60 * 60 * 24 * 14

    def model_post_init(self, __context) -> None:
        object.__setattr__(
            self, "REDIS_HOST", "redis" if self.IS_DOCKERIZED else "localhost"
        )
        object.__setattr__(
            self,
            "REDIS_URL",
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}",
        )


class GunicornSettings(AppSettings):
    HOST: str = "localhost"
    PORT: int = 8080
    TIMEOUT: int = 900

    def model_post_init(self, __context) -> None:
        object.__setattr__(
            self, "WORKERS", 1 if self.IS_DEBUG else 4
        )
        object.__setattr__(
            self,
            "LOG_LEVEL", "DEBUG" if self.IS_DEBUG else "INFO",
        )


class Settings(AppSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    session: SessionSettings = SessionSettings()
    redis: RedisSettings = RedisSettings()
    gunicorn: GunicornSettings = GunicornSettings()


settings = Settings()


@CsrfProtect.load_config
def get_csrf_config():
    return settings.session
