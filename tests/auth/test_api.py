import pytest

from tests.factory import make_credentials


async def test_get_csrf_token(client):
    response = await client.get("/auth/csrf-token")

    assert response.status_code == 200
    assert response.cookies.get("csrf_token")


@pytest.mark.parametrize(
    "credentials",
    [
        make_credentials(),
        make_credentials(),
        make_credentials(),
    ],
)
async def test_registration(client, credentials):
    response = await client.post("/auth/registration", json=credentials.model_dump())

    assert response.status_code == 201
    assert response.cookies.get("session_id")


@pytest.mark.parametrize(
    "credentials",
    [
        make_credentials(),
        make_credentials(),
        make_credentials(),
    ],
)
async def test_login(client, credentials):
    await client.post("/auth/registration", json=credentials.model_dump())

    response = await client.post("/auth/login", json=credentials.model_dump())

    assert response.status_code == 200
    assert response.cookies.get("session_id")


@pytest.mark.parametrize(
    "credentials",
    [
        make_credentials(),
        make_credentials(),
        make_credentials(),
    ],
)
async def test_logout(client, credentials):
    registration_response = await client.post(
        "/auth/registration", json=credentials.model_dump()
    )

    response = await client.post(
        f"/auth/logout?cookie_session_id={registration_response.cookies.get('session_id')}"
    )

    assert response.status_code == 204
    assert not response.cookies.get("session_id")
