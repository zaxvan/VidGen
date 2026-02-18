# VidGen

VidGen is a deployable text-to-video generator with a clean web UI and API.

## Features
- Prompt-based video generation with async job tracking.
- Provider architecture:
  - `mock` provider for local testing with no API keys.
  - `replicate` provider for production-ready generation.
- Model aliases for popular families:
  - `sora`
  - `veo3`
  - `kling`
  - or pass any Replicate model slug directly.
- Dockerized deployment.

## Quick start (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
uvicorn app.main:app --reload
```
Open `http://localhost:8000`.

## Configure production generation
1. Set `REPLICATE_API_TOKEN` in `.env`.
2. Set `DEFAULT_PROVIDER=replicate`.
3. Optionally change alias slugs:
   - `SORA_MODEL_SLUG`
   - `VEO3_MODEL_SLUG`
   - `KLING_MODEL_SLUG`

## API
- `POST /api/generate`
- `GET /api/jobs/{job_id}`

Example request:
```json
{
  "prompt": "A cinematic shot of a red fox running in snow",
  "provider": "replicate",
  "model": "kling",
  "aspect_ratio": "16:9",
  "duration_seconds": 5
}
```

## Deploy with Docker
```bash
docker compose up --build
```
