from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Single repo-root .env is the source of truth; src/.env is an optional fallback.
_HERE = os.path.dirname(__file__)
load_dotenv(os.path.join(_HERE, "..", "..", ".env"))  # repo-root .env
load_dotenv(os.path.join(_HERE, "..", ".env"))  # src/.env (optional fallback)

groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.5,
    max_tokens=1000,
    api_key=groq_api_key
)



