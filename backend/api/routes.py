from pathlib import Path
import uuid

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.rate_limit import enforce_rate_limit
from backend.core.security import require_api_key
from backend.database.session import get_db
from backend.models.entities import Person
from backend.schemas import RecognizeResponse, SearchResponse, UploadResponse
from backend.services.inference import embed_text, run_inference
from backend.vector.qdrant_client import client
from backend.workers.tasks import process_upload

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get("/health/live")
async def live() -> dict:
    return {"status": "live"}


@router.get("/health/ready")
async def ready(db: AsyncSession = Depends(get_db)) -> dict:
    await db.execute(text("SELECT 1"))
    return {"status": "ready"}


@router.post("/upload", response_model=UploadResponse)
async def upload(request: Request, files: list[UploadFile] = File(...), name: str | None = Form(default=None)) -> UploadResponse:
    enforce_rate_limit(request)
    if len(files) > settings.max_upload_files:
        raise HTTPException(status_code=400, detail="Too many files")
    batch_id = str(uuid.uuid4())
    storage = Path("storage/originals") / batch_id
    storage.mkdir(parents=True, exist_ok=True)
    saved = []
    for file in files:
        content = await file.read()
        if len(content) > settings.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File too large: {file.filename}")
        target = storage / (file.filename or f"{uuid.uuid4().hex}.jpg")
        target.write_bytes(content)
        saved.append({"path": str(target), "name": name})
    job = process_upload.delay({"batch_id": batch_id, "files": saved, "name": name})
    return UploadResponse(job_id=job.id, accepted=len(saved))


@router.get("/jobs/{job_id}")
async def job_status(request: Request, job_id: str) -> dict:
    enforce_rate_limit(request)
async def job_status(job_id: str) -> dict:
    result = AsyncResult(job_id)
    return {"job_id": job_id, "status": result.status, "result": result.result if result.ready() else None}


@router.post("/recognize", response_model=RecognizeResponse)
async def recognize(request: Request, db: AsyncSession = Depends(get_db), file: UploadFile = File(...), top_k: int = Form(default=5)) -> RecognizeResponse:
    enforce_rate_limit(request)
    data = await run_inference(await file.read())
    hits = client.search(collection_name=settings.face_collection, query_vector=data.face_embedding, limit=top_k)
async def recognize(db: AsyncSession = Depends(get_db), file: UploadFile = File(...), top_k: int = Form(default=5)) -> RecognizeResponse:
    data = await run_inference(await file.read())
    hits = client.search(collection_name=settings.face_collection, query_vector=data["face_embedding"], limit=top_k)
    matches = []
    for hit in hits:
        person_name = "unknown"
        person_id = (hit.payload or {}).get("person_id")
        if person_id:
            person = await db.scalar(select(Person).where(Person.id == person_id))
            if person and person.name:
                person_name = person.name
        matches.append({"person": person_name, "confidence": round(float(hit.score), 4)})
    return RecognizeResponse(matches=matches)


@router.get("/search", response_model=SearchResponse)
async def search(request: Request, q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)) -> SearchResponse:
    enforce_rate_limit(request)
async def search(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)) -> SearchResponse:
    vec = await embed_text(q)
    hits = client.search(collection_name=settings.semantic_collection, query_vector=vec, limit=limit)
    return SearchResponse(
        query=q,
        results=[{"image_id": (h.payload or {}).get("image_id"), "person_id": (h.payload or {}).get("person_id"), "score": round(float(h.score), 4)} for h in hits],
    )


@router.get("/cluster/suggestions")
async def cluster_suggestions(request: Request) -> dict:
    enforce_rate_limit(request)
async def cluster_suggestions() -> dict:
    return {"thresholds": {"auto_attach": settings.face_auto_attach_threshold, "suggest_merge": settings.face_suggest_merge_threshold}}
