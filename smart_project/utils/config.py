"""
Configuration utility for SmartCampusAI.
Loads environment variables from .env and exposes API keys.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from typing import Optional

# Load environment variables
ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)

def get_gemini_api_key() -> Optional[str]:
    """
    Retrieve the Gemini API key from environment variables.
    
    Returns:
        str | None: The API key if found, else None.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return api_key.strip()
