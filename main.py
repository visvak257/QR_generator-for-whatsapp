from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse


app = FastAPI()

VERIFY_TOKEN = "visvak123"


@app.get("/")
def home():
    return {"message": "WhatsApp Ecommerce Backend is running"}


@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("MODE =", mode)
    print("TOKEN =", token)
    print("CHALLENGE =", challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verified")
        return PlainTextResponse(content=challenge, status_code=200)

    print("❌ Verification failed")
    return PlainTextResponse(
        content="Verification failed",
        status_code=403
    )

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    print("Incoming WhatsApp data:")
    print(data)

    return {"status": "received"}