"""
Main FastAPI application entry point.
Backend API for Tavus Shopping Assistant Chrome Extension.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx

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


# Response model for conversation creation
class ConversationResponse(BaseModel):
    """Response for conversation creation"""
    success: bool
    conversation_url: Optional[str] = None
    message: str
    error: Optional[str] = None


# Endpoint to create Tavus conversation with page context
@app.post("/api/create-conversation", response_model=ConversationResponse)
async def create_conversation(page_context: PageContext):
    """
    Create a Tavus conversation with page context and product recommendations.
    
    Flow:
    1. Get product recommendations (stub from CSV)
    2. Format context with page info + recommendations
    3. Call Tavus API to create conversation
    4. Return conversation_url
    """
    try:
        from services.recommendation_engine import get_recommendations
        from services.tavus_client import create_tavus_conversation
        
        print(f"Creating conversation for: {page_context.merchant} - {page_context.url}")
        
        # Step 1: Get product recommendations (stub)
        recommendations_data = get_recommendations(
            merchant=page_context.merchant,
            clothing_type="graphic tees"  # Could be extracted from URL in future
        )
        products = recommendations_data.get("products", [])
        print(f"Found {len(products)} product recommendations")
        
        # Step 2 & 3: Create Tavus conversation with context
        page_context_dict = {
            "merchant": page_context.merchant,
            "url": page_context.url
        }
        
        rec_engine_summary = f"Based on browsing {page_context.merchant}, we've identified {len(products)} graphic tees that match your style preferences."
        
        conversation_url = await create_tavus_conversation(
            page_context=page_context_dict,
            products=products,
            rec_engine_summary=rec_engine_summary
        )
        
        print(f"✓ Conversation created: {conversation_url}")
        
        return {
            "success": True,
            "conversation_url": conversation_url,
            "message": "Conversation created successfully"
        }
        
    except ValueError as e:
        print(f"Error: {e}")
        return {
            "success": False,
            "message": "Configuration error",
            "error": str(e)
        }
    except httpx.HTTPError as e:
        print(f"Tavus API error: {e}")
        return {
            "success": False,
            "message": "Failed to create Tavus conversation",
            "error": f"API error: {str(e)}"
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
