import logging
import asyncio
from fastapi import FastAPI
from app.core.config import settings
from app.api import webhook
from app.db.database import engine
from app.models.game_history import Base
from app.menssager_client.telegram_client import set_webhook
from app.admin.router import router as admin_router

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

app.include_router(webhook.router, prefix="/api/v1", tags=["Telegram"])

app.include_router(admin_router, prefix="/admin", tags=["Admin"])