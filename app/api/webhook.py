import json
import logging
from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import response_formatter, game_service
from app.menssager_client import telegram_client


router = APIRouter()

@router.post("/webhook")
async def handle_telegram_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    data = await request.json()
    
    try:
        # Extrai dados relevantes do payload do Telegram
        if "message" not in data or "text" not in data["message"]:
            return {"status": "ok"} # Ignora atualizações sem mensagem de texto

        user_id = str(data["message"]["from"]["id"])
        text = data["message"]["text"].strip().upper()
        
        logging.info(f"Mensagem '{text}' recebida do usuário {user_id}")

        # Se for um comando /start, envia as instruções
        if text == "/START":
            reply_text = response_formatter.get_initial_instructions()
        else:
            # Caso contrário, processa o turno do jogo
            reply_text = game_service.process_user_turn(db=db, user_id=user_id, text=text)

        # Envia a resposta em background para não bloquear o webhook
        background_tasks.add_task(telegram_client.send_message, user_id=user_id, text=reply_text)

    except Exception as e:
        logging.error(f"Erro ao processar webhook do Telegram: {e}", exc_info=True)
        # Notifica o usuário que algo deu errado
        error_message = "Desculpe, ocorreu um erro inesperado. Tente novamente mais tarde."
        background_tasks.add_task(telegram_client.send_message, user_id=user_id, text=error_message)
    
    return {"status": "ok"}