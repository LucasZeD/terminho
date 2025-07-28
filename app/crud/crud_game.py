import json
from sqlalchemy.orm import Session
from app.models.game_history import GameHistory

def _guesses_to_string(guesses: list[dict]) -> str:
    """
    Converte a lista de dicionários de tentativas em uma única string
    de palavras separadas por vírgula.
    """
    word_list = [attempt.get("word", "?????") for attempt in guesses]
    return ",".join(word_list)

def save_finished_game(db: Session, user_id: str, session_data: dict):
    guesses_string = _guesses_to_string(session_data["guesses"])
    history_entry = GameHistory(
        user_id=user_id,
        secret_word = session_data["secret_word"],
        was_successful = (session_data["status"] == "WON"),
        guess_count = len(session_data["guesses"]),
        # guesses_list = json.dumps(session_data["guesses"])
        guesses_list=guesses_string
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry