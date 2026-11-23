# CLAUDE.md

Guidance for Claude Code (and humans) working in this repository.

## Overview

Fullstack monorepo: a FastAPI API (`apps/api`), a Next.js web app (`apps/web`) and PostgreSQL, run together with Docker Compose. See README.md for the full picture.

## Commands

Run from the repository root:

- `make check`: lint, format check, type check and tests for both apps. **Run it before saying a task is done.**
- `make fix`: auto-fix lint and formatting.
- `make test`: API tests only (starts the database container if needed).
- `make migration m="..."` then `make migrate`: create and apply a migration after changing a model.
- `make api-types`: regenerate `apps/web/src/lib/api/schema.d.ts` after changing any API route or schema.
- `make dev` / `make up` / `make down`: run the stack (hot reload / background / stop).

Inside an app: `cd apps/api && uv run <tool>` (never `pip`; add dependencies with `uv add`), `cd apps/web && npm run <script>`.

## API (`apps/api`)

Layers, each in its own package. Keep them separate:

- `app/models/`: SQLAlchemy 2 models (`Mapped[...]`, `mapped_column`). Import every new model in `app/models/__init__.py`, otherwise Alembic does not see it.
- `app/schemas/`: Pydantic request/response models. Never return a model with secrets (e.g. `hashed_password`): use a `...Read` schema.
- `app/services/`: business logic and queries. Functions take the `Session` as first argument. Raise domain exceptions, not `HTTPException`.
- `app/routes/`: thin HTTP layer: parse input, call a service, map exceptions to HTTP errors. Register new routers in `app/main.py`.
- `app/core/`: settings (`get_settings()`), database session (`get_db`), security helpers, dependencies (`CurrentUser` for authenticated routes).

Conventions:

- Type everything; mypy runs in strict mode.
- Settings come from environment variables via `app/core/config.py`. Add new ones there and in `.env.example` (and in `compose.yaml` if the containers need them). Secrets use `SecretStr`.
- Migrations: always generate with `make migration`, then read the generated file before applying it. Never edit a migration that is already on `main`.
- Tests mirror `app/` under `tests/`. They hit a real PostgreSQL test database; use the fixtures in `tests/conftest.py` (`client`, `db`, `fake_db`). Structure each test as Arrange / Act / Assert.

## Web (`apps/web`)

- **Next.js 16 differs from older versions** (e.g. `proxy.ts` instead of middleware, Cache Components). Before writing Next.js code, read the relevant guide in `apps/web/node_modules/next/dist/docs/` (see `apps/web/AGENTS.md`).
- App Router with Cache Components: anything that reads cookies or calls the API per request must render inside a `<Suspense>` boundary.
- All API calls happen on the server, through the typed client in `src/lib/api/client.ts` (`import "server-only"`). The access token lives in an httpOnly cookie handled by `src/lib/auth/session.ts`; never expose it to client components.
- Mutations use server actions (`"use server"`), forms use `useActionState`.
- `src/lib/api/schema.d.ts` is generated: never edit it by hand, run `make api-types`.
- Styling: Tailwind CSS utility classes.

## Rules

- Never read, print or commit `.env`. Document new variables in `.env.example` with an empty value for secrets.
- Code, comments, docs and commit messages in English. Commits follow Conventional Commits (`feat:`, `fix:`, `docs:`...).
- Prefer small, focused changes that follow the existing patterns; do not add dependencies without a reason.
