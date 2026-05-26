import hmac

from fastapi import Header, HTTPException, status

from backend.core.config import settings


async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    provided = x_api_key or ""
    expected = settings.api_key
    if not hmac.compare_digest(provided, expected):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
