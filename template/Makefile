# Every day commands. Run `make` (or `make help`) to list them.
.DEFAULT_GOAL := help
.PHONY: help setup hooks dev up down logs ps prod db db-shell \
        check check-api check-web fix test migration migrate rollback db-status \
        api-types create-user reset

API := apps/api
WEB := apps/web
COMPOSE := docker compose

help: ## Show this help
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2} /^# --- / {title = $$0; gsub(/^# --- | ---$$/, "", title); printf "\n\033[1m%s\033[0m\n", title}' $(MAKEFILE_LIST)

# --- Setup ---
setup: ## First-time setup: check tools, create .env, install everything, start the stack
	@scripts/setup.sh

hooks: ## Install the git hooks (pre-commit)
	uvx pre-commit install --install-hooks

# --- Run ---
dev: ## Start the stack with hot reload, logs in the foreground (Ctrl+C to stop)
	$(COMPOSE) up --build --watch

up: ## Start the stack in the background
	$(COMPOSE) up --detach --build --wait

down: ## Stop the stack (data is kept)
	$(COMPOSE) down

logs: ## Follow the logs of every service
	$(COMPOSE) logs --follow

ps: ## Show the services and their health
	$(COMPOSE) ps --all

prod: ## Start a production-like stack (no hot reload, optimized builds)
	$(COMPOSE) -f compose.yaml up --detach --build --wait

# --- Quality ---
check: check-api check-web ## Run every check (lint, format, types, tests): do it before each commit

check-api: db ## Check the API only
	cd $(API) && uv run ruff check . && uv run ruff format --check . && uv run mypy . && uv run pytest

check-web: ## Check the web app only
	cd $(WEB) && npm run lint && npm run typecheck && npm run format:check

fix: ## Auto-fix lint and formatting issues
	cd $(API) && uv run ruff check --fix . && uv run ruff format .
	cd $(WEB) && npm run lint -- --fix && npm run format

test: db ## Run the API tests (starts the database if needed)
	cd $(API) && uv run pytest

# --- Database ---
db: ## Start only the database
	@$(COMPOSE) up --detach --wait db

migration: db ## Create a migration from your model changes: make migration m="add avatar to users"
	@test -n "$(m)" || (echo 'Missing message: make migration m="describe the change"' && exit 1)
	cd $(API) && uv run alembic revision --autogenerate -m "$(m)"

migrate: db ## Apply the pending migrations
	cd $(API) && uv run alembic upgrade head

rollback: db ## Undo the last migration
	cd $(API) && uv run alembic downgrade -1

db-status: db ## Show the current migration and the history
	cd $(API) && uv run alembic current && uv run alembic history

db-shell: db ## Open a psql console on the database
	$(COMPOSE) exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

reset: ## Delete the database and start from scratch (asks for confirmation)
	@read -p "This deletes all local data. Continue? [y/N] " answer && [ "$$answer" = y ]
	$(COMPOSE) down --volumes
	$(MAKE) up

# --- API ---
api-types: ## Regenerate the frontend's typed API client after changing a route or schema
	cd $(API) && uv run python -m scripts.export_openapi ../web/openapi.json
	cd $(WEB) && npm run api:types

create-user: ## Create a user in the running stack: make create-user email=alice@example.com
	@test -n "$(email)" || (echo 'Missing email: make create-user email=alice@example.com' && exit 1)
	$(COMPOSE) exec api python -m scripts.create_user "$(email)"
