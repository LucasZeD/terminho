'''
game brain

does not matter which messager app it uses
'''
import json
from sqlalchemy.orm import Session
from app.db.redis_client import redis_client
from app.services import game_logic, response_formatter
from app.crud import crud_game
from app.core.config import settings

word_list = game_logic.load_dictionary()

def process_user_turn(db: Session, user_id: str, text: str) -> str:
    """Processa uma única jogada de um usuário e retorna o texto da resposta."""
    session_key = f"wordle_session:{user_id}"
    session_json = redis_client.get(session_key)
    session = json.loads(session_json) if session_json else None

    # Se não há jogo ou o jogo anterior terminou, inicia um novo jogo
    if not session or session.get("status") in ["WON", "LOST"]:
        new_word = game_logic.get_random_word()
        session = {
            "secret_word": new_word,
            "guesses": [],
            "status": "IN_PROGRESS"
        }
        # redis_client.set(session_key, json.dumps(new_session), ex=settings.SESSION_TTL_SECONDS)
        # return response_formatter.get_initial_instructions()

    # Se um jogo está em andamento, processa a tentativa
    # Validações da tentativa
    if len(text) != 5:
        return "Por favor, envie uma palavra de 5 letras."
    if text not in word_list:
        return f"A palavra '{text}' não está no nosso dicionário. Tente outra."
    if any(g["word"] == text for g in session["guesses"]):
        return f"Você já tentou a palavra '{text}'.\n\n{response_formatter.format_current_game(session)}"

    # Processa a tentativa válida
    result = game_logic.check_guess(text, session["secret_word"])
    session["guesses"].append({"word": text, "result": result})

    # Checa condição de vitória/derrota
    if text == session["secret_word"]:
        session["status"] = "WON"
    elif len(session["guesses"]) == 6:
        session["status"] = "LOST"

    # Formata a resposta e gerencia o estado
    if session["status"] in ["WON", "LOST"]:
        reply_text = response_formatter.format_final_message(session)
        # Salva no DB e remove do Redis
        crud_game.save_finished_game(db=db, user_id=user_id, session_data=session)
        redis_client.delete(session_key)
    else: # Jogo continua
        reply_text = response_formatter.format_current_game(session)
        redis_client.set(session_key, json.dumps(session), ex=settings.SESSION_TTL_SECONDS)
    
    return reply_text