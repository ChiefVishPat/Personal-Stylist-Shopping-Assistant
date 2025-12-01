"""
Application configuration and settings.
Loads environment variables and defines Tavus API config.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Tavus API Configuration
TAVUS_CONFIG = {
    "API_ENDPOINT": "https://tavusapi.com/v2/conversations",
    "API_KEY": os.getenv("TAVUS_API_KEY"),
    "PERSONA_ID": os.getenv("PERSONA_ID", "p78a4e6a3f3f"),
    "REPLICA_ID": os.getenv("REPLICA_ID", "rf4703150052"),
    "TIMEOUT_MS": 15000,  # 15 seconds
    "DOCUMENT_IDS": os.getenv("DOCUMENT_IDS", "db-63693bf189f3,d2-52056d49cbfc,d4-22b4520c7a99").split(",") if os.getenv("DOCUMENT_IDS") else [],
    "DOCUMENT_TAGS": os.getenv("DOCUMENT_TAGS", "early_20s_fashion,mens_fashion,uniqlo_men_fashion,street_wear,pinterest").split(",") if os.getenv("DOCUMENT_TAGS") else [],
}

# Server Configuration
SERVER_CONFIG = {
    "HOST": os.getenv("HOST", "0.0.0.0"),
    "PORT": int(os.getenv("PORT", 8000)),
    "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
    "DEBUG": os.getenv("DEBUG", "True").lower() == "true",
}
