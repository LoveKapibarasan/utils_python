import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
if not api_key:
    raise ValueError("OPEN_API_KEY not found in .env")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Initialize message history
messages = []

print("Start chatting with the assistant (type 'exit' to stop):")

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("Exiting chat.")
        break

    # Add user message to the history
    messages.append({"role": "user", "content": user_input})

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    print("response:", response)
    # Extract assistant reply and print
    assistant_message = response.choices[0].message.content
    print("Assistant:", assistant_message)

    # Add assistant message to history
    messages.append({"role": "assistant", "content": assistant_message})
