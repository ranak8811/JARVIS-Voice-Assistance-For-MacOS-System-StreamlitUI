# Jarvis AI - Your Personal Desktop Assistant (macOS)

Jarvis AI is a Python-based personal desktop assistant designed for macOS, inspired by the iconic AI from Marvel's Iron Man. This project allows you to interact with your computer using voice commands, performing various tasks like browsing the web, playing music, opening applications, and fetching information.

## Features

- **Voice Interaction:** Utilizes Speech Recognition to understand your commands and `pyttsx3` for spoken responses.
- **Contextual Greetings:** Greets you based on the time of day.
- **Time Inquiry:** Tells you the current time.
- **Web Browsing:** Open popular websites like Google, Facebook, GitHub, and YouTube with simple voice commands. You can also search directly on YouTube.
- **Music Playback:** Plays random `.mp3` songs from a designated `music` directory.
- **Application Launcher:** Opens native macOS applications such as Calendar, Calculator, and Terminal.
- **Wikipedia Search:** Fetches and reads summaries from Wikipedia for your queries.
- **Logging:** All interactions and errors are logged to `logs/application.log` for debugging and monitoring.
- **AI-Powered Answers:** Uses Google Gemini to answer queries not explicitly handled by the assistant, leveraging the `google-generativeai` package.

## Prerequisites

Before you begin, ensure you have the following installed on your macOS system:

- **Python 3.x:** This project is developed with Python.
- **pip:** Python's package installer.
- **PortAudio:** A cross-platform audio I/O library required by `pyaudio`.

### Installing PortAudio on macOS

You can install PortAudio using Homebrew:

```bash
brew install portaudio
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ranak8811/JARVIS-Voice-Assistance-For-MacOS-System.git
   cd JARVIS-Voice-Assistance-For-MacOS-System
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv jarvis_env
   source jarvis_env/bin/activate
   ```

3. **Install dependencies:**
   The project uses the following Python packages:

   - `SpeechRecognition==3.14.3`
   - `pyttsx3`
   - `pyaudio`
   - `wikipedia`
   - `google-generativeai`
   - `python-dotenv`

   You can install them using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not available, you can install them manually:

   ```bash
   pip install SpeechRecognition==3.14.3 pyttsx3 pyaudio wikipedia
   ```

4. **Configure Environment Variables:**
   For the AI-Powered Answers feature (Google Gemini), you need to set up a `.env` file in the root directory of the project. This file should contain your Google Gemini API key.

   Create a file named `.env` in the project root and add the following line:

   ```
   GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
   ```

   Replace `"YOUR_GEMINI_API_KEY"` with your actual Google Gemini API key. You can obtain a key from the Google AI Studio or Google Cloud Console.

## Usage

1. **Ensure your microphone is properly configured and accessible.**

2. **Run the `app.py` script:**

   ```bash
   python3 app.py
   ```

3. **Start giving commands:**
   Jarvis will greet you and then wait for your voice commands. Here are some examples of commands you can use:

   - "Good morning/afternoon/evening" (Jarvis will respond based on the time)
   - "What is your name?"
   - "What time is it?"
   - "How are you?"
   - "Who made you?"
   - "Thank you"
   - "Play music"
   - "Open Google"
   - "Open Facebook"
   - "Open GitHub"
   - "Open Calendar"
   - "Open Calculator"
   - "Open Terminal"
   - "Open YouTube" (opens default YouTube)
   - "Open YouTube [search query]" (e.g., "Open YouTube latest tech news")
   - "Wikipedia [your query]" (e.g., "Wikipedia Python programming language")
   - "Exit", "Quit", or "Stop" (to end the program)

## Project Structure

```
.
├── app.py                  # Main application logic for Jarvis AI
├── requirements.txt        # List of Python dependencies
├── README.md               # Project README file
├── logs/                   # Directory for application logs
│   └── application.log     # Log file for Jarvis interactions
└── music/                  # Directory to store MP3 music files
    ├── song1.mp3
    └── song2.mp3
```

## Contributing

Feel free to fork the repository, create pull requests, or open issues for any suggestions or bug reports.

## License

This project is open-source and available under the [MIT License](LICENSE). _(You might need to create a LICENSE file if one doesn't exist)_

## Acknowledgements

- Inspired by the Jarvis AI from Marvel.
- Thanks to the developers of `SpeechRecognition`, `pyttsx3`, `pyaudio`, and `wikipedia` libraries.
