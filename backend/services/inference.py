import httpx

from backend.core.config import settings


async def run_inference(image_bytes: bytes) -> dict:
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{settings.hf_space_url}/infer",
            files={"file": ("image.jpg", image_bytes, "image/jpeg")},
        )
        response.raise_for_status()
        payload = response.json()
        for key in ["face_embedding", "semantic_embedding"]:
            if key not in payload:
                raise ValueError(f"HF payload missing required field: {key}")
        return payload


async def embed_text(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(f"{settings.hf_space_url}/embed-text", json={"text": text})
        response.raise_for_status()
        payload = response.json()
        emb = payload.get("embedding")
        if not emb:
            raise ValueError("HF text embedding response missing `embedding`")
        return emb
