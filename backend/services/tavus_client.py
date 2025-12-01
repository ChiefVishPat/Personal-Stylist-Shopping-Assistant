"""
Tavus API client.
Handles conversation creation with JSON context and product recommendations.
"""

import json
import os
from typing import Any, Dict, List

import httpx

from config.settings import TAVUS_CONFIG


def format_conversational_context(
    website_name: str,
    page_url: str,
    user_prefs: str,
    rec_engine_summary: str,
    recommended_items_json: str,
    products_summary: str = ""
) -> str:
    """
    Format the conversational context string for Tavus.
    
    Args:
        website_name: Name of the website/merchant
        page_url: Current page URL
        user_prefs: User's style preferences (from persona)
        rec_engine_summary: Summary from recommendation engine
        recommended_items_json: JSON string of recommended items
    
    Returns:
        Formatted conversational context string
    """
    context = f"""The user launched the stylist assistant through their Chrome extension while browsing {website_name}. The current page URL is {page_url}.

Use the user's known style preferences: {user_prefs}.

The recommendation engine has already run in the background and identified some top pieces that match the user's style, based on the site they're browsing. Here are the insights from the engine:

{rec_engine_summary}

=== PRODUCT RECOMMENDATIONS ===
You have access to specific product recommendations below. You must use these products when discussing recommendations.

{products_summary}

Full product details (JSON format):
{recommended_items_json}

=== CRITICAL INSTRUCTIONS ===
- When the user asks "what recommendations do you have" or "tell me the XYZ", you MUST list the specific product names from above
- Use the product names, prices, ratings, sizes, and colors from the JSON data
- Reference products by their full names in a natural language way (e.g., "Anime Chainsaw Man UT Graphic T-Shirt | Reze Arc" for $24.90 --> "Chainsaw Man UT Graphic T-Shirt for $24.90")
- Mention specific prices (e.g., "$24.90", "$9.90", "$3.90")
- Share ratings when relevant (e.g., "5 out of 5 stars with 8 reviews")
- List available sizes and colors from the JSON
- Do NOT say you can't access the recommendations - you have them above
- Do NOT be vague or generic - be specific about the products listed

When the user asks about recommendations, immediately reference the specific products from the list above with their exact names, prices, and details."""
    
    return context


async def create_tavus_conversation(
    page_context: Dict[str, str],
    products: List[Dict[str, Any]],
    rec_engine_summary: str = "Based on the current browsing context, we've identified several sweatshirts and hoodies that match your style preferences."
) -> str:
    """
    Create a Tavus conversation with formatted context.
    
    Args:
        page_context: Dictionary with 'merchant' and 'url'
        products: List of product recommendations
        rec_engine_summary: Summary from recommendation engine
    
    Returns:
        conversation_url from Tavus API
    
    Raises:
        httpx.HTTPError: If API call fails
        ValueError: If API key is missing
    """
    api_key = os.getenv("TAVUS_API_KEY")
    if not api_key:
        raise ValueError("TAVUS_API_KEY not found in environment variables")
    
    # Convert products to JSON string
    recommended_items_json = json.dumps(products, indent=2) if products else "[]"
    
    # Create a quick reference summary for easier parsing
    products_summary = ""
    if products:
        products_summary = "\n\nQuick Reference - Product Names:\n"
        for i, product in enumerate(products, 1):
            name = product.get('product_name', 'Unknown')
            price = product.get('price', 'N/A')
            products_summary += f"{i}. {name} - {price}\n"
    
    # Format conversational context
    # Note: user_prefs are in the persona, so we reference them generically
    conversational_context = format_conversational_context(
        website_name=page_context.get('merchant', 'this site'),
        page_url=page_context.get('url', ''),
        user_prefs="Your style preferences are already configured in your persona profile.",
        rec_engine_summary=rec_engine_summary,
        recommended_items_json=recommended_items_json,
        products_summary=products_summary
    )
    
    # Format custom greeting
    website_name = page_context.get('merchant', 'this site')
    custom_greeting = f"Hi there, I'm Michael. I see you're browsing {website_name}. Want me to help you find pieces that match your style?"
    
    # Prepare request data
    data = {
        "replica_id": TAVUS_CONFIG["REPLICA_ID"],
        "conversation_name": "Personal Stylist | Shopping Assistant",
        "persona_id": TAVUS_CONFIG["PERSONA_ID"],
        "custom_greeting": custom_greeting,
        "conversational_context": conversational_context,
        "document_ids": TAVUS_CONFIG.get("DOCUMENT_IDS", []),
        "document_tags": TAVUS_CONFIG.get("DOCUMENT_TAGS", []),
        "properties": {
            "max_call_duration": 180,
            "participant_left_timeout": 0,
            "language": "english",
            "participant_absent_timeout": 30
        }
    }
    
    # Make API call
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TAVUS_CONFIG["API_ENDPOINT"],
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key
            },
            json=data,
            timeout=TAVUS_CONFIG["TIMEOUT_MS"] / 1000
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract conversation_url from response
        conversation_url = result.get("conversation_url")
        if not conversation_url:
            raise ValueError("No conversation_url in Tavus API response")
        
        return conversation_url
