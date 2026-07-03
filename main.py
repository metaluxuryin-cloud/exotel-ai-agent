from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import requests

app = FastAPI()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")
PHONE_ID = os.getenv("ELEVENLABS_PHONE_ID")


class Product(BaseModel):
    name: str
    quantity: int
    price: float


class OrderData(BaseModel):
    order_id: int
    customer_name: str
    phone: str
    amount: float
    address: str
    city: str
    state: str
    pincode: str
    products: List[Product]


@app.get("/")
def home():
    return {
        "status": "running",
        "service": "MetaLuxury AI Backend"
    }


@app.get("/test-call")
def test_call():

    payload = {
        "call_name": "MetaLuxury Test Call",
        "agent_id": AGENT_ID,
        "agent_phone_number_id": PHONE_ID,
        "recipients": [
            {
                "phone_number": "+917990403189",
                "conversation_initiation_client_data": {
                    "dynamic_variables": {
                        "customer_name": "Jagrut",
                        "product_name": "Test Product",
                        "size": "UK 9",
                        "quantity": "1",
                        "amount": "999",
                        "address": "Surat Gujarat"
                    }
                }
            }
        ]
    }

    response = requests.post(
        "https://api.elevenlabs.io/v1/convai/batch-calling/submit",
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        },
        json=payload
    )

    return {
        "status_code": response.status_code,
        "response": response.json()
    }


@app.post("/create-call")
def create_call(order: OrderData):

    return {
        "success": True,
        "message": "WooCommerce integration comes next"
    }
