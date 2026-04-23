from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.core.database import SessionDep  # noqa
from src.recipes.models import Category, Recipe
from src.recipes.schemas import RecipeData, RecipeRequest, RecipeResponse
from src.core.logging_app import get_logger


logger = get_logger(__name__)


class Repository:
    @classmethod
    async def get_all_recipes(cls, session: SessionDep) -> list[RecipeResponse] | str:
        query = select(Recipe).options(selectinload(Recipe.categories))
        recipes = (await session.execute(query)).scalars().all()
        if recipes:
            return [RecipeResponse.model_validate(recipe) for recipe in recipes]
        return "Recipes not found"

    @classmethod
    async def get_recipe(
        cls, recipe_title: str, session: SessionDep
    ) -> RecipeResponse | str:
        query = (
            select(Recipe)
            .options(joinedload(Recipe.categories.id))
            .where(Recipe.title == recipe_title)
        )
        recipe = (await session.execute(query)).scalar()
        if recipe:
            return RecipeResponse.model_validate(recipe)
        return "Recipe not found"

    @classmethod
    async def get_recipe_with_ingredient(
        cls, ingredient: str, session: SessionDep
    ) -> RecipeResponse | str:
        query = (
            select(Recipe)
            .options(joinedload(Recipe.categories))
            .where(Recipe.ingredients.contains(ingredient))
        )
        recipe = (await session.execute(query)).scalar()
        if recipe:
            return RecipeResponse.model_validate(recipe)
        return "Recipe not found"

    @classmethod
    async def add_recipe(
        cls, data: RecipeRequest, session: SessionDep
    ) -> RecipeResponse | None:
        logger.info("Creating recipe", title=data.title)
        query = select(Category).where(Category.id.in_(data.categories))
        categories = await session.execute(query)
        recipe = Recipe(
            title=data.title,
            ingredients=data.ingredients,
            description=data.description,
            steps=data.steps,
            time_cooking=data.time_cooking,
            categories=categories.scalars().all(),
        )

        session.add(recipe)
        await session.commit()
        await session.refresh(recipe)
        logger.info("Recipe created", recipe_id=recipe.id)
        return RecipeResponse.model_validate(recipe)

    @classmethod
    async def update_recipe(
        cls, id_: int, data: RecipeData, session: SessionDep
    ) -> RecipeResponse | str:
        logger.info("Updating recipe", recipe_id=id_)
        query = (
            select(Recipe)
            .options(selectinload(Recipe.categories))
            .where(Recipe.id == id_)
        )
        recipe = (await session.execute(query)).scalar()
        if not recipe:
            logger.warning("Recipe for update not found", recipe_id=id_)
            return "Recipe not found"

        payload = data.model_dump(exclude_unset=True, exclude_none=True)
        category_ids = payload.pop("categories", None)

        for field, value in payload.items():
            setattr(recipe, field, value)

        if not category_ids:
            recipe.categories = []
        else:
            category_query = select(Category).where(Category.id.in_(category_ids))
            categories = (await session.execute(category_query)).scalars().all()
            recipe.categories = categories

        await session.commit()
        await session.refresh(recipe, attribute_names=["categories"])
        logger.info("Recipe updated", recipe_id=id_)
        return RecipeResponse.model_validate(recipe)

    @classmethod
    async def delete_recipe(cls, id_: int, session: SessionDep) -> dict:
        logger.info("Deleting recipe", recipe_id=id_)
        query = select(Recipe).where(Recipe.id == id_)
        recipe = (await session.execute(query)).scalar()
        if recipe:
            await session.delete(recipe)
            await session.commit()
            logger.info("Recipe deleted", recipe_id=id_)
            return {"message": True}
        logger.warning("Recipe for delete not found", recipe_id=id_)
        return {"error": "Recipe not found"}
