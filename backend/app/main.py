"""FastAPI entrypoint for the Fitness AI Bot backend."""
from __future__ import annotations

import hashlib
import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .firebase import verify_token
from .models import GenerateRequest, GenerateResponse
from .service import (
    create_conversation_chat_prompt,
    create_nutrition_type_prompt,
    create_user_profile_prompt,
    create_workout_type_prompt,
    generate_ai_response,
)

load_dotenv()

app = FastAPI(title="Fitness AI Bot", version="1.0.0")

_origins = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


def _session_id_for(user: Dict[str, Any], suffix: str) -> str:
    uid = user.get("uid", "anon")
    digest = hashlib.md5(f"{uid}:{suffix}".encode()).hexdigest()[:10]
    return f"user_{digest}"


def _run(kind: str, req: GenerateRequest, user: Dict[str, Any]) -> GenerateResponse:
    profile_dict = req.profile.model_dump()
    profile_dict.setdefault("name", user.get("name") or user.get("email", "User"))
    profile_prompt = create_user_profile_prompt(profile_dict)

    if kind == "workout":
        prompt = create_workout_type_prompt(profile_prompt)
    elif kind == "nutrition":
        prompt = create_nutrition_type_prompt(profile_prompt)
    elif kind == "chat":
        if not req.message:
            raise HTTPException(status_code=400, detail="message is required for chat")
        prompt = create_conversation_chat_prompt(profile_prompt, req.message)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown kind: {kind}")

    session_id = _session_id_for(user, kind)
    try:
        content = generate_ai_response(prompt, session_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"LLM error: {exc}") from exc

    return GenerateResponse(response=str(content), session_id=session_id)


@app.post("/api/workout", response_model=GenerateResponse)
def generate_workout(req: GenerateRequest, user=Depends(verify_token)) -> GenerateResponse:
    return _run("workout", req, user)


@app.post("/api/nutrition", response_model=GenerateResponse)
def generate_nutrition(req: GenerateRequest, user=Depends(verify_token)) -> GenerateResponse:
    return _run("nutrition", req, user)


@app.post("/api/chat", response_model=GenerateResponse)
def generate_chat(req: GenerateRequest, user=Depends(verify_token)) -> GenerateResponse:
    return _run("chat", req, user)


@app.get("/api/me")
def me(user=Depends(verify_token)) -> Dict[str, Any]:
    return {
        "uid": user.get("uid"),
        "email": user.get("email"),
        "name": user.get("name"),
        "picture": user.get("picture"),
    }
