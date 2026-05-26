from pydantic import BaseModel


class UploadItem(BaseModel):
    image_id: str
    identity: str
    status: str
    confidence: float | None = None


class UploadResponse(BaseModel):
    job_id: str
    accepted: int


class RecognizeResponse(BaseModel):
    matches: list[dict]


class SearchResponse(BaseModel):
    query: str
    results: list[dict]
