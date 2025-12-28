import google.generativeai as genai
import logging

class GeminiEngine:
    """
    Handles interactions with the Google Gemini API.
    """
    def __init__(self, api_key, model_name="gemini-2.5-flash"):
        """
        Initializes the Gemini Engine.

        Args:
            api_key (str): The API key for the Gemini service.
            model_name (str): The name of the model to use.
        """
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
        else:
            self.model = None
            logging.error("Gemini API key not provided. GeminiEngine not initialized.")

    def generate(self, prompt):
        """
        Generates a response from the Gemini model based on the prompt.

        Args:
            prompt (list): A list of conversation history or a simple prompt string.

        Returns:
            str: The generated text response, or an error message.
        """
        if not self.model:
            return "Error: Gemini Engine is not initialized. Please check your API key."

        try:
            response = self.model.generate_content(prompt)
            # Handle cases where the response might be blocked or empty
            return response.text
        except ValueError:
            # This catches the "Invalid operation" error when response.text is accessed on a blocked prompt
            logging.warning("Blocked prompt or empty response from Gemini API.")
            return "I'm sorry, I can't respond to that. Is there something else I can help with?"
        except Exception as e:
            logging.error(f"An error occurred with the Gemini API: {e}")
            return f"Sorry, I encountered an error while trying to connect to the AI service."

    def generate_stream(self, prompt):
        """
        Generates a streaming response from the Gemini model.

        Args:
            prompt (list): A list of conversation history or a simple prompt string.

        Yields:
            str: Chunks of the generated text response.
        """
        if not self.model:
            yield "Error: Gemini Engine is not initialized. Please check your API key."
            return

        try:
            response_stream = self.model.generate_content(prompt, stream=True)
            for chunk in response_stream:
                try:
                    yield chunk.text
                except ValueError:
                    # This can happen if a specific chunk is empty/blocked.
                    # We can log it and continue to the next chunk.
                    logging.warning("A chunk in the stream was blocked or empty.")
                    continue
        except Exception as e:
            logging.error(f"An error occurred with the Gemini API stream: {e}")
            yield "I'm sorry, I can't respond to that. Let's try a different topic."
