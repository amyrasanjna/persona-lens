import time

from fastapi import HTTPException, Request, status
from redis import Redis

from backend.core.config import settings

redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


def enforce_rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    minute = int(time.time() // 60)
    key = f"rl:{ip}:{minute}"

    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, 61)

    if current > settings.rate_limit_per_minute:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
