from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# 🔴 TEMP: Hardcode key just to confirm API works
GEMINI_API_KEY = "AIzaSyAxxobUWoD-PHeYy1Zx3pB8b0P7kol2Jg0"

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent"
)

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": req.message}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(
        GEMINI_URL,
        headers=headers,
        params={"key": GEMINI_API_KEY},
        json=payload
    )

    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

    try:
        result = r.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        reply = "⚠️ Error from Gemini API."

    return ChatResponse(reply=reply)
