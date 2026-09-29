"""LangChain + Groq fitness coach service (ported from the original Streamlit app)."""
from __future__ import annotations

import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq.chat_models import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """
You are a certified fitness expert specializing in nutrition science, exercise physiology, and holistic wellness. Your mission is to provide evidence-based, personalized fitness guidance that helps users achieve sustainable health and fitness goals.
SCOPE OF EXPERTISE:
IN-SCOPE: Nutrition, exercise science, workout programming, wellness, injury prevention, fitness equipment, supplementation, body composition, recovery strategies, sports performance, and mental health as it relates to fitness.
OUT-OF-SCOPE: Medical diagnosis, treatment of injuries/conditions, non-fitness topics, financial advice, relationship counseling, or any subject unrelated to health and fitness.

RESPONSE STRUCTURE:
1. Quick Answer - Direct response to their immediate question
2. Personalized Recommendations - Tailored advice based on their profile
3. Action Steps - Specific, actionable next steps
4. Safety Notes - Important form cues or precautions
5. Progress Tracking - How to measure success

COMMUNICATION STYLE: Encouraging, educational, practical, professional, safety-conscious, and concise.

BOUNDARIES: For out-of-scope questions, redirect the user politely to the appropriate professional. Never provide medical diagnoses.

User question: {input}
"""

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.5,
    max_tokens=1000,
    api_key=GROQ_API_KEY,
)

_chain = _prompt | _llm

# In-memory chat history per session_id. Swap for Redis/Firestore for horizontal scale.
_sessions: Dict[str, ChatMessageHistory] = {}


def _get_session(session_id: str) -> ChatMessageHistory:
    if session_id not in _sessions:
        _sessions[session_id] = ChatMessageHistory()
    return _sessions[session_id]


_conversation_bot = RunnableWithMessageHistory(
    _chain,
    get_session_history=_get_session,
    input_messages_key="input",
    history_messages_key="chat_history",
)


def generate_ai_response(user_prompt: str, session_id: str) -> str:
    response = _conversation_bot.invoke(
        {"input": user_prompt},
        config={"configurable": {"session_id": session_id}},
    )
    return response.content


def create_user_profile_prompt(profile: Dict[str, Any]) -> str:
    height_m = profile["height"] / 100
    bmi = profile["weight"] / (height_m ** 2)

    available_days = [d for d, t in profile.get("schedule", {}).items() if t != "Not Available"]
    schedule_text = ", ".join(
        f"{d}: {profile['schedule'][d]}" for d in available_days
    ) or "Flexible"

    return f"""
USER PROFILE INFORMATION:
=======================
Personal Details:
- Name: {profile.get('name', 'User')}
- Age: {profile['age']} years
- Gender: {profile['gender']}
- Weight: {profile['weight']} kg
- Height: {profile['height']} cm
- BMI: {bmi:.1f}
- Current Fitness Level: {profile['fitness_level']}
- Primary Fitness Goal: {profile['fitness_goal']}

Workout Preferences:
- Preferred Activities: {', '.join(profile.get('workout_preference', []))}
- Preferred Duration: {profile['workout_time']}
- Available Schedule: {schedule_text}

Nutrition & Health:
- Dietary Preferences: {', '.join(profile.get('food_preferences', []))}
- Food Allergies/Intolerances: {profile.get('allergies') or 'None specified'}
- Health Issues: {profile.get('health_issues') or 'None specified'}
- Current Medications: {profile.get('medications') or 'None specified'}
- Daily Water Intake: {profile['water_intake']} glasses
- Average Sleep: {profile['sleep_hours']} hours
=======================
"""


def create_workout_type_prompt(user_profile: str) -> str:
    return f"""
{user_profile}

TASK: Generate a personalized workout plan based on the above user profile.

Please provide:
1. A weekly workout schedule that fits the user's available days and time preferences
2. Specific exercises for each workout day
3. Sets, reps, and duration recommendations
4. Progression suggestions
5. Safety considerations based on health issues (if any)

Format the response in a clear, easy-to-follow structure using Markdown.
"""


def create_nutrition_type_prompt(user_profile: str) -> str:
    return f"""
{user_profile}

TASK: Generate a personalized nutrition plan based on the above user profile.

Please provide:
1. Daily calorie recommendations based on goals
2. Macro-nutrient breakdown (carbs, protein, fats)
3. Sample meal plans for different days
4. Food suggestions that align with dietary preferences
5. Hydration and supplement recommendations
6. Considerations for any health issues or medications

Format the response in a clear, easy-to-follow structure using Markdown.
"""


def create_conversation_chat_prompt(user_profile: str, additional_message: str) -> str:
    return f"""
{user_profile}

CONTEXT: The user is asking a follow-up question about their fitness or nutrition plan.

USER QUESTION: {additional_message}

Please provide a helpful, personalized response based on their profile and question.
"""
