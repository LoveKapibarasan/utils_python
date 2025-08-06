# System Audio Recording on Linux (Ubuntu) - How To

## 1. Install Required Packages

```bash
sudo apt update
sudo apt install libportaudio2 pavucontrol pulseaudio-utils
pip install sounddevice numpy lameenc
```

## 2. Set Up a Virtual Sink for System Audio Capture

Create a virtual (silent) audio sink using PulseAudio:

```bash
pactl load-module module-null-sink sink_name=Virtual_Sink sink_properties=device.description=Virtual_Sink
```

This creates a new output device called `Virtual_Sink` and a corresponding input source called `Monitor of Virtual_Sink`.

## 3. Open pavucontrol

Start the PulseAudio Volume Control GUI:

```bash
pavucontrol
```

### pavucontrol Settings

- **Playback Tab:**  
  - Play your system audio (e.g., YouTube, music player).
  - Find your audio application in the list.
  - Change its output device to `Virtual_Sink`.  
    *Result: No sound will come from your speakers; audio is routed to the virtual sink.*

- **Recording Tab:**  
  - Start your Python recording script.
  - Find your script (e.g., "python3" or "python") in the list.
  - Change its input source to `Monitor of Virtual_Sink`.  
    *Result: Your script will record the digital system audio, not microphone or speaker output.*

- **Output Devices Tab:**  
  - You should see `Virtual_Sink` listed.  
    You can adjust its volume if needed.

- **Input Devices Tab:**  
  - You should see `Monitor of Virtual_Sink` listed.  
    This is what your script should be recording from.

## 4. Run Your Python Script

- Use the default device in your script (do not set a device index).
- The script will record whatever is routed to `Monitor of Virtual_Sink`.

## 5. Stop and Unload the Virtual Sink (Optional)

To remove the virtual sink after you're done:

```bash
pactl unload-module module-null-sink
```

---

## Troubleshooting

- If you do not see `Virtual_Sink` or its monitor in pavucontrol, make sure the `pactl load-module ...` command succeeded.
- If you hear no sound, check that your audio application's output is set to `Virtual_Sink`.
- If your script records silence, check that its input is set to `Monitor of Virtual_Sink` in the Recording tab.

---

**This method allows you to record system audio digitally and silently on Linux, without using the microphone or