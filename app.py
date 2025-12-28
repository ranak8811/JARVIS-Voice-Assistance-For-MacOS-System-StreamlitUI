import streamlit as st
from config.settings import Settings
from jarvis.gemini_engine import GeminiEngine
from jarvis.memory import Memory
from jarvis.prompt_controller import PromptController
from jarvis.assistant import JarvisAssistant
from jarvis.voice_io import take_command, text_to_audio_file
import os

# --- INITIALIZATION ---
@st.cache_resource
def initialize_assistant():
    settings = Settings()
    api_key = settings.load_api_key()
    if not api_key: return None
    engine = GeminiEngine(api_key=api_key)
    memory = Memory()
    prompt_controller = PromptController()
    return JarvisAssistant(engine=engine, prompt_controller=prompt_controller, memory=memory)

assistant = initialize_assistant()

# --- UI SETUP ---
st.set_page_config(page_title="JARVIS", page_icon="🤖", layout="wide")

if not assistant:
    st.error("FATAL: JARVIS could not be initialized. Check your GEMINI_API_KEY.")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "play_audio_for_index" not in st.session_state:
    st.session_state.play_audio_for_index = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("JARVIS Controls")
    
    with st.expander("🗣️ Voice Options", expanded=True):
        selected_voice = st.selectbox(
            "Choose a Voice",
            ("Default (US)", "British (UK)", "Australian", "Indian"),
            key="selected_voice"
        )
        VOICE_MAP = {
            "Default (US)": "com", 
            "British (UK)": "co.uk", 
            "Australian": "com.au",
            "Indian": "co.in"
        }
        voice_accent = VOICE_MAP[selected_voice]

    st.markdown("---")
    
    with st.expander("🎙️ Voice Command"):
        if st.button("Start Listening"):
            st.session_state.prompt_from_voice = take_command()
            if not st.session_state.get("prompt_from_voice"):
                st.toast("Could not recognize speech.")

    st.markdown("---")

    with st.expander("📜 Conversation"):
        if st.button("Clear Conversation History"):
            assistant.clear_memory()
            st.session_state.messages = []
            st.session_state.play_audio_for_index = None
            st.toast("Conversation cleared!")
            st.rerun()

# --- MAIN INTERFACE ---
st.title("🤖 JARVIS – Your AI Assistant")

# Determine the prompt to process
prompt_to_process = st.session_state.pop("prompt_from_voice", None) or st.chat_input("Ask JARVIS...")

# Process prompt and update chat
if prompt_to_process:
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})
    with st.spinner("JARVIS is thinking..."):
        response = assistant.respond(prompt_to_process, role="Default")
        st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Add play button and conditional audio player for assistant messages
        if message["role"] == "assistant":
            if st.button("▶️ Play Audio", key=f"play_{i}", help="Play this message"):
                # Set the index of the message to play and rerun
                st.session_state.play_audio_for_index = i
                st.rerun()

        # If the button for this message was just clicked, render the audio player
        if st.session_state.play_audio_for_index == i:
            with st.spinner("Generating audio..."):
                audio_file = text_to_audio_file(message["content"], accent=voice_accent)
                if audio_file:
                    st.audio(audio_file, autoplay=True)
                    # Clean up the temporary audio file after playing if desired
                    os.remove(audio_file) 
                else:
                    st.error("Could not generate audio file.")
            # Reset state so the player disappears on the next interaction
            st.session_state.play_audio_for_index = None