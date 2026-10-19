"""Core fitness-coach service: prompt construction + agent invocation.

This module is the single AI engine used by the FastAPI backend. It builds
personalized prompts from a user profile and runs them through the LangChain
agent defined in ``src/agents/agent.py``.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from src.agents.agent import agent
from src.prompts.prompt import (
    CONVERSATION_CHAT_TEMPLATE,
    NUTRITION_PLAN_TEMPLATE,
    USER_PROFILE_TEMPLATE,
    WORKOUT_PLAN_TEMPLATE,
)


def generate_ai_response(user_prompt: str, session_id: str = "default") -> str:
    """Run a prompt through the agent and return its text response.

    ``session_id`` maps to a LangGraph ``thread_id`` so each user/feature keeps
    an isolated, memory-aware conversation.
    """
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_prompt}]},
        config={"configurable": {"thread_id": session_id}},
    )
    messages = result.get("messages", [])
    if not messages:
        return ""
    last = messages[-1]
    content = getattr(last, "content", last)
    if isinstance(content, list):
        # Some providers return a list of content blocks.
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    return str(content)


def _as_text(value: Any, fallback: str = "None specified") -> str:
    if value is None:
        return fallback
    if isinstance(value, (list, tuple)):
        joined = ", ".join(str(v) for v in value if str(v).strip())
        return joined or fallback
    text = str(value).strip()
    return text or fallback


def create_user_profile_prompt(profile: Dict[str, Any]) -> str:
    """Render the human-readable profile block from a raw profile dict."""
    height_cm = float(profile.get("height", 0) or 0)
    weight_kg = float(profile.get("weight", 0) or 0)
    height_m = height_cm / 100 if height_cm else 0
    bmi = weight_kg / (height_m**2) if height_m else 0.0

    schedule = profile.get("schedule") or {}
    if isinstance(schedule, dict):
        schedule_text = ", ".join(
            f"{day}: {time}"
            for day, time in schedule.items()
            if time and time != "Not Available"
        ) or "No fixed schedule"
    else:
        schedule_text = _as_text(schedule, "No fixed schedule")

    timestamp = profile.get("timestamp") or datetime.now(timezone.utc).isoformat()

    return USER_PROFILE_TEMPLATE.format(
        age=profile.get("age", "N/A"),
        gender=profile.get("gender", "N/A"),
        weight=weight_kg,
        height=height_cm,
        bmi=bmi,
        fitness_level=profile.get("fitness_level", "N/A"),
        fitness_goal=profile.get("fitness_goal", "N/A"),
        activities=_as_text(profile.get("workout_preference"), "No preference"),
        workout_time=profile.get("workout_time", "N/A"),
        schedule_text=schedule_text,
        dietary_preferences=_as_text(profile.get("food_preferences"), "No restrictions"),
        allergies=_as_text(profile.get("allergies")),
        health_issues=_as_text(profile.get("health_issues")),
        medications=_as_text(profile.get("medications")),
        water_intake=profile.get("water_intake", "N/A"),
        sleep_hours=profile.get("sleep_hours", "N/A"),
        timestamp=timestamp,
    )


def create_workout_type_prompt(user_profile: str) -> str:
    return WORKOUT_PLAN_TEMPLATE.format(user_profile=user_profile)


def create_nutrition_type_prompt(user_profile: str) -> str:
    return NUTRITION_PLAN_TEMPLATE.format(user_profile=user_profile)


def create_conversation_chat_prompt(user_profile: str, additional_message: str) -> str:
    return CONVERSATION_CHAT_TEMPLATE.format(
        user_profile=user_profile, additional_message=additional_message
    )
