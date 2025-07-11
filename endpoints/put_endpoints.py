from fastapi import APIRouter
from sqlalchemy import select

from db.models import Recipe
from db.sessions import SessionDep


router_put = APIRouter(prefix="/api", tags=["Recipes"])


@router_put.put("/update_recipe/{recipe_title}/ingredient{recipe_ingredient}")
async def update_recipe_ingredient(title: str, ingredient: str, session: SessionDep):
    query = select(Recipe).where(Recipe.title == title)
    recipe = (await session.execute(query)).scalar()
    if recipe:
        recipe.ingredients = ingredient
        await session.commit()
        await session.refresh(recipe)
        return {"status": True, "recipe": recipe}
    return {"error": "Recipe not found"}
