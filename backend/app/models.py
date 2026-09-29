"""Pydantic models shared across API endpoints."""
from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    name: Optional[str] = ""
    age: int = Field(ge=13, le=100)
    weight: float = Field(ge=30, le=300)
    height: float = Field(ge=100, le=250)
    gender: str
    workout_preference: List[str] = []
    workout_time: str
    fitness_level: str
    fitness_goal: str
    schedule: Dict[str, str] = {}
    food_preferences: List[str] = []
    allergies: str = ""
    health_issues: str = ""
    medications: str = ""
    water_intake: int = 8
    sleep_hours: int = 7
    timestamp: Optional[str] = None


class GenerateRequest(BaseModel):
    profile: UserProfile
    message: Optional[str] = ""


class GenerateResponse(BaseModel):
    response: str
    session_id: str
