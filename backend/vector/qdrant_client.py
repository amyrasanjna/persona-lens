from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from backend.core.config import settings

client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)


def ensure_collections() -> None:
    for name, size in [(settings.face_collection, 512), (settings.semantic_collection, 512)]:
        if not client.collection_exists(name):
            client.create_collection(name, vectors_config=VectorParams(size=size, distance=Distance.COSINE))
