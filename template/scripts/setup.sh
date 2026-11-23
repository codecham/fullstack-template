#!/usr/bin/env bash
# One-time setup: check the prerequisites, create .env, install dependencies,
# install the git hooks and start the stack. Safe to run again.
set -euo pipefail
cd "$(dirname "$0")/.."

bold() { printf '\n\033[1m%s\033[0m\n' "$1"; }
fail() { printf '\033[31m✗ %s\033[0m\n' "$1" >&2; exit 1; }

bold "1/5 Checking prerequisites"
missing=0
require() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "✓ $1"
  else
    printf '\033[31m✗ %s is missing: %s\033[0m\n' "$1" "$2" >&2
    missing=1
  fi
}
require docker "https://docs.docker.com/get-started/get-docker/"
require uv "https://docs.astral.sh/uv/getting-started/installation/"
require node "https://nodejs.org (version: see apps/web/.nvmrc)"
require npm "comes with Node.js"
require openssl "install it with your package manager"
[[ $missing -eq 0 ]] || fail "Install the missing tools, then run make setup again"

docker info >/dev/null 2>&1 || fail "Docker is installed but not running: start Docker Desktop (or the daemon)"
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required (docker compose ...)"

required_node=$(cat apps/web/.nvmrc)
current_node=$(node -p 'process.versions.node.split(".")[0]')
if [[ "$current_node" -lt "$required_node" ]]; then
  fail "Node.js $required_node or newer is required (found $(node -v))"
fi

bold "2/5 Creating .env"
scripts/generate-env.sh

bold "3/5 Installing dependencies"
(cd apps/api && uv sync --locked)
(cd apps/web && npm ci --no-audit --no-fund)

bold "4/5 Installing git hooks"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  uvx pre-commit install --install-hooks
else
  echo "Not a git repository yet: run 'git init && make hooks' later"
fi

bold "5/5 Starting the stack (first build takes a few minutes)"
docker compose up --detach --build --wait

set -a; source .env; set +a
bold "Ready!"
echo "  Frontend  http://localhost:${WEB_PORT}"
echo "  API docs  http://localhost:${API_PORT}/docs"
echo "  Next      make help"
