# Backend API

FastAPI backend that orchestrates the flow between the Chrome extension and Tavus API.

## Setup

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Add your Tavus API key and config to .env
# Required: TAVUS_API_KEY
# Optional: PERSONA_ID, REPLICA_ID, DOCUMENT_IDS, DOCUMENT_TAGS
```

## Running

```bash
uv run uvicorn app:app --reload --port 8000
```

Server runs on `http://localhost:8000`

## Endpoints

- `GET /` - Health check
- `POST /api/create-conversation` - Creates a Tavus conversation with page context and product recommendations

## Architecture

**Flow:**
1. Extension sends page context (URL, merchant) → `POST /api/create-conversation`
2. Backend calls `recommendation_engine.get_recommendations()` (stub from CSV)
3. Backend formats context with products as JSON
4. Backend calls `tavus_client.create_tavus_conversation()` with context
5. Returns `conversation_url` to extension

**Services:**
- `services/recommendation_engine.py` - Stub that loads from CSV (future: Parallel API)
- `services/tavus_client.py` - Handles Tavus API calls and context formatting
- `config/settings.py` - Environment variables and Tavus config

## Environment Variables

See `.env.example` for all required variables. Key ones:
- `TAVUS_API_KEY` - Your Tavus API key (required)
- `PERSONA_ID` - Tavus persona ID (default: `p78a4e6a3f3f`)
- `REPLICA_ID` - Tavus replica ID (default: `rf4703150052`)

## Stub Data

Currently uses `data/shopping_result.csv` for product recommendations. This is a placeholder for the future Parallel AI API integration. The CSV contains product data in JSON format that gets parsed and passed to Tavus.
