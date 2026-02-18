import asyncio
from datetime import datetime, timezone
from uuid import uuid4
from app.providers.base import VideoProvider
from app.schemas import GenerateRequest, JobState


class GenerationService:
    def __init__(self, providers: dict[str, VideoProvider], default_provider: str):
        self.providers = providers
        self.default_provider = default_provider
        self.jobs: dict[str, JobState] = {}

    def _provider_for(self, req: GenerateRequest) -> VideoProvider:
        provider_name = (req.provider or self.default_provider).lower()
        if provider_name not in self.providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        return self.providers[provider_name]

    async def create(self, req: GenerateRequest) -> JobState:
        provider = self._provider_for(req)
        now = datetime.now(timezone.utc)
        job = JobState(
            id=str(uuid4()),
            prompt=req.prompt,
            provider=provider.name,
            model=req.model,
            status="queued",
            created_at=now,
            updated_at=now,
        )
        self.jobs[job.id] = job
        asyncio.create_task(self._run(job.id, provider, req))
        return job

    async def _run(self, job_id: str, provider: VideoProvider, req: GenerateRequest):
        job = self.jobs[job_id]
        job.status = "running"
        job.updated_at = datetime.now(timezone.utc)
        try:
            url = await provider.generate(req)
            job.status = "succeeded"
            job.output_url = url
        except Exception as exc:
            job.status = "failed"
            job.error = str(exc)
        finally:
            job.updated_at = datetime.now(timezone.utc)

    def get(self, job_id: str) -> JobState | None:
        return self.jobs.get(job_id)
