from faker import Faker

from src.auth.models import User
from src.auth.schemas import CredentialsSchema
from src.recipes.schemas import RecipeIn

_faker = Faker()


def make_credentials():
    return CredentialsSchema(
        username=_faker.user_name(),
        password=_faker.password(),
        email=_faker.email(),
    )


def make_session_key():
    return _faker.uuid7()


def make_user():
    return User(
        username=_faker.user_name(),
        email=_faker.email(),
        password=_faker.password(),
    )


def make_recipe():
    return RecipeIn(
        title=_faker.sentence(),
        description=_faker.sentence(),
        ingredients=_faker.sentence(),
        steps=_faker.sentence(),
        time_cooking=_faker.sentence(),
        categories=[_faker.random_int(min=1, max=5)],
    )
