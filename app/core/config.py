#pull secret data from .env file

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    WEBHOOK_URL: str
    TELEGRAM_BOT_TOKEN: str
    SESSION_TTL_SECONDS: int = 57600
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
     
    ENVIRONMENT: str = "production"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()