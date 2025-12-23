import google.generativeai as genai

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
            print("ERROR: Gemini API key not provided. GeminiEngine not initialized.")

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
            return response.text
        except Exception as e:
            print(f"ERROR: An error occurred with the Gemini API: {e}")
            return f"Sorry, I encountered an error while generating a response: {e}"
