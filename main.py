from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from whatsapp_service import send_whatsapp_message


app = FastAPI()

VERIFY_TOKEN = "visvak123"


@app.get("/")
def home():
    return {
        "message": "WhatsApp Ecommerce Backend is running"
    }


@app.get("/webhook")
async def verify_webhook(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("MODE =", mode)
    print("TOKEN =", token)
    print("CHALLENGE =", challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified")

        return PlainTextResponse(
            content=str(challenge),
            status_code=200
        )

    print("Verification failed")

    return PlainTextResponse(
        content="Verification failed",
        status_code=403
    )


@app.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    print("========== INCOMING WHATSAPP ==========")
    print(data)
    print("=======================================")

    try:

        value = (
            data["entry"][0]
            ["changes"][0]
            ["value"]
        )

        # Ignore delivery/read/status webhooks
        if "messages" not in value:
            print("No incoming message")
            return {"status": "ignored"}

        message = value["messages"][0]

        sender = message["from"]

        print("Sender:", sender)

        # Only handle text for now
        if message.get("type") == "text":

            text = message["text"]["body"]

            print("Customer message:", text)

            reply = f"You sent: {text}"

            send_whatsapp_message(
                sender,
                reply
            )

    except Exception as e:
        print("Webhook error:", str(e))

    return {"status": "received"}