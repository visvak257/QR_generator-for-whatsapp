from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import qrcode
import urllib.parse
import os

from products import products

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "WhatsApp Ecommerce Backend is running"
    }

@app.get("/products")
def get_products():
    return products


@app.get("/generate-qr/{product_id}")
def generate_qr(product_id: str):

    if product_id not in products:
        return {
            "error": "Product not found"
        }

    phone_number = "919080141931"

    message = f"Hi, I am interested in Product ID: {product_id}"

    encoded_message = urllib.parse.quote(message)

    whatsapp_url = (
        f"https://wa.me/{phone_number}"
        f"?text={encoded_message}"
    )

    os.makedirs("qr_codes", exist_ok=True)

    file_name = f"qr_codes/{product_id}.png"

    qr = qrcode.make(whatsapp_url)

    qr.save(file_name)

    return {
        "message": "QR generated successfully",
        "product_id": product_id,
        "product": products[product_id],
        "whatsapp_url": whatsapp_url,
        "qr_url": f"http://localhost:8000/view-qr/{product_id}"
    }


@app.get("/view-qr/{product_id}")
def view_qr(product_id: str):

    file_name = f"qr_codes/{product_id}.png"

    if not os.path.exists(file_name):
        return {
            "error": "QR not found. Generate QR first."
        }

    return FileResponse(
        file_name,
        media_type="image/png"
    )


from fastapi import Request
import os

from dotenv import load_dotenv


load_dotenv()


VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.get("/webhook")
async def verify_webhook(request: Request):

    mode = request.query_params.get(
        "hub.mode"
    )

    token = request.query_params.get(
        "hub.verify_token"
    )

    challenge = request.query_params.get(
        "hub.challenge"
    )


    if (
        mode == "subscribe"
        and
        token == VERIFY_TOKEN
    ):

        return int(challenge)


    return {
        "error": "Verification failed"
    }