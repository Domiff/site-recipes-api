from typing import Annotated, Any

from fastapi import Body
from pydantic import BaseModel, ConfigDict, field_validator


class Recipe(BaseModel):
    title: str | None = None
    description: str | None = None
    ingredients: str | None = None
    steps: str | None = None
    time_cooking: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RecipeRequest(Recipe):
    categories: list[int] | None = None


class RecipeResponse(Recipe):
    id: int
    categories: list[str] | None = None

    @field_validator("categories", mode="before")
    @classmethod
    def serialize_categories(cls, categories: Any) -> Any:
        return (
            [category.name for category in categories]
            if isinstance(categories, list)
            else categories
        )

    model_config = ConfigDict(from_attributes=True)


RecipeData = Annotated[RecipeRequest, Body()]
