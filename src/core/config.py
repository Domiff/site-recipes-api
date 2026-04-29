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
    DB_URL: str = Field(default="sqlite+aisqlite:///db.sqlite3")


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
    EXPIRE: int = 60 * 60

    def model_post_init(self, __context) -> None:
        object.__setattr__(
            self, "REDIS_HOST", "redis" if self.IS_DOCKERIZED else "localhost"
        )
        object.__setattr__(
            self,
            "REDIS_URL",
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}",
        )


class Settings(AppSettings):
    app_settings: AppSettings = AppSettings()
    db_settings: DBSettings = DBSettings()
    session_settings: SessionSettings = SessionSettings()
    redis_settings: RedisSettings = RedisSettings()


settings = Settings()


@CsrfProtect.load_config
def get_csrf_config():
    return settings.session_settings
