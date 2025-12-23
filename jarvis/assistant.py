from jarvis.actions import ActionHandler
import datetime

class JarvisAssistant:
    """
    The main coordinator for the JARVIS assistant.
    Orchestrates the interaction between memory, prompt control, actions, and the AI engine.
    """
    def __init__(self, engine, prompt_controller, memory):
        """
        Initializes the JarvisAssistant.

        Args:
            engine (GeminiEngine): The AI engine for generating responses.
            prompt_controller (PromptController): The controller for building prompts.
            memory (Memory): The manager for conversation history.
        """
        self.engine = engine
        self.prompt_controller = prompt_controller
        self.memory = memory
        self.action_handler = ActionHandler()

    def respond(self, user_input, role="Default"):
        """
        Generates a response to user input. It first checks for specific commands,
        and if none are found, it queries the generative AI model.

        Args:
            user_input (str): The input text from the user.
            role (str): The role the assistant should adopt for this response.

        Returns:
            str: The response, either from an action or from the AI.
        """
        query = user_input.lower()

        # --- Command Handling ---
        # First, check for specific, non-ambiguous commands.
        if 'play music' in query or 'play song' in query:
            response = self.action_handler.play_music()
        elif 'wikipedia' in query:
            search_query = query.replace("wikipedia", "").strip()
            if search_query:
                response = self.action_handler.search_wikipedia(search_query)
            else:
                response = "Please tell me what you want to search on Wikipedia."
        elif 'open google' in query:
            response = self.action_handler.open_website("https://www.google.com/", "Google")
        elif 'open youtube' in query:
            response = self.action_handler.open_website("https://www.youtube.com/", "YouTube")
        elif 'open github' in query:
            response = self.action_handler.open_website("https://github.com/", "GitHub")
        elif 'open calendar' in query:
            response = self.action_handler.open_application("Calendar")
        elif 'close calendar' in query:
            response = self.action_handler.close_application("Calendar")
        elif 'open calculator' in query:
            response = self.action_handler.open_application("Calculator")
        elif 'close calculator' in query:
            response = self.action_handler.close_application("Calculator")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            response = f"Sir, the time is {strTime}"
        elif 'thank you' in query:
            response = "It's my pleasure, sir. Always happy to help."
        # Add more commands here as needed...
        else:
            # --- Generative AI Fallback ---
            # If no command is matched, use the AI model.
            self.memory.add("user", user_input)
            history = self.memory.get_history()
            prompt_for_engine = self.prompt_controller.build_prompt(history, role)
            
            response = self.engine.generate(prompt_for_engine)
            
            if response:
                self.memory.add("model", response)
        
        return response

    def clear_memory(self):
        """
        Clears the conversation history for the generative AI.
        """
        self.memory.clear()
