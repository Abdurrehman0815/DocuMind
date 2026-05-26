from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "AI Life Admin Agent"
    environment: str = "dev"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://appuser:appuser123@localhost:5432/ai_life_admin"
    cors_origins: str = "http://localhost:5173"
    jwt_secret_key: str = "change-me-in-env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    huggingface_token: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    
    # Twilio / WhatsApp Settings
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_whatsapp_number: Optional[str] = None
    user_whatsapp_number: Optional[str] = None
    supabase_url: str = ""
    supabase_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
