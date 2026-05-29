# Site Recipes API

REST API for a recipe website. FastAPI backend with cookie-based sessions, recipe CRUD with categories, and CORS for a Vite frontend.

## Stack

- **FastAPI** — HTTP API
- **SQLAlchemy 2** (async) — SQLite locally, **PostgreSQL** in Docker
- **Redis** — active session storage
- **Alembic** — database migrations
- **Gunicorn + Uvicorn** — application server
- **structlog** — structured logging
- **bcrypt**, **fastapi-csrf-protect** — passwords and CSRF

## Features

- Registration, login, and logout (`/auth`)
- CSRF token in a cookie (`GET /auth/csrf-token`)
- Session in an HttpOnly `session_id` cookie (Redis + DB record on registration)
- Recipe CRUD (`/recipes`), authenticated users only
- Categories: appetizer, main course, breakfast, drink, soup (ids 1–5)
- Liveness check: `GET /health` (database availability)

## Requirements

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/) (dependency manager)
- Docker Compose (optional, for containerized setup)

## Quick start (local)

```bash
git clone <repository-url>
cd site-recipes-api
cp .env.template .env
uv sync
alembic upgrade head
python -m src.main
```

API: `http://localhost:8080`  
OpenAPI (when `IS_DEBUG=true`): `http://localhost:8080/docs`

By default locally: **SQLite** (`db.sqlite3`) and **Redis** at `localhost:6379`.

## Docker

```bash
cp .env.template .env
# set POSTGRES_* and other variables as needed
docker compose up --build
```

Services: `backend` (port 8080), PostgreSQL 16, Redis 8. With `IS_DOCKERIZED=true`, the app connects to Postgres and Redis by service name.

Run migrations before the first use (e.g. `docker compose exec backend alembic upgrade head`).

## Environment variables

| Variable | Description |
|----------|-------------|
| `IS_DEBUG` | Debug mode, log level, `/docs` availability |
| `IS_DOCKERIZED` | `true` — use Postgres and Redis from compose |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Postgres credentials (Docker) |
| `POSTGRES_HOST`, `POSTGRES_PORT` | Postgres host and port (default `localhost:5432`) |
| `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` | Redis connection |
| `SECRET_KEY` | CSRF secret (generated at startup if unset) |

Template: `.env.template`.

## API overview

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Database healthcheck |
| `GET` | `/auth/csrf-token` | Issue CSRF cookie |
| `POST` | `/auth/registration` | Register + session cookie |
| `POST` | `/auth/login` | Login + session cookie |
| `POST` | `/auth/logout` | Logout (requires `session_id` cookie) |
| `GET` | `/recipes/` | List recipes |
| `GET` | `/recipes/{recipe_title}` | Recipe by title |
| `POST` | `/recipes/` | Create recipe |
| `PATCH` | `/recipes/update/{id}` | Update recipe |
| `DELETE` | `/recipes/delete/{id}` | Delete recipe |

Protected routes require a `session_id` cookie after login.

## Project structure

```
src/
  main.py           # entry point (Gunicorn)
  core/             # config, database, logging, middleware
  auth/             # users, sessions, router
  recipes/          # models, repository, router
alembic/            # migrations
docker-compose.yml
Dockerfile
```

## Development

```bash
uv sync
ruff check .
ruff format .
```

## Author

Dmitriy Levykin — dmlegasy@gmail.com
