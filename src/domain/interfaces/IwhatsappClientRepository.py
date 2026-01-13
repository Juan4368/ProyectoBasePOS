from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IwhatsappClientRepository(ABC):
    @abstractmethod
    def send_message(self, recipient_id: str, message: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def send_buttons(
        self,
        recipient_id: str,
        body_text: str,
        buttons: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Envia un mensaje interactivo con botones de respuesta rapida.
        Cada boton debe contener keys: id y title.
        """
        ...
