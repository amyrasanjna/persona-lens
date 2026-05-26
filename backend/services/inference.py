from typing import Any

import httpx
from pydantic import BaseModel, Field, ValidationError
import httpx

from backend.core.config import settings


class InferPayload(BaseModel):
    face_embedding: list[float] = Field(min_length=1)
    semantic_embedding: list[float] = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TextEmbedPayload(BaseModel):
    embedding: list[float] = Field(min_length=1)


async def run_inference(image_bytes: bytes) -> InferPayload:
async def run_inference(image_bytes: bytes) -> dict:
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{settings.hf_space_url}/infer",
            files={"file": ("image.jpg", image_bytes, "image/jpeg")},
        )
        response.raise_for_status()
        try:
            return InferPayload.model_validate(response.json())
        except ValidationError as exc:
            raise ValueError(f"Invalid HF inference payload: {exc}") from exc
        payload = response.json()
        for key in ["face_embedding", "semantic_embedding"]:
            if key not in payload:
                raise ValueError(f"HF payload missing required field: {key}")
        return payload


async def embed_text(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(f"{settings.hf_space_url}/embed-text", json={"text": text})
        response.raise_for_status()
        try:
            payload = TextEmbedPayload.model_validate(response.json())
        except ValidationError as exc:
            raise ValueError(f"Invalid HF text embedding payload: {exc}") from exc
        return payload.embedding
        payload = response.json()
        emb = payload.get("embedding")
        if not emb:
            raise ValueError("HF text embedding response missing `embedding`")
        return emb
