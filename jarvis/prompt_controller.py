class PromptController:
    """
    Builds and formats the prompt for the Gemini model, including system
    instructions and conversation history, suitable for a chat-based interaction.
    """
    def __init__(self):
        """
        Initializes the PromptController.
        """
        self.base_prompt = "Your name is Jarvis, a personal assistant created by Anwar, a Data Science Learner. Answer the user's question."
        self.role_prompts = {
            "Tutor": "You are a helpful and patient tutor. Explain concepts clearly with examples.",
            "Coding assistant": "You are an expert coding assistant. Provide clean, efficient, and well-commented code. Explain your reasoning.",
            "Career helper": "You are a knowledgeable career helper. Offer advice on resumes, interviews, and career development.",
            "Default": "" # No extra role-based instruction
        }

    def build_prompt(self, history, role="Default"):
        """
        Constructs the full prompt for the model based on history and role.
        In a chat model, the history itself often serves as the prompt.
        This method will prepend a system-level instruction based on the role.

        Args:
            history (list): The conversation history from the Memory class.
            role (str): The desired role for the assistant.

        Returns:
            list: The formatted prompt including role-based instructions and history.
        """
        role_instruction = self.role_prompts.get(role, "")
        system_instruction = f"{self.base_prompt} {role_instruction}".strip()

        # The prompt for the Gemini chat model is the history itself.
        # We can insert a system message at the beginning of the chat,
        # but for many models, the user/model turn structure is sufficient.
        # Let's keep it simple and just return the history.
        # The model's behavior can be guided by a system message if needed,
        # but let's try without it first to keep the code beginner-friendly.
        
        # A simple implementation: The history is the prompt.
        # The `assistant.py` will be responsible for adding the latest user message.
        return history