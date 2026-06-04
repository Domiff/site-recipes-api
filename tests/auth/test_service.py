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
async def test_authenticate_by_credentials(user_repo, service, credentials):
    await user_repo.create(credentials)

    result = await service.authenticate(credentials)

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
async def test_authenticate_by_user(user_repo, service, user):
    await user_repo.create(user)

    result = await service.authenticate(user)

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
async def test_register(service, credentials):
    result = await service.register(credentials)

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
async def test_login(user_repo, service, credentials):
    await user_repo.create(credentials)

    result = await service.login(credentials)

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
async def test_logout(user_repo, session_repo, service, credentials, session_key):
    user = await user_repo.create(credentials)
    await session_repo.create(session_key, user.username, user)
    session_id = await service.login(credentials)

    result = await service.logout(session_id)

    assert result is not None
    assert result
