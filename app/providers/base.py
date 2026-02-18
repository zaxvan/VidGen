from abc import ABC, abstractmethod
from app.schemas import GenerateRequest


class VideoProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, req: GenerateRequest) -> str:
        """Return URL to generated video."""
