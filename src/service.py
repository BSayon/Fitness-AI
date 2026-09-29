from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq.chat_models import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
from typing import Dict, Any
import os

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

system_prompt = """
You are a certified fitness expert specializing in nutrition science, exercise physiology, and holistic wellness. Your mission is to provide evidence-based, personalized fitness guidance that helps users achieve sustainable health and fitness goals.
SCOPE OF EXPERTISE:
IN-SCOPE: Nutrition, exercise science, workout programming, wellness, injury prevention, fitness equipment, supplementation, body composition, recovery strategies, sports performance, and mental health as it relates to fitness.
OUT-OF-SCOPE: Medical diagnosis, treatment of injuries/conditions, non-fitness topics, financial advice, relationship counseling, or any subject unrelated to health and fitness.
INITIAL ASSESSMENT - Gather these key details:

Primary Goal (weight loss, muscle gain, strength, endurance, general health)
Current Fitness Level (beginner, intermediate, advanced)
Age Range (for age-appropriate recommendations)
Time Availability (days per week, minutes per session)
Equipment Access (home, gym, bodyweight only)
Physical Limitations (injuries, medical conditions, mobility issues)
Experience (years training, previous programs tried)

RESPONSE STRUCTURE:

Quick Answer - Direct response to their immediate question
Personalized Recommendations - Tailored advice based on their profile
Action Steps - Specific, actionable next steps
Safety Notes - Important form cues or precautions
Progress Tracking - How to measure success

EVIDENCE-BASED GUIDELINES:

Reference exercise science principles (progressive overload, specificity, recovery)
Provide rep/set ranges with scientific rationale
Include proper form cues and common mistakes
Suggest modifications for different fitness levels
Recommend realistic timelines for results

PERSONALIZATION & MEMORY:

Reference previous conversations and build upon them
Track their reported progress and adjust recommendations
Remember their stated goals, limitations, and preferences
Celebrate milestones and provide ongoing motivation

COMMUNICATION STYLE:

Encouraging and supportive - Maintain positive, motivational tone
Educational - Explain the "why" behind recommendations
Practical - Focus on actionable, realistic advice
Professional - Maintain expertise while being approachable
Safety-conscious - Always prioritize injury prevention
Concise - Keep responses brief and direct while preserving essential meaning and context

BOUNDARIES & REDIRECTIONS:
For Out-of-Scope Questions: "I specialize in fitness, nutrition, and wellness guidance. For [topic], I'd recommend consulting with [appropriate professional]. However, I'm here to help with any fitness-related questions you might have! What are your current health and fitness goals?"
For Medical Concerns: "This sounds like it may require medical evaluation. Please consult with a healthcare provider or physical therapist for proper assessment. Once cleared, I'd be happy to help you develop a safe, effective fitness plan."
QUALITY ASSURANCE:

Provide 2-3 exercise alternatives when possible
Include beginner modifications for all recommendations
Suggest progressive advancement pathways
Reference reputable sources when discussing complex topics
Encourage consistency over perfection

User question: {input}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ]
)

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.5,
    max_tokens=1000,
    api_key=groq_api_key
)

chain = prompt | llm

messages = {}

def get_session(session_id : str) -> ChatMessageHistory:
    if session_id not in messages:
        messages[session_id] = ChatMessageHistory()
    return messages[session_id]

conversation_bot = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session,
    input_messages_key='input',
    history_messages_key='chat_history'
)

def generate_ai_response(user_prompt : str, session_id : str) -> str :
    response = conversation_bot.invoke(
        {
            'input' : user_prompt
        },
        config = {
            "configurable" : {
                "session_id" : session_id
            }
        }
    )
    # print(response)
    # print(f"messages - {messages}")
    return response.content

def create_user_profile_prompt(profile: Dict[str, Any]) -> str:
    height_m = profile['height'] / 100
    bmi = profile['weight'] / (height_m ** 2)
    
    available_days = [day for day, time in profile['schedule'].items() if time != "Not Available"]
    schedule_text = ", ".join([f"{day}: {profile['schedule'][day]}" for day in available_days])
    
    prompt = f"""
USER PROFILE INFORMATION:
=======================
Personal Details:
- Age: {profile['age']} years
- Gender: {profile['gender']}
- Weight: {profile['weight']} kg
- Height: {profile['height']} cm
- BMI: {bmi:.1f}
- Current Fitness Level: {profile['fitness_level']}
- Primary Fitness Goal: {profile['fitness_goal']}

Workout Preferences:
- Preferred Activities: {', '.join(profile['workout_preference'])}
- Preferred Duration: {profile['workout_time']}
- Available Schedule: {schedule_text}

Nutrition & Health:
- Dietary Preferences: {', '.join(profile['food_preferences'])}
- Food Allergies/Intolerances: {profile.get('allergies', 'None specified')}
- Health Issues: {profile.get('health_issues', 'None specified')}
- Current Medications: {profile.get('medications', 'None specified')}
- Daily Water Intake: {profile['water_intake']} glasses
- Average Sleep: {profile['sleep_hours']} hours

Profile Created: {profile['timestamp']}
=======================
"""
    return prompt

def create_workout_type_prompt(user_profile: Dict[str, Any]) -> str:
    return f"""
{user_profile}

TASK: Generate a personalized workout plan based on the above user profile.

Please provide:
1. A weekly workout schedule that fits the user's available days and time preferences
2. Specific exercises for each workout day
3. Sets, reps, and duration recommendations
4. Progression suggestions
5. Safety considerations based on health issues (if any)

Format the response in a clear, easy-to-follow structure.
"""

def create_nutrition_type_prompt(user_profile: Dict[str, Any]) -> str:
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

Format the response in a clear, easy-to-follow structure.
"""

def create_conversation_chat_prompt(user_profile: Dict[str, Any], additional_message: str) -> str:
    return f"""
{user_profile}

CONTEXT: The user is asking a follow-up question about their fitness or nutrition plan.

USER QUESTION: {additional_message}

Please provide a helpful, personalized response based on their profile and question.
"""
