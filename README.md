# JARVIS - Hybrid AI Assistant

JARVIS is an advanced, Python-based personal AI assistant with a modular Object-Oriented Programming (OOP) architecture. It offers two distinct interfaces for interaction: a rich, modern web UI built with Streamlit and a classic, voice-controlled command-line interface (CLI).

This project is inspired by the iconic AI from Marvel's Iron Man and is designed to be both a powerful productivity tool and a showcase of modern Python development practices.

## ✨ Key Features

- **Dual Interface:**
  - **Web UI (Streamlit):** A full-featured chat interface where you can type or speak commands. It includes a dynamic audio player for each response with play/pause/seek controls.
  - **CLI:** A traditional voice-only mode for quick, hands-free commands and responses.

- **Intelligent & Conversational:**
  - Powered by the **Google Gemini API** for handling general questions, brainstorming, and complex conversational tasks.

- **Command & Control:**
  - **Application Management:** Opens and closes macOS applications like Calendar, Calculator, Terminal, and Music.
  - **Web Search:** Opens Google, Facebook, GitHub, and performs specific searches on YouTube.
  - **Information Retrieval:** Fetches and reads summaries from Wikipedia.
  - **Media Control:** Plays music from a local `music/` directory.

- **Customizable Voice Output:**
  - The web UI allows you to choose from multiple English accents (US, UK, Australian, Indian) for the text-to-speech voice, powered by Google's Text-to-Speech service.

## 🛠️ Tech Stack & Architecture

- **Core:** Python 3.10+
- **Web Interface:** Streamlit
- **AI Model:** Google Gemini
- **Voice Input:** `SpeechRecognition`
- **Voice Output:** `gTTS` (Web UI) & `pyttsx3` (CLI)
- **Architecture:** The project follows an OOP design for modularity and scalability.

## 📁 Project Structure

```
.
├── app.py                      # Streamlit Web UI entry point
├── cli.py                      # Command-Line Interface entry point
├── requirements.txt            # List of Python dependencies
├── README.md                   # Project documentation
├── .env                        # Environment variables (e.g., GEMINI_API_KEY)
├── config/
│   └── settings.py             # Handles loading environment settings
├── jarvis/
│   ├── __init__.py             # Python package initializer
│   ├── assistant.py            # Main JarvisAssistant class (the brain)
│   ├── gemini_engine.py        # Handles communication with Gemini API
│   ├── memory.py               # Manages conversation history
│   ├── prompt_controller.py    # Builds prompts for the AI model
│   ├── actions.py              # Executes system-level commands (e.g., open apps, play music)
│   ├── voice_io.py             # Centralizes voice input and audio generation
│   └── conversation_history.json # Stores chat history
├── logs/                       # Directory for application logs
│   └── application.log         # Log file for Jarvis interactions
└── music/                      # Directory to store MP3 music files
    └── <your_songs>.mp3        # Example: song1.mp3, groovy-vibe.mp3
```

## 📦 Dependencies

The project relies on the following Python packages. These are listed in `requirements.txt`:

- `google-generativeai`: For interacting with the Google Gemini API.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `streamlit`: For building the interactive web user interface.
- `SpeechRecognition`: For converting spoken language into text.
- `pyttsx3`: A cross-platform text-to-speech conversion library (used in CLI).
- `pyaudio`: Required by `SpeechRecognition` for microphone access.
- `wikipedia`: For searching and retrieving information from Wikipedia.
- `gTTS`: Google Text-to-Speech library for generating audio files (used in Web UI).

## 🚀 Setup and Installation

### 1. Prerequisites
- **Python 3.10 or higher.**
- **Homebrew** (for macOS) to install `portaudio`.

Install `portaudio`, which is required for voice input:
```bash
brew install portaudio
```

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/JARVIS-Voice-Assistance-For-MacOS-System.git
cd JARVIS-Voice-Assistance-For-MacOS-System
```

### 3. Set Up a Virtual Environment
```bash
python3 -m venv jarvis_env
source jarvis_env/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Your API Key
Create a file named `.env` in the root of the project and add your Google Gemini API key:
```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```
You can get a free API key from [Google AI Studio](https://aistudio.google.com/).

## ▶️ How to Run

You can run JARVIS in two modes:

### 1. Web UI Mode
For the full experience with chat, voice selection, and audio players:
```bash
streamlit run app.py
```

### 2. CLI Mode
For the classic, voice-only terminal experience:
```bash
python cli.py
```

## 🗣️ Supported Commands

You can use the following commands in either the web UI (via text or voice) or the CLI:

- **General Conversation:**
  - "What is your name?"
  - "What time is it?"
  - "How are you?"
  - "Who made you?"
  - "Thank you"

- **Actions & Commands:**
  - "Play music"
  - "Close music"
  - "Open Google"
  - "Open Facebook"
  - "Open GitHub"
  - "Open Calendar" / "Close Calendar"
  - "Open Calculator" / "Close Calculator"
  - "Open Terminal" / "Close Terminal"
  - "Open YouTube"
  - "Open YouTube [your search query]"
  - "Wikipedia [your search query]"

- **Exiting (CLI only):**
  - "Exit", "Quit", or "Stop"