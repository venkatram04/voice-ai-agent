import redis
import json

from app.config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

SESSION_TTL = 1800

def get_session(session_id):

    data = redis_client.get(session_id)

    if data:
        return json.loads(data)

    return {}

def save_session(session_id, data):

    redis_client.setex(
        session_id,
        SESSION_TTL,
        json.dumps(data)
    )