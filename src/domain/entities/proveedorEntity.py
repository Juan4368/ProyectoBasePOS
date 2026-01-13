from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProveedorEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para proveedores.
    """

    id: UUID = Field(default_factory=uuid.uuid4)
    nombre: str = Field(..., min_length=1, max_length=255)
    telefono: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=255)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        value = (v or "").strip()
        if not value:
            raise ValueError("El nombre es requerido")
        return value

    @field_validator("telefono", "email", mode="before")
    def _strip_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        val = str(v).strip()
        return val or None

    @classmethod
    def from_model(cls, obj: Any) -> "ProveedorEntity":
        return cls.model_validate(obj)
