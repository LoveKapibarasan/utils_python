import os
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI


from create_assistant import create_and_save_assistant
from get_api_key import get_api_key  # Import the function here


api_key = get_api_key()
client = OpenAI(api_key=api_key)

# Ask for Assistant ID, or create one if not provided
ASSISTANT_ID = input("🔧 Enter the Assistant ID (leave blank to create new): ").strip()
if not ASSISTANT_ID:
    print("🆕 No Assistant ID provided. Creating a new assistant...")
    ASSISTANT_ID = create_and_save_assistant(json_path="assistant_info.json", api_key=api_key)

# Ask for thread ID or create one
user_thread = input("📎 Enter existing thread_id or press Enter to create a new one: ").strip()

if user_thread:
    thread_id = user_thread
    print(f"🔁 Using existing thread: {thread_id}")
else:
    thread = client.beta.threads.create()
    thread_id = thread.id
    print(f"🧵 Created new thread: {thread_id}")
    with open("thread_id.txt", "a") as f:  # ✅ fixed file mode
        f.write(thread_id + "\n")

# Ask for temperature (default = 0.7)
temp_input = input("🌡️ Enter temperature (default = 0.7): ").strip()
try:
    temperature = float(temp_input) if temp_input else 0.7
except ValueError:
    print("❌ Invalid temperature, using default 0.7")
    temperature = 0.7



print("\n💬 Start chatting with GPT-4o (Assistants API)")
print("📝 Multiline input. End input with a line containing only 'SEND'. Type 'exit' to quit.\n")

while True:
    try:
        print("You (end with 'SEND'):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "SEND":
                break
            lines.append(line)
        user_input = "\n".join(lines).strip()

        if user_input.lower() in {"exit", "quit"}:
            print("👋 Exiting chat.")
            break

        # ✅ Initialize file_ids list
        file_ids = []

        # 📎 User input: multiple file paths or file_ids separated by commas
        file_input = input("📁 Enter file paths or file_ids (comma-separated), or press Enter to skip: ").strip()

        if file_input:
            for item in file_input.split(","):
                item = item.strip()
                if os.path.isfile(item):
                    # Upload local file
                    try:
                        with open(item, "rb") as f:
                            uploaded_file = client.files.create(file=f, purpose="assistants")
                        file_ids.append(uploaded_file.id)
                        print(f"✅ Uploaded: {item} → {uploaded_file.id}")
                        with open("file_id_record.csv", "a", newline="") as record_file:
                            record_file.write(f"{uploaded_file.id}\n")
                    except Exception as e:
                        print(f"❌ Failed to upload '{item}': {e}")
                elif item.startswith("file-"):
                    # Use existing file_id
                    file_ids.append(item)
                    print(f"📎 Reusing file ID: {item}")
                else:
                    print(f"⚠️ Skipped invalid input: '{item}'")

        attachments = [
            {"file_id": fid, "tools": [{"type": "file_search"}]}
            for fid in file_ids
        ]
        # Add user message to thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input,
            attachments=attachments
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
            temperature=temperature
        )

        # Wait for assistant to complete
        print("⏳ Waiting for assistant...")
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == "completed":
                break
            elif run_status.status in {"failed", "cancelled"}:
                print(f"❌ Run {run_status.status}.")
                break
            time.sleep(1)

        # Retrieve assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_message = ""

        print("[DEBUG] Messages retrieved:", messages)
        for msg in reversed(messages.data):
            if msg.role == "assistant" and msg.run_id == run.id:
                assistant_message = msg.content[0].text.value
                print("\n🤖 Assistant:\n" + assistant_message)
                break

        # Save to log file
        os.makedirs("output", exist_ok=True)
        log_file = f"output/{thread_id}_log.txt"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(f"User:\n{user_input}\n\n")
            f.write(f"Assistant:\n{assistant_message}\n")
            if file_ids:
                f.write(f"Attached File ID(s): {', '.join(file_ids)}\n")


    except KeyboardInterrupt:
        print("\n👋 Exiting by keyboard interrupt.")
        break
