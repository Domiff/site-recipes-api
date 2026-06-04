dev:
    uv run python -m src.main

revision msg:
    uv run alembic revision --autogenerate -m {{msg}}

upgrade:
    uv run alembic upgrade head

test-all:
    uv run pytest

test dir:
    uv run pytest {{dir}}

format-all:
    uv run ruff format .

format dir:
    uv run ruff format {{dir}}
