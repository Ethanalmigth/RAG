from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL:str
    POSTGRES_DB:str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    QDRANT_URL:str
    GEMINI_API_KEY:str
    GEMINI_MODEL:str

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()