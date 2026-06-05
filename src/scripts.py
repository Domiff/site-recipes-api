from sqlalchemy import insert

from src.core.database import engine
from src.recipes.models import Category


async def prepare_categories():
    async with engine.begin() as conn:
        stmt = insert(Category).values(
            [
                {"name": "Закуска"},
                {"name": "Основное"},
                {"name": "Завтрак"},
                {"name": "Напиток"},
                {"name": "Суп"},
            ]
        )
        await conn.execute(stmt)
        await conn.commit()
