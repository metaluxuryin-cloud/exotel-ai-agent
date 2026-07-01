from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from groq import Groq
import os
import json

app = FastAPI()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


@app.get("/")
async def root():
    return {
        "status": "running",
        "groq": "connected" if os.getenv("GROQ_API_KEY") else "missing",
        "deepgram": "connected" if os.getenv("DEEPGRAM_API_KEY") else "missing"
    }


@app.get("/test-groq")
async def test_groq():
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": "Reply with only OK"
                }
            ]
        )

        return {
            "status": "success",
            "reply": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }


@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()

    print("Exotel connected")

    try:
        while True:
            data = await websocket.receive_text()

            try:
                payload = json.loads(data)

                event = payload.get("event")

                print("EVENT:", event)

                if event == "connected":
                    print("STREAM CONNECTED")

                elif event == "start":
                    print("CALL STARTED")

               elif event == "media":
    media = payload.get("media", {})

    payload_audio = media.get("payload")

    print("AUDIO RECEIVED")
    print("Payload length:", len(payload_audio))

                elif event == "stop":
                    print("CALL ENDED")
                    break

            except Exception as e:
                print("JSON ERROR:", str(e))

    except WebSocketDisconnect:
        print("Exotel disconnected")

    except Exception as e:
        print("SERVER ERROR:", str(e))

    finally:
        try:
            await websocket.close()
        except:
            pass
