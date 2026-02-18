import asyncio
from typing import Any
import replicate
from app.config import Settings
from app.providers.base import VideoProvider
from app.schemas import GenerateRequest


MODEL_ALIASES = {
    "sora": "sora_model_slug",
    "veo3": "veo3_model_slug",
    "kling": "kling_model_slug",
}


class ReplicateProvider(VideoProvider):
    name = "replicate"

    def __init__(self, settings: Settings):
        if not settings.replicate_api_token:
            raise RuntimeError("REPLICATE_API_TOKEN is not configured")
        self.client = replicate.Client(api_token=settings.replicate_api_token)
        self.settings = settings

    def _resolve_model(self, model: str) -> str:
        attr = MODEL_ALIASES.get(model.lower())
        if attr:
            return getattr(self.settings, attr)
        return model

    async def generate(self, req: GenerateRequest) -> str:
        model_ref = self._resolve_model(req.model)
        payload: dict[str, Any] = {
            "prompt": req.prompt,
            "duration": req.duration_seconds,
            "aspect_ratio": req.aspect_ratio,
        }
        if req.negative_prompt:
            payload["negative_prompt"] = req.negative_prompt

        output = await asyncio.to_thread(self.client.run, model_ref, input=payload)

        if isinstance(output, str):
            return output
        if isinstance(output, list) and output:
            return str(output[0])
        raise RuntimeError("Replicate returned no output URL")
