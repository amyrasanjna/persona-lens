import os

import pytest

fastapi = pytest.importorskip("fastapi")

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://u:p@localhost:5432/db")
os.environ.setdefault("QDRANT_URL", "http://localhost:6333")
os.environ.setdefault("QDRANT_API_KEY", "k")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("HF_SPACE_URL", "http://localhost:7860")
os.environ.setdefault("API_KEY", "test-key")

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from backend.core.config import settings
from backend.core.security import require_api_key

app = FastAPI()


@app.get("/private", dependencies=[Depends(require_api_key)])
async def private():
    return {"ok": True}


@app.get("/denied", dependencies=[Depends(require_api_key)])
async def denied():
    return {"ok": False}


client = TestClient(app)
settings.api_key = "test-key"


def test_allow_key():
    r = client.get("/private", headers={"x-api-key": "test-key"})
    assert r.status_code == 200


def test_reject_key():
    r = client.get("/denied", headers={"x-api-key": "bad"})
    assert r.status_code == 401
