# app/admin/router.py
import secrets
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.crud.crud_admin import get_dashboard_stats, get_recent_games # Adicionar get_recent_games
from app.services import game_logic # Precisamos da lógica de verificação de palavras
from app.core.config import settings
from app.db.database import get_db
from app.db.redis_client import get_active_games, get_recent_games
from app.crud.crud_admin import get_dashboard_stats

router = APIRouter()
security = HTTPBasic()

templates = Jinja2Templates(directory="app/admin/templates")

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.get("/dashboard", name="admin_dashboard")
async def get_admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    """
    Rota principal do painel admin.
    Busca, processa e exibe estatísticas e o histórico de jogos recentes.
    """
    stats = get_dashboard_stats(db)
    active_games = get_active_games()
    ecent_games_raw = get_recent_games(db)
    
    # Processa os jogos recentes para reconstruir os resultados
    recent_games_processed = []
    for game in recent_games_raw:
        guesses = game.guesses_list.split(',') # Transforma a string "PALAVRA,OUTRA" em uma lista
        
        # Recalcula o resultado para cada tentativa
        reconstructed_history = []
        for guess in guesses:
            result_emojis = game_logic.check_guess(guess, game.secret_word)
            reconstructed_history.append({"word": guess, "result": "".join(result_emojis)})
        
        # Adiciona o histórico reconstruído ao objeto do jogo
        game.reconstructed_history = reconstructed_history
        recent_games_processed.append(game)

    context = {
        "request": request,
        "stats": stats,
        "active_games": active_games,
        "recent_games": recent_games_processed, # Envia a lista processada
        "username": username
    }
    
    return templates.TemplateResponse("admin.html", context)