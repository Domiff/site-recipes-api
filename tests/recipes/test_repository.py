import pytest
from sqlalchemy import Select

from src.recipes.models import Recipe
from src.scripts import prepare_categories
from tests.factory import make_recipe


@pytest.mark.parametrize(
    "recipe_schema",
    [
        make_recipe(),
        make_recipe(),
        make_recipe(),
    ],
)
async def test_create(recipe_repo, recipe_schema):
    recipe = await recipe_repo.create(recipe_schema)

    assert recipe
    assert isinstance(recipe, Recipe)


@pytest.mark.parametrize(
    "recipe_schema",
    [
        make_recipe(),
        make_recipe(),
        make_recipe(),
    ],
)
async def test_get_all(recipe_repo, recipe_schema):
    await prepare_categories()
    await recipe_repo.create(recipe_schema)

    query = await recipe_repo.get_all()

    assert query is not None
    assert isinstance(query, Select)


@pytest.mark.parametrize(
    "recipe_schema",
    [
        make_recipe(),
        make_recipe(),
        make_recipe(),
    ],
)
async def test_get_by_title(recipe_repo, recipe_schema):
    await prepare_categories()
    await recipe_repo.create(recipe_schema)

    query = await recipe_repo.get_by_title(recipe_schema.title)

    assert query is not None
    assert isinstance(query, Select)


@pytest.mark.parametrize(
    "recipe_schema",
    [
        make_recipe(),
        make_recipe(),
        make_recipe(),
    ],
)
async def test_get_by_ingredient(recipe_repo, recipe_schema):
    await prepare_categories()
    await recipe_repo.create(recipe_schema)

    query = await recipe_repo.get_by_ingredient(recipe_schema.ingredients)

    assert query is not None
    assert isinstance(query, Select)


@pytest.mark.parametrize(
    ["recipe_schema", "updating_recipe_schema"],
    [
        (make_recipe(), make_recipe()),
        (make_recipe(), make_recipe()),
        (make_recipe(), make_recipe()),
    ],
)
async def test_update(recipe_repo, recipe_schema, updating_recipe_schema):
    await prepare_categories()
    recipe = await recipe_repo.create(recipe_schema)

    recipe = await recipe_repo.update(recipe.id, updating_recipe_schema)

    assert recipe
    assert isinstance(recipe, Recipe)


@pytest.mark.parametrize(
    "recipe_schema",
    [
        make_recipe(),
        make_recipe(),
        make_recipe(),
    ],
)
async def test_delete(recipe_repo, recipe_schema):
    await prepare_categories()
    recipe = await recipe_repo.create(recipe_schema)

    result = await recipe_repo.delete(recipe.id)

    assert isinstance(result, bool)
    assert result
