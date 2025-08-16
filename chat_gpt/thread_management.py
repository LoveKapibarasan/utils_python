# thread_management.py
from dataclasses import dataclass
from typing import Optional

# Conversation state with Responses API uses previous_response_id
# Docs: Conversation state guide. :contentReference[oaicite:2]{index=2}

DEFAULT_MODEL = "gpt-5"  # per docs quickstart; change to "gpt-4o" if you prefer. :contentReference[oaicite:3]{index=3}

@dataclass
class ConversationState:
    previous_response_id: Optional[str] = None


def init_conversation_state() -> ConversationState:
    return ConversationState(previous_response_id=None)


def update_conversation_state(state: ConversationState, new_response_id: str) -> ConversationState:
    state.previous_response_id = new_response_id
    return state


def prompt_session_name() -> str:
    name = input("📝 Session name for logs [default=session]: ").strip()
    return name or "session"


def get_model_choice() -> str:
    model = input(f"🧠 Model [default={DEFAULT_MODEL}]: ").strip()
    return model or DEFAULT_MODEL
