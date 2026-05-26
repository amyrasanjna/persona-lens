import pytest

pytest.importorskip("httpx")

from backend.services.inference import InferPayload, TextEmbedPayload


def test_infer_payload_validates():
    payload = InferPayload.model_validate(
        {
            "face_embedding": [0.1, 0.2],
            "semantic_embedding": [0.3, 0.4],
            "metadata": {"title": "t"},
        }
    )
    assert payload.metadata["title"] == "t"


def test_text_embed_payload_validates():
    payload = TextEmbedPayload.model_validate({"embedding": [0.1]})
    assert payload.embedding == [0.1]
