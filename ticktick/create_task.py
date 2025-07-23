import requests
import datetime
import pytz
from dotenv import load_dotenv
import os

load_dotenv()

file_path = r"input.csv"
load_dotenv()

token = os.getenv("TICKTICK_ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

url = "https://api.ticktick.com/open/v1/task"


def send_task(title, content, priority, start_date, end_date):
    berlin = pytz.timezone("Europe/Berlin")

    # Ensure datetime is timezone-aware
    if start_date.tzinfo is None:
        start_date = berlin.localize(start_date)
    if end_date.tzinfo is None:
        end_date = berlin.localize(end_date)

    # Format datetime as string
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S%z')
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S%z')

    print("time_data", start_date_str, end_date_str)

    payload = {
        "title": title,
        "content": content,
        "startDate": start_date_str,
        "dueDate": end_date_str,
        "timeZone": "Europe/Berlin",
        "priority": int(priority)
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    response.raise_for_status()
    created_task = response.json()
    print("Created Task ID:", created_task["id"])
    print("Created Task Title:", created_task["title"])


def create_task():
    global f, priority
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()

        # Search for "<start>"
        start_index = None
        for idx, line in enumerate(lines):
            if line.strip() == "<start>":
                start_index = idx
                break

        if start_index is None:
            raise ValueError("No <start> found!")

        # Remove "<start>"
        lines = [line for line in lines if line.strip() != "<start>"]

        # Process only lines after "<start>"
        tasks_to_process = lines[start_index:]

        for line in tasks_to_process:
            task = line.replace(r"(", "").replace(r")", "").split(",")
            if len(task) < 5:
                print(f"Invalid line skipped: {line}")
                continue

            title = task[0].strip()
            content_text = task[1].strip()
            priority = task[2].strip()
            start_date = datetime.datetime.strptime(task[3].strip(), "%Y-%m-%d %H:%M")
            end_date = datetime.datetime.strptime(task[4].strip(), "%Y-%m-%d %H:%M")

            send_task(title, content_text, priority, start_date, end_date)

        f.seek(0)
        f.write("\n".join(lines) + "\n<start>")
        f.truncate()

if __name__ == "__main__":
    create_task()
