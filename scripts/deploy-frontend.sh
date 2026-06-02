#!/usr/bin/env bash
# Rebuild and deploy the frontend with the latest git commit (no stale Docker cache).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

git fetch origin main
git checkout main
git pull origin main

SHA="$(git rev-parse --short HEAD)"
echo "Deploying frontend at commit ${SHA}"

docker compose build --no-cache --build-arg GIT_SHA="${SHA}" frontend
docker compose up -d frontend

echo "Verifying social links in the built image..."
docker compose exec -T frontend sh -c \
  'grep -rl "linkedin.com/in/jotalvaro" /usr/share/nginx/html/assets/*.js | head -1' \
  || { echo "ERROR: Social URLs not found in container. Check git pull path."; exit 1; }

echo "Done. Hard-refresh the site (Ctrl+Shift+R) or try incognito."
