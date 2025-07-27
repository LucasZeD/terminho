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
SESSION_TTL_SECONDS = 57600 # 16h
# 86400 #24horas

# r = redis.Redis(
#     host='redis-11254.crce197.us-east-2-1.ec2.redns.redis-cloud.com',
#     port=11254,
#     decode_responses=True,
#     username="default",
#     password="*******",
# )

# success = r.set('foo', 'bar')
# # True

# result = r.get('foo')
# print(result)
# # >>> bar