import logging
import datetime
import sys

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
    Main function to run the JARVIS voice assistant in CLI mode.
    """
    # --- INITIALIZATION ---
    settings = Settings()
    api_key = settings.load_api_key()
    if not api_key:
        speak("Fatal error: Could not load Gemini API key.")
        return

    # Initialize components with file path for history
    engine = GeminiEngine(api_key=api_key)
    memory = Memory(file_path="jarvis/conversation_history.json")
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

        # --- Command Handling ---
        if 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye, have a nice day!")
            break
        
        if 'export conversation' in query:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_export_{timestamp}.json"
            memory.export_history(filename)
            speak(f"Conversation exported successfully to {filename}")
            continue

        # --- Streaming Response ---
        print("JARVIS: ", end="", flush=True)
        full_response = ""
        for chunk in assistant.respond_stream(query):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print("\n") # Newline after the response is complete
        
        # Speak the full response after streaming it to the console
        if full_response:
            speak(full_response)

if __name__ == "__main__":
    main()
