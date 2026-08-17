from fastapi import FastAPI
from fastapi.responses import FileResponse
import qrcode
import urllib.parse
import os

app = FastAPI()

# Sample product catalog
products = {
    "P001": {
        "name": "Smart Watch",
        "price": 3999,
        "description": "Fitness tracking smart watch"
    },
    "P002": {
        "name": "Running Shoes",
        "price": 2499,
        "description": "Lightweight sports running shoes"
    },
    "P003": {
        "name": "Travel Backpack",
        "price": 1499,
        "description": "Waterproof travel backpack"
    }
}

@app.get("/")
def home():
    return {"message": "WhatsApp Product QR Generator"}

@app.get("/products")
def get_products():
    return products

@app.get("/generate-qr/{product_id}")
def generate_qr(product_id: str):
    # Check whether the product exists
    if product_id not in products:
        return {"error": "Product not found"}

    # Your WhatsApp number
    phone_number = "country code with phone number (dont specify + symbol for country code)"

    # Message that customer will see
    message = f"Hi, I am interested in Product ID: {product_id}"

    # Convert message to URL format
    encoded_message = urllib.parse.quote(message)

    # Create WhatsApp link
    whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"

    # Create QR code
    qr = qrcode.make(whatsapp_url)

    # Create folder if it doesn't exist
    os.makedirs("qr_codes", exist_ok=True)

    # File name
    file_name = f"qr_codes/{product_id}.png"

    # Save QR
    qr.save(file_name)

    # Return product info + QR file path
    return {
        "message": "QR generated successfully",
        "product_id": product_id,
        "product": products[product_id],
        "whatsapp_url": whatsapp_url,
        "qr_file": file_name
    }

@app.get("/view-qr/{product_id}")
def view_qr(product_id: str):
    file_name = f"qr_codes/{product_id}.png"
    if not os.path.exists(file_name):
        return {"error": "QR code not found. Please generate it first."}
    return FileResponse(file_name, media_type="image/png")
