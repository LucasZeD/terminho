'''
Redis com TTL
Objetivo principal: Custo zero para geranciamento de sessões
Espaço disponível plano gratuito: 30MB

TTL:
Sessões com 24horas de tempo de vida.
'''
import redis
from app.core.config import settings
import json

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_active_games() -> list[dict]:
    active_games = []
    # Usar scan_iter para não bloquear o Redis em caso de muitas chaves
    for key in redis_client.scan_iter("wordle_session:*"):
        try:
            session_json = redis_client.get(key)
            session_data = json.loads(session_json)
            user_id = key.split(":")[1]
            active_games.append({
                "user_id": user_id,
                "secret_word": session_data.get("secret_word", "N/A"),
                "guess_count": len(session_data.get("guesses", [])),
            })
        except Exception:
            # Ignora chaves malformadas ou expiradas durante a leitura
            continue
    return active_games