import json
import os
from openai import OpenAI
from get_api_key import get_api_key  # Import the function here


def create_and_save_assistant(json_path="assistant_info.json"):
    client = OpenAI(api_key=get_api_key())

    name = input("🤖 Assistant name [default = My Assistant]: ").strip() or "My Assistant"
    instructions = input("📝 Instructions [default = You are a helpful assistant.]: ").strip() or "You are a helpful assistant."
    model = input("🧠 Model [default = gpt-4-1106-preview]: ").strip() or "gpt-4-1106-preview"
    include_file_search = input("📎 Include file_search tool? (yes/no) [default = yes]: ").strip().lower() or "yes"
    include_code_interpreter = input("🧮 Include code_interpreter tool? (yes/no) [default = no]: ").strip().lower() or "no"

    tools = []
    if include_file_search in {"yes", "y"}:
        tools.append({"type": "file_search"})
    if include_code_interpreter in {"yes", "y"}:
        tools.append({"type": "code_interpreter"})

    print("🚀 Creating assistant...")
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=tools
    )

    assistant_info = {
        "id": assistant.id,
        "name": assistant.name,
        "instructions": assistant.instructions,
        "model": assistant.model,
        "tools": [tool.type for tool in assistant.tools],
        "created_at": assistant.created_at
    }

    # Ensure file exists and is a JSON array
    if not os.path.exists(json_path):
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(json_path, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
        except json.JSONDecodeError:
            data = []
        data.append(assistant_info)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

    print(f"💾 Assistant info saved to '{json_path}'")
    return assistant.id


def delete_assistant(assistant_id, json_path="assistant_info.json"):
    client = OpenAI(api_key=get_api_key())

    try:
        client.beta.assistants.delete(assistant_id)
        print(f"🗑️ Assistant '{assistant_id}' deleted from OpenAI.")
    except Exception as e:
        print(f"⚠️ Failed to delete assistant '{assistant_id}' from OpenAI: {e}")

    # Remove from JSON file
    if os.path.exists(json_path):
        with open(json_path, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    new_data = [a for a in data if a.get("id") != assistant_id]
                else:
                    new_data = []
            except json.JSONDecodeError:
                new_data = []

            f.seek(0)
            json.dump(new_data, f, indent=2)
            f.truncate()

        print(f"🧹 Removed assistant '{assistant_id}' from '{json_path}'.")
    else:
        print(f"⚠️ JSON file '{json_path}' does not exist, nothing to clean up.")


if __name__ == "__main__":
    action = input("Choose action (create/delete): ").strip().lower()
    if action == "create":
        create_and_save_assistant()
    elif action == "delete":
        assistant_id = input("Enter assistant ID to delete: ").strip()
        delete_assistant(assistant_id)
    else:
        print("❌ Invalid action. Please choose 'create' or 'delete'.")
