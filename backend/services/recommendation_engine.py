"""
Product recommendation engine.
Stub implementation that loads recommendations from CSV file.
Future: Replace with actual Parallel API call (see commented code below).
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict

# Future: Uncomment when using Parallel API
# from typing import List

# Future: Uncomment and use this when ready to call Parallel API
# from pydantic import BaseModel, Field
# from parallel import Parallel
# from parallel.types import TaskSpecParam
#
#
# def build_task_spec_param(
#     input_schema: type[BaseModel], output_schema: type[BaseModel]
# ) -> TaskSpecParam:
#     """Build a TaskSpecParam from an input and output schema."""
#     return {
#         "input_schema": {
#             "type": "json",
#             "json_schema": input_schema.model_json_schema(),
#         },
#         "output_schema": {
#             "type": "json",
#             "json_schema": output_schema.model_json_schema(),
#         },
#     }
#
#
# class InputModel(BaseModel):
#     n_recommendations: int = Field(
#         description="The number of product recommendations to return (default is 10)."
#     )
#     page_url: str = Field(
#         description="The specific URL of the page to scrape for products (optional)."
#     )
#     gender: str = Field(
#         description="The gender filter for products (e.g., 'men', 'women', 'unisex')."
#     )
#     merchant_site: str = Field(
#         description="The merchant site (e.g., Uniqlo) to search for products."
#     )
#     category: str = Field(
#         description="The product category to search within (default is 'sale/clearance')."
#     )
#
#
# class Products(BaseModel):
#     reviews: str = Field(
#         description="The total number of customer reviews for the product, represented as a string (e.g., \"125 reviews\"). If unavailable, return null."
#     )
#     product_url: str = Field(
#         description="The direct URL to the product page on the merchant site. If unavailable, return null."
#     )
#     product_name: str = Field(
#         description="The full name of the product as displayed on the merchant site. If unavailable, return null."
#     )
#     price: str = Field(
#         description="The current selling price of the product, including currency symbol (e.g., \"$19.90\"). If a sale price is available, provide the sale price. If unavailable, return null."
#     )
#     colors: str = Field(
#         description="A comma-separated list of available colors for the product (e.g., \"Black, White, Navy, Red\"). If unavailable, return null."
#     )
#     sizes: str = Field(
#         description="A comma-separated list of available sizes for the product (e.g., \"XS, S, M, L, XL\"). If unavailable, return null."
#     )
#     ratings: str = Field(
#         description="The average customer rating for the product, typically on a scale of 1 to 5, represented as a string (e.g., \"4.5/5\"). If unavailable, return null."
#     )
#
#
# class OutputModel(BaseModel):
#     products: List[Products] = Field(
#         description="Array of products found on the merchant site matching the search criteria."
#     )
#
#
# def call_parallel_api(input_data: InputModel) -> Dict[str, Any]:
#     """
#     Call Parallel API to get product recommendations.
#     
#     Args:
#         input_data: InputModel with search parameters
#     
#     Returns:
#         Dictionary with 'products' key containing list of product dicts
#     """
#     client = Parallel(api_key=os.getenv("PARALLEL_API_KEY"))
#     
#     task_spec = build_task_spec_param(InputModel, OutputModel)
#     task_run = client.task_run.create(
#         input=input_data.model_dump(),
#         task_spec=task_spec,
#         processor="base"
#     )
#     
#     print(f"Parallel API run id: {task_run.run_id}")
#     
#     # Wait for the task run to complete (timeout: 1 hour)
#     run_result = client.task_run.result(task_run.run_id, api_timeout=3600)
#     
#     # Convert Pydantic model to dict
#     output_dict = run_result.output.model_dump() if hasattr(run_result.output, 'model_dump') else run_result.output
#     
#     return output_dict


def get_recommendations(merchant: str, clothing_type: str = "sweatshirts & hoodies") -> Dict[str, Any]:
    """
    Get product recommendations (stub - loads from CSV).
    
    Currently loads from shopping_result.csv. In the future, this will call
    the Parallel API to get real-time recommendations.
    
    Args:
        merchant: The merchant/brand name (e.g., "Uniqlo")
        clothing_type: Type of clothing (e.g., "sweatshirts & hoodies")
    
    Returns:
        Dictionary with 'products' key containing list of product dicts.
        Format matches Parallel API enrich response structure.
    
    Future Implementation:
        # Uncomment the Parallel API code above and replace this stub with:
        # input_data = InputModel(
        #     n_recommendations=10,
        #     page_url=page_url,  # From page context
        #     gender="men",  # Extract from user profile or page
        #     merchant_site=merchant,
        #     category=clothing_type
        # )
        # return call_parallel_api(input_data)
    """
    # STUB: Load from CSV file (replace with Parallel API call in future)
    csv_path = Path(__file__).parent.parent / "data" / "shopping_result.csv"
    
    if not csv_path.exists():
        print(f"Warning: CSV file not found at {csv_path}")
        return {"products": []}
    
    # Read CSV and extract products from the pro-fast processor row
    # This row has more detailed product information
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Use the pro-fast processor row (second data row, index 1)
        if len(rows) >= 2:
            products_json_str = rows[1].get('output.products', '[]')
        elif len(rows) >= 1:
            products_json_str = rows[0].get('output.products', '[]')
        else:
            print("Warning: No product data found in CSV")
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
        print(f"Error parsing products JSON from CSV: {e}")
        return {"products": []}
