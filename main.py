from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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

    print("Exotel connected")

    try:
        while True:
            data = await websocket.receive_text()

            try:
                payload = json.loads(data)

                event = payload.get("event")
                print("EVENT:", event)

                if event == "media":
                    media = payload.get("media", {})
                    print("MEDIA OBJECT:")
                    print(media)

                elif event == "start":
                    print("CALL STARTED")

                elif event == "stop":
                    print("CALL ENDED")
                    break

            except Exception as e:
                print("JSON ERROR:", e)

    except WebSocketDisconnect:
        print("Exotel disconnected")

    except Exception as e:
        print("SERVER ERROR:", e)

    finally:
        try:
            await websocket.close()
        except:
            pass
