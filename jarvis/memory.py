import json
import os

class Memory:
    """
    Manages the conversation history in a JSON file.
    """
    def __init__(self, history_file="jarvis/conversation_history.json"):
        """
        Initializes the Memory class.

        Args:
            history_file (str): The path to the JSON file for storing history.
        """
        self.history_file = history_file
        # Ensure the history file exists
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)

    def add(self, role, message):
        """
        Adds a new message to the conversation history.

        Args:
            role (str): The role of the speaker ('user' or 'model').
            message (str): The message content.
        """
        history = self.get_history()
        history.append({"role": role, "parts": [message]})
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=4)

    def get_history(self):
        """
        Loads the conversation history from the JSON file.

        Returns:
            list: A list of conversation messages.
        """
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def clear(self):
        """
        Clears the conversation history by emptying the JSON file.
        """
        with open(self.history_file, 'w') as f:
            json.dump([], f)
