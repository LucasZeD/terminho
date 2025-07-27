import logging
import asyncio
from fastapi import FastAPI
from app.core.config import settings
from app.api import webhook
from app.services.telegram_client import set_webhook

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Terminho Bot para Telegram",
    description = "Um bot de telegram para jogar termo",
    version = "1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await set_webhook()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Wordle Bot is running!"}

app.include_router(webhook.router, prefix="/api/v1", tags=["Telegram"])