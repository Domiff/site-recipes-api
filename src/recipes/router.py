from fastapi import APIRouter

from src.core.database import SessionDep  # noqa
from src.recipes.repository import Repository
from src.recipes.schemas import RecipeData, RecipeResponse  # noqa

router = APIRouter()


@router.get("/recipe")
async def get_all_recipes(session: SessionDep) -> list[RecipeResponse] | str:
    return await Repository.get_all_recipes(session)


@router.get("/recipe/{recipe_title}")
async def get_recipe(recipe_title: str, session: SessionDep) -> RecipeResponse | str:
    return await Repository.get_recipe(recipe_title, session)


@router.get("/recipe/{recipe_ingredient}")
async def get_recipe_with_ingredient(
    ingredient: str, session: SessionDep
) -> RecipeResponse | str:
    return await Repository.get_recipe_with_ingredient(ingredient, session)


@router.post("/add_recipe")
async def add_recipe(data: RecipeData, session: SessionDep) -> RecipeResponse | None:
    """
    Id category for recipes:
    1 - Закуска
    2 - Основное
    3 - Завтрак
    4 - Напиток
    5 - Суп
    """
    return await Repository.add_recipe(data, session)


@router.patch("/update_recipe/{id_}")
async def update_recipe(
    id_: int, data: RecipeData, session: SessionDep
) -> RecipeResponse | str:
    return await Repository.update_recipe(id_, data, session)


@router.delete("/delete_recipe/{id}")
async def delete_recipe(id_: int, session: SessionDep) -> dict[str, bool | str]:
    return await Repository.delete_recipe(id_, session)
