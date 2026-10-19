"""Convenience launcher for local development.

Runs the FastAPI backend (which imports the shared AI engine from ``src``).

    uv run python main.py          # starts http://127.0.0.1:8000

Environment variables are read from a repo-root ``.env`` (and ``src/.env``).
Required: GROQ_API_KEY and Firebase credentials
(GOOGLE_APPLICATION_CREDENTIALS or FIREBASE_SERVICE_ACCOUNT_JSON).
"""
import os

import uvicorn


def main() -> None:
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()
