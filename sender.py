import requests
import os
from dotenv import load_dotenv
load_dotenv()

def send_to_api(data):
    url = os.getenv("API_URL")
    try:
        res = requests.post(url, json=data)
        print("Status kirim:", res.status_code, res.text)
    except Exception as e:
        print("[SEND ERROR]", e)
