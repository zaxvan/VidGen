from datetime import datetime
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=2000)
    model: str = Field(default="kling")
    provider: str | None = None
    aspect_ratio: str = "16:9"
    duration_seconds: int = Field(default=5, ge=3, le=10)
    negative_prompt: str | None = None


class JobState(BaseModel):
    id: str
    prompt: str
    provider: str
    model: str
    status: str
    created_at: datetime
    updated_at: datetime
    output_url: str | None = None
    error: str | None = None
