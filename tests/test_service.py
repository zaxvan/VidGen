import asyncio
import pytest
from app.service import GenerationService
from app.providers.base import VideoProvider
from app.schemas import GenerateRequest


class OkProvider(VideoProvider):
    name = "ok"

    async def generate(self, req: GenerateRequest) -> str:
        return "https://example.com/video.mp4"


@pytest.mark.asyncio
async def test_job_completes_successfully():
    service = GenerationService({"ok": OkProvider()}, default_provider="ok")
    job = await service.create(GenerateRequest(prompt="test prompt", provider="ok", model="kling"))
    for _ in range(20):
        state = service.get(job.id)
        if state and state.status == "succeeded":
            break
        await asyncio.sleep(0.05)
    finished = service.get(job.id)
    assert finished is not None
    assert finished.output_url == "https://example.com/video.mp4"
