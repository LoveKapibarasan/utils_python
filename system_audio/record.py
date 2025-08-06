import sounddevice as sd
import numpy as np
import queue
import soundfile as sf
import os

try:
    import lameenc
except ImportError:
    print("Please install lameenc: pip install lameenc")
    exit(1)

# Settings
SAMPLE_RATE = 44100
CHANNELS = 2
BLOCKSIZE = 1024
THRESHOLD = 0.01  # Silence threshold (RMS)
SILENCE_SECONDS = 2  # Skip if silence for this many seconds
OUTPUT_MP3 = "output.mp3"

q_audio = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    q_audio.put(indata.copy())

def record_audio():
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        blocksize=BLOCKSIZE,
        dtype='float32',  # Ensure correct dtype for RMS and encoding
        callback=audio_callback,
        # device=13  # Use PulseAudio or set to your monitor device if needed
    ):
        print("Recording... Press Ctrl+C to stop.")
        encoder = lameenc.Encoder()
        encoder.set_bit_rate(128)
        encoder.set_in_sample_rate(SAMPLE_RATE)
        encoder.set_channels(CHANNELS)
        encoder.set_quality(2)
        mp3_data = bytearray()

        silence_buffer = []
        silence_blocks = int(SILENCE_SECONDS * SAMPLE_RATE / BLOCKSIZE)
        silent = False

        try:
            while True:
                indata = q_audio.get()
                # Convert float32 [-1, 1] to int16 for MP3 encoding
                pcm16 = np.int16(np.clip(indata, -1, 1) * 32767)
                rms = np.sqrt(np.mean(indata**2))
                if rms < THRESHOLD:
                    silence_buffer.append(pcm16)
                    if len(silence_buffer) >= silence_blocks:
                        if not silent:
                            print("Silence detected, skipping...")
                            silent = True
                        continue
                else:
                    if silent:
                        print("Audio detected, resuming recording...")
                        silent = False
                    # Write any buffered non-silent audio
                    for buf in silence_buffer:
                        mp3_data += encoder.encode(buf.tobytes())
                    silence_buffer.clear()
                    mp3_data += encoder.encode(pcm16.tobytes())
        except KeyboardInterrupt:
            print("Stopping recording...")
        finally:
            # Flush encoder
            mp3_data += encoder.flush()
            with open(OUTPUT_MP3, "wb") as f:
                f.write(mp3_data)
            print(f"Saved to {OUTPUT_MP3}")

if __name__ == "__main__":
    record_audio()