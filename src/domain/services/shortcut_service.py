from __future__ import annotations
from typing import Optional


class ShortcutService:
    """
    Reglas de negocio para los atajos de mensajes recibidos (+/-).
    """

    def __init__(self, shortcuts: Optional[dict[str, str]] = None):
        self.shortcuts = shortcuts or {
            "I": "Cual es el monto del ingreso de dinero.",
            "S": "Cual es el monto de la salida de dinero.",
        }
        # Solo este numero puede disparar el atajo protegido para categorias.
        # Se valida usando los ultimos digitos para tolerar prefijos (e.g. 57, +57).
        self.allowed_category_senders = {"3004356388"}

    def get_reply_for_shortcut(
        self, text: str, sender: Optional[str] = None
    ) -> Optional[str]:
        """
        Devuelve el mensaje de respuesta si el texto coincide con un atajo conocido.
        """
        if text is None:
            return None
        normalized = text.strip()

        # Responde solo a los atajos basicos (I/S). El atajo A se maneja en el webhook.
        return self.shortcuts.get(normalized)

    def is_allowed_category_sender(self, sender: Optional[str]) -> bool:
        """
        Valida si el remitente puede ejecutar el atajo protegido de categorias.
        """
        if not sender:
            return False

        # Extrae solo digitos para tolerar formatos como "573004356388" o "+57...".
        digits = "".join(ch for ch in sender if ch.isdigit())
        if not digits:
            return False

        # Considera valido si termina con alguno de los numeros permitidos.
        return any(digits.endswith(allowed) for allowed in self.allowed_category_senders)
