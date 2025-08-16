import os
from dotenv import load_dotenv


def get_api_key():
    # Try to get API key from environment
    load_dotenv()
    api_key = os.getenv("OPEN_API_KEY")
    if not api_key:
        raise ValueError("❌ OPEN_API_KEY not found in .env or input")
    return api_key