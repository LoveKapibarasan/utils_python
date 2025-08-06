import os
import time
import csv
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
if not api_key:
    raise ValueError("❌ OPEN_API_KEY not found in .env")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# 📂 CSV file to store uploaded file IDs
RECORD_FILE = "file_id_record.csv"

# 📄 Create file_id_record.csv if it doesn't exist
def ensure_file_id_record():
    if not os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file_id"])

# 🚀 Upload file with proper error handling
def upload_file(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ File not found: {path}")
    
    print("📤 Uploading file...")
    try:
        upload = client.files.create(
            file=open(path, "rb"),
            purpose="assistants"
        )
        print(f"✅ Uploaded File ID: {upload.id}")
        return upload.id
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        raise

# ✍️ Append file_id to CSV log
def record_file_id(file_id):
    with open(RECORD_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([file_id])

# 👟 Main workflow
if __name__ == "__main__":
    while True:
        ensure_file_id_record()
        file_path = input("📎 Enter the path to the file to upload: ").strip()
    
        if not file_path:
            print("❌ No file path provided.")
            exit(1)

        try:
            file_id = upload_file(file_path)
            record_file_id(file_id)
        except Exception:
            print("💥 Operation aborted due to error.")
        if input("🔄 Upload another file? (yes/no): ").strip().lower() != "yes":
            print("👋 Exiting.")
            break