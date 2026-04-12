from collections.abc import AsyncGenerator  # noqa
from typing import Annotated

import structlog
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings


logger = structlog.get_logger(__name__)


class Base(DeclarativeBase):
    pass


url = settings.DB_URL
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
