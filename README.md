# Tavus Personal Shopping Assistant

A Chrome extension that brings an AI-powered shopping stylist right into your browser. Browse any retail site, click the extension, and get personalized product recommendations through a natural video conversation with your stylist agent.

## What This Does

You're browsing Uniqlo (or any store), see something you like, and want a second opinion. Instead of scrolling through reviews or guessing sizes, you open the extension and chat with your personal stylist. The agent knows your style preferences, budget, and what you're looking at - and gives you real recommendations based on products that actually match your vibe.

Right now it's set up for sweatshirts & hoodies from Uniqlo, but the architecture is built to work with any site and product category.

## Loom
<div style="position: relative; padding-bottom: 64.63195691202873%; height: 0;"><iframe src="https://www.loom.com/embed/a4a1e7a244d34738a4febd70b7ec47f3" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Architecture

**Extension (Frontend)**
- Chrome Manifest V3 extension
- Content script injects a draggable widget on any page
- Popup triggers the conversation flow
- Communicates with Python backend via REST API

**Backend (Python/FastAPI)**
- Receives page context (URL, merchant) from extension
- Calls a recommendation engine (currently stubbed with CSV data)
- Formats product recommendations as JSON
- Creates a Tavus conversation with all this context
- Returns the conversation URL to embed in the widget

**Tavus Integration**
- Uses Tavus Conversational Video Interface (CVI)
- Persona is pre-configured with your style preferences
- Product recommendations are passed as `conversational_context`
- Guardrails ensure natural, conversational responses (no JSON reading)

## Tech Stack

- **Extension**: Chrome Manifest V3, Vanilla JavaScript
- **Backend**: Python 3.12+, FastAPI, `uv` for package management
- **Tavus API**: Persona `p78a4e6a3f3f`, Replica `rf4703150052`
- **Future**: Parallel AI API for real-time product recommendations (currently stubbed)

## Quick Start

### Backend Setup

```bash
cd backend
uv sync
cp .env.example .env
# Add your TAVUS_API_KEY to .env
uv run uvicorn app:app --reload --port 8000
```

### Extension Setup

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the `extension/` folder
5. Pin the extension to your toolbar

### Using It

1. Navigate to any retail site (e.g., Uniqlo)
2. Click the extension icon
3. Click "Start Conversation"
4. The widget appears in the top-right corner
5. Chat with your stylist about product recommendations

## Project Structure

```
tavus_project/
├── extension/          # Chrome extension
│   ├── popup/         # Extension popup UI
│   ├── content/       # Content scripts (widget injection)
│   ├── background/    # Service worker
│   └── manifest.json  # Extension config
├── backend/           # Python FastAPI server
│   ├── app.py        # Main API endpoints
│   ├── services/     # Business logic (Tavus client, recommendation engine)
│   ├── config/       # Settings and env vars
│   └── data/         # Stub data (CSV with product recommendations)
└── README.md         # This file
```

## How It Works

1. **User opens extension** → Popup extracts current page URL and merchant name
2. **Backend receives context** → Calls recommendation engine (stub loads from CSV)
3. **Recommendations formatted** → Products converted to JSON, added to conversational context
4. **Tavus conversation created** → API call with page context + product recommendations
5. **Widget displays** → Iframe embeds the Tavus conversation URL
6. **User chats** → Agent uses the JSON context to give specific product recommendations naturally

## Future Enhancements

If I had more time, here's what I'd add:

**Core Functionality:**
- **Real-time recommendations** - Replace CSV stub with Parallel AI API for live product data. Latency is high so waiting is unreliable. Stubbed for demo.
- **Smart URL parsing** - Automatically detect clothing type/category from page URL (e.g., extract "graphic tees" from `/men/tops/ut-graphic-tees`)
- **Gender detection** - Extract gender filter from URL or user profile or perception instead of hardcoding
- **Perception Model** - use perception model to get visual context of user via webcam or from screen sharing and seeing what the user is looking at to pass into recommendation engine.

**User Experience:**
- **Clickable product links** - Make recommendations clickable with direct product URLs
- **Save favorites** - Let users bookmark products they're interested in
- **Conversation history** - Show past conversations and recommendations
- **User profile management** - Allow users to update style preferences, budget, sizes directly in extension

**Technical Improvements:**
- **Caching layer** - Cache recommendations per page/merchant to reduce API calls
- **Better error handling** - Retry logic, graceful degradation, better user feedback
- **Background sync** - Pre-fetch recommendations when extension detects retail sites
- **Analytics** - Track which recommendations users engage with to improve suggestions

## Notes

- The recommendation engine is currently a stub that loads from `backend/data/shopping_result.csv`
- Product category is hardcoded to "sweatshirts & hoodies" for the demo
- Each extension open creates a new Tavus conversation (no reuse yet)
- Guardrails are configured to prevent the agent from reading JSON verbatim
