import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
if not api_key:
    raise ValueError("❌ OPEN_API_KEY not found in .env")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Prompt user for assistant configuration
name = input("🤖 Assistant name [default = My Assistant]: ").strip() or "My Assistant"

instructions = input("📝 Instructions [default = You are a helpful assistant.]: ").strip() or \
    "You are a helpful assistant."

model = input("🧠 Model [default = gpt-4-1106-preview]: ").strip() or "gpt-4-1106-preview"

include_file_search = input("📎 Include file_search tool? (yes/no) [default = yes]: ").strip().lower() or "yes"
include_code_interpreter = input("🧮 Include code_interpreter tool? (yes/no) [default = no]: ").strip().lower() or "no"

# Build tools list
tools = []
if include_file_search in {"yes", "y"}:
    tools.append({"type": "file_search"})
if include_code_interpreter in {"yes", "y"}:
    tools.append({"type": "code_interpreter"})

# Create assistant
print("🚀 Creating assistant...")
assistant = client.beta.assistants.create(
    name=name,
    instructions=instructions,
    model=model,
    tools=tools
)


# Save assistant details to JSON
assistant_info = {
    "id": assistant.id,
    "name": assistant.name,
    "instructions": assistant.instructions,
    "model": assistant.model,
    "tools": [tool.type for tool in assistant.tools],
    "created_at": assistant.created_at
}

with open("assistant_info.json", "a", encoding="utf-8") as f:
    json.dump(assistant_info, f, indent=2)

print("💾 Assistant info saved to 'assistant_info.json'")

