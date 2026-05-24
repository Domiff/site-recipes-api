FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./pyproject.toml ./

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync

COPY . .

EXPOSE 8080
