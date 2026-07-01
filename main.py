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

            print("Received:")
            print(data)

            try:
                payload = json.loads(data)

                if payload.get("event") == "start":
                    print("Call started")

                elif payload.get("event") == "media":
    print("========== MEDIA EVENT ==========")
    print(json.dumps(payload, indent=2))

                elif payload.get("event") == "stop":
                    print("Call ended")
                    break

            except Exception as e:
                print("JSON parse error:", e)

    except WebSocketDisconnect:
        print("Exotel disconnected")

    except Exception as e:
        print("Error:", e)

    finally:
        try:
            await websocket.close()
        except:
            pass
