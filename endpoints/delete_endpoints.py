from fastapi import APIRouter
from sqlalchemy import select

from db.models import Recipe
from db.sessions import SessionDep


router_delete = APIRouter(prefix="/api", tags=["Recipes"])


@router_delete.delete("/delete_recipe/{recipe_title}")
async def delete_recipe(recipe_title: str, session: SessionDep):
    query = select(Recipe).where(Recipe.title == recipe_title)
    recipe = (await session.execute(query)).scalar()
    if recipe:
        await session.delete(recipe)
        await session.commit()
        return {"status": True}
    return {"error": "Recipe not found"}
