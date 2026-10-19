"""FastAPI entrypoint for the AI Fitness Coach backend.

Responsibilities:
* Verify Firebase ID tokens (Auth).
* Create/read the user's Firestore record via the Admin SDK.
* Generate workout / nutrition plans and chat replies through the shared
  ``src`` agent, persisting results to Firestore.
* Expose health-goal tracking (daily metric logs) and an aggregated dashboard.
"""
from __future__ import annotations

import hashlib
import os
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import firestore

from .firebase import get_db, verify_token
from .models import (
    DashboardData,
    GenerateRequest,
    GenerateResponse,
    MetricLog,
    ProfileRequest,
    UserProfile,
)
from .service import (
    create_conversation_chat_prompt,
    create_nutrition_type_prompt,
    create_user_profile_prompt,
    create_workout_type_prompt,
    generate_ai_response,
)

load_dotenv()

app = FastAPI(title="Zesayro API", version="1.0.0")

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


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _user_ref(uid: str):
    return get_db().collection("users").document(uid)


def _ensure_user_doc(user: Dict[str, Any]) -> None:
    """Create the base user record on first contact (Firestore Admin SDK)."""
    ref = _user_ref(user["uid"])
    if not ref.get().exists:
        ref.set(
            {
                "email": user.get("email"),
                "name": user.get("name") or "",
                "createdAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP,
            }
        )


def _get_record(uid: str) -> Dict[str, Any]:
    snap = _user_ref(uid).get()
    return snap.to_dict() if snap.exists else {}


def _session_id_for(user: Dict[str, Any], suffix: str) -> str:
    uid = user.get("uid", "anon")
    digest = hashlib.md5(f"{uid}:{suffix}".encode()).hexdigest()[:10]
    return f"user_{digest}"


def _resolve_profile(req: GenerateRequest, uid: str) -> Dict[str, Any]:
    if req.profile is not None:
        return req.profile.model_dump()
    stored = _get_record(uid).get("profile")
    if not stored:
        raise HTTPException(status_code=400, detail="No profile found. Create one first.")
    return stored


def _bmi(profile: Dict[str, Any]) -> Optional[float]:
    try:
        h = float(profile["height"]) / 100
        return round(float(profile["weight"]) / (h * h), 1) if h else None
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return None


def _compute_stats(profile: Optional[Dict[str, Any]], metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    stats: Dict[str, Any] = {}
    if profile:
        stats["bmi"] = _bmi(profile)
        stats["goal"] = profile.get("fitness_goal")
        stats["startingWeight"] = profile.get("weight")

    logged_weights = [(m.get("date"), m.get("weight")) for m in metrics if m.get("weight") is not None]
    logged_weights.sort(key=lambda x: x[0] or "")
    if logged_weights:
        stats["latestWeight"] = logged_weights[-1][1]
        baseline = (profile or {}).get("weight") or logged_weights[0][1]
        if baseline is not None:
            stats["weightChange"] = round(logged_weights[-1][1] - float(baseline), 1)

    stats["totalWorkouts"] = sum(int(m.get("workouts_completed") or 0) for m in metrics)
    stats["daysTracked"] = len({m.get("date") for m in metrics if m.get("date")})

    recent = sorted(metrics, key=lambda m: m.get("date") or "")[-7:]
    sleeps = [float(m["sleep_hours"]) for m in recent if m.get("sleep_hours") is not None]
    waters = [int(m["water_glasses"]) for m in recent if m.get("water_glasses") is not None]
    if sleeps:
        stats["avgSleep"] = round(sum(sleeps) / len(sleeps), 1)
    if waters:
        stats["avgWater"] = round(sum(waters) / len(waters), 1)

    # Current consecutive-day logging streak (ending today or yesterday).
    logged_dates = {m.get("date") for m in metrics if m.get("date")}
    streak = 0
    cursor = date.today()
    if cursor.isoformat() not in logged_dates:
        cursor = cursor - timedelta(days=1)
    while cursor.isoformat() in logged_dates:
        streak += 1
        cursor = cursor - timedelta(days=1)
    stats["streak"] = streak
    return stats


# --------------------------------------------------------------------------- #
# Health / identity
# --------------------------------------------------------------------------- #
@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/api/me")
def me(user=Depends(verify_token)) -> Dict[str, Any]:
    _ensure_user_doc(user)
    return {
        "uid": user.get("uid"),
        "email": user.get("email"),
        "name": user.get("name"),
        "picture": user.get("picture"),
    }


# --------------------------------------------------------------------------- #
# Profile (Firestore record creation happens here)
# --------------------------------------------------------------------------- #
@app.get("/api/profile")
def get_profile(user=Depends(verify_token)) -> Dict[str, Any]:
    return {"profile": _get_record(user["uid"]).get("profile")}


@app.post("/api/profile")
def save_profile(req: ProfileRequest, user=Depends(verify_token)) -> Dict[str, Any]:
    """Create/update the user's fitness record using the Firestore Admin SDK."""
    _ensure_user_doc(user)
    profile = req.profile.model_dump()
    if not profile.get("timestamp"):
        profile["timestamp"] = datetime.now(timezone.utc).isoformat()
    if not profile.get("name"):
        profile["name"] = user.get("name") or user.get("email") or "User"

    _user_ref(user["uid"]).set(
        {"profile": profile, "updatedAt": firestore.SERVER_TIMESTAMP},
        merge=True,
    )
    return {"ok": True, "profile": profile}


# --------------------------------------------------------------------------- #
# Plan generation (agent) + persistence
# --------------------------------------------------------------------------- #
def _generate_plan(kind: str, req: GenerateRequest, user: Dict[str, Any]) -> GenerateResponse:
    profile_dict = _resolve_profile(req, user["uid"])
    profile_dict.setdefault("name", user.get("name") or user.get("email", "User"))
    profile_prompt = create_user_profile_prompt(profile_dict)

    if kind == "workout":
        prompt = create_workout_type_prompt(profile_prompt)
        field = "workoutPlan"
    else:
        prompt = create_nutrition_type_prompt(profile_prompt)
        field = "nutritionPlan"

    session_id = _session_id_for(user, kind)
    try:
        content = generate_ai_response(prompt, session_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"LLM error: {exc}") from exc

    _ensure_user_doc(user)
    _user_ref(user["uid"]).set(
        {field: content, "updatedAt": firestore.SERVER_TIMESTAMP}, merge=True
    )
    return GenerateResponse(response=content, session_id=session_id)


@app.post("/api/workout", response_model=GenerateResponse)
def generate_workout(req: GenerateRequest, user=Depends(verify_token)) -> GenerateResponse:
    return _generate_plan("workout", req, user)


@app.post("/api/nutrition", response_model=GenerateResponse)
def generate_nutrition(req: GenerateRequest, user=Depends(verify_token)) -> GenerateResponse:
    return _generate_plan("nutrition", req, user)


# --------------------------------------------------------------------------- #
# Chat
# --------------------------------------------------------------------------- #
@app.post("/api/chat", response_model=GenerateResponse)
def chat(req: GenerateRequest, user=Depends(verify_token)) -> GenerateResponse:
    if not req.message:
        raise HTTPException(status_code=400, detail="message is required for chat")

    profile_dict = _resolve_profile(req, user["uid"])
    profile_prompt = create_user_profile_prompt(profile_dict)
    prompt = create_conversation_chat_prompt(profile_prompt, req.message)

    session_id = _session_id_for(user, "chat")
    try:
        content = generate_ai_response(prompt, session_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"LLM error: {exc}") from exc

    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    _ensure_user_doc(user)
    _user_ref(user["uid"]).set(
        {
            "chatHistory": firestore.ArrayUnion(
                [
                    {"role": "user", "content": req.message, "ts": now_ms},
                    {"role": "assistant", "content": content, "ts": now_ms + 1},
                ]
            ),
            "updatedAt": firestore.SERVER_TIMESTAMP,
        },
        merge=True,
    )
    return GenerateResponse(response=content, session_id=session_id)


@app.get("/api/chat/history")
def chat_history(user=Depends(verify_token)) -> Dict[str, Any]:
    return {"chatHistory": _get_record(user["uid"]).get("chatHistory", [])}


# --------------------------------------------------------------------------- #
# Health-goal tracking
# --------------------------------------------------------------------------- #
@app.get("/api/metrics")
def list_metrics(user=Depends(verify_token)) -> Dict[str, Any]:
    metrics = _get_record(user["uid"]).get("metrics", [])
    metrics.sort(key=lambda m: m.get("date") or "")
    return {"metrics": metrics}


@app.post("/api/metrics")
def add_metric(entry: MetricLog, user=Depends(verify_token)) -> Dict[str, Any]:
    _ensure_user_doc(user)
    record = _get_record(user["uid"])
    metrics: List[Dict[str, Any]] = record.get("metrics", [])
    # Replace an existing same-day entry instead of duplicating it.
    metrics = [m for m in metrics if m.get("date") != entry.date]
    metrics.append(entry.model_dump())
    metrics.sort(key=lambda m: m.get("date") or "")
    _user_ref(user["uid"]).set(
        {"metrics": metrics, "updatedAt": firestore.SERVER_TIMESTAMP}, merge=True
    )
    return {"ok": True, "metrics": metrics}


# --------------------------------------------------------------------------- #
# Dashboard aggregation
# --------------------------------------------------------------------------- #
@app.get("/api/dashboard", response_model=DashboardData)
def dashboard(user=Depends(verify_token)) -> DashboardData:
    _ensure_user_doc(user)
    record = _get_record(user["uid"])
    profile = record.get("profile")
    metrics = record.get("metrics", [])
    metrics.sort(key=lambda m: m.get("date") or "")
    return DashboardData(
        profile=UserProfile(**profile) if profile else None,
        workoutPlan=record.get("workoutPlan"),
        nutritionPlan=record.get("nutritionPlan"),
        metrics=[MetricLog(**m) for m in metrics],
        stats=_compute_stats(profile, metrics),
    )
