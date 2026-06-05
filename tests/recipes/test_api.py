import pytest

from tests.factory import make_credentials, make_recipe
from tests.utils import authenticate


@pytest.mark.parametrize(
    ["credentials", "recipe_schema"],
    [
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
    ],
)
async def test_add_recipe(client, credentials, recipe_schema):
    await authenticate(client, credentials)

    response = await client.post(
        "/recipes/",
        json=recipe_schema.model_dump(),
    )

    assert response.status_code == 201
    assert response.content
    assert isinstance(response.content, bytes)


@pytest.mark.parametrize(
    ["credentials", "recipe_schema"],
    [
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
    ],
)
async def test_get_all_recipes(client, credentials, recipe_schema):
    await authenticate(client, credentials)
    await client.post(
        "/recipes/",
        json=recipe_schema.model_dump(),
    )

    response = await client.get("/recipes/")

    assert response.status_code == 200
    assert response.content
    assert isinstance(response.content, bytes)


@pytest.mark.parametrize(
    ["credentials", "recipe_schema"],
    [
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
    ],
)
async def test_get_recipe(client, credentials, recipe_schema):
    await authenticate(client, credentials)
    await client.post(
        "/recipes/",
        json=recipe_schema.model_dump(),
    )

    response = await client.get(f"/recipes/title/{recipe_schema.title}")

    assert response.status_code == 200
    assert response.content
    assert isinstance(response.content, bytes)


@pytest.mark.parametrize(
    ["credentials", "recipe_schema"],
    [
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
    ],
)
async def test_get_recipe_with_ingredient(client, credentials, recipe_schema):
    await authenticate(client, credentials)
    await client.post(
        "/recipes/",
        json=recipe_schema.model_dump(),
    )

    response = await client.get(
        f"/recipes/ingredient/{recipe_schema.ingredients}?size=50"
    )

    assert response.status_code == 200
    assert response.content
    assert isinstance(response.content, bytes)


@pytest.mark.parametrize(
    ["credentials", "recipe_schema", "updating_recipe_schema"],
    [
        (make_credentials(), make_recipe(), make_recipe()),
        (make_credentials(), make_recipe(), make_recipe()),
        (make_credentials(), make_recipe(), make_recipe()),
    ],
)
async def test_update_recipe(
    client, credentials, recipe_schema, updating_recipe_schema
):
    await authenticate(client, credentials)
    recipe = await client.post(
        "/recipes/",
        json=recipe_schema.model_dump(),
    )

    response = await client.patch(
        f"/recipes/update/{recipe.json().get('id')}",
        json=updating_recipe_schema.model_dump(),
    )

    assert response.status_code == 200
    assert response.json()
    assert response.json().get("title") != recipe_schema.title
    assert response.json().get("description") != recipe_schema.description
    assert response.json().get("ingredients") != recipe_schema.ingredients
    assert response.json().get("title") == updating_recipe_schema.title
    assert response.json().get("description") == updating_recipe_schema.description
    assert response.json().get("ingredients") == updating_recipe_schema.ingredients


@pytest.mark.parametrize(
    ["credentials", "recipe_schema"],
    [
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
        (make_credentials(), make_recipe()),
    ],
)
async def test_delete_recipe(client, credentials, recipe_schema):
    await authenticate(client, credentials)
    recipe = await client.post(
        "/recipes/",
        json=recipe_schema.model_dump(),
    )

    response = await client.delete(f"/recipes/delete/{recipe.json().get('id')}")

    assert response.status_code == 204
    assert not response.content
