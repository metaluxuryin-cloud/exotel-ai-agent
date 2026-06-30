from fastapi import FastAPI, WebSocket
import json

app = FastAPI()

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

            print("Received event:", event.get("event"))

            if event.get("event") == "connected":
                print("Exotel Connected")

            elif event.get("event") == "start":
                print("Call Started")

            elif event.get("event") == "media":
                print("Audio Packet Received")

            elif event.get("event") == "stop":
                print("Call Ended")
                break

    except Exception as e:
        print("Error:", e)

    await websocket.close()
