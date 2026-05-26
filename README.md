# Persona Lens (Production-Ready Baseline)

## Stack
- FastAPI API
- PostgreSQL (Supabase-compatible) via SQLAlchemy async
- Qdrant Cloud vectors
- Upstash Redis + Celery workers
- Hugging Face Space inference endpoints

## Security
All endpoints require `x-api-key` header.

## Run
```bash
cp .env.example .env
docker compose up --build
```

## API
- `POST /upload` enqueue upload job
- `GET /jobs/{job_id}` queue status/result
- `POST /recognize` HF infer + Qdrant face search
- `GET /search` HF text embed + Qdrant semantic search
- `GET /cluster/suggestions`
- `GET /health`

## Production checklist
- Set strong API key and rotate regularly
- Configure HTTPS ingress + WAF + rate limiting at gateway
- Attach managed Postgres/Qdrant/Redis
- Run multiple API and worker replicas
- Add Alembic migrations before schema changes
