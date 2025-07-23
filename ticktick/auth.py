import webbrowser
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("TICKTICK_CLIENT_ID")
REDIRECT_URI = "http://localhost:5000/callback"
AUTH_URL = "https://ticktick.com/oauth/authorize"
STATE = "random_string"

params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": "tasks:read tasks:write",
    "state": STATE,
}

url = AUTH_URL + "?" + urllib.parse.urlencode(params)
print("Open in browser:", url)
webbrowser.open(url)
