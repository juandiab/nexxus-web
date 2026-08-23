#!/usr/bin/env bash
# Watch origin/main and redeploy the stack whenever new commits land.
#
# Usage:
#   ./scripts/auto-deploy.sh              # one check, deploy if main moved
#   ./scripts/auto-deploy.sh --loop       # keep checking every INTERVAL seconds
#   ./scripts/auto-deploy.sh --force      # redeploy even if there are no new commits
#   ./scripts/auto-deploy.sh --status     # show local vs remote HEAD and exit
#
# Environment (optional):
#   INTERVAL   Seconds between checks in --loop mode (default: 120)
#   SERVICES   Space-separated services to rebuild (default: frontend frontend-react)
#   LOG_FILE   Where to append log lines (default: /var/log/nexxus-auto-deploy.log)
#
# Designed to run unattended (cron / systemd timer). It refuses to deploy when the
# working tree is dirty, so manual edits on the server are never silently discarded.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BRANCH="${BRANCH:-main}"
INTERVAL="${INTERVAL:-120}"
SERVICES="${SERVICES:-frontend frontend-react}"
LOG_FILE="${LOG_FILE:-/var/log/nexxus-auto-deploy.log}"
LOCK_FILE="/tmp/nexxus-auto-deploy.lock"

log() {
  local line
  line="$(date '+%Y-%m-%d %H:%M:%S') $*"
  echo "$line"
  if [[ -w "$(dirname "$LOG_FILE")" || -w "$LOG_FILE" ]]; then
    echo "$line" >> "$LOG_FILE" 2>/dev/null || true
  fi
}

working_tree_dirty() {
  [[ -n "$(git status --porcelain --untracked-files=no)" ]]
}

remote_head() {
  git fetch --quiet origin "$BRANCH"
  git rev-parse "origin/${BRANCH}"
}

deploy() {
  local before after
  before="$(git rev-parse --short HEAD)"

  log "Pulling origin/${BRANCH}..."
  git checkout --quiet "$BRANCH"
  git pull --quiet --ff-only origin "$BRANCH"

  after="$(git rev-parse --short HEAD)"
  log "Now at ${after} (was ${before}). Rebuilding: ${SERVICES}"

  # shellcheck disable=SC2086
  docker compose build --build-arg GIT_SHA="${after}" $SERVICES
  # shellcheck disable=SC2086
  docker compose up -d $SERVICES

  # nginx config lives in the repo too — reload it if it changed.
  if ! git diff --quiet "${before}..${after}" -- nginx/ 2>/dev/null; then
    log "nginx config changed — reloading nexxustech-nginx"
    docker compose up -d --force-recreate nginx
  fi

  if docker compose exec -T frontend sh -c 'wget -qO- http://127.0.0.1:80/ 2>/dev/null | head -c 80' | grep -q '<!DOCTYPE html>'; then
    log "Deploy OK — frontend serving at ${after}"
  else
    log "WARNING: frontend did not answer on :80 after deploy"
    return 1
  fi
}

check_once() {
  local local_head remote

  local_head="$(git rev-parse HEAD)"
  remote="$(remote_head)"

  if [[ "${1:-}" != "--force" && "$local_head" == "$remote" ]]; then
    return 0
  fi

  if working_tree_dirty; then
    log "SKIP: local changes present (git status is dirty). Commit or stash first."
    return 0
  fi

  log "New commits on origin/${BRANCH} — deploying"
  deploy
}

status() {
  local remote
  remote="$(remote_head)"
  echo "branch:      ${BRANCH}"
  echo "local HEAD:  $(git rev-parse --short HEAD) $(git log -1 --format=%s | cut -c1-60)"
  echo "origin HEAD: $(git rev-parse --short "$remote") $(git log -1 --format=%s "$remote" | cut -c1-60)"
  if working_tree_dirty; then
    echo "tree:        DIRTY (auto-deploy would skip)"
  else
    echo "tree:        clean"
  fi
}

main() {
  # Serialize runs so a slow build never overlaps the next tick.
  exec 9>"$LOCK_FILE"
  if ! flock -n 9; then
    log "Another auto-deploy run is in progress — exiting."
    exit 0
  fi

  case "${1:-}" in
    --status|-s) status ;;
    --force|-f)  check_once --force ;;
    --loop|-l)
      log "Watching origin/${BRANCH} every ${INTERVAL}s"
      while true; do
        check_once || log "Deploy failed — will retry on next tick"
        sleep "$INTERVAL"
      done
      ;;
    --help|-h)  sed -n '2,20p' "$0" ;;
    "")         check_once ;;
    *)          echo "Unknown option: $1" >&2; exit 1 ;;
  esac
}

main "$@"
