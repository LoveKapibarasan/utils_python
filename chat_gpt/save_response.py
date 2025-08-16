# save_response.py
from datetime import datetime
from typing import List
import os


def log_interaction(
    session_name: str,
    user_text: str,
    assistant_text: str,
    file_ids: List[str],
    model: str,
    temperature: float,
    timestamp: datetime,
) -> None:
    os.makedirs("output", exist_ok=True)
    log_file = f"output/{session_name}_log.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n=== {timestamp.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(f"Model: {model} | Temperature: {temperature}\n")
        f.write(f"User:\n{user_text}\n\n")
        f.write(f"Assistant:\n{assistant_text}\n")
        if file_ids:
            f.write(f"Attached File ID(s): {', '.join(file_ids)}\n")
