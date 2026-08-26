import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "CartBaba"
    DEBUG = True

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DATA_AGENT_MODEL = os.getenv("DATA_AGENT_MODEL", "groq/gpt-oss-20b")
    INTENT_AGENT_MODEL = os.getenv("INTENT_AGENT_MODEL", "groq/gpt-oss-120b")
    FINAL_AGENT_MODEL = os.getenv("FINAL_AGENT_MODEL", "groq/gpt-oss-120b")
    REVIEW_AGENT_MODEL = os.getenv("REVIEW_AGENT_MODEL", "groq/gpt-oss-120b")
    TOOL_AGENT_MODEL = os.getenv("TOOL_AGENT_MODEL", "groq/gpt-oss-20b")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

settings = Settings()
