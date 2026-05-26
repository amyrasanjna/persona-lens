from fastapi import FastAPI

from backend.api.routes import router
from backend.core.logging import setup_logging
from backend.database.session import engine
from backend.models.base import Base
from backend.vector.qdrant_client import ensure_collections

setup_logging()
app = FastAPI(title="Persona Lens API", version="1.1.0")
app.include_router(router)


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    ensure_collections()
