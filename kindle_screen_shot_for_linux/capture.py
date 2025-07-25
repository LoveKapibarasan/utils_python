import pyscreenshot as ImageGrab
import time
import os
from pynput import keyboard

output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

capture_area = None  # Will hold (left, top, right, bottom) tuple

def ask_repeat_count():
    while True:
        try:
            return int(input("How many screenshots to take? "))
        except ValueError:
            print("Enter a valid integer.")

def grab_area_once():
    print("Please select the area to capture using the mouse...")
    img = ImageGrab.grab(bbox=None)
    bbox = img.getbbox()
    print(f"Area selected: {bbox}")
    return bbox

def capture_loop(bbox, count):
    for i in range(count):
        im = ImageGrab.grab(bbox=bbox)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(output_dir, f"screenshot_{i+1:03}_{timestamp}.png")
        im.save(filename)
        print(f"Saved: {filename}")
        time.sleep(2)  # Allow time for user to change page, etc.

def on_press(key):
    if key == keyboard.Key.f8:
        print("F8 pressed.")
        global capture_area
        capture_area = grab_area_once()
        count = ask_repeat_count()
        capture_loop(capture_area, count)
        print("Done. Press F8 again to repeat or Ctrl+C to exit.")

def main():
    print("Press F8 to start selecting an area and taking repeated screenshots.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
