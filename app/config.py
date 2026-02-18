from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VidGen"
    replicate_api_token: str | None = None
    default_provider: str = "mock"
    host: str = "0.0.0.0"
    port: int = 8000
    # Aliases can be overridden in env and mapped to any Replicate model slug.
    sora_model_slug: str = Field(default="minimax/video-01", alias="SORA_MODEL_SLUG")
    veo3_model_slug: str = Field(default="google/veo-3", alias="VEO3_MODEL_SLUG")
    kling_model_slug: str = Field(default="kwaivgi/kling-v1.6-pro", alias="KLING_MODEL_SLUG")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
