from typing import Optional, List

from pydantic import BaseModel


class RecipeSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    ingredients: Optional[str]
    steps: str
    time_cooking: str
    author_id: int
    category_ids: List[int]

    class Config:
        orm_mode = True
