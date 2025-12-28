from jarvis.actions import ActionHandler
import datetime
import webbrowser

class JarvisAssistant:
    """
    The main coordinator for the JARVIS assistant.
    Orchestrates the interaction between memory, prompt control, actions, and the AI engine.
    """
    def __init__(self, engine, prompt_controller, memory):
        self.engine = engine
        self.prompt_controller = prompt_controller
        self.memory = memory
        self.action_handler = ActionHandler()

    def respond(self, user_input, role="Default"):
        """
        Generates a complete response to user input by consuming the streaming generator.
        """
        full_response = ""
        for chunk in self.respond_stream(user_input, role):
            full_response += chunk
        return full_response

    def respond_stream(self, user_input, role="Default"):
        """
        Generates a streaming response to user input. It first checks for specific commands,
        and if none are found, it queries the generative AI model via a stream.
        """
        query = user_input.lower()

        # --- Command Handling ---
        # (These are handled instantly and don't need to be streamed)
        command_response = self._handle_commands(query)
        if command_response:
            yield command_response
            return

        # --- Generative AI Fallback ---
        self.memory.add("user", user_input)
        history = self.memory.get_generative_history() # Use the correct history format
        prompt_for_engine = self.prompt_controller.build_prompt(history, role)
        
        full_response = ""
        # Stream the response from the engine
        for chunk in self.engine.generate_stream(prompt_for_engine):
            full_response += chunk
            yield chunk
        
        # Add the complete model response to memory after streaming is complete
        if full_response:
            self.memory.add("model", full_response)

    def _handle_commands(self, query):
        """Helper to process simple, non-AI commands."""
        if 'your name' in query:
            return "My name is Jarvis, your personal assistant."
        elif 'how are you' in query:
            return "I am functioning at full capacity, sir. Thank you for asking."
        elif 'who made you' in query:
            return "I was created by Anwar, a Data Science Learner."
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            return f"Sir, the time is {strTime}"
        elif 'thank you' in query:
            return "It's my pleasure, sir. Always happy to help."
        elif 'open music' in query:
            return self.action_handler.open_application("Music")
        elif 'play music' in query or 'play song' in query:
            return self.action_handler.play_music()
        elif 'search wikipedia' in query:
            search_query = query.replace("search wikipedia", "").strip()
            if search_query:
                return self.action_handler.search_wikipedia(search_query)
            else:
                return "Please tell me what you want to search on Wikipedia."
        elif 'open google' in query:
            return self.action_handler.open_website("https://www.google.com/", "Google")
        elif 'open facebook' in query:
            return self.action_handler.open_website("https://www.facebook.com/", "Facebook")
        elif 'open github' in query:
            return self.action_handler.open_website("https://github.com/", "GitHub")
        elif 'youtube' in query:
            # Simplified logic as per user request
            search_query = query.replace("open youtube", "").replace("search youtube for", "").replace("search youtube", "").strip()
            if search_query:
                # Not using urllib.parse.quote as per user request
                url = f"https://www.youtube.com/results?search_query={search_query}"
                return self.action_handler.open_website(url, f"YouTube for '{search_query}'")
            else:
                return self.action_handler.open_website("https://www.youtube.com/", "YouTube")
        elif 'open calendar' in query:
            return self.action_handler.open_application("Calendar")
        elif 'close calendar' in query:
            return self.action_handler.close_application("Calendar")
        elif 'open calculator' in query:
            return self.action_handler.open_application("Calculator")
        elif 'close calculator' in query:
            return self.action_handler.close_application("Calculator")
        elif 'open terminal' in query:
            return self.action_handler.open_application("Terminal")
        elif 'close terminal' in query:
            return self.action_handler.close_application("Terminal")
        elif 'close music' in query:
            return self.action_handler.close_application("Music")
        return None

    def clear_memory(self):
        """
        Clears the conversation history for the generative AI.
        """
        self.memory.clear()