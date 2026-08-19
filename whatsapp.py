import os
import requests

from dotenv import load_dotenv


load_dotenv()


WHATSAPP_TOKEN = os.getenv(
    "WHATSAPP_TOKEN"
)

PHONE_NUMBER_ID = os.getenv(
    "PHONE_NUMBER_ID"
)


def send_whatsapp_message(to, message):

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization":
            f"Bearer {WHATSAPP_TOKEN}",

        "Content-Type":
            "application/json"
    }


    data = {

        "messaging_product": "whatsapp",

        "to": to,

        "type": "text",

        "text": {
            "body": message
        }
    }


    response = requests.post(
        url,
        headers=headers,
        json=data
    )


    print(
        "WhatsApp Response:",
        response.text
    )


    return response.json()