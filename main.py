from fastapi ,deepgram import FastAPI, WebSocket, WebSocketDisconnect ,DeepgramClient
import json
import base64
import wave

app = FastAPI()
deepgram = DeepgramClient(
    os.getenv("DEEPGRAM_API_KEY")
)

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "Exotel Voicebot Test"
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

            # ----------------------------------
            # CONNECTED EVENT
            # ----------------------------------

            if event == "connected":
                print("STREAM CONNECTED")

            # ----------------------------------
            # START EVENT
            # ----------------------------------

            elif event == "start":

                print("CALL STARTED")

                try:

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

                except Exception as audio_error:
                    print(
                        "AUDIO ERROR:",
                        str(audio_error)
                    )

            # ----------------------------------
            # CUSTOMER AUDIO
            # ----------------------------------

            elif event == "media":

                media = payload.get(
                    "media",
                    {}
                )

                audio_payload = media.get(
                    "payload"
                )

                if audio_payload:

                    print(
                        "CUSTOMER SPEAKING"
                    )

                    print(
                        "PAYLOAD SIZE:",
                        len(audio_payload)
                    )

            # ----------------------------------
            # STOP EVENT
            # ----------------------------------

            elif event == "stop":

                print(
                    "CALL ENDED"
                )

                break

            else:

                print(
                    "UNKNOWN EVENT:",
                    event
                )

    except WebSocketDisconnect:

        print(
            "EXOTEL DISCONNECTED"
        )

    except Exception as e:

        print(
            "SERVER ERROR:",
            str(e)
        )

    finally:

        print(
            "SESSION CLOSED"
        )
