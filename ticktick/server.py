from flask import Flask, request
import requests
from dotenv import load_dotenv
import os



app = Flask(__name__)

load_dotenv()
REDIRECT_URI = "http://localhost:5000/callback"
CLIENT_ID = os.getenv("TICKTICK_CLIENT_ID")
CLIENT_SECRET = os.getenv("TICKTICK_CLIENT_SECRET")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    print("Authorization code:", code)
    token = exchange_token(code)
    print("Access token:", token)
    return "Success!"

def exchange_token(code):
    resp = requests.post("https://ticktick.com/oauth/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

if __name__ == "__main__":
    app.run(port=5000)
