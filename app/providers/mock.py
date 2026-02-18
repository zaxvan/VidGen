import asyncio
from app.providers.base import VideoProvider
from app.schemas import GenerateRequest


class MockProvider(VideoProvider):
    name = "mock"

    async def generate(self, req: GenerateRequest) -> str:
        await asyncio.sleep(2)
        # Public domain sample mp4 useful in local/dev deployments.
        return "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
