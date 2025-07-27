import httpx
from app.core.config import settings

META_GRAPH_API_URL = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
HEADERS = {
    "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
    "Content-Type": "application/json",
}

async def send_message(to: str, text: str):
    json_data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text},
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(META_GRAPH_API_URL, json=json_data, headers=HEADERS)
            response.raise_for_status()
            #add logging
        except httpx.HTTPStatusError as e:
            #add logging
            print(f"Erro ao enviar mensagem para a API do WhatsApp: {e.response.text}")