# app/admin/router.py
import secrets
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.db.redis_client import get_active_games
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
    stats = get_dashboard_stats(db)
    active_games = get_active_games()
    
    context = {
        "request": request,
        "stats": stats,
        "active_games": active_games,
        "username": username
    }
    
    return templates.TemplateResponse("admin.html", context)