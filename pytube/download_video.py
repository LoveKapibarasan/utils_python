from pytube import YouTube
import os

# Replace with your target YouTube URL
url = input("Input an url.")

# Create YouTube object
yt = YouTube(url)

# Get the highest resolution progressive stream (contains both video and audio)
stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

# Define output directory
output_dir = 'output'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Download the video to the output folder
stream.download(output_path=output_dir, filename='video.mp4')

# create output folder
os.mkdir()

# Download to current directory (or specify path)
stream.download(output_path='.', filename='output/video.mp4')

print("Download complete!")
