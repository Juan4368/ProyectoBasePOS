from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from domain.enums.contabilidadEnums import CategoriaTipo


class ContabilidadCategoriaEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `categorias` (contabilidad).
    """

    id: UUID = Field(default_factory=uuid.uuid4)
    nombre: str = Field(..., min_length=1, max_length=150)
    tipo: CategoriaTipo
    descripcion: Optional[str] = None
    activa: bool = True
    creada_por_whatsapp_user_id: str = Field(..., min_length=1, max_length=255)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @field_validator("descripcion", mode="before")
    def _strip_descripcion(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        stripped = str(v).strip()
        return stripped or None

    @field_validator("creada_por_whatsapp_user_id", mode="before")
    def _strip_user_id(cls, v: Optional[str]) -> str:
        value = (v or "").strip()
        if not value:
            raise ValueError("creada_por_whatsapp_user_id es requerido")
        return value

    @classmethod
    def from_model(cls, obj: Any) -> "ContabilidadCategoriaEntity":
        return cls.model_validate(obj)

