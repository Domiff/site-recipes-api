from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from db.models import Recipe
from db.sessions import SessionDep


router_get = APIRouter(prefix="/api", tags=["Recipes"])


@router_get.get("/")
async def get_all_recipes(session: SessionDep):
    query = select(Recipe).options(selectinload(Recipe.categories))
    recipes = (await session.execute(query)).scalars().all()
    if recipes:
        return {"recipes": recipes}
    return {"error": "Recipes not found"}


@router_get.get("/recipe_title/{recipe_title}")
async def get_recipe(recipe_title: str, session: SessionDep):
    query = (
        select(Recipe)
        .options(joinedload(Recipe.categories))
        .where(Recipe.title == recipe_title)
    )
    recipe = (await session.execute(query)).scalar()
    if recipe:
        return {"recipe": recipe}
    return {"error": "Recipe not found"}


@router_get.get("/recipe_ingredient/{recipe_ingredient}")
async def get_recipe_with_ingredient(ingredient: str, session: SessionDep):
    query = (
        select(Recipe)
        .options(joinedload(Recipe.categories))
        .where(Recipe.ingredients.contains(ingredient))
    )
    recipe = (await session.execute(query)).scalar()
    if recipe:
        return {"recipe": recipe}
    return {"error": "Recipe not found"}
