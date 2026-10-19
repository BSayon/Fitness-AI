#!/usr/bin/env bash
# Runs the FastAPI backend (internal) and the Next.js frontend (public) together
# inside a single container. The frontend proxies /api and /health to the
# backend via Next.js rewrites, so only $PORT is exposed.
set -euo pipefail

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${PORT:-3000}"

echo "[entrypoint] starting backend on 127.0.0.1:${BACKEND_PORT}"
uvicorn backend.app.main:app --host 127.0.0.1 --port "${BACKEND_PORT}" &
backend_pid=$!

echo "[entrypoint] starting frontend on 0.0.0.0:${FRONTEND_PORT}"
(
  cd /app/frontend
  exec node_modules/.bin/next start -H 0.0.0.0 -p "${FRONTEND_PORT}"
) &
frontend_pid=$!

shutdown() {
  echo "[entrypoint] shutting down"
  kill "${backend_pid}" "${frontend_pid}" 2>/dev/null || true
}
trap shutdown TERM INT

# If either process exits, stop the other and exit non-zero so the platform
# can restart the container.
wait -n "${backend_pid}" "${frontend_pid}"
exit_code=$?
echo "[entrypoint] a process exited (code ${exit_code}); stopping container"
shutdown
wait || true
exit "${exit_code}"
