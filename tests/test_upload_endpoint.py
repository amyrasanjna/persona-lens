from types import SimpleNamespace

import pytest

fastapi = pytest.importorskip("fastapi")

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.api import routes
from backend.core.config import settings


@pytest.fixture
def client(tmp_path, monkeypatch):
    settings.api_key = "test-key"
    settings.max_upload_files = 3
    settings.max_upload_size_mb = 1

    monkeypatch.setattr(routes, "enforce_rate_limit", lambda _request: None)

    class FakeTask:
        id = "job-123"

    monkeypatch.setattr(
        routes,
        "process_upload",
        SimpleNamespace(delay=lambda _payload: FakeTask()),
    )

    monkeypatch.setattr(routes, "Path", lambda p: tmp_path / p)

    app = FastAPI()
    app.include_router(routes.router)
    return TestClient(app)


def test_upload_accepts_image_and_returns_job(client):
    files = [("files", ("face.jpg", b"\xff\xd8\xff\xd9", "image/jpeg"))]
    response = client.post("/upload", files=files, headers={"x-api-key": "test-key"})

    assert response.status_code == 200
    assert response.json()["job_id"] == "job-123"
    assert response.json()["accepted"] == 1
