from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


recipe_category = Table(
    "site_recipes_app_recipe_category",
    Base.metadata,
    Column("recipe_id", ForeignKey("site_recipes_app_recipe.id"), primary_key=True),
    Column("category_id", ForeignKey("site_recipes_app_category.id"), primary_key=True),
)


class Recipe(Base):
    __tablename__ = "site_recipes_app_recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    steps: Mapped[str] = mapped_column(String)
    ingredients: Mapped[str] = mapped_column(String)
    time_cooking: Mapped[str] = mapped_column(String)

    author_id: Mapped[int] = mapped_column(Integer)

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary=recipe_category,
        back_populates="recipes"
    )


class Category(Base):
    __tablename__ = "site_recipes_app_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe",
        secondary=recipe_category,
        back_populates="categories"
    )
