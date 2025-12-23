import os
import webbrowser
import wikipedia
import random
import subprocess
import logging
from jarvis.voice_io import speak

class ActionHandler:
    """
    This class handles the execution of commands that interact with the OS,
    such as opening applications, websites, or searching for information.
    """

    def play_music(self):
        """
        Plays a random song from the 'music' directory.
        """
        music_dir = 'music'
        try:
            songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
            if not songs:
                return "No music files found in the music directory."
            
            random_song = random.choice(songs)
            music_path = os.path.join(music_dir, random_song)
            speak(f"Playing {os.path.basename(music_path)}")
            subprocess.call(["open", music_path])
            return f"Now playing: {os.path.basename(music_path)}"
        except FileNotFoundError:
            return "Music directory not found. Please create a 'music' folder."
        except Exception as e:
            logging.error(f"Music playback error: {e}")
            return f"Sorry, an error occurred while trying to play music: {e}"

    def open_website(self, url, site_name):
        """
        Opens a specified URL in the default web browser.
        """
        try:
            webbrowser.open(url)
            return f"Opening {site_name}..."
        except Exception as e:
            logging.error(f"Error opening website {url}: {e}")
            return f"Sorry, I couldn't open {site_name}."

    def search_wikipedia(self, query):
        """
        Searches Wikipedia for a query and returns a summary.
        """
        try:
            speak(f"Searching Wikipedia for {query}...")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            return results
        except wikipedia.exceptions.PageError:
            return f"Sorry, I could not find anything on Wikipedia for '{query}'."
        except wikipedia.exceptions.DisambiguationError:
            return f"There are multiple results for '{query}'. Please be more specific."
        except Exception as e:
            logging.error(f"Wikipedia search error: {e}")
            return "Sorry, an error occurred while searching Wikipedia."
    
    def open_application(self, app_name):
        """
        Opens a macOS application.
        """
        try:
            subprocess.Popen(["open", "-a", app_name])
            return f"Opening {app_name}..."
        except Exception as e:
            logging.error(f"Error opening application {app_name}: {e}")
            return f"Sorry, I couldn't open {app_name}."

    def close_application(self, app_name):
        """
        Closes a macOS application.
        """
        try:
            subprocess.Popen(["osascript", "-e", f'tell application "{app_name}" to quit'])
            return f"Closing {app_name}..."
        except Exception as e:
            logging.error(f"Error closing application {app_name}: {e}")
            return f"Sorry, I couldn't close {app_name}."
