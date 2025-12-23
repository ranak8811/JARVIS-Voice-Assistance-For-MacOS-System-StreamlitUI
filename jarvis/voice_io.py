import speech_recognition as sr
import pyttsx3
import logging
from gtts import gTTS
import os

def speak(text):
    """
    Converts text to speech directly using pyttsx3 (for CLI mode).
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        voices = engine.getProperty("voices")
        if len(voices) > 7:
            engine.setProperty('voice', voices[7].id)
        else:
            engine.setProperty('voice', voices[0].id)
        
        logging.info(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        logging.error(f"Error in pyttsx3 speak function: {e}")
        print(f"ERROR: Could not speak the text. Check system TTS config. Details: {e}")

def text_to_audio_file(text, accent='com', filename="temp_audio.mp3"):
    """
    Converts text to an MP3 audio file using Google Text-to-Speech (gTTS).

    Args:
        text (str): The text to convert.
        accent (str): The top-level domain for the Google Translate host,
                      which determines the accent (e.g., 'com', 'co.uk').
        filename (str): The path to save the audio file.

    Returns:
        str: The path to the generated audio file.
    """
    try:
        tts = gTTS(text=text, lang='en', tld=accent, slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        logging.error(f"Error generating audio file with gTTS: {e}")
        return None

def take_command():
    """
    Listens for microphone input and converts it to text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening for voice command...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        r.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("No speech detected within the time limit.")
            return ""

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        logging.info(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        logging.error(f"Speech Recognition service error: {e}")
        print("Could not request results from the speech recognition service.")
        return ""
    except Exception as e:
        logging.error(f"An unexpected error occurred during speech recognition: {e}")
        return ""