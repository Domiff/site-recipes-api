from fastapi import FastAPI
from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from uvicorn_worker import UvicornWorker


class UvloopWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "httptools"}


def get_app_options(
    host: str,
    port: int,
    timeout: int,
    workers: int,
    log_level: str,
) -> dict:
    return {
        "accesslog": "-",
        "errorlog": "-",
        "bind": f"{host}:{port}",
        "loglevel": log_level,
        "logger_class": Logger,
        "timeout": timeout,
        "workers": workers,
        "worker_class": UvloopWorker,
    }


class Gunicorn(BaseApplication):
    def __init__(
        self,
        application: FastAPI,
        options: dict | None = None,

    ):
        self.application = application
        self.options = options or {}
        super().__init__()

    def load(self):
        return self.application

    @property
    def config_options(self) -> dict:
        return {
            k: v
            for k, v in self.options.items()
            if k in self.cfg.settings and v is not None
        }

    def load_config(self):
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)
