from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.providers.mock import MockProvider
from app.providers.replicate_provider import ReplicateProvider
from app.schemas import GenerateRequest
from app.service import GenerationService

settings = get_settings()
providers = {"mock": MockProvider()}

if settings.replicate_api_token:
    providers["replicate"] = ReplicateProvider(settings)

service = GenerationService(providers=providers, default_provider=settings.default_provider)

app = FastAPI(title=settings.app_name)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "app_name": settings.app_name,
            "providers": sorted(list(providers.keys())),
            "default_provider": settings.default_provider,
        },
    )


@app.post("/api/generate")
async def generate(req: GenerateRequest):
    try:
        return await service.create(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    job = service.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
