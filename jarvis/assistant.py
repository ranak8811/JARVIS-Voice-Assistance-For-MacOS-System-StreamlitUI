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
        Generates a response to user input. It first checks for specific commands,
        and if none are found, it queries the generative AI model.
        """
        query = user_input.lower()

        # --- Command Handling ---
        if 'your name' in query:
            response = "My name is Jarvis, your personal assistant."
        elif 'how are you' in query:
            response = "I am functioning at full capacity, sir. Thank you for asking."
        elif 'who made you' in query:
            response = "I was created by Anwar, a Data Science Learner."
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            response = f"Sir, the time is {strTime}"
        elif 'thank you' in query:
            response = "It's my pleasure, sir. Always happy to help."
        elif 'play music' in query or 'play song' in query:
            response = self.action_handler.play_music()
        elif 'wikipedia' in query:
            search_query = query.replace("wikipedia", "").strip()
            if search_query:
                response = self.action_handler.search_wikipedia(search_query)
            else:
                response = "Please tell me what you want to search on Wikipedia."
        elif 'open google' in query:
            response = self.action_handler.open_website("https://www.google.com/", "Google")
        elif 'open facebook' in query:
            response = self.action_handler.open_website("https://www.facebook.com/", "Facebook")
        elif 'open github' in query:
            response = self.action_handler.open_website("https://github.com/", "GitHub")
        elif 'open youtube' in query:
            search_query = query.replace("open youtube", "").strip()
            if search_query:
                encoded_query = webbrowser.quote(search_query)
                url = f"https://www.youtube.com/results?search_query={encoded_query}"
                response = self.action_handler.open_website(url, f"YouTube for '{search_query}'")
            else:
                response = self.action_handler.open_website("https://www.youtube.com/", "YouTube")
        elif 'open calendar' in query:
            response = self.action_handler.open_application("Calendar")
        elif 'close calendar' in query:
            response = self.action_handler.close_application("Calendar")
        elif 'open calculator' in query:
            response = self.action_handler.open_application("Calculator")
        elif 'close calculator' in query:
            response = self.action_handler.close_application("Calculator")
        elif 'open terminal' in query:
            response = self.action_handler.open_application("Terminal")
        elif 'close terminal' in query:
            response = self.action_handler.close_application("Terminal")
        elif 'close music' in query:
            response = self.action_handler.close_application("Music")
        # --- Generative AI Fallback ---
        else:
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