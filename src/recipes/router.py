from fastapi import APIRouter, Depends, status
from fastapi_pagination import set_page
from fastapi_pagination.ext.sqlalchemy import apaginate

from src.auth.depends import get_current_user
from src.recipes.repository import RecipeRepoDep
from src.recipes.schemas import (
    RecipeData,
    RecipeOut,
    WithoutTotalCursorPage,
    WithoutTotalCursorParamsDep,
)

router = APIRouter(prefix="/recipes", dependencies=[Depends(get_current_user)])


@router.get("/", response_model_exclude_none=True)
async def get_all_recipes(
    repo: RecipeRepoDep, params: WithoutTotalCursorParamsDep
) -> WithoutTotalCursorPage[RecipeOut]:
    set_page(WithoutTotalCursorPage)
    query = await repo.get_all()
    return await apaginate(query=query, conn=repo.session, params=params)


@router.get("/title/{recipe_title}", response_model_exclude_none=True)
async def get_recipe(
    recipe_title: str, repo: RecipeRepoDep, params: WithoutTotalCursorParamsDep
) -> WithoutTotalCursorPage[RecipeOut]:
    set_page(WithoutTotalCursorPage)
    query = await repo.get_by_title(recipe_title)
    return await apaginate(query=query, conn=repo.session, params=params)


@router.get("/ingredient/{recipe_ingredient}", response_model_exclude_none=True)
async def get_recipe_with_ingredient(
    recipe_ingredient: str, repo: RecipeRepoDep, params: WithoutTotalCursorParamsDep
) -> WithoutTotalCursorPage[RecipeOut]:
    set_page(WithoutTotalCursorPage)
    query = await repo.get_by_ingredient(recipe_ingredient)
    return await apaginate(query=query, conn=repo.session, params=params)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_recipe(data: RecipeData, repo: RecipeRepoDep) -> RecipeOut | None:
    """
    Id category for recipes:
    1 - Закуска
    2 - Основное
    3 - Завтрак
    4 - Напиток
    5 - Суп
    """
    recipe = await repo.create(data)
    return RecipeOut.model_validate(recipe)


@router.patch("/update/{id_}")
async def update_recipe(
    id_: int, data: RecipeData, repo: RecipeRepoDep
) -> RecipeOut | str:
    recipe = await repo.update(id_, data)
    if not recipe:
        return "Recipe not found"
    return RecipeOut.model_validate(recipe)


@router.delete("/delete/{id_}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(id_: int, repo: RecipeRepoDep) -> None:
    await repo.delete(id_)
