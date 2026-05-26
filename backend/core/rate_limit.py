import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

from backend.core.config import settings

_BUCKETS: dict[str, deque[float]] = defaultdict(deque)


def enforce_rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = 60
    dq = _BUCKETS[ip]
    while dq and now - dq[0] > window:
        dq.popleft()
    if len(dq) >= settings.rate_limit_per_minute:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
    dq.append(now)
