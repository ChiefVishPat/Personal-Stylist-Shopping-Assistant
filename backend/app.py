"""
Main FastAPI application entry point.
Backend API for Tavus Shopping Assistant Chrome Extension.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Tavus Shopping Assistant API",
    description="Backend API for Chrome extension",
    version="1.0.0"
)

# CORS middleware - allows Chrome extension to call this API
# For development, allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Request/Response models
class PageContext(BaseModel):
    """Page context from extension"""
    url: str
    merchant: str
    timestamp: str = None


# Simple health check
@app.get("/")
async def root():
    """Health check"""
    return {"status": "Backend is running!"}


# Endpoint to receive page context from extension
@app.post("/api/page-context")
async def receive_page_context(page_context: PageContext):
    """
    Receive page context from Chrome extension.
    This will be used to create Tavus conversations with context.
    """
    print(f"Received page context: {page_context.merchant} - {page_context.url}")
    
    # TODO: Use this context to create Tavus conversation
    # For now, just acknowledge receipt
    return {
        "success": True,
        "message": f"Received context from {page_context.merchant}",
        "merchant": page_context.merchant,
        "url": page_context.url
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
