from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from groq import Groq
import os
import json

app = FastAPI()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.get("/")
async def root():
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": "Say hello in one sentence"
                }
            ]
        )

        return {
            "groq_status": "connected",
            "reply": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "groq_status": "failed",
            "error": str(e)
        }


@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()

    print("Exotel connected")

    try:
        while True:
            data = await websocket.receive_text()

            payload = json.loads(data)

            event = payload.get("event")

            print("EVENT:", event)

            if event == "connected":
                print("WEBSOCKET CONNECTED")

            elif event == "start":
                print("CALL STARTED")

            elif event == "media":
                media = payload.get("media", {})
                print("MEDIA OBJECT:")
                print(media)

            elif event == "stop":
                print("CALL ENDED")
                break

    except WebSocketDisconnect:
        print("Exotel disconnected")

    except Exception as e:
        print("ERROR:", str(e))

    finally:
        try:
            await websocket.close()
        except:
            pass
