from src.core.setup import create_app
from src.core.gunicorn import Gunicorn, get_app_options
from src.core.config import settings


def main():
    app = create_app()
    options = get_app_options(
        host=settings.gunicorn_settings.HOST,
        port=settings.gunicorn_settings.PORT,
        workers=settings.gunicorn_settings.WORKERS,
        timeout=settings.gunicorn_settings.TIMEOUT,
        log_level=settings.gunicorn_settings.LOG_LEVEL,
    )
    gunicorn = Gunicorn(
        application=app,
        options=options,
    )
    gunicorn.run()


if __name__ == "__main__":
    main()
