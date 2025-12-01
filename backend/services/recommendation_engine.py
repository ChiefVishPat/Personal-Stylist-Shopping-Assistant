"""
Product recommendation engine.
Stub implementation that loads recommendations from CSV file.
Future: Replace with actual Parallel API call.
"""

import csv
import json
from pathlib import Path
from typing import Dict, Any


def get_recommendations(merchant: str, clothing_type: str = "graphic tees") -> Dict[str, Any]:
    """
    Get product recommendations (stub - loads from CSV).
    
    Args:
        merchant: The merchant/brand name (e.g., "Uniqlo")
        clothing_type: Type of clothing (e.g., "graphic tees")
    
    Returns:
        Dictionary with 'products' key containing list of product dicts
        Format matches Parallel API enrich response structure
    """
    # Load CSV file
    csv_path = Path(__file__).parent.parent / "data" / "shopping_result.csv"
    
    if not csv_path.exists():
        # Return empty recommendations if file doesn't exist
        return {"products": []}
    
    # Read CSV and extract products from the pro-fast processor row (row 3, index 2)
    # This has more detailed product information
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Use the pro-fast processor row (second data row, index 1)
        if len(rows) >= 2:
            products_json_str = rows[1].get('output.products', '[]')
        elif len(rows) >= 1:
            products_json_str = rows[0].get('output.products', '[]')
        else:
            return {"products": []}
    
    # Parse the JSON string from CSV
    try:
        products = json.loads(products_json_str)
        
        # Clean up product data - ensure all fields are present
        cleaned_products = []
        for product in products:
            cleaned_product = {
                "product_name": product.get("product_name", "Unknown Product"),
                "price": product.get("price", "N/A"),
                "ratings": product.get("ratings", "N/A"),
                "sizes": product.get("sizes", "N/A"),
                "colors": product.get("colors", "N/A") if product.get("colors") != "null" else "Various colors available"
            }
            cleaned_products.append(cleaned_product)
        
        return {"products": cleaned_products}
        
    except json.JSONDecodeError as e:
        print(f"Error parsing products JSON: {e}")
        return {"products": []}
