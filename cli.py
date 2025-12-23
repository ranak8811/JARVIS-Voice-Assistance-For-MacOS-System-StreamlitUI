import logging
import datetime

from config.settings import Settings
from jarvis.gemini_engine import GeminiEngine
from jarvis.memory import Memory
from jarvis.prompt_controller import PromptController
from jarvis.assistant import JarvisAssistant
from jarvis.voice_io import speak, take_command

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to run the JARVIS voice assistant.
    """
    # --- INITIALIZATION ---
    settings = Settings()
    api_key = settings.load_api_key()
    if not api_key:
        speak("Fatal error: Could not load Gemini API key.")
        return

    engine = GeminiEngine(api_key=api_key)
    memory = Memory()
    prompt_controller = PromptController()
    assistant = JarvisAssistant(
        engine=engine,
        prompt_controller=prompt_controller,
        memory=memory
    )

    # --- GREETING ---
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Sir! How are you doing?")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir! How are you doing?")
    else:
        speak("Good Evening Sir! How are you doing?")
    speak("I am Jarvis. How may I help you today?")

    # --- MAIN LOOP ---
    while True:
        query = take_command()

        if not query:
            continue

        if 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye, have a nice day!")
            break
        
        response = assistant.respond(query)
        speak(response)

if __name__ == "__main__":
    main()
