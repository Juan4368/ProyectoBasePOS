import logging

import requests

from domain.interfaces.IwhatsappClientRepository import IwhatsappClientRepository

logger = logging.getLogger("whatsapp_client")


class WhatsAppClient(IwhatsappClientRepository):
    def __init__(self, api_url: str, token: str):
        # api_url debe ser https://graph.facebook.com/v22.0/<PHONE_NUMBER_ID>
        self.api_url = api_url.rstrip("/")
        self.token = token

    def send_message(self, recipient_id: str, message: str):
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {"body": message},
        }
        response = requests.post(
            f"{self.api_url}/messages",
            json=payload,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10,
        )
        logger.info(
            "WhatsApp API response status=%s body=%s",
            response.status_code,
            response.text,
        )
        response.raise_for_status()
        return response.json()

    def send_buttons(self, recipient_id: str, body_text: str, buttons):
        # buttons es una lista de dicts con id y title
        mapped = [
            {"type": "reply", "reply": {"id": btn["id"], "title": btn["title"]}}
            for btn in buttons
        ][:3]  # WhatsApp permite max 3

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": mapped},
            },
        }
        response = requests.post(
            f"{self.api_url}/messages",
            json=payload,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10,
        )
        logger.info(
            "WhatsApp API response status=%s body=%s",
            response.status_code,
            response.text,
        )
        response.raise_for_status()
        return response.json()
