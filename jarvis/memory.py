import json
import os
import shutil

class Memory:
    """
    Manages the conversation history in memory and syncs with a JSON file.
    """
    def __init__(self, file_path="jarvis/conversation_history.json"):
        """
        Initializes the Memory class.

        Args:
            file_path (str): The path to the JSON file for storing history.
        """
        self.file_path = file_path
        self.history = self._load_history()

    def _load_history(self):
        """Loads conversation history from the JSON file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load history from {self.file_path}. Starting fresh. Error: {e}")
        return []

    def _save_history(self):
        """Saves the current conversation history to the JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.history, f, indent=4)
        except IOError as e:
            print(f"Error: Could not save history to {self.file_path}. Error: {e}")

    def add(self, role, message):
        """
        Adds a new message to the conversation history and saves it.

        Args:
            role (str): The role of the speaker ('user' or 'model').
            message (str): The message content.
        """
        # The format for Gemini API is a list of dicts with 'role' and 'parts'
        self.history.append({"role": role, "parts": [message]})
        self._save_history()

    def get_history(self):
        """
        Returns the conversation history, converting it to a simpler format
        for UI display if needed. ('parts' -> 'content')
        """
        display_history = []
        for entry in self.history:
            # The 'content' key is used by the Streamlit UI
            display_history.append({
                "role": entry["role"],
                "content": entry["parts"][0] if entry["parts"] else ""
            })
        return display_history

    def get_generative_history(self):
        """
        Returns the raw history in the format expected by the generative AI model.
        """
        return self.history

    def clear(self):
        """
        Clears the conversation history from memory and the file.
        """
        self.history = []
        self._save_history()

    def get_exported_history_content(self):
        """
        Returns the content of the conversation history file as a string for export.
        """
        try:
            with open(self.file_path, 'r') as f:
                return f.read()
        except IOError as e:
            print(f"Error: Could not read history from {self.file_path} for export. Error: {e}")
            return None
