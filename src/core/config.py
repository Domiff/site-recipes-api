import secrets
from pathlib import Path
from typing import Literal

from fastapi_csrf_protect import CsrfProtect
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).parent.parent.parent


class AppSettings(BaseSettings):
    DB_URL: str = Field(default="sqlite+aisqlite:///db.sqlite3")

    IS_DEBUG: bool = Field(default=True)
    IS_DOCKERIZED: bool = Field(default=False)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class CsrfSettings(BaseSettings):
    cookie_key: str = "csrf_token"
    secret_key: str = secrets.token_urlsafe(50)
    cookie_samesite: Literal["lax", "strict", "none"] = "lax"
    cookie_secure: bool = True
    httponly: bool = True


class Settings(BaseSettings):
    app_settings: AppSettings = AppSettings()
    csrf_settings: CsrfSettings = CsrfSettings()


settings = Settings()

@CsrfProtect.load_config
def get_csrf_config():
    return settings.csrf_settings
