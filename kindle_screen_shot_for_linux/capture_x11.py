import time
import os
from PIL import Image
import mss
from pynput.keyboard import Controller, Key

# Setup
output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

# User inputs
count = int(input("How many screenshots to take? "))
key_input = input("Which key to press after each shot? (e.g., right, space, n): ").lower()

# Map special keys
special_keys = {
    "right": Key.right,
    "left": Key.left,
    "space": Key.space,
    "enter": Key.enter,
    "tab": Key.tab,
    "esc": Key.esc
}
key_to_press = special_keys.get(key_input, key_input)

# Region input
region_choice = input("Use full screen? (Y/n): ").strip().lower()
monitor = None

with mss.mss() as sct:
    if region_choice == 'n':
        try:
            left = int(input("Left: "))
            top = int(input("Top: "))
            width = int(input("Width: "))
            height = int(input("Height: "))
            monitor = {"left": left, "top": top, "width": width, "height": height}
        except ValueError:
            print("❌ Invalid input. Falling back to full screen.")
            monitor = sct.monitors[1]
    else:
        monitor = sct.monitors[1]

    print("Starting in 12 seconds... Please prepare the window.")
    time.sleep(12)

    keyboard = Controller()
    for i in range(1, count + 1):
        img = sct.grab(monitor)
        img_pil = Image.frombytes("RGB", img.size, img.rgb)

        filename = os.path.join(output_dir, f"{i}.png")
        img_pil.save(filename)
        print(f"✅ Saved: {filename}")

        keyboard.press(key_to_press)
        keyboard.release(key_to_press)

        time.sleep(5)
