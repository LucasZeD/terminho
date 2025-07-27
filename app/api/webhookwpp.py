import json
import logging
from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks
from structure2.app.client import whatsapp_client
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db
from app.db.redis_client import redis_client, SESSION_TTL_SECONDS
from app.services import game_logic, response_formatter
from app.crud import crud_game

router = APIRouter()
word_list = game_logic.load_dictionary()

@router.get("/webhook")
async def verify_webhook(request: Request):
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get("hub.verify_token") == settings.VERIFY_TOKEN:
        return int(request.query_params.get("hub.challenge"))
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@router.post("/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    data = await request.json()
    
    try:
        if "message" not in data["entry"][0]["changes"][0]["value"]:
            return {"status": "ok"}
        message_data = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_id = message_data["from"]
        text = message_data["text"]["body"].strip().upper()
        logging.info(f"Mensagem recebida do usuário {user_id}")
    except Exception as e:
        logging.error(f"Erro inesperado ao processar a mensagem do usuário {user_id}: {e}", exc_info=True)
        return {"status": "ok"}

    session_key = f"wordle_session: {user_id}"
    session_json = redis_client.get(session_key)
    session = json.loads(session_json) if session_json else None

    # Fluxo principal do jogo
    if not session or session["status"] in ["WON", "LOST"]:
        # iniciar novo game
        new_word = game_logic.get_random_word()
        new_session = {
            "secret_word": new_word,
            "guesses": [],
            "status": "GOING"
        }
        redis_client.set(session_key, json.dumps(new_session), ex=SESSION_TTL_SECONDS)
        reply_text = response_formatter.get_initial_instructions()
                
    else: # jogo em andamento
        #validar tentativa
        if len(text) != 5:
            reply_text = "Por favor, envie uma palavra de 5 letras."
        elif text not in word_list:
            reply_text = f"A palavra '{text}' não está no dicionário. Tente outra."
        elif any(g["word"] == text for g in session["guesses"]):
            reply_text = f"Você já tentou a palavra '{text}'.\n\n{response_formatter.format_current_game(session)}"
        #palavra valida
        else:
            result = game_logic.check_guess(text, session["secret_word"])
            session["guesses"].append({"word":text, "result":result})
            # checar se palavra correta
            if text == session["secret_word"]:
                session["status"] = "WON"
            elif len(session["guesses"]) == 6:
                session["status"] = "LOST"
            # formatar resposta
            if session["status"] in ["WON", "LOST"]:
                reply_text = response_formatter.format_final_message(session)
                # save on db for history
                background_tasks.add_task(crud_game.save_finished_game, db=db, user_id=user_id, session_data=session)
                # remove from redis after end of the game
                redis_client.delete(session_key)
            else:
                reply_text = response_formatter.format_current_game(session)
                redis_client.set(session_key, json.dumps(session), ex=SESSION_TTL_SECONDS)
    background_tasks.add_task(whatsapp_client.send_message, to=user_id, text=reply_text)
    return {"status": "ok"}