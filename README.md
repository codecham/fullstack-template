# Fullstack Template

A production-minded starter for fullstack web apps: **FastAPI + PostgreSQL + Next.js**, with authentication, Docker, tests, CI and a Claude Code setup, generated in one command.

```bash
uvx copier copy --trust gh:codecham/fullstack-template my-app
```

Answer a few questions, and the project is created, installed and running at http://localhost:3000.

## Why this template

- **Works on the first run.** `make setup` checks your tools, generates `.env` with random secrets, installs the dependencies and git hooks, and starts the stack. No secret placeholder that "works" by accident.
- **Real authentication, done safely.** Sign-up, login, logout and a protected page. Argon2 password hashing, signed JWTs, and the token kept in an httpOnly cookie by the Next.js server, so browser JavaScript never sees it.
- **Type-safe from the database to the page.** SQLAlchemy 2 typed models, Pydantic schemas, strict mypy, and a TypeScript client generated from the API's OpenAPI schema: change an endpoint and the compiler shows every page to update.
- **Tests that test something.** pytest against a real PostgreSQL database, migrated with Alembic and rolled back after each test. A test fails if a model changes without a migration.
- **Docker without the pain.** One Compose file for a production-like stack (non-root images, migrations as a one-off job, health checks) and a dev override with hot reload through Compose Watch, which avoids the bind-mount freezes of Docker Desktop on macOS.
- **Ready for Claude Code.** A `CLAUDE.md` describing the architecture and conventions, pre-approved safe commands, `.env` protected from reads, and an `add-feature` skill that walks through model, migration, endpoint, tests, typed client and page. Ask *"add a notes feature"* and it follows the project's patterns.
- **CI included.** GitHub Actions for lint, types, tests, frontend build, API type drift and a Docker smoke test, plus Dependabot.
- **Updatable.** Built with [Copier](https://copier.readthedocs.io): pull later template improvements into your project with `copier update`.

## What you get

| Part | Technology |
| --- | --- |
| API | FastAPI, Python 3.15, uv, SQLAlchemy 2, Alembic, Pydantic Settings, PyJWT, pwdlib (Argon2) |
| Web | Next.js 16 (App Router, Cache Components), React 19, TypeScript, Tailwind CSS 4, openapi-fetch |
| Database | PostgreSQL 18, optionally with pgvector |
| Quality | Ruff, mypy (strict), pytest, ESLint, Prettier, pre-commit |
| Ops | Docker Compose, Makefile, GitHub Actions, Dependabot |
| Docs | README, CONTRIBUTING, SECURITY, LICENSE, CLAUDE.md |

The generated project's README explains how everything fits together.

## Requirements

- [Docker](https://docs.docker.com/get-started/get-docker/), running
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (also provides `uvx`)
- [Node.js](https://nodejs.org) 26 or newer
- `make`, `git` and `openssl` (preinstalled on macOS and most Linux distributions)

## Usage

### Create a project

```bash
uvx copier copy --trust gh:codecham/fullstack-template my-app
```

You are asked for:

| Question | Default |
| --- | --- |
| Project name | (required) |
| Project slug, used for folders, containers and the database | derived from the name |
| Description | A fullstack web application |
| Author name and email | used in LICENSE and SECURITY.md |
| License | MIT (or Apache-2.0, or none) |
| Use pgvector | no |

`--trust` lets the template run its post-generation tasks: `git init` and `make setup`. To only generate the files, add `--skip-tasks` and run `make setup` yourself later.

### Update a project

When the template improves, pull the changes into your project (commit your work first):

```bash
uvx copier update --trust --skip-tasks
```

Copier applies the template's changes and shows conflicts like a git merge.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
