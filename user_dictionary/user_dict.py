import pyperclip
import json
import os

DICT_FILE = "dict.json"

def load_user_dict(filename):
    if not os.path.exists(filename):
        print(f"Dictionary file '{filename}' not found. Using empty dictionary.")
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_text(input_text, dictionary):
    words = input_text.split()
    translated_words = [
        dictionary.get(word.lower(), word)  # fallback to original word
        for word in words
    ]
    return ' '.join(translated_words)

if __name__ == "__main__":
    user_dict = load_user_dict(DICT_FILE)
    print("Enter text to translate. Type 'quit' to exit.\n")
    while True:
        input_text = input("Text: ")
        if input_text.strip().lower() == "quit":
            print("Goodbye.")
            break
        translated_text = translate_text(input_text, user_dict)
        pyperclip.copy(translated_text)
        print("→ Copied to clipboard:", translated_text)

