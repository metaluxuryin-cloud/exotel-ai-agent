from fastapi import FastAPI
from groq import Groq
import os

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
