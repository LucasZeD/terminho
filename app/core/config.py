#pull secret data from .env file

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SENTRY_DSN: str
    WHATSAPP_API_TOKEN: str
    WHATSAPP_PHONE_NUMBER_ID: str
    VERIFY_TOKEN: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()