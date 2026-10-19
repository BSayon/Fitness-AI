"""Firebase Admin initialization and FastAPI auth dependency."""
from __future__ import annotations

import json
import os
from typing import Optional

import firebase_admin
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as fb_auth
from firebase_admin import credentials, firestore

# Load env BEFORE Firebase initializes (which happens at import time below).
# A single repo-root .env is the source of truth for BOTH frontend and backend.
# (backend/.env and src/.env remain optional fallbacks; first value wins.)
_HERE = os.path.dirname(__file__)
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
load_dotenv(os.path.join(_ROOT, ".env"))  # repo-root .env (single source of truth)
load_dotenv(os.path.join(_HERE, "..", ".env"))  # backend/.env (optional)
load_dotenv(os.path.join(_ROOT, "src", ".env"))  # src/.env (optional)


_initialized = False
_db = None


def _service_account_from_env() -> Optional[dict]:
    """Assemble a service-account dict from individual env vars.

    Lets you keep the Firebase Admin credentials as plain .env entries instead
    of a JSON file. Requires FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, and
    FIREBASE_PRIVATE_KEY (newlines may be written as literal "\\n").
    """
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
    private_key = os.getenv("FIREBASE_PRIVATE_KEY")

    if not (project_id and client_email and private_key):
        return None

    private_key = private_key.replace("\\n", "\n")
    info = {
        "type": "service_account",
        "project_id": project_id,
        "client_email": client_email,
        "private_key": private_key,
        "token_uri": os.getenv(
            "FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"
        ),
    }
    # Optional fields — included only if provided.
    for env_name, key in (
        ("FIREBASE_PRIVATE_KEY_ID", "private_key_id"),
        ("FIREBASE_CLIENT_ID", "client_id"),
    ):
        value = os.getenv(env_name)
        if value:
            info[key] = value
    return info


def _init_firebase() -> None:
    global _initialized
    if _initialized or firebase_admin._apps:
        _initialized = True
        return

    env_account = _service_account_from_env()
    raw_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # Legacy fallback: a service-account key file at the repository root.
    default_key = os.path.join(_ROOT, "serviceAccountKey.json")

    if env_account:
        cred = credentials.Certificate(env_account)
    elif raw_json:
        cred = credentials.Certificate(json.loads(raw_json))
    elif cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
    elif os.path.exists(default_key):
        cred = credentials.Certificate(default_key)
    else:
        # Fall back to application default (e.g. Cloud Run metadata server).
        cred = credentials.ApplicationDefault()

    firebase_admin.initialize_app(cred)
    _initialized = True


_init_firebase()


def get_db():
    """Return a cached Firestore client (Admin SDK)."""
    global _db
    if _db is None:
        _db = firestore.client()
    return _db


_bearer = HTTPBearer(auto_error=False)


def verify_token(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> dict:
    """FastAPI dependency: validates a Firebase ID token and returns the decoded claims."""
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        decoded = fb_auth.verify_id_token(creds.credentials)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return decoded
