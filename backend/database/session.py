from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import ssl
from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode

from backend.core.config import settings


def _create_engine_from_url(db_url: str):
    parts = urlsplit(db_url)
    qs = parse_qs(parts.query, keep_blank_values=True)

    # Determine if SSL is requested via query params and remove them from the URL
    ssl_ctx = None
    ssl_requested = False
    if "sslmode" in qs:
        mode = qs.get("sslmode", [None])[0]
        if mode and mode.lower() != "disable":
            ssl_requested = True
        qs.pop("sslmode", None)

    if "ssl" in qs:
        val = qs.get("ssl", [None])[0]
        if val and str(val).lower() in ("1", "true", "yes"):
            ssl_requested = True
        qs.pop("ssl", None)

    # Rebuild a clean URL without ssl/sslmode query params
    new_query = urlencode(qs, doseq=True)
    clean_url = urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, parts.fragment))

    if ssl_requested:
        ssl_ctx = ssl.create_default_context()

    connect_args = {}
    if ssl_ctx is not None:
        connect_args["ssl"] = ssl_ctx

    return create_async_engine(clean_url, pool_pre_ping=True, connect_args=connect_args)


engine = _create_engine_from_url(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
