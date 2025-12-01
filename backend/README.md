# Backend API

FastAPI backend for Tavus Shopping Assistant.

## Setup
```bash
uv sync
cp .env.example .env
# Add your Tavus API key to .env
uv run uvicorn app:app --reload --port 5000
```

## Endpoints
- `GET /` - Health check
- `POST /api/create-conversation` - Create Tavus conversation
