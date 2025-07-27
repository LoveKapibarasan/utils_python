# Full Screen Screenshot Automation Tool (X11)

This tool repeatedly captures full-screen screenshots and presses a key (like `right` or `space`) after each shot. Useful for automating page turns in eBooks or presentations.

## Setup

* Run measure_size to know an exact document size.

```bash
pip install -r requirements.txt
sudo apt install python3-tk
```

✅ You must be running **X11** (not Wayland). Check with:

```bash
echo $XDG_SESSION_TYPE
```

## Run

```bash
python screenshot_tool.py
```

Press `Ctrl+C` to cancel early. Screenshots will be saved in the `screenshots/` folder.
