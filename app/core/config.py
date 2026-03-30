from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "LangGraph Chat API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = "HS256"
    OPENAI_API_KEY: str = Field(default="sk-dummy")
    GEMINI_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = Settings()
