# You should also create config.py in the core directory:

# backend/app/core/config.py
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Tailor Tutor"
    DEBUG: bool = True
    API_V1_STR: str = "/api"
    PROJECT_ROOT: str = str(Path(__file__).parent.parent.parent)

settings = Settings()
