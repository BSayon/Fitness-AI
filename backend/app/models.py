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


class ProfileRequest(BaseModel):
    profile: UserProfile


class GenerateRequest(BaseModel):
    profile: Optional[UserProfile] = None
    message: Optional[str] = ""


class GenerateResponse(BaseModel):
    response: str
    session_id: str


class ChatMessage(BaseModel):
    role: str
    content: str
    ts: int


class MetricLog(BaseModel):
    """A single daily health-tracking entry."""

    date: str  # ISO date (YYYY-MM-DD)
    weight: Optional[float] = Field(default=None, ge=20, le=400)
    water_glasses: Optional[int] = Field(default=None, ge=0, le=30)
    sleep_hours: Optional[float] = Field(default=None, ge=0, le=24)
    workouts_completed: Optional[int] = Field(default=None, ge=0, le=20)
    calories: Optional[int] = Field(default=None, ge=0, le=20000)
    note: Optional[str] = ""


class DashboardData(BaseModel):
    profile: Optional[UserProfile] = None
    workoutPlan: Optional[str] = None
    nutritionPlan: Optional[str] = None
    metrics: List[MetricLog] = []
    stats: Dict[str, object] = {}
