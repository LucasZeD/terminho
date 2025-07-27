import httpx
import logging
from app.core.config import settings

TELEGRAM_API_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"

async def send_message(user_id: str, text: str):
    """Envia mensagem de texto para o usuario no telegram"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{TELEGRAM_API_URL}/sendMessage",
                params={"chat_id": user_id, "text": text, "parse_mode": "Markdown"}
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logging.error(f"Erro ao enviar mensagem para o Telegram: {e.response.text}")

async def set_webhook():
    """Define a URL do webhook no Telegram"""
    WEBHOOK_URL = settings.WEBHOOK_URL
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TELEGRAM_API_URL}/setWebhook", params={"url": WEBHOOK_URL})
        logging.info(f"Resultado da configuração do Webhook: {response.json()}")