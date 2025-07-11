from fastapi import APIRouter
from sqlalchemy import select

from db.models import Recipe, Category
from db.sessions import SessionDep
from schemas.recipe import RecipeSchema


router_post = APIRouter(prefix="/api", tags=["Recipes"])


@router_post.post("/add_recipe/{recipe}")
async def add_recipe(data: RecipeSchema, session: SessionDep):
    """
    Id category for recipes:
    1 - Закуска,
    2 - Основное,
    3 - Завтрак,
    4 - Напиток,
    5 - Суп

    Id author: 1
    """
    if data.category_ids:
        query = select(Category).where(Category.id.in_(data.category_ids))
        category = await session.execute(query)
        recipe = Recipe(
            title=data.title,
            ingredients=data.ingredients,
            description=data.description,
            steps=data.steps,
            time_cooking=data.time_cooking,
            author_id=data.author_id,
            categories=category.scalars().all()
        )

        session.add(recipe)
        await session.commit()
        await session.refresh(recipe)
        return {"status": True, "recipe": recipe}

    await session.rollback()
    return {"status": False}
