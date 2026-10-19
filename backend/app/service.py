"""Thin adapter that exposes the shared ``src`` AI engine to the API layer.

All prompt construction and agent invocation live in ``src/`` (the "agent
folder"). This keeps the FastAPI backend as a transport layer over the same
engine used by notebooks/prototypes.
"""
from __future__ import annotations

from src.service.service import (  # noqa: F401  (re-exported for the API layer)
    create_conversation_chat_prompt,
    create_nutrition_type_prompt,
    create_user_profile_prompt,
    create_workout_type_prompt,
    generate_ai_response,
)

__all__ = [
    "create_conversation_chat_prompt",
    "create_nutrition_type_prompt",
    "create_user_profile_prompt",
    "create_workout_type_prompt",
    "generate_ai_response",
]
