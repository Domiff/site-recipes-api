from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    DB_URL: str = Field(default="sqlite+aisqlite:///db.sqlite3")

    IS_DEBUG: bool = Field(default=True)
    IS_DOCKERIZED: bool = Field(default=False)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
