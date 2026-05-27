from types import SimpleNamespace

import pytest

fastapi = pytest.importorskip("fastapi")

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.api import routes
from backend.core.config import settings
from backend.database.session import get_db
from backend.services.inference import InferPayload


class FakeDB:
    async def scalar(self, _query):
        return SimpleNamespace(name="Alice")


@pytest.fixture
def client(monkeypatch):
    settings.api_key = "test-key"

    async def fake_inference(_image_bytes: bytes) -> InferPayload:
        return InferPayload(face_embedding=[0.1, 0.2], semantic_embedding=[0.3, 0.4], metadata={})

    monkeypatch.setattr(routes, "run_inference", fake_inference)
    monkeypatch.setattr(
        routes,
        "client",
        SimpleNamespace(search=lambda **_kwargs: [SimpleNamespace(score=0.91, payload={"person_id": 1})]),
    )
    monkeypatch.setattr(routes, "enforce_rate_limit", lambda _request: None)

    app = FastAPI()
    app.include_router(routes.router)

    async def override_get_db():
        yield FakeDB()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_recognize_with_image_upload(client):
    files = {"file": ("face.jpg", b"\xff\xd8\xff\xd9", "image/jpeg")}
    data = {"top_k": "3"}
    response = client.post("/recognize", files=files, data=data, headers={"x-api-key": "test-key"})

    assert response.status_code == 200
    assert response.json() == {"matches": [{"person": "Alice", "confidence": 0.91}]}
