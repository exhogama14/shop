#!/usr/bin/env bash
# DiamondStore — Production start script (Linux / macOS)
# Usage:  ./start.sh
set -euo pipefail

cd "$(dirname "$0")"

# Pick a free port if none provided
PORT="${PORT:-8000}"
export PORT
export BIND="${BIND:-0.0.0.0:$PORT}"

echo "💎 Starting DiamondStore (production mode)"
echo "   → bind:      $BIND"
echo "   → workers:   ${WEB_CONCURRENCY:-auto}"
echo "   → log level: ${LOG_LEVEL:-info}"

exec gunicorn -c gunicorn_config.py wsgi:app
