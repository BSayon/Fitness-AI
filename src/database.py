# # database.py
# import sqlite3
# import json
# from datetime import datetime
# from typing import Optional, Dict

# DB_PATH = "users.db"

# # Ensure DB and table are created on import
# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         session_alias TEXT PRIMARY KEY,
#         name TEXT,
#         created_at TEXT,
#         profile TEXT,
#         chat_history TEXT,
#         workout_plan TEXT,
#         nutrition_plan TEXT,
#         last_updated TEXT
#     )
#     """)
#     conn.commit()
#     conn.close()


# def save_user_data(session_alias: str, user_data: Dict):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute("""
#     INSERT INTO users (
#         session_alias, name, created_at, profile, chat_history,
#         workout_plan, nutrition_plan, last_updated
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     ON CONFLICT(session_alias) DO UPDATE SET
#         name=excluded.name,
#         profile=excluded.profile,
#         chat_history=excluded.chat_history,
#         workout_plan=excluded.workout_plan,
#         nutrition_plan=excluded.nutrition_plan,
#         last_updated=excluded.last_updated
#     """, (
#         session_alias,
#         user_data.get("name", ""),
#         user_data.get("created_at", datetime.now().isoformat()),
#         json.dumps(user_data.get("profile", {})),
#         json.dumps(user_data.get("chat_history", [])),
#         json.dumps(user_data.get("workout_plan", {})),
#         json.dumps(user_data.get("nutrition_plan", {})),
#         datetime.now().isoformat()
#     ))

#     conn.commit()
#     conn.close()


# def get_user_data(session_alias: str) -> Optional[Dict]:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE session_alias = ?", (session_alias,))
#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         return None

#     return {
#         "session_alias": row[0],
#         "name": row[1],
#         "created_at": row[2],
#         "profile": json.loads(row[3] or "{}"),
#         "chat_history": json.loads(row[4] or "[]"),
#         "workout_plan": json.loads(row[5] or "{}"),
#         "nutrition_plan": json.loads(row[6] or "{}"),
#         "last_updated": row[7]
#     }


# def create_user(session_alias: str, name: str):
#     # Only called when new user logs in
#     user_data = {
#         "name": name,
#         "created_at": datetime.now().isoformat(),
#         "profile": {},
#         "chat_history": [],
#         "workout_plan": {},
#         "nutrition_plan": {}
#     }
#     save_user_data(session_alias, user_data)


# # Always call on app start
# init_db()
