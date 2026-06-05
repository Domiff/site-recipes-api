import pytest

from tests.factory import make_credentials, make_session_key, make_user


@pytest.mark.parametrize(
    "credentials",
    [
        make_credentials(),
        make_credentials(),
        make_credentials(),
    ],
)
async def test_authenticate_by_credentials(user_repo, auth_service, credentials):
    await user_repo.create(credentials)

    result = await auth_service.authenticate(credentials)

    assert result is not None
    assert isinstance(result, str)


@pytest.mark.parametrize(
    "user",
    [
        make_user(),
        make_user(),
        make_user(),
    ],
)
async def test_authenticate_by_user(user_repo, auth_service, user):
    await user_repo.create(user)

    result = await auth_service.authenticate(user)

    assert result is not None
    assert isinstance(result, str)


@pytest.mark.parametrize(
    "credentials",
    [
        make_credentials(),
        make_credentials(),
        make_credentials(),
    ],
)
async def test_register(auth_service, credentials):
    result = await auth_service.register(credentials)

    assert result is not None
    assert isinstance(result, str)


@pytest.mark.parametrize(
    "credentials",
    [
        make_credentials(),
        make_credentials(),
        make_credentials(),
    ],
)
async def test_login(user_repo, auth_service, credentials):
    await user_repo.create(credentials)

    result = await auth_service.login(credentials)

    assert result is not None
    assert isinstance(result, str)


@pytest.mark.parametrize(
    ["credentials", "session_key"],
    [
        (make_credentials(), make_session_key()),
        (make_credentials(), make_session_key()),
        (make_credentials(), make_session_key()),
    ],
)
async def test_logout(user_repo, session_repo, auth_service, credentials, session_key):
    user = await user_repo.create(credentials)
    await session_repo.create(session_key, user.username, user)
    session_id = await auth_service.login(credentials)

    result = await auth_service.logout(session_id)

    assert result is not None
    assert result
