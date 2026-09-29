# import streamlit as st
# import json
# from datetime import datetime
# from typing import Dict, Any, List
# import pandas as pd
# import hashlib
# import os
# from service import generate_ai_response, create_user_profile_prompt, create_workout_type_prompt, create_nutrition_type_prompt, create_conversation_chat_prompt

# # Configure page
# st.set_page_config(
#     page_title="AI Fitness Coach",
#     page_icon="💪",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #FF6B35;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .section-header {
#         font-size: 1.5rem;
#         font-weight: bold;
#         color: #2E86AB;
#         margin: 1rem 0;
#         border-bottom: 2px solid #2E86AB;
#         padding-bottom: 0.5rem;
#     }
#     .profile-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1rem;
#         border-radius: 10px;
#         color: white;
#         margin: 1rem 0;
#     }
#     .chat-message {
#         padding: 1rem;
#         border-radius: 10px;
#         margin: 0.5rem 0;
#         border-left: 4px solid #FF6B35;
#         background-color: #f8f9fa;
#     }
#     .success-box {
#         background-color: #d4edda;
#         border: 1px solid #c3e6cb;
#         color: #155724;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 1rem 0;
#     }
#     .login-container {
#         max-width: 400px;
#         margin: 2rem auto;
#         padding: 2rem;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         border-radius: 15px;
#         color: white;
#     }
#     .login-header {
#         text-align: center;
#         font-size: 2rem;
#         font-weight: bold;
#         margin-bottom: 2rem;
#         color: white;
#     }
# </style>
# """, unsafe_allow_html=True)

# def init_database():
#     """Initialize in-memory database if it doesn't exist"""
#     if 'users_db' not in st.session_state:
#         st.session_state.users_db = {}

# # Authentication functions
# def hash_password(password: str) -> str:
#     """Hash a password using SHA-256"""
#     return hashlib.sha256(password.encode()).hexdigest()

# def load_users() -> Dict[str, Dict]:
#     """Load users from in-memory database"""
#     init_database()
#     return st.session_state.users_db

# def save_users(users: Dict[str, Dict]):
#     """Save users to in-memory database"""
#     st.session_state.users_db = users

# def create_user(username: str, password: str, name: str = "") -> bool:
#     """Create a new user account"""
#     users = load_users()
    
#     if username in users:
#         return False  # User already exists
    
#     users[username] = {
#         'password_hash': hash_password(password),
#         'name': name,
#         'created_at': datetime.now().isoformat(),
#         'profile': {},
#         'chat_history': [],
#         'workout_plan': None,
#         'nutrition_plan': None
#     }
#     save_users(users)
#     return True

# def authenticate_user(username: str, password: str) -> bool:
#     """Authenticate user credentials"""
#     users = load_users()
    
#     if username not in users:
#         return False
    
#     return users[username]['password_hash'] == hash_password(password)

# def get_user_data(username: str) -> Dict:
#     """Get user's stored data"""
#     users = load_users()
#     return users.get(username, {})

# def save_user_data(username: str, user_data: Dict):
#     """Save user's data"""
#     users = load_users()
#     if username in users:
#         users[username].update(user_data)
#         save_users(users)

# # Initialize session state
# def init_session_state():
#     """Initialize all session state variables"""
#     init_database()  # Initialize the in-memory database
    
#     if 'authenticated' not in st.session_state:
#         st.session_state.authenticated = False
#     if 'username' not in st.session_state:
#         st.session_state.username = ""
#     if 'user_profile' not in st.session_state:
#         st.session_state.user_profile = {}
#     if 'chat_history' not in st.session_state:
#         st.session_state.chat_history = []
#     if 'workout_plan' not in st.session_state:
#         st.session_state.workout_plan = None
#     if 'nutrition_plan' not in st.session_state:
#         st.session_state.nutrition_plan = None
#     if 'profile_submitted' not in st.session_state:
#         st.session_state.profile_submitted = False
#     if 'current_session_id' not in st.session_state:
#         st.session_state.current_session_id = None

# def load_user_session(username: str):
#     """Load user's session data"""
#     user_data = get_user_data(username)
    
#     st.session_state.user_profile = user_data.get('profile', {})
#     st.session_state.chat_history = user_data.get('chat_history', [])
#     st.session_state.workout_plan = user_data.get('workout_plan', None)
#     st.session_state.nutrition_plan = user_data.get('nutrition_plan', None)
#     st.session_state.profile_submitted = bool(st.session_state.user_profile)

# def save_user_session(username: str):
#     """Save current session data to user's account"""
#     user_data = {
#         'profile': st.session_state.user_profile,
#         'chat_history': st.session_state.chat_history,
#         'workout_plan': st.session_state.workout_plan,
#         'nutrition_plan': st.session_state.nutrition_plan,
#         'last_updated': datetime.now().isoformat()
#     }
#     save_user_data(username, user_data)

# def login_page():
#     """Display login/registration page"""
#     st.markdown('<div class="main-header">🏋️ AI Fitness Coach</div>', unsafe_allow_html=True)
    
#     # Create tabs for login and registration
#     tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
#     with tab1:
#         st.markdown('<div class="login-header">Welcome!</div>', unsafe_allow_html=True)
        
#         with st.form("login_form"):
#             username = st.text_input("Username", placeholder="Enter your username")
#             password = st.text_input("Password", type="password", placeholder="Enter your password")
            
#             col1, col2 = st.columns([1, 2])
#             with col1:
#                 login_button = st.form_submit_button("Login", type="primary", use_container_width=True)
            
#             if login_button:
#                 if username and password:
#                     if authenticate_user(username, password):
#                         st.session_state.authenticated = True
#                         st.session_state.username = username
#                         load_user_session(username)
#                         st.success("✅ Login successful!")
#                         st.rerun()
#                     else:
#                         st.error("❌ Invalid username or password!")
#                 else:
#                     st.warning("⚠️ Please enter both username and password!")
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with tab2:
#         st.markdown('<div class="login-header">Create Account</div>', unsafe_allow_html=True)
        
#         with st.form("register_form"):
#             name = st.text_input("Name", placeholder="Enter your name")
#             new_username = st.text_input("Choose Username", placeholder="Enter a unique username")
#             new_password = st.text_input("Password", type="password", placeholder="Choose a strong password")
#             confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
#             col1, col2 = st.columns([1, 2])
#             with col1:
#                 register_button = st.form_submit_button("Register", type="primary", use_container_width=True)
            
#             if register_button:
#                 if not name.strip():
#                     st.error("❌ Name is mandatory!")
#                 if new_username and new_password and confirm_password:
#                     if new_password != confirm_password:
#                         st.error("❌ Passwords do not match!")
#                     elif len(new_password) < 6:
#                         st.error("❌ Password must be at least 6 characters long!")
#                     elif len(new_username) < 3:
#                         st.error("❌ Username must be at least 3 characters long!")
#                     else:
#                         if create_user(new_username, new_password, name):
#                             st.success("✅ Account created successfully! Please login.")
#                             st.balloons()
#                         else:
#                             st.error("❌ Username already exists! Please choose a different username.")
#                 else:
#                     st.warning("⚠️ Please fill in all required fields!")
        
#         st.markdown('</div>', unsafe_allow_html=True)

# def call_backend_service(request_type: str, user_profile: Dict[str, Any], additional_message: str = "") -> Dict[str, Any]:
#     """Call the backend LangChain service using generateResponse method"""
#     try:
#         # Generate session_id based on user profile (you can modify this logic)
#         import hashlib
#         profile_hash = hashlib.md5(str(user_profile.get('timestamp', 'default')).encode()).hexdigest()[:8]
#         session_id = f"user_{profile_hash}"
        
#         # Format the user prompt based on request type
#         profile_prompt = create_user_profile_prompt(user_profile)
        
#         if request_type == 'workout':
#             user_prompt = create_workout_type_prompt(profile_prompt)
        
#         elif request_type == 'nutrition':
#             user_prompt = create_nutrition_type_prompt(profile_prompt)
        
#         elif request_type == 'chat':
#             user_prompt = create_conversation_chat_prompt(profile_prompt, additional_message)
        
#         else:
#             user_prompt = additional_message
               
#         response = generate_ai_response(user_prompt, session_id)
        
#         if response:
#             return {
#                     'response': str(response),
#                     'session_id': session_id
#                 }
#         else:
#             return {'error': f'Backend error: {response.status_code} - {response.text}'}
            
#     except Exception as e:
#         return {'error': f'Unexpected error: {str(e)}'}

# def collect_user_profile():
#     """Collect user profile information"""
#     st.markdown('<div class="section-header">👤 User Profile Information</div>', unsafe_allow_html=True)
    
#     # Get the user's name from the database
#     user_data = get_user_data(st.session_state.username)
#     user_name = user_data.get('name', '')

#     col1, col2 = st.columns(2)
    
#     with col1:
#         age = st.number_input("Age", min_value=13, max_value=100, value=25)
#         weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
#         height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
#         gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        
#     with col2:
#         workout_preference = st.multiselect(
#             "Workout Preferences",
#             ["Cardio", "Strength Training", "Yoga", "Pilates", "HIIT", "CrossFit", "Swimming", "Running", "Cycling", "Dancing"],
#             default=["Cardio", "Strength Training"]
#         )
        
#         workout_time = st.selectbox(
#             "Preferred Workout Duration",
#             ["15-30 minutes", "30-45 minutes", "45-60 minutes", "60-90 minutes", "90+ minutes"]
#         )
        
#         fitness_level = st.selectbox(
#             "Current Fitness Level",
#             ["Beginner", "Intermediate", "Advanced"]
#         )
        
#         fitness_goal = st.selectbox(
#             "Primary Fitness Goal",
#             ["Weight Loss", "Muscle Gain", "Endurance", "Strength", "Flexibility", "General Health"]
#         )
    
#     st.markdown('<div class="section-header">📅 Weekly Schedule</div>', unsafe_allow_html=True)
    
#     days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#     schedule = {}
    
#     cols = st.columns(7)
#     for i, day in enumerate(days_of_week):
#         with cols[i]:
#             available = st.checkbox(f"{day[:3]}", key=f"day_{i}")
#             if available:
#                 time_slot = st.selectbox(
#                     "Time",
#                     ["Morning (6-10 AM)", "Afternoon (12-4 PM)", "Evening (5-8 PM)", "Night (8-10 PM)"],
#                     key=f"time_{i}"
#                 )
#                 schedule[day] = time_slot
#             else:
#                 schedule[day] = "Not Available"
    
#     st.markdown('<div class="section-header">🍽️ Dietary Preferences & Health</div>', unsafe_allow_html=True)
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         food_preferences = st.multiselect(
#             "Dietary Preferences",
#             ["Vegetarian", "Vegan", "Pescatarian", "Keto", "Paleo", "Mediterranean", "Low-carb", "High-protein", "Gluten-free", "No restrictions"],
#             default=["No restrictions"]
#         )
        
#         allergies = st.text_area("Food Allergies/Intolerances", placeholder="e.g., nuts, dairy, shellfish")
        
#     with col2:
#         health_issues = st.text_area(
#             "Health Issues/Medical Conditions",
#             placeholder="e.g., diabetes, hypertension, joint problems, injuries"
#         )
        
#         medications = st.text_area("Current Medications", placeholder="List any medications that might affect exercise or diet")
    
#     # Water intake and sleep
#     col1, col2 = st.columns(2)
#     with col1:
#         water_intake = st.slider("Daily Water Intake (glasses)", 1, 15, 8)
#     with col2:
#         sleep_hours = st.slider("Average Sleep Hours", 4, 12, 7)
    
#     user_profile = {
#         'name': user_name,
#         'age': age,
#         'weight': weight,
#         'height': height,
#         'gender': gender,
#         'workout_preference': workout_preference,
#         'workout_time': workout_time,
#         'fitness_level': fitness_level,
#         'fitness_goal': fitness_goal,
#         'schedule': schedule,
#         'food_preferences': food_preferences,
#         'allergies': allergies,
#         'health_issues': health_issues,
#         'medications': medications,
#         'water_intake': water_intake,
#         'sleep_hours': sleep_hours,
#         'timestamp': datetime.now().isoformat()
#     }
    
#     return user_profile

# def display_profile_summary():
#     """Display user profile summary"""
#     if st.session_state.user_profile:
#         profile = st.session_state.user_profile
        
#         st.markdown('<div class="section-header">📋 Profile Summary</div>', unsafe_allow_html=True)
        
#         # Calculate BMI
#         height_m = profile['height'] / 100
#         bmi = profile['weight'] / (height_m ** 2)
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.metric("Age", f"{profile['age']} years")
#             st.metric("Weight", f"{profile['weight']} kg")
            
#         with col2:
#             st.metric("Height", f"{profile['height']} cm")
#             st.metric("BMI", f"{bmi:.1f}")
            
#         with col3:
#             st.metric("Fitness Level", profile['fitness_level'])
#             st.metric("Primary Goal", profile['fitness_goal'])
            
#         with col4:
#             available_days = len([day for day, time in profile['schedule'].items() if time != "Not Available"])
#             st.metric("Available Days", f"{available_days}/7")
#             st.metric("Water Intake", f"{profile['water_intake']} glasses/day")

# def generate_plans():
#     """Generate workout and nutrition plans"""
#     if not st.session_state.user_profile:
#         st.error("Please complete your profile first!")
#         return
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         if st.button("🏋️ Generate Workout Plan", type="primary", use_container_width=True):
#             with st.spinner("Creating your personalized workout plan..."):
#                 response = call_backend_service('workout', st.session_state.user_profile)
                
#                 if 'error' in response:
#                     st.error(f"Error generating workout plan: {response['error']}")
#                 else:
#                     st.session_state.workout_plan = response
#                     st.session_state.current_session_id = response.get('session_id')
#                     # Add to chat history
#                     st.session_state.chat_history.append({
#                         'type': 'workout_request',
#                         'user_profile': st.session_state.user_profile,
#                         'response': response,
#                         'session_id': response.get('session_id'),
#                         'timestamp': datetime.now().isoformat()
#                     })
#                     # Save to user account
#                     save_user_session(st.session_state.username)
#                     st.success("✅ Workout plan generated successfully!")
#                     st.rerun()
    
#     with col2:
#         if st.button("🥗 Generate Nutrition Plan", type="primary", use_container_width=True):
#             with st.spinner("Creating your personalized nutrition plan..."):
#                 response = call_backend_service('nutrition', st.session_state.user_profile)
                
#                 if 'error' in response:
#                     st.error(f"Error generating nutrition plan: {response['error']}")
#                 else:
#                     st.session_state.nutrition_plan = response
#                     st.session_state.current_session_id = response.get('session_id')
#                     # Add to chat history
#                     st.session_state.chat_history.append({
#                         'type': 'nutrition_request',
#                         'user_profile': st.session_state.user_profile,
#                         'response': response,
#                         'session_id': response.get('session_id'),
#                         'timestamp': datetime.now().isoformat()
#                     })
#                     # Save to user account
#                     save_user_session(st.session_state.username)
#                     st.success("✅ Nutrition plan generated successfully!")
#                     st.rerun()

# def display_workout_plan():
#     """Display the generated workout plan"""
#     if st.session_state.workout_plan:
#         st.markdown('<div class="section-header">🏋️ Your Workout Plan</div>', unsafe_allow_html=True)
        
#         # Display the response content
#         workout_data = st.session_state.workout_plan
        
#         if isinstance(workout_data, dict) and 'response' in workout_data:
#             st.markdown(workout_data['response'])
#         elif isinstance(workout_data, dict) and 'content' in workout_data:
#             st.markdown(workout_data['content'])
#         else:
#             st.markdown(str(workout_data))
        
#         # Download option
#         col1, col2 = st.columns([1, 4])
#         with col1:
#             download_content = workout_data.get('response', workout_data.get('content', str(workout_data)))
#             st.download_button(
#                 "📥 Download Plan",
#                 data=download_content,
#                 file_name=f"workout_plan_{datetime.now().strftime('%Y%m%d')}.txt",
#                 mime="text/plain"
#             )

# def display_nutrition_plan():
#     """Display the generated nutrition plan"""
#     if st.session_state.nutrition_plan:
#         st.markdown('<div class="section-header">🥗 Your Nutrition Plan</div>', unsafe_allow_html=True)
        
#         # Display the response content
#         nutrition_data = st.session_state.nutrition_plan
        
#         if isinstance(nutrition_data, dict) and 'response' in nutrition_data:
#             st.markdown(nutrition_data['response'])
#         elif isinstance(nutrition_data, dict) and 'content' in nutrition_data:
#             st.markdown(nutrition_data['content'])
#         else:
#             st.markdown(str(nutrition_data))
        
#         # Download option
#         col1, col2 = st.columns([1, 4])
#         with col1:
#             download_content = nutrition_data.get('response', nutrition_data.get('content', str(nutrition_data)))
#             st.download_button(
#                 "📥 Download Plan",
#                 data=download_content,
#                 file_name=f"nutrition_plan_{datetime.now().strftime('%Y%m%d')}.txt",
#                 mime="text/plain"
#             )

# def chat_interface():
#     """Chat interface for follow-up questions"""
#     st.markdown('<div class="section-header">💬 Chat with Your AI Coach</div>', unsafe_allow_html=True)
    
#     # Display chat history
#     for i, message in enumerate(st.session_state.chat_history):
#         if message['type'] in ['user_message', 'assistant_message']:
#             with st.chat_message(message['type'].replace('_message', '')):
#                 st.write(message['content'])
    
#     # Chat input
#     if prompt := st.chat_input("Ask questions about your workout or nutrition plan..."):
#         # Add user message to chat
#         st.session_state.chat_history.append({
#             'type': 'user_message',
#             'content': prompt,
#             'timestamp': datetime.now().isoformat()
#         })
        
#         with st.chat_message("user"):
#             st.write(prompt)
        
#         # Get response from backend
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 response = call_backend_service('chat', st.session_state.user_profile, prompt)
                
#                 if 'error' in response:
#                     assistant_response = f"I apologize, but I encountered an error: {response['error']}. Please try again."
#                 else:
#                     assistant_response = response.get('response', 'I apologize, but I couldn\'t process your request.')
                
#                 st.write(assistant_response)
                
#                 # Add assistant response to chat history
#                 st.session_state.chat_history.append({
#                     'type': 'assistant_message',
#                     'content': assistant_response,
#                     'session_id': response.get('session_id'),
#                     'timestamp': datetime.now().isoformat()
#                 })
                
#                 # Save to user account
#                 save_user_session(st.session_state.username)

# def sidebar_navigation():
#     """Sidebar navigation and settings"""
#     with st.sidebar:
#         st.markdown("### 🏃‍♀️ AI Fitness Coach")
        
#         # User info and logout
#         if st.session_state.authenticated:
#             user_name = st.session_state.username
#             # if users[user_name]['name']:
#             #     user_name = st.session_state.user_profile['name']
#             st.markdown(f"**👤 Welcome, {user_name}!**")
#             if st.button("🚪 Logout", type="secondary", use_container_width=True):
#                 # Save session before logout
#                 save_user_session(st.session_state.username)
                
#                 # Clear session
#                 st.session_state.authenticated = False
#                 st.session_state.username = ""
#                 st.session_state.user_profile = {}
#                 st.session_state.chat_history = []
#                 st.session_state.workout_plan = None
#                 st.session_state.nutrition_plan = None
#                 st.session_state.profile_submitted = False
#                 st.session_state.current_session_id = None
#                 st.rerun()
        
#         st.markdown("---")
        
#         # Navigation
#         page = st.radio(
#             "Navigation",
#             ["👤 Profile Setup", "📊 Dashboard", "💬 Chat Coach", "⚙️ Settings"]
#         )
                
#         # Quick stats if profile exists
#         if st.session_state.user_profile:
#             st.markdown("### 📈 Quick Stats")
#             profile = st.session_state.user_profile
#             # BMI calculation
#             height_m = profile['height'] / 100
#             bmi = profile['weight'] / (height_m ** 2)
            
#             if bmi < 18.5:
#                 bmi_status = "Underweight"
#                 bmi_color = "blue"
#             elif bmi < 25:
#                 bmi_status = "Normal"
#                 bmi_color = "green"
#             elif bmi < 30:
#                 bmi_status = "Overweight"
#                 bmi_color = "orange"
#             else:
#                 bmi_status = "Obese"
#                 bmi_color = "red"
                
#             st.markdown(f"**BMI:** <span style='color:{bmi_color}'>{bmi:.1f} ({bmi_status})</span>", unsafe_allow_html=True)
#             st.markdown(f"**Goal:** {profile['fitness_goal']}")
#             st.markdown(f"**Level:** {profile['fitness_level']}")
            
#             available_days = len([day for day, time in profile['schedule'].items() if time != "Not Available"])
#             st.markdown(f"**Available Days:** {available_days}/7")
            
#             # Show current session ID if available
#             if st.session_state.current_session_id:
#                 st.markdown(f"**Session:** {st.session_state.current_session_id}")

#         st.markdown("---")
#         st.markdown(
#             "<div style='text-align: left; color: #888; font-size: 1em; margin-top: 2rem;'>"
#             "Created by Sayon"
#             "</div>",
#             unsafe_allow_html=True
#         )        
#     return page

# def main():
#     """Main application function"""
#     init_session_state()
    
#     # Check authentication
#     if not st.session_state.authenticated:
#         login_page()
#         return
    
#     # Header
#     st.markdown('<div class="main-header">🏋️ AI Fitness Coach</div>', unsafe_allow_html=True)
#     st.markdown("*Your personalized fitness and nutrition companion powered by AI*")
#     st.markdown("---")
    
#     # Sidebar navigation
#     current_page = sidebar_navigation()
    
#     if current_page == "👤 Profile Setup":
#         user_profile = collect_user_profile()
        
#         st.markdown("---")
        
#         if st.button("💾 Save Profile & Continue", type="primary", use_container_width=True):
#             st.session_state.user_profile = user_profile
#             st.session_state.profile_submitted = True
#             # Save to user account
#             save_user_session(st.session_state.username)
#             st.success("✅ Profile saved successfully!")
#             st.balloons()
#             st.rerun()
    
#     elif current_page == "📊 Dashboard":
#         if not st.session_state.user_profile:
#             st.warning("⚠️ Please complete your profile setup first!")
#             if st.button("Go to Profile Setup"):
#                 st.rerun()
#         else:
#             display_profile_summary()
#             st.markdown("---")
#             generate_plans()
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 display_workout_plan()
#             with col2:
#                 display_nutrition_plan()
    
#     elif current_page == "💬 Chat Coach":
#         if not st.session_state.user_profile:
#             st.warning("⚠️ Please complete your profile setup first!")
#         else:
#             chat_interface()
    
#     elif current_page == "⚙️ Settings":
#         st.markdown('<div class="section-header">⚙️ Application Settings</div>', unsafe_allow_html=True)
        
#         # Account Information
#         st.subheader("👤 Account Information")
#         user_data = get_user_data(st.session_state.username)
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.info(f"**Username:** {st.session_state.username}")
#             st.info(f"**Account Created:** {user_data.get('created_at', 'Unknown')[:10]}")
#         with col2:
#             st.info(f"**Name:** {user_data.get('name', 'Not provided')}")
#             if user_data.get('last_updated'):
#                 st.info(f"**Last Updated:** {user_data.get('last_updated')[:10]}")
      
#         # Danger Zone
#         st.subheader("🚨 Danger Zone")
#         with st.expander("Delete Account"):
#             st.error("⚠️ **Warning**: This action cannot be undone!")
#             st.write("This will permanently delete your account and all associated data.")
            
#             confirm_delete = st.text_input("Type 'DELETE' to confirm account deletion:")
            
#             if st.button("🗑️ Delete Account", type="secondary") and confirm_delete == "DELETE":
#                 # Delete user from users.json
#                 users = load_users()
#                 if st.session_state.username in users:
#                     del users[st.session_state.username]
#                     save_users(users)
                
#                 # Clear session and logout
#                 st.session_state.authenticated = False
#                 st.session_state.username = ""
#                 st.session_state.user_profile = {}
#                 st.session_state.chat_history = []
#                 st.session_state.workout_plan = None
#                 st.session_state.nutrition_plan = None
#                 st.session_state.profile_submitted = False
#                 st.session_state.current_session_id = None
                
#                 st.success("Account deleted successfully. You will be redirected to the login page.")
#                 st.rerun()

# if __name__ == "__main__":
#     main()