from fastapi import APIRouter, Depends

from src.auth.depends import get_current_user
from src.recipes.repository import RecipeRepoDep
from src.recipes.schemas import RecipeData, RecipeResponse  # noqa

router = APIRouter(prefix="/recipes", dependencies=[Depends(get_current_user)])


@router.get("/")
async def get_all_recipes(repo: RecipeRepoDep) -> list[RecipeResponse] | str:
    recipes = await repo.get_all_recipes()
    if not recipes:
        return "Recipes not found"
    return [RecipeResponse.model_validate(recipe) for recipe in recipes]


@router.get("/{recipe_title}")
async def get_recipe(recipe_title: str, repo: RecipeRepoDep) -> RecipeResponse | str:
    recipe = await repo.get_recipe(recipe_title)
    if not recipe:
        return "Recipe not found"
    return RecipeResponse.model_validate(recipe)


@router.get("/{recipe_ingredient}")
async def get_recipe_with_ingredient(
    ingredient: str, repo: RecipeRepoDep
) -> RecipeResponse | str:
    recipe = await repo.get_recipe_with_ingredient(ingredient)
    if not recipe:
        return "Recipe not found"
    return RecipeResponse.model_validate(recipe)


@router.post("/")
async def add_recipe(data: RecipeData, repo: RecipeRepoDep) -> RecipeResponse | None:
    """
    Id category for recipes:
    1 - Закуска
    2 - Основное
    3 - Завтрак
    4 - Напиток
    5 - Суп
    """
    recipe = await repo.add_recipe(data)
    return RecipeResponse.model_validate(recipe)


@router.patch("/update/{id_}")
async def update_recipe(
    id_: int, data: RecipeData, repo: RecipeRepoDep
) -> RecipeResponse | str:
    recipe = await repo.update_recipe(id_, data)
    if not recipe:
        return "Recipe not found"
    return RecipeResponse.model_validate(recipe)


@router.delete("/delete/{id}")
async def delete_recipe(id_: int, repo: RecipeRepoDep) -> dict[str, bool | str]:
    deleted = await repo.delete_recipe(id_)
    if deleted:
        return {"message": True}
    return {"error": "Recipe not found"}
