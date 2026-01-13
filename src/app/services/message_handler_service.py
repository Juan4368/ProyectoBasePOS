from typing import Optional

from src.domain.dtos.clienteDto import ClienteRequest
from src.domain.interfaces.IwhatsappClientRepository import IwhatsappClientRepository
from src.domain.services.cliente_service import ClienteService


class MessageHandlerService:
    """
    Servicio simple para enviar mensajes de texto a traves de un cliente de WhatsApp.
    """

    def __init__(
        self,
        whatsapp_client: Optional[IwhatsappClientRepository] = None,
        cliente_service: Optional[ClienteService] = None,
    ):
        self.whatsapp_client = whatsapp_client
        self.cliente_service = cliente_service

    def set_cliente_service(self, cliente_service: ClienteService) -> None:
        self.cliente_service = cliente_service

    def send_text(self, recipient_id: str, message: str) -> dict:
        if self.whatsapp_client is None:
            raise RuntimeError("WhatsApp client no configurado")
        return self.whatsapp_client.send_message(recipient_id, message)

    async def send_menu(self, recipient_id: str) -> dict:
        """
        Envia un menu basico de opciones con botones.
        """
        if self.whatsapp_client is None:
            raise RuntimeError("WhatsApp client no configurado")

        body = "*Menu*\nElige una opcion:"
        buttons = [
            {"id": "crear_cliente", "title": "Crear cliente"},
        ]

        # Intentar usar botones; si no existe el metodo, degradar a texto.
        send_buttons = getattr(self.whatsapp_client, "send_buttons", None)
        if callable(send_buttons):
            return send_buttons(recipient_id, body, buttons)


    def is_greeting(self, message: str) -> bool:
        """
        Devuelve True si el texto coincide exactamente con un saludo conocido.
        """
        if not message:
            return False
        normalized = message.strip().lower()
        greetings = {"hola", "hello", "hi", "buenas tardes"}
        return normalized in greetings

    def create_cliente_from_text(self, message: str) -> dict:
        """
        Crea un cliente a partir de hasta 3 lineas: nombre, telefono, email.
        """
        if self.cliente_service is None:
            raise RuntimeError("Cliente service no configurado")

        lines = [ln.strip() for ln in message.splitlines() if ln.strip()] or [message.strip()]
        nombre = lines[0] if lines else ""
        telefono = lines[1] if len(lines) > 1 else None
        email = lines[2] if len(lines) > 2 else None

        if not nombre:
            raise ValueError("El nombre es obligatorio para crear el cliente.")

        payload = ClienteRequest(nombre=nombre, telefono=telefono, email=email)
        created = self.cliente_service.create_cliente(payload)
        return {"status": "handled", "type": "cliente_created", "id": created.id, "nombre": created.nombre}

    async def handle_incoming_message(self, message: str, sender_info: dict) -> dict:
        """
        Maneja un mensaje entrante. Detecta atajos (+, -, A) y saludos.
        """
        if not message:
            return {"status": "ignored", "reason": "empty_message"}

        normalized_text = message.strip()
        sender_id = sender_info.get("id") if sender_info else None
        sender_name = sender_info.get("name") if sender_info else None

        # Atajos simples
        if normalized_text in {"+", "-"}:
            return {
                "status": "handled",
                "type": "shortcut",
                "shortcut": normalized_text,
                "recipient": sender_id,
            }

        if normalized_text.upper() == "A":
            if self.whatsapp_client and sender_id:
                await self.send_menu(sender_id)
            return {
                "status": "handled",
                "type": "shortcut",
                "shortcut": "A",
                "recipient": sender_id,
            }

        # Saludo
        if self.is_greeting(normalized_text):
            reply = f"Hola {sender_name}".strip() if sender_name else "Hola"
            if self.whatsapp_client and sender_id:
                self.send_text(sender_id, reply)
            return {"status": "handled", "type": "greeting", "recipient": sender_id}

        # Intento de creacion de cliente via texto multilinea
        if "\n" in message and self.cliente_service:
            try:
                result = self.create_cliente_from_text(message)
                if self.whatsapp_client and sender_id:
                    self.send_text(
                        sender_id,
                        f"Cliente creado: {result['nombre']}.",
                    )
                return result
            except Exception as exc:
                if self.whatsapp_client and sender_id:
                    self.send_text(sender_id, f"No se pudo crear el cliente: {exc}")
                return {"status": "error", "type": "cliente", "error": str(exc)}

        return {"status": "ignored", "type": "unknown", "recipient": sender_id}

    async def handleIncomingMessage(self, message: str, senderInfo: dict) -> dict:
        """
        Alias en estilo camelCase que delega en handle_incoming_message.
        """
        return await self.handle_incoming_message(message, senderInfo)

    async def sendMenu(self, recipient_id: str) -> dict:
        """
        Alias en camelCase para send_menu.
        """
        return await self.send_menu(recipient_id)
