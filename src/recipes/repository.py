from typing import Annotated

from fastapi import Depends
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.database import SessionDep  # noqa
from src.core.logging_app import get_logger
from src.recipes.models import Category, Recipe
from src.recipes.schemas import RecipeData, RecipeRequest

logger = get_logger(__name__)


class RecipeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_recipes(self) -> Select:
        return (
            select(Recipe).options(selectinload(Recipe.categories)).order_by(Recipe.id)
        )

    async def get_recipe(self, recipe_title: str) -> Select:
        query = (
            select(Recipe)
            .options(selectinload(Recipe.categories))
            .where(Recipe.title == recipe_title)
            .order_by(Recipe.id)
        )
        return query

    async def get_recipe_with_ingredient(self, ingredient: str) -> Select:
        query = (
            select(Recipe)
            .options(selectinload(Recipe.categories))
            .where(Recipe.ingredients.icontains(ingredient))
            .order_by(Recipe.id)
        )
        return query

    async def add_recipe(self, data: RecipeRequest) -> Recipe:
        logger.info("Creating recipe", title=data.title)
        query = select(Category).where(Category.id.in_(data.categories))
        categories = await self.session.execute(query)
        recipe = Recipe(
            title=data.title,
            ingredients=data.ingredients,
            description=data.description,
            steps=data.steps,
            time_cooking=data.time_cooking,
            categories=categories.scalars().all(),
        )

        self.session.add(recipe)
        await self.session.commit()
        await self.session.refresh(recipe)
        logger.info("Recipe created", recipe_id=recipe.id)
        return recipe

    async def update_recipe(self, id_: int, data: RecipeData) -> Recipe | None:
        logger.info("Updating recipe", recipe_id=id_)
        query = (
            select(Recipe)
            .options(selectinload(Recipe.categories))
            .where(Recipe.id == id_)
        )
        recipe = (await self.session.execute(query)).scalar()
        if not recipe:
            logger.warning("Recipe for update not found", recipe_id=id_)
            return None

        payload = data.model_dump(exclude_unset=True, exclude_none=True)
        category_ids = payload.pop("categories", None)

        for field, value in payload.items():
            setattr(recipe, field, value)

        if not category_ids:
            recipe.categories = []
        else:
            category_query = select(Category).where(Category.id.in_(category_ids))
            categories = (await self.session.execute(category_query)).scalars().all()
            recipe.categories = categories

        await self.session.commit()
        await self.session.refresh(recipe, attribute_names=["categories"])
        logger.info("Recipe updated", recipe_id=id_)
        return recipe

    async def delete_recipe(self, id_: int) -> bool:
        logger.info("Deleting recipe", recipe_id=id_)
        query = select(Recipe).where(Recipe.id == id_)
        recipe = (await self.session.execute(query)).scalar()
        if recipe:
            await self.session.delete(recipe)
            await self.session.commit()
            logger.info("Recipe deleted", recipe_id=id_)
            return True
        logger.warning("Recipe for delete not found", recipe_id=id_)
        return False


def get_recipe_repo(session: SessionDep) -> RecipeRepository:
    return RecipeRepository(session)


RecipeRepoDep = Annotated[RecipeRepository, Depends(get_recipe_repo)]
