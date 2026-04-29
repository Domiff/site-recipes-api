from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(String(75), unique=True)
    first_name: Mapped[str] = mapped_column(String(50), default="")
    last_name: Mapped[str] = mapped_column(String(50), default="")
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Session(Base):
    session_key: Mapped[str] = mapped_column(String(200), unique=True)
    session_data: Mapped[str] = mapped_column(String(200))
    expire_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        return f"<Session {self.session_key}>"
