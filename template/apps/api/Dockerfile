# syntax=docker/dockerfile:1

# --- Build stage: install the dependencies into /code/.venv with uv ---
FROM python:3.15-slim AS build

COPY --from=ghcr.io/astral-sh/uv:0.13 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /code
# Only the lock files: this layer stays cached until the dependencies change
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# --- Runtime stage: no uv, no build tools, non-root user ---
FROM python:3.15-slim AS runtime

ENV PATH="/code/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 1000 app
WORKDIR /code

COPY --from=build /code/.venv ./.venv
# Owned by "app" so `docker compose watch` can sync edited files into the container
COPY --chown=app:app alembic.ini ./
COPY --chown=app:app migrations ./migrations
COPY --chown=app:app scripts ./scripts
COPY --chown=app:app app ./app

USER app
EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
