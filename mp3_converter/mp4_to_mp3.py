import os
from moviepy import VideoFileClip

INPUT_FOLDER = r"input"
OUTPUT_FOLDER = r"MP3"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".mp4"):
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_filename = os.path.splitext(filename)[0] + ".mp3"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        try:
            video = VideoFileClip(input_path)
            video.audio.write_audiofile(output_path)
            video.close()
        except Exception as e:
            print(f"Error processing {filename}: {e}")
