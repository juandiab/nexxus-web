#!/usr/bin/env bash
# Interactive (or flagged) rebuild for the Nexxus Tech Docker stack.
#
# Usage:
#   ./scripts/rebuild-stack.sh              # prompt: dev or prod
#   ./scripts/rebuild-stack.sh --dev
#   ./scripts/rebuild-stack.sh --prod
#   ./scripts/rebuild-stack.sh --status
#
# Dev mode: Vite hot reload at https://nexxus-tech.com (via nginx + VITE_HMR_HOST).
# Prod mode: static frontend build behind nginx on port 80 inside the container.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

COMPOSE=(docker compose)
COMPOSE_DEV=(docker compose -f docker-compose.yml -f docker-compose.dev.yml)

SITE_HOST="${SITE_HOST:-nexxus-tech.com}"
SITE_URL="https://${SITE_HOST}"

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
info() { printf '→ %s\n' "$*"; }
ok() { printf '✓ %s\n' "$*"; }
warn() { printf '⚠ %s\n' "$*"; }
err() { printf '✗ %s\n' "$*" >&2; }

usage() {
  cat <<EOF
Usage: $(basename "$0") [--dev | --prod | --status | --help]

  --dev     Start development stack (Vite HMR via ${SITE_URL})
  --prod    Start production stack (built static frontend)
  --status  Show whether dev or prod is running
  --help    Show this help

Environment (optional):
  SITE_HOST       Public hostname (default: nexxus-tech.com)
  VITE_HMR_HOST   Vite HMR host for dev (default: SITE_HOST)
  REBUILD_SERVICES  Space-separated services to rebuild (default: all)

Without flags, the script asks which mode you want.
EOF
}

load_env() {
  if [[ -f .env ]]; then
    local hmr
    hmr="$(grep -E '^VITE_HMR_HOST=' .env 2>/dev/null | cut -d= -f2- | tr -d '\r"' | head -1 || true)"
    if [[ -n "$hmr" ]]; then
      export VITE_HMR_HOST="$hmr"
    fi
  fi
  export VITE_HMR_HOST="${VITE_HMR_HOST:-$SITE_HOST}"
}

stack_running() {
  docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^nexxustech-nginx$'
}

detect_mode() {
  if ! stack_running; then
    echo "stopped"
    return 0
  fi
  if docker exec nexxustech-nginx grep -q 'frontend:5173' /etc/nginx/nginx.conf 2>/dev/null; then
    echo "dev"
  else
    echo "prod"
  fi
}

print_status() {
  local mode
  mode="$(detect_mode)"
  bold "Stack status: ${mode}"
  if [[ "$mode" == "stopped" ]]; then
    info "No nexxustech-nginx container is running."
    return 0
  fi
  docker compose ps 2>/dev/null || "${COMPOSE_DEV[@]}" ps 2>/dev/null || true
  echo
  if [[ "$mode" == "dev" ]]; then
    info "Site URL: ${SITE_URL} (Vite dev + hot reload)"
    info "Vite direct: http://localhost:5173"
    info "VITE_HMR_HOST: ${VITE_HMR_HOST:-not set}"
  else
    info "Site URL: ${SITE_URL} (production build)"
  fi
}

stop_all() {
  info "Stopping any running stack..."
  "${COMPOSE_DEV[@]}" down --remove-orphans 2>/dev/null || true
  "${COMPOSE[@]}" down --remove-orphans 2>/dev/null || true
}

wait_for_healthy() {
  local service="$1"
  local attempts="${2:-30}"
  local i=0
  while (( i < attempts )); do
    local status
    status="$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "nexxustech-${service}" 2>/dev/null || echo missing)"
    if [[ "$status" == "healthy" || "$status" == "none" ]]; then
      if docker ps --format '{{.Names}}' | grep -q "^nexxustech-${service}$"; then
        ok "${service} is up"
        return 0
      fi
    fi
    sleep 2
    (( i += 1 )) || true
  done
  warn "${service} did not become healthy in time (may still be starting)"
  return 0
}

verify_dev_stack() {
  info "Verifying dev stack..."

  if ! docker exec nexxustech-nginx grep -q 'frontend:5173' /etc/nginx/nginx.conf; then
    err "nginx is not using dev config (expected frontend:5173)."
    err "Did you start with both compose files?"
    return 1
  fi
  ok "nginx dev config active"

  if docker exec nexxustech-frontend sh -c 'wget -qO- http://127.0.0.1:5173/ 2>/dev/null | head -c 80' | grep -q '<!DOCTYPE html>'; then
    ok "Vite dev server responding on :5173"
  else
    err "Vite is not responding inside the frontend container on port 5173."
    err "Check logs: ${COMPOSE_DEV[*]} logs -f frontend"
    return 1
  fi

  if docker exec nexxustech-nginx sh -c "wget -qO- http://frontend:5173/ 2>/dev/null | head -c 80" | grep -q 'nexxus\|Nexxus\|<!DOCTYPE html>'; then
    ok "nginx can reach Vite upstream"
  else
    warn "nginx → frontend:5173 check inconclusive (site may still work via HTTPS)"
  fi
}

verify_prod_stack() {
  info "Verifying production stack..."

  if docker exec nexxustech-nginx grep -q 'frontend:5173' /etc/nginx/nginx.conf; then
    err "nginx is still using dev config. Run this script with --prod again."
    return 1
  fi
  ok "nginx production config active"

  if docker exec nexxustech-nginx sh -c 'wget -qO- http://frontend:80/ 2>/dev/null | head -c 80' | grep -q '<!DOCTYPE html>'; then
    ok "production frontend responding on :80"
  else
    err "production frontend is not responding on port 80."
    return 1
  fi
}

ensure_hmr_env() {
  if [[ -f .env ]] && grep -q '^VITE_HMR_HOST=' .env; then
    info "Using VITE_HMR_HOST from .env"
    return 0
  fi

  info "VITE_HMR_HOST not in .env — using ${VITE_HMR_HOST} for this session."
  info "To persist, add to .env:  VITE_HMR_HOST=${SITE_HOST}"
}

start_dev() {
  load_env
  ensure_hmr_env

  local current
  current="$(detect_mode)"
  if [[ "$current" == "prod" ]]; then
    warn "Switching from production → development."
  fi

  stop_all

  bold "Building and starting DEV stack (hot reload)..."
  info "VITE_HMR_HOST=${VITE_HMR_HOST}"

  if [[ -n "${REBUILD_SERVICES:-}" ]]; then
    # shellcheck disable=SC2086
    VITE_HMR_HOST="$VITE_HMR_HOST" "${COMPOSE_DEV[@]}" up -d --build $REBUILD_SERVICES
  else
    VITE_HMR_HOST="$VITE_HMR_HOST" "${COMPOSE_DEV[@]}" up -d --build
  fi

  wait_for_healthy mongodb
  wait_for_healthy licensing
  verify_dev_stack

  echo
  bold "Dev stack is ready."
  info "Browse: ${SITE_URL}/products"
  info "Hot reload: edit files under frontend/src/ and save"
  info "Logs: ${COMPOSE_DEV[*]} logs -f frontend"
  info "When finished, run: $(basename "$0") --prod"
}

start_prod() {
  load_env

  local current
  current="$(detect_mode)"
  if [[ "$current" == "dev" ]]; then
    warn "Switching from development → production."
  fi

  stop_all

  bold "Building and starting PRODUCTION stack..."

  if [[ -n "${REBUILD_SERVICES:-}" ]]; then
    # shellcheck disable=SC2086
    "${COMPOSE[@]}" up -d --build $REBUILD_SERVICES
  else
    "${COMPOSE[@]}" up -d --build
  fi

  wait_for_healthy mongodb
  wait_for_healthy licensing
  verify_prod_stack

  echo
  bold "Production stack is ready."
  info "Browse: ${SITE_URL}/products"
  info "Hard-refresh after deploy: Ctrl+Shift+R"
}

prompt_mode() {
  local current
  current="$(detect_mode)"

  echo
  bold "Nexxus Tech — rebuild stack"
  if [[ "$current" != "stopped" ]]; then
    info "Currently running: ${current}"
  else
    info "Stack is not running."
  fi
  echo
  echo "  1) Development  — hot reload at ${SITE_URL}"
  echo "  2) Production   — built static site (live)"
  echo "  3) Status only"
  echo "  4) Cancel"
  echo
  read -r -p "Choose [1-4]: " choice

  case "$choice" in
    1|dev|Dev|DEV) start_dev ;;
    2|prod|Prod|PROD) start_prod ;;
    3|status|Status) print_status ;;
    4|q|Q|cancel|Cancel) info "Cancelled."; exit 0 ;;
    *) err "Invalid choice."; exit 1 ;;
  esac
}

main() {
  if ! command -v docker >/dev/null 2>&1; then
    err "docker is not installed or not in PATH."
    exit 1
  fi

  case "${1:-}" in
    --dev|-d) start_dev ;;
    --prod|-p) start_prod ;;
    --status|-s) load_env; print_status ;;
    --help|-h) usage ;;
    "") prompt_mode ;;
    *) err "Unknown option: $1"; usage; exit 1 ;;
  esac
}

main "$@"
