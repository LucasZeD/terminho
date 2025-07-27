'''
Redis com TTL
Objetivo principal: Custo zero para geranciamento de sessões
Espaço disponível plano gratuito: 30MB

TTL:
Sessões com 24horas de tempo de vida.
'''
import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)