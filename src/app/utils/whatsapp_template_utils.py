from typing import Any, Iterable, List, Optional


class WhatsAppTemplateUtils:
    """
    Utilidades asincronas para construir payloads de listas (mensajes interactivos) de WhatsApp Cloud.
    Todas las funciones devuelven dicts listos para enviarse al endpoint /messages.
    """

    @staticmethod
    async def build_list_message(
        to: str,
        body_text: str,
        button_text: str,
        sections: List[dict],
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None,
    ) -> dict:
        """
        Crea un payload de mensaje interactivo tipo lista.
        - to: wa_id del destinatario.
        - body_text: texto principal de la lista.
        - button_text: texto del boton que abre la lista.
        - sections: lista de secciones con filas, cada seccion: {"title": str, "rows": [{"id": str, "title": str, "description": Optional[str]}]}.
        - header_text y footer_text son opcionales.
        """
        interactive: dict[str, Any] = {
            "type": "list",
            "body": {"text": body_text},
            "action": {
                "button": button_text,
                "sections": sections,
            },
        }
        if header_text:
            interactive["header"] = {"type": "text", "text": header_text}
        if footer_text:
            interactive["footer"] = {"text": footer_text}

        return {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": interactive,
        }

    @staticmethod
    async def build_sections_from_items(
        items: Iterable[Any],
        *,
        section_title: str = "Opciones",
        id_attr: str = "id",
        title_attr: str = "title",
        description_attr: Optional[str] = None,
    ) -> List[dict]:
        """
        Genera una unica seccion de filas a partir de un iterable de objetos/dicts.
        - section_title: titulo de la seccion.
        - id_attr/title_attr/description_attr: nombres de los atributos o llaves a usar.
        """
        rows = []
        for idx, item in enumerate(items, start=1):
            # Permite dicts u objetos con atributos.
            get_val = item.get if isinstance(item, dict) else getattr
            row_id = str(get_val(item, id_attr, idx))
            row_title = str(get_val(item, title_attr, f"Item {idx}"))
            row: dict[str, str] = {"id": row_id, "title": row_title}
            if description_attr:
                desc_val = get_val(item, description_attr, None)
                if desc_val:
                    row["description"] = str(desc_val)
            rows.append(row)

        return [{"title": section_title, "rows": rows}]
