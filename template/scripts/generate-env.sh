#!/usr/bin/env bash
# Create .env from .env.example, filling every secret with a fresh random value.
# Never overwrites an existing .env.
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ -f .env ]]; then
  echo "✓ .env already exists, left unchanged"
  exit 0
fi

random_secret() { openssl rand -hex 32; }

while IFS= read -r line || [[ -n "$line" ]]; do
  case "$line" in
    POSTGRES_PASSWORD= | JWT_SECRET_KEY=) echo "${line}$(random_secret)" ;;
    *) echo "$line" ;;
  esac
done < .env.example > .env
chmod 600 .env

echo "✓ .env created with freshly generated secrets"
