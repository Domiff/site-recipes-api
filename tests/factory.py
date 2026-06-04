import uuid

from faker import Faker

from src.auth.schemas import CredentialsSchema

_faker = Faker()


def make_credentials():
    return CredentialsSchema(
        username=_faker.user_name(),
        password=_faker.password(),
        email=_faker.email(),
    )


def make_session_key():
    return uuid.uuid4().hex
