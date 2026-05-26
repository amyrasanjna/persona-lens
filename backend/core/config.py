from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Persona Lens API"
    env: str = "dev"
    database_url: str
    qdrant_url: str
    qdrant_api_key: str
    redis_url: str
    hf_space_url: str
    api_key: str

    face_collection: str = "face_embeddings"
    semantic_collection: str = "semantic_embeddings"

    face_auto_attach_threshold: float = 0.80
    face_suggest_merge_threshold: float = 0.65

    max_upload_files: int = 10
    max_upload_size_mb: int = 20


settings = Settings()
