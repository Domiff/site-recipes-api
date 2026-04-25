import logging
import os
import sys
from typing import Any

import structlog
from pythonjsonlogger.json import JsonFormatter

from src.core.config import BASE_DIR, settings

LOG_LEVEL = "INFO"


def sanitize_for_logging(data: Any) -> Any:
    if not isinstance(data, dict):
        return data
    sensitive_names = {
        "password",
        "token",
        "authorization",
        "cookie",
        "secret",
        "key",
    }
    redacted: dict[str, Any] = {}
    for k, v in data.items():
        if any(sensitive_name in k.lower() for sensitive_name in sensitive_names):
            redacted[k] = "***SENSITIVE***"
        elif isinstance(v, dict):
            redacted[k] = sanitize_for_logging(v)
        else:
            redacted[k] = v
    return redacted


def configure_logging() -> None:
    processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
    ]

    if settings.app_settings.IS_DEBUG:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
        formatter = None
    else:
        processors.append(structlog.processors.JSONRenderer())
        formatter = JsonFormatter()

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    handler = logging.StreamHandler(sys.stdout)
    if formatter:
        handler.setFormatter(formatter)

    handlers: list[logging.Handler] = [handler]

    try:
        if settings.app_settings.IS_DOCKERIZED:
            log_dir = f"{BASE_DIR}/logs"
            os.makedirs(log_dir, exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, "app.log"), maxBytes=5_000_000, backupCount=3
            )
            if formatter:
                file_handler.setFormatter(formatter)
            handlers.append(file_handler)
    except Exception:
        pass

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        handlers=handlers,
        format="%(message)s" if settings.app_settings.IS_DEBUG else None,
    )

    for logger_name in ["uvicorn.access"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def get_logger(name: str):
    return structlog.get_logger(name)
