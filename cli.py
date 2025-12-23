import speech_recognition as sr
import pyttsx3
import logging
import datetime

from config.settings import Settings
from jarvis.gemini_engine import GeminiEngine
from jarvis.memory import Memory
from jarvis.prompt_controller import PromptController
from jarvis.assistant import JarvisAssistant

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def speak(text):
    """
    Converts text to speech using pyttsx3.
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        voices = engine.getProperty("voices")
        # A common male voice index, adjust if necessary
        if len(voices) > 7:
            engine.setProperty('voice', voices[7].id)
        else:
            engine.setProperty('voice', voices[0].id)
        
        print(f"JARVIS: {text}")
        logging.info(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        logging.error(f"Error in speak function: {e}")
        print(f"Error: Could not use text-to-speech. Details: {e}")

def take_command():
    """
    Listens for microphone input and converts it to text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        logging.info(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the audio. Please try again.")
        return ""
    except sr.RequestError as e:
        speak("Could not request results from the speech recognition service.")
        logging.error(f"Speech Recognition service error: {e}")
        return ""
    except Exception as e:
        logging.error(f"An unexpected error during speech recognition: {e}")
        return ""

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
