from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from groq import Groq
import os
import json
import base64

app = FastAPI()

# -------------------------------
# GROQ INITIALIZATION
# -------------------------------

groq_api_key = os.getenv("GROQ_API_KEY")

groq_client = None
if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)

# -------------------------------
# ROOT ENDPOINT
# -------------------------------

@app.get("/")
async def root():
    return {
        "status": "running",
        "groq": "connected" if os.getenv("GROQ_API_KEY") else "missing",
        "deepgram": "connected" if os.getenv("DEEPGRAM_API_KEY") else "missing"
    }

# -------------------------------
# TEST GROQ
# -------------------------------

@app.get("/test-groq")
async def test_groq():

    if not groq_client:
        return {
            "status": "failed",
            "error": "GROQ_API_KEY missing"
        }

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

# -------------------------------
# EXOTEL WEBSOCKET
# -------------------------------

@app.websocket("/stream")
async def stream(websocket: WebSocket):

    await websocket.accept()

    print("========== EXOTEL CONNECTED ==========")

    stream_sid = None

    try:

        while True:

            data = await websocket.receive_text()

            print("RAW DATA RECEIVED")

            try:

                payload = json.loads(data)

                event = payload.get("event", "unknown")

                print(f"EVENT: {event}")

                # -----------------------
                # CONNECTED EVENT
                # -----------------------

                if event == "connected":
                    print("STREAM CONNECTED")

                # -----------------------
                # START EVENT
                # -----------------------

                elif event == "start":

                    print("CALL STARTED")

                    stream_sid = payload.get("stream_sid")

                    print("STREAM SID:", stream_sid)

                    try:

                        with open("hello.raw", "rb") as audio_file:
                            audio_bytes = audio_file.read()

                        response = {
                            "event": "media",
                            "stream_sid": stream_sid,
                            "media": {
                                "payload": base64.b64encode(
                                    audio_bytes
                                ).decode("ascii")
                            }
                        }

                        await websocket.send_text(
                            json.dumps(response)
                        )

                        print(
                            "HELLO AUDIO SENT TO EXOTEL SUCCESSFULLY"
                        )

                    except Exception as audio_error:
                        print(
                            f"AUDIO SEND ERROR: {str(audio_error)}"
                        )

                # -----------------------
                # MEDIA EVENT
                # -----------------------

                elif event == "media":

                    media = payload.get("media", {})

                    audio_payload = media.get("payload")

                    print("MEDIA OBJECT RECEIVED")

                    if audio_payload:
                        print(
                            f"AUDIO PAYLOAD LENGTH: {len(audio_payload)}"
                        )
                    else:
                        print("EMPTY AUDIO PAYLOAD")

                # -----------------------
                # STOP EVENT
                # -----------------------

                elif event == "stop":

                    print("STOP EVENT RECEIVED")
                    print("EXOTEL ENDED THE CALL")

                    break

                # -----------------------
                # UNKNOWN EVENT
                # -----------------------

                else:
                    print(f"UNKNOWN EVENT: {event}")

            except json.JSONDecodeError:
                print("INVALID JSON RECEIVED")

            except Exception as inner_error:
                print(
                    f"EVENT PROCESSING ERROR: {str(inner_error)}"
                )

    except WebSocketDisconnect:
        print("EXOTEL DISCONNECTED")

    except Exception as outer_error:
        print(
            f"WEBSOCKET SERVER ERROR: {str(outer_error)}"
        )

    finally:

        print("WEBSOCKET SESSION FINISHED")

        try:
            await websocket.close()
        except:
            pass
