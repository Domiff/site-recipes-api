import pytest

from src.auth.models import Session, User
from tests.factory import make_credentials, make_session_key


@pytest.mark.parametrize(
    "credentials",
    [
        (make_credentials()),
        (make_credentials()),
        (make_credentials()),
    ],
)
async def test_create_user(user_repo, credentials):
    user = await user_repo.create(credentials)

    assert user is not None
    assert isinstance(user, User)
    assert isinstance(user.username, str)


@pytest.mark.parametrize(
    ["credentials", "session_key"],
    [
        (make_credentials(), make_session_key()),
        (make_credentials(), make_session_key()),
        (make_credentials(), make_session_key()),
    ],
)
async def test_create_session(user_repo, session_repo, credentials, session_key):
    user = await user_repo.create(credentials)
    session = await session_repo.create(session_key, user.username, user)

    assert user is not None
    assert isinstance(user, User)

    assert session is not None
    assert isinstance(session, Session)


@pytest.mark.parametrize(
    "credentials",
    [
        make_credentials(),
        make_credentials(),
        make_credentials(),
    ],
)
async def test_get_user_by_email(user_repo, credentials):
    await user_repo.create(credentials)
    user = await user_repo.get_user_by_email(credentials.email)

    assert user is not None
    assert isinstance(user, User)


@pytest.mark.parametrize(
    ["credentials", "session_key"],
    [
        (make_credentials(), make_session_key()),
        (make_credentials(), make_session_key()),
        (make_credentials(), make_session_key()),
    ],
)
async def test_delete_session(user_repo, session_repo, credentials, session_key):
    user = await user_repo.create(credentials)
    await session_repo.create(session_key, user.username, user)

    assert await session_repo.delete(session_key)
