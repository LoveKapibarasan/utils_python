# temperature.py
def prompt_temperature(default: float = 0.7) -> float:
    raw = input(f"🌡️ Enter temperature (default = {default}): ").strip()
    if not raw:
        return default
    try:
        val = float(raw)
        # Optional: clamp to [0, 2] per common guidance
        if val < 0:
            val = 0.0
        if val > 2:
            val = 2.0
        return val
    except ValueError:
        print(f"❌ Invalid temperature, using default {default}")
        return default
