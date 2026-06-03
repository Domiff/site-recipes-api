from typing import Annotated, Any

from fastapi import Body, Depends
from fastapi_pagination.bases import CursorRawParams
from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.customization import CustomizedPage, UseIncludeTotal
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


class WithoutTotalCursorParams(CursorParams):
    def to_raw_params(self) -> CursorRawParams:
        return CursorRawParams(
            cursor=self.decode_cursor(self.cursor),
            size=self.size,
            include_total=False,
        )


WithoutTotalCursorPage = CustomizedPage[
    CursorPage,
    UseIncludeTotal(False),
]

RecipeData = Annotated[RecipeRequest, Body()]
WithoutTotalCursorParamsDep = Annotated[WithoutTotalCursorParams, Depends()]
