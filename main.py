from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


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


@app.post("/create-call")
def create_call(order: OrderData):

    print("========== NEW ORDER ==========")
    print("ORDER ID:", order.order_id)
    print("CUSTOMER:", order.customer_name)
    print("PHONE:", order.phone)
    print("AMOUNT:", order.amount)
    print("ADDRESS:", order.address)
    print("CITY:", order.city)
    print("STATE:", order.state)
    print("PINCODE:", order.pincode)

    for product in order.products:
        print(
            f"PRODUCT: {product.name} "
            f"QTY:{product.quantity} "
            f"PRICE:{product.price}"
        )

    return {
        "success": True,
        "message": "Order received successfully"
    }
