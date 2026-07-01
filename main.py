from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import os
import base64
import wave

app = FastAPI()


@app.get("/")
async def root():
    return {
        "status": "running"
    }


@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()

    print("========== EXOTEL CONNECTED ==========")

    try:
        while True:
            data = await websocket.receive_text()

            payload = json.loads(data)

            event = payload.get("event")

            print("EVENT:", event)

            if event == "connected":
                print("STREAM CONNECTED")

            elif event == "start":
                print("CALL STARTED")

                with wave.open("hello.wav", "rb") as wav_file:
                    audio_data = wav_file.readframes(
                        wav_file.getnframes()
                    )

                chunk_size = 320

                for i in range(0, len(audio_data), chunk_size):
                    chunk = audio_data[i:i + chunk_size]

                    message = {
                        "event": "media",
                        "media": {
                            "payload": base64.b64encode(
                                chunk
                            ).decode("utf-8")
                        }
                    }

                    await websocket.send_text(
                        json.dumps(message)
                    )

                print("HELLO AUDIO SENT")

            elif event == "media":
                pass

            elif event == "stop":
                print("CALL ENDED")

    except WebSocketDisconnect:
        print("EXOTEL DISCONNECTED")

    except Exception as e:
        print("ERROR:", str(e))

    finally:
        print("SESSION CLOSED")
