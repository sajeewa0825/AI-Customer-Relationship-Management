import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.3))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 512))
    EMAIL_HOST: str = os.getenv("EMAIL_HOST")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS") 
    TEXT_FILTER_MODEL: str = os.getenv("TEXT_FILTER_MODEL")
    Top_K_Context: int = int(os.getenv("Top_K_Context", 1))
    CHAT_HISTORY_LIMIT: int = int(os.getenv("CHAT_HISTORY_LIMIT", 10))


settings = Settings()
