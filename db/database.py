import os

from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv


load_dotenv()

config = {
    "NAME": os.getenv("POSTGRES_DB"),
    "USER": os.getenv("POSTGRES_USER"),
    "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "HOST": os.getenv("POSTGRES_HOST"),
    "PORT": os.getenv("POSTGRES_PORT"),
}


DATABASE_URL = (
    f"postgresql+asyncpg://{config['USER']}:"
    f"{config['PASSWORD']}@"
    # f"{config['HOST']}:"
    f"localhost:"
    f"{config['PORT']}/"
    f"{config['NAME']}"
)

engine = create_async_engine(DATABASE_URL)
