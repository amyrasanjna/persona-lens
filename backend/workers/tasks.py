import asyncio

import httpx
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.core.config import settings
from backend.services.identity_service import save_image_and_vectors, upsert_person
from backend.vector.qdrant_client import ensure_collections
from backend.workers.celery_app import celery_app


@celery_app.task(name="process_upload", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5})
def process_upload(payload: dict) -> dict:
    return asyncio.run(_process_upload_async(payload))


async def _process_upload_async(payload: dict) -> dict:
    ensure_collections()
    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    session_local = async_sessionmaker(engine, expire_on_commit=False)
    processed = []
    async with session_local() as session:
        for item in payload["files"]:
            with open(item["path"], "rb") as f:
                async with httpx.AsyncClient(timeout=180) as client:
                    resp = await client.post(f"{settings.hf_space_url}/infer", files={"file": f})
                resp.raise_for_status()
                data = resp.json()
            person = await upsert_person(session, item.get("name"))
            result = await save_image_and_vectors(
                session,
                path=item["path"],
                person=person,
                metadata=data.get("metadata", {}),
                face_vector=data["face_embedding"],
                semantic_vector=data["semantic_embedding"],
            )
            processed.append(result)
        await session.commit()
    await engine.dispose()
    return {"batch_id": payload["batch_id"], "processed": processed}
