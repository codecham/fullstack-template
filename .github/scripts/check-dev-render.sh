#!/usr/bin/env bash
# Render every page with `next dev`, logged out and logged in, and fail if Next.js logs
# an error. Catches dev-only problems that `next build` misses (e.g. Cache Components
# prerender errors such as "unstable value Date.now()").
# Run from a generated project whose API is up (docker compose up --wait api).
set -euo pipefail

API=http://localhost:${API_PORT:-8000}
WEB_PORT=3100
WEB=http://localhost:$WEB_PORT
LOG=$(mktemp)

(cd apps/web && API_URL=$API npx next dev --port $WEB_PORT >"$LOG" 2>&1) &
trap 'pkill -f "next dev --port $WEB_PORT" || true' EXIT
for _ in $(seq 1 60); do curl --silent --output /dev/null "$WEB/" && break; sleep 1; done

curl --silent --fail -X POST "$API/auth/register" -H 'Content-Type: application/json' \
  -d '{"email": "render-check@example.com", "password": "render-check-password"}' >/dev/null || true
token=$(curl --silent --fail -X POST "$API/auth/login" \
  -d 'username=render-check@example.com&password=render-check-password' |
  python3 -c 'import json, sys; print(json.load(sys.stdin)["access_token"])')

for page in / /login /register /account; do
  curl --silent --output /dev/null --write-out "logged out $page %{http_code}\n" "$WEB$page"
  curl --silent --output /dev/null --write-out "logged in  $page %{http_code}\n" \
    --cookie "session=$token" "$WEB$page"
done
sleep 3 # let the dev server flush its validation errors

if grep -q "Error" "$LOG"; then
  echo "::error::next dev reported errors while rendering the pages:"
  cat "$LOG"
  exit 1
fi
echo "✓ every page renders without errors in next dev"
