#!/usr/bin/env python3
import os
import time
import subprocess


def run_cmd(cmd: list) -> str:
    """Run a shell command and return its output (stripped)."""
    return subprocess.check_output(cmd, text=True).strip()


def press_key(key: str):
    """Send key press using wtype."""
    # Map input to wtype key names if needed
    key_map = {
        "right": "Right",
        "left": "Left",
        "space": "space",
        "enter": "Return",
        "tab": "Tab",
        "esc": "Escape",
    }
    mapped_key = key_map.get(key, key)
    subprocess.run(["wtype", "-k", mapped_key])


def main():
    # Setup
    output_dir = "screenshots"
    os.makedirs(output_dir, exist_ok=True)

    # User inputs
    try:
        count = int(input("How many screenshots to take? "))
    except ValueError:
        print("❌ Invalid number, defaulting to 1.")
        count = 1

    key_input = input("Which key to press after each shot? (e.g., right, space, n): ").lower()

    # Region choice
    region_choice = input("Use full screen? (Y/n): ").strip().lower()
    region = None
    if region_choice == "n":
        print("👉 Select region with mouse...")
        region = run_cmd(["slurp"])
        print(f"Selected region: {region}")

    print("Starting in 12 seconds... prepare the window.")
    time.sleep(12)

    for i in range(1, count + 1):
        filename = os.path.join(output_dir, f"{i}.png")

        if region:
            subprocess.run(["grim", "-g", region, filename])
        else:
            subprocess.run(["grim", filename])

        print(f"✅ Saved: {filename}")

        press_key(key_input)

        time.sleep(5)


if __name__ == "__main__":
    main()
