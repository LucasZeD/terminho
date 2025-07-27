import json
from sqlalchemy.orm import Session
from app.models.game_history import GameHistory

def save_finished_game(db: Session, user_id: str, session_data: dict):
    history_entry = GameHistory(
        user_id=user_id,
        secret_word = session_data["secret_word"],
        was_sucessful = (session_data["status"] == "WON"),
        guess_count = len(session_data["guesses"]),
        guesses_list = json.dumps(session_data["guesses"])
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry