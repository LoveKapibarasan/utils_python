from pynput import keyboard
import subprocess, os, time

display = os.environ.get("DISPLAY", ":0")
AUDIO_SOURCE = "Virtual_Sink.monitor"  # must exist

def wait_for_source(name, timeout=5):
    t0 = time.time()
    while time.time() - t0 < timeout:
        out = subprocess.check_output(["pactl", "list", "short", "sources"], text=True)
        if any(name in line.split()[1] for line in out.splitlines()):
            return True
        time.sleep(0.2)
    return False

ffmpeg_cmd = [
    "ffmpeg",
    "-hide_banner", "-loglevel", "warning",
    "-nostdin", "-y",
    "-f", "x11grab", "-framerate", "30", "-i", display,
    "-f", "pulse", "-thread_queue_size", "1024", "-i", AUDIO_SOURCE,
    "-map", "0:v:0", "-map", "1:a:0",
    "-vcodec", "libx264", "-preset", "ultrafast",
    "-acodec", "aac",
    "-movflags", "+faststart",
    "output_fullscreen.mp4"
]

process = None
current_keys = set()
START_KEYS = {keyboard.Key.ctrl, keyboard.Key.alt, keyboard.KeyCode.from_char('r')}
STOP_KEYS  = {keyboard.Key.ctrl, keyboard.Key.alt, keyboard.KeyCode.from_char('s')}

def on_press(key):
    global process
    current_keys.add(key)
    if START_KEYS.issubset(current_keys) and process is None:
        if not wait_for_source(AUDIO_SOURCE, 5):
            print(f"Audio source {AUDIO_SOURCE} not found.")
            return
        print("録画開始")
        process = subprocess.Popen(ffmpeg_cmd)

    if STOP_KEYS.issubset(current_keys) and process:
        print("録画終了")
        process.terminate()
        process = None
        return False

def on_release(key):
    current_keys.discard(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Ctrl+Alt+R で録画開始、Ctrl+Alt+S で録画停止")
    listener.join()
