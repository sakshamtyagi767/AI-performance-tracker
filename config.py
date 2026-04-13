

import os
from dotenv import load_dotenv

# Load variables from .env file into the environment.
# If .env doesn't exist, the program will raise a clear error below.
load_dotenv()


def get_api_key() -> str:
    """
    Retrieve the Gemini API key from the environment.

    Returns:
        str: The API key string.

    Raises:
        ValueError: If the API key is not set in the .env file.
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key or key == "your_gemini_api_key_here":
        raise ValueError(
            "\n[ERROR] GEMINI_API_KEY not set!\n"
            "Please copy .env.example to .env and paste your real API key.\n"
            "Get one free at: https://aistudio.google.com/app/apikey\n"
        )
    return key


# --- Tunable Settings ---

# Model confirmed working on free tier for this account
GEMINI_MODEL: str = "gemma-3-4b-it"

# How many top processes to include in the report
TOP_PROCESS_COUNT: int = 10

# Minimum CPU % for a process to be colour-highlighted as "heavy"
HEAVY_CPU_THRESHOLD: float = 10.0

# Minimum RAM (MB) for a process to be flagged as memory-heavy
HEAVY_RAM_THRESHOLD_MB: float = 500.0
