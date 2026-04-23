from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

recipe_category = Table(
    "recipe_with_category",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class Recipe(Base):
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    steps: Mapped[str] = mapped_column(String)
    ingredients: Mapped[str] = mapped_column(String)
    time_cooking: Mapped[str] = mapped_column(String)

    categories: Mapped[list["Category"]] = relationship(
        "Category", secondary=recipe_category, back_populates="recipes", lazy="selectin",
    )


class Category(Base):
    name: Mapped[str] = mapped_column(String)

    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe", secondary=recipe_category, back_populates="categories", lazy="selectin",
    )
