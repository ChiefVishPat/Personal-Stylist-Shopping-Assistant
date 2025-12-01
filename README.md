# Tavus Personal Shopping Assistant

Chrome extension with Python backend providing AI-powered shopping stylist via Tavus CVI.

## Project Structure
- `extension/` - Chrome extension (frontend)
- `backend/` - FastAPI Python backend (API orchestration)

## Quick Start
1. Backend: `cd backend && uv sync && uv run uvicorn app:app --reload --port 5000`
2. Extension: Load unpacked from `chrome://extensions/`

## Tech Stack
- Extension: Chrome Manifest V3, Vanilla JS
- Backend: Python 3.11+, FastAPI, uv
- Integration: Tavus API (Persona: p78a4e6a3f3f, Replica: rf4703150052)
