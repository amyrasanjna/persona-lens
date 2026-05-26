import pytest

fastapi = pytest.importorskip("fastapi")

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.core.config import settings
from backend.core.security import require_api_key

app = FastAPI()


@app.get("/private", dependencies=[])
async def private(_: None = None):
    await require_api_key(settings.api_key)
    return {"ok": True}


@app.get("/denied")
async def denied(_: None = None):
    await require_api_key("bad-key")
    return {"ok": False}


client = TestClient(app)


def test_allow_key():
    r = client.get("/private")
    assert r.status_code == 200


def test_reject_key():
    r = client.get("/denied")
    assert r.status_code == 401
