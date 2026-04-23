from collections.abc import AsyncGenerator  # noqa
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.database import ping_database
from src.core.logging_app import configure_logging, get_logger
from src.recipes.router import router


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    params = {
        "is_debug": settings.IS_DEBUG,
        "is_dockerized": settings.IS_DOCKERIZED,
    }
    logger.info("Starting application", **params)
    logger.info("Application started")

    yield

    logger.info("Starting graceful shutdown")
    logger.info("Graceful shutdown completed")


def create_app() -> FastAPI:
    configure_logging()
    logger.info("Creating FastAPI application")

    app = FastAPI(
        title="Site Recipes",
        version="1",
        lifespan=lifespan,
        openapi_url="/openapi.json" if settings.IS_DEBUG else None,
    )

    setup_middlewares(app)
    setup_healthcheck(app)

    app.include_router(router, tags=["recipes"])
    logger.info("Application routes configured")

    return app


def setup_middlewares(app: FastAPI) -> None:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=origins,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    )
    logger.info("CORS middleware configured", allowed_origins=origins)


def setup_healthcheck(app: FastAPI) -> None:
    @app.get("/health", tags=["health"])
    async def health() -> bool:
        is_database_available = await ping_database()
        if not is_database_available:
            logger.warning("Healthcheck failed: database is unavailable")
        return is_database_available
