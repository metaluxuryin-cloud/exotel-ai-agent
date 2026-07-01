from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import base64

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

    print("Exotel connected")

    try:
        while True:
            data = await websocket.receive_text()

            payload = json.loads(data)

            event = payload.get("event")

            print(f"EVENT: {event}")

            if event == "start":
                print("CALL STARTED")

            elif event == "media":
                media = payload.get("media", {})

                audio_payload = media.get("payload")

                if audio_payload:
                    audio_bytes = base64.b64decode(audio_payload)

                    print("Audio bytes length:", len(audio_bytes))
                    print("First 20 bytes:", audio_bytes[:20])

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
