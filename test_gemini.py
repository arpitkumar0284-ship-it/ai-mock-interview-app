import os

import requests
from dotenv import load_dotenv

load_dotenv()  # .env file se key load karega

api_key = os.getenv("GEMINI_API_KEY")

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-flash-lite-latest:generateContent?key={api_key}"
)

payload = {
    "contents": [
        {"parts": [{"text": "Say hello in one short sentence."}]}
    ]
}

response = requests.post(url, json=payload)
data = response.json()

if "candidates" in data:
    print(data["candidates"][0]["content"]["parts"][0]["text"])
else:
    print("Error from Gemini:", data)