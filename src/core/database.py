from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.core.config import settings
from src.core.logging_app import get_logger
from src.core.utils import to_snake_plural

logger = get_logger(__name__)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return to_snake_plural(cls.__name__)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


url = settings.db.DB_URL
engine = create_async_engine(url)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def ping_database() -> bool:
    try:
        async with new_session() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("Database ping failed", error=str(e))
        return False


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
