from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.game_history import GameHistory

def get_dashboard_stats(db: Session) -> dict:
    total_games = db.query(func.count(GameHistory.id)).scalar()
    games_won = db.query(func.count(GameHistory.id)).filter(GameHistory.was_successful == True).scalar()
    
    win_rate = (games_won / total_games * 100) if total_games > 0 else 0
    
    avg_guesses = db.query(func.avg(GameHistory.guess_count)).filter(GameHistory.was_successful == True).scalar()

    return {
        "total_games": total_games or 0,
        "games_won": games_won or 0,
        "win_rate": round(win_rate, 2),
        "avg_guesses_on_win": round(avg_guesses, 2) if avg_guesses else 0
    }
    
def get_recent_games(db: Session, limit: int = 10) -> list[GameHistory]:
    """Busca os últimos jogos finalizados no banco de dados."""
    return db.query(GameHistory).order_by(GameHistory.finished_at.desc()).limit(limit).all()