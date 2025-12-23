import streamlit as st
from config.settings import Settings
from jarvis.gemini_engine import GeminiEngine
from jarvis.memory import Memory
from jarvis.prompt_controller import PromptController
from jarvis.assistant import JarvisAssistant

# --- INITIALIZATION ---
# Use Streamlit's caching to load the assistant only once
@st.cache_resource
def initialize_assistant():
    """
    Initializes and returns the main JARVIS assistant object.
    This function is cached so it only runs on the first script run.
    """
    settings = Settings()
    api_key = settings.load_api_key()

    if not api_key:
        return None

    engine = GeminiEngine(api_key=api_key)
    memory = Memory()
    prompt_controller = PromptController()
    
    assistant = JarvisAssistant(
        engine=engine,
        prompt_controller=prompt_controller,
        memory=memory
    )
    return assistant

# Load the assistant
assistant = initialize_assistant()

# --- UI SETUP ---
st.set_page_config(page_title="JARVIS", page_icon="🤖", layout="wide")

# Check if initialization failed
if not assistant:
    st.error("FATAL: JARVIS could not be initialized. Please check your GEMINI_API_KEY in the .env file.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("JARVIS Controls")
    
    # Role selection dropdown
    assistant_role = st.selectbox(
        "Choose JARVIS's Role",
        ("Default", "Tutor", "Coding assistant", "Career helper"),
        key="assistant_role",
        help="Select the personality and expertise for JARVIS."
    )

    # Clear conversation button
    if st.button("Clear Conversation History"):
        assistant.clear_memory()
        # Reset the messages in the session state as well
        st.session_state.messages = []
        st.success("Conversation history cleared!")

# --- MAIN CHAT INTERFACE ---
st.title("🤖 JARVIS – Your AI Assistant")
st.caption("Powered by Google Gemini and Streamlit")

# Initialize session_state.messages if it doesn't exist
if "messages" not in st.session_state:
    # Load history from file to persist across browser tabs
    history = assistant.memory.get_history()
    # Streamlit's session state expects a list of dicts with "role" and "content"
    st.session_state.messages = [
        {"role": msg["role"], "content": msg["parts"][0]} for msg in history
    ]

# Display past messages from the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if user_prompt := st.chat_input("Ask JARVIS..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate and display the assistant's response
    with st.spinner("JARVIS is thinking..."):
        # The assistant handles everything: history, prompt, and response
        response = assistant.respond(user_prompt, role=assistant_role)
        
        # Add assistant response to session state and display it
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
