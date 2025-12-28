import streamlit as st
from config.settings import Settings
from jarvis.gemini_engine import GeminiEngine
from jarvis.memory import Memory
from jarvis.prompt_controller import PromptController
from jarvis.assistant import JarvisAssistant
from jarvis.voice_io import take_command, text_to_audio_file
import os
import datetime
import time

# --- INITIALIZATION ---
@st.cache_resource
def initialize_assistant():
    settings = Settings()
    api_key = settings.load_api_key()
    if not api_key: return None
    engine = GeminiEngine(api_key=api_key)
    memory = Memory(file_path="jarvis/conversation_history.json")
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
    st.session_state.messages = assistant.memory.get_history()
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
        voice_accent = VOICE_MAP.get(selected_voice, "com")

    st.markdown("---")
    
    with st.expander("🎙️ Voice Command"):
        if st.button("Start Listening"):
            st.toast("Listening...")
            st.session_state.prompt_from_voice = take_command()
            if not st.session_state.get("prompt_from_voice"):
                st.toast("Could not recognize speech.")
            else:
                st.rerun()

    st.markdown("---")

    with st.expander("📜 Conversation"):
        if st.button("Clear Conversation History"):
            assistant.clear_memory()
            st.session_state.messages = []
            st.session_state.play_audio_for_index = None
            st.toast("Conversation cleared!")
            st.rerun()
            
        # Export Conversation button
        history_content = assistant.memory.get_exported_history_content()
        if history_content:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_export_{timestamp}.json"
            st.download_button(
                label="Export Conversation",
                data=history_content,
                file_name=filename,
                mime="application/json",
                key="download_conversation"
            )
        else:
            st.info("No conversation history to export.")

# --- MAIN INTERFACE ---
st.title("🤖 JARVIS – Your AI Assistant")

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(message["content"])
            # Handle audio playback UI
            if st.session_state.play_audio_for_index == i:
                with st.spinner("Generating audio..."):
                    audio_file = text_to_audio_file(message["content"], accent=voice_accent)
                    if audio_file:
                        st.audio(audio_file, autoplay=True)
                        # Reset the index to hide the player on the next run
                        st.session_state.play_audio_for_index = None
                    else:
                        st.error("Could not generate audio file.")
        with col2:
            if message["role"] == "assistant":
                if st.button("▶️", key=f"play_{i}", help="Play this message"):
                    st.session_state.play_audio_for_index = i
                    st.rerun()

# Determine prompt and input method
is_voice_input = False
prompt_to_process = st.session_state.pop("prompt_from_voice", None)
if prompt_to_process:
    is_voice_input = True
else:
    prompt_to_process = st.chat_input("Ask JARVIS...")

# Process prompt and update chat
if prompt_to_process:
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})
    with st.chat_message("user"):
        st.markdown(prompt_to_process)

    with st.chat_message("assistant"):
        with st.spinner("JARVIS is thinking..."):
            placeholder = st.empty()
            time.sleep(1)
            placeholder.empty()

            response_stream = assistant.respond_stream(prompt_to_process, role="Default")
            full_response = st.write_stream(response_stream)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # If the input was voice, automatically play the response
    if is_voice_input:
        # Set the index of the message to be played to the last one (the one we just added)
        st.session_state.play_audio_for_index = len(st.session_state.messages) - 1
        st.rerun()
    else:
        st.rerun()