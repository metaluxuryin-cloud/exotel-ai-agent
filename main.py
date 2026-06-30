from fastapi import FastAPI, WebSocket
import json
import os
from groq import Groq

app = FastAPI()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.get("/")
async def root():
    return {
        "status": "AI Agent Running",
        "service": "Exotel AgentStream"
    }

@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            event = json.loads(data)

            print("Received:", event)

    except Exception as e:
        print(e)

    try:
    await websocket.close()
except:
    pass
