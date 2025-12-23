import os
from dotenv import load_dotenv

class Settings:
    """
    Handles loading of environment variables from a .env file.
    """
    def __init__(self):
        """
        Initializes the Settings class and loads environment variables.
        """
        load_dotenv()

    def load_api_key(self):
        """
        Loads the Gemini API key from the environment variables.

        Returns:
            str: The Gemini API key, or None if not found.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            print("ERROR: GEMINI_API_KEY not found or not set in .env file.")
            return None
        return api_key
