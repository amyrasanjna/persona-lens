import uuid

from qdrant_client.http.models import PointStruct
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.models.entities import FaceEmbedding, Image, Person, SemanticEmbedding
from backend.vector.qdrant_client import client


async def upsert_person(session: AsyncSession, name: str | None) -> Person:
    if name:
        existing = await session.scalar(select(Person).where(Person.name == name))
        if existing:
            return existing
        person = Person(name=name, is_unknown=False)
    else:
        person = Person(name=f"unknown_{uuid.uuid4().hex[:8]}", is_unknown=True)
    session.add(person)
    await session.flush()
    return person


async def save_image_and_vectors(
    session: AsyncSession,
    *,
    path: str,
    person: Person,
    metadata: dict,
    face_vector: list[float],
    semantic_vector: list[float],
) -> dict:
    image = Image(
        person_id=person.id,
        path=path,
        title=metadata.get("title"),
        caption=metadata.get("caption"),
        alt_text=metadata.get("alt_text"),
        description=metadata.get("description"),
        metadata_json=metadata,
    )
    session.add(image)
    await session.flush()

    face_vector_id = uuid.uuid4().hex
    semantic_vector_id = uuid.uuid4().hex

    client.upsert(settings.face_collection, [PointStruct(id=face_vector_id, vector=face_vector, payload={"image_id": str(image.id), "person_id": str(person.id)})])
    client.upsert(settings.semantic_collection, [PointStruct(id=semantic_vector_id, vector=semantic_vector, payload={"image_id": str(image.id), "person_id": str(person.id)})])

    session.add(FaceEmbedding(image_id=image.id, person_id=person.id, vector_id=face_vector_id, confidence=None))
    session.add(SemanticEmbedding(image_id=image.id, vector_id=semantic_vector_id))

    await session.flush()
    return {"image_id": str(image.id), "identity": person.name or "unknown"}
