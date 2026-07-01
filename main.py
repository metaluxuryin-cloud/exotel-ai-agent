from fastapi import FastAPI
from groq import Groq
import os

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
