import speech_recognition as sr 
import pyttsx3 
import logging 
import os 
import datetime 
import wikipedia 
import webbrowser 
import random 
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging configuration 
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format = "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)

def speak(text):
    """
    Converts text to speech using pyttsx3. Initializes the engine for each call to ensure robustness
    and sets a consistent speaking rate and preferred voice.

    Args:
        text (str): The text to be spoken.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # Setting a consistent speaking rate

    voices = engine.getProperty("voices")
    # Try to set a specific voice, fallback to the first available if index 7 is not present
    if len(voices) > 7:
        engine.setProperty('voice', voices[7].id)  # Male voice
    else:
        engine.setProperty('voice', voices[0].id)  # Fallback to the first voice

    print(f"Speaking: {text}")  # Log the text being spoken
    logging.info(f"Speaking: {text}") # Also log to file
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Ensure the engine is stopped and resources are released

def takeCommand():
    """
    Listens to the user's microphone input and converts it to text using Google Speech Recognition.

    Returns:
        str: The recognized text query in lowercase, or "None" if speech is unintelligible.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Seconds of non-speaking audio before a phrase is considered complete
        r.adjust_for_ambient_noise(source, duration=1) # Adjust for ambient noise for better accuracy
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")  # Log the recognized query for user feedback
        logging.info(f"User said: {query}") # Also log to file

    except sr.UnknownValueError:
        print("Sorry, I could not understand your audio. Please say that again.")
        logging.warning("Speech Recognition could not understand audio.")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        logging.error(f"Speech Recognition service error: {e}")
        return "None"
    except Exception as e:
        logging.error(f"An unexpected error occurred during speech recognition: {e}")
        print("An unexpected error occurred. Please try again.")
        return "None"
    
    return query.lower()


def greeting():
    """
    Greets the user based on the current time of day.
    """
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning sir! How are you doing?")
    elif 12 <= hour <= 18:
        speak("Good Afternoon sir! How are you doing?")
    else:
        speak("Good Evening sir! How are you doing?")
    
    speak("I am Jarvis. Please tell me how may I help you today?")


def play_music():
    """
    Plays a random song from the 'music' directory.
    Supports macOS by using the 'open' command.
    """
    music_dir = 'music'
    try:
        songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')] # Only consider mp3 files
        if songs:
            random_song = random.choice(songs)
            music_path = os.path.join(music_dir, random_song)
            speak(f"Playing {random_song} on Music app.")
            try:
                # Use 'open' command to play music on macOS, which defaults to the Music app for .mp3 files
                subprocess.call(["open", music_path])
                logging.info(f"Playing music: {random_song}")
            except Exception as sub_e:
                logging.error(f"Error playing music: {sub_e}")
                speak("Sorry, I couldn't play the music.")
        else:
            speak("No music found in the music directory. Please add some music.")
            logging.info("No music files found in the 'music' directory.")
    except FileNotFoundError:
        speak("Music directory not found. Please create a 'music' folder and add songs.")
        logging.error(f"Music directory '{music_dir}' not found.")
    except Exception as e:
        logging.error(f"Music playback error: {e}")
        speak("An unexpected error occurred while trying to play music.")
        return

def open_website(url, site_name="website"):
    """
    Opens a specified URL in the default web browser.

    Args:
        url (str): The URL to open.
        site_name (str): A user-friendly name for the website, used in spoken feedback.
    """
    speak(f"Opening {site_name}...")
    try:
        webbrowser.open(url)
        logging.info(f"Opened {site_name}: {url}")
    except Exception as e:
        speak(f"Sorry, I couldn't open {site_name}.")
        logging.error(f"Error opening {site_name} at {url}: {e}")

def gemini_model_response(user_input):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        logging.error("GEMINI_API_KEY not found in environment variables.")
        return "Sorry, the AI model is not configured correctly."
        
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = '''Your name is Jarvis, a personal assistant.
        Answer the provided question in short form. Question: ''' + user_input
    response = model.generate_content(prompt)
    result = response.text
    return result

def main():
    """
    Main function to run the Jarvis personal assistant.
    Handles greetings, takes voice commands, and executes various tasks.
    """
    greeting()    

    while True:
        query = takeCommand() # takeCommand already returns lowercase
        if query != "none": # Only proceed if a valid query was recognized

            if 'your name' in query:
                speak('My name is Jarvis, your personal assistant. How can I help you today?')
                logging.info("User asked for assistant's name.")

            elif 'time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")
                logging.info("User asked for the time.")

            elif "how are you" in query:
                speak("I am functioning at full capacity sir!")
                logging.info("User asked about assistant's well-being.")

            elif "who made you" in query:
                speak("I was created by Anwar, a Data Science Learner!")
                logging.info("User asked about assistant's creator.")

            elif "thank you" in query:
                speak("It's my pleasure sir. Always happy to help.")
                logging.info("User expressed gratitude.")

            elif 'play music' in query:
                play_music()
                logging.info("User asked to play music.")
        
            # Core features start here
            elif 'open google' in query:
                open_website("https://www.google.com/", "Google")

            elif 'open facebook' in query:
                open_website("https://www.facebook.com/", "Facebook")
                
            elif 'open github' in query:
                open_website("https://github.com/", "GitHub")

            elif 'open calendar' in query or 'open my calendar' in query:
                # On macOS, this opens the default Calendar app
                speak("Opening Calendar...")
                try:
                    subprocess.Popen(["open", "-a", "Calendar"])
                    logging.info("User requested to open Calendar application.")
                except Exception as e:
                    speak("Sorry, I couldn't open the Calendar application.")
                    logging.error(f"Error opening Calendar app: {e}")

            elif "open calculator" in query or "calculator" in query:
                speak("Opening calculator")
                try:
                    subprocess.Popen(["open", "-a", "Calculator"])
                    logging.info("User requested to open Calculator.")
                except Exception as e:
                    speak("Sorry, I couldn't open the Calculator application.")
                    logging.error(f"Error opening Calculator app: {e}")

            elif 'open terminal' in query:
                speak("Opening Terminal...")
                try:
                    subprocess.Popen(["open", "-a", "Terminal"])
                    logging.info("User asked to open Terminal.")
                except Exception as e:
                    speak("Sorry, I couldn't open the Terminal application.")
                    logging.error(f"Error opening Terminal app: {e}")

            elif 'open youtube' in query:
                search_query = query.replace("open youtube", "").strip()
                if search_query:
                    open_website(f"https://www.youtube.com/results?search_query={search_query}", f"YouTube for {search_query}")
                else:
                    open_website("https://www.youtube.com/", "default YouTube")

            elif 'wikipedia' in query:
                search_query = query.replace("wikipedia", "").strip()
                if search_query:
                    speak(f"Searching Wikipedia for {search_query}...")
                    try:
                        results = wikipedia.summary(search_query, sentences=2)
                        speak("According to Wikipedia")
                        speak(results)
                        logging.info(f"User asked to search Wikipedia for: {search_query}. Results: {results}")
                    except wikipedia.exceptions.PageError:
                        speak(f"Sorry, I could not find anything on Wikipedia for '{search_query}'.")
                        logging.warning(f"Wikipedia PageError for query: {search_query}")
                    except wikipedia.exceptions.DisambiguationError as e:
                        speak(f"There are multiple results for '{search_query}'. Please be more specific.")
                        logging.warning(f"Wikipedia DisambiguationError for query: {search_query}. Options: {e.options}")
                    except Exception as e:
                        speak("Sorry, I encountered an error while searching Wikipedia.")
                        logging.error(f"General error searching Wikipedia: {e}")
                else:
                    speak("Please tell me what you want to search on Wikipedia.")
                    logging.info("User asked for Wikipedia without a query.")
                    
            # Core features end here

            elif 'exit' in query or 'quit' in query or 'stop' in query:
                speak("Goodbye, have a nice day!")
                logging.info("User asked to exit the program.")
                exit()
            else:
                if query == "None":
                    speak('I am sorry, I can not help you with that. Please try again.')
                    logging.info("User asked for an unsupported feature.")
                else:
                    response = gemini_model_response(query)
                    speak(response)
                    logging.info(f"User asked: {query}. Response: {response}")

if __name__ == "__main__":
    main()
