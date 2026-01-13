from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from domain.enums.contabilidadEnums import MedioPago


class EgresoEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `egresos`.
    """

    id: UUID = Field(default_factory=uuid.uuid4)
    fecha: date
    monto: Decimal = Field(..., ge=Decimal("0.00"))
    medio_pago: MedioPago
    descripcion: Optional[str] = None
    categoria_id: UUID
    whatsapp_user_id: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=1, max_length=50)
    proveedor: Optional[str] = Field(default=None, max_length=255)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: str, UUID: str},
    )

    @field_validator("monto", mode="before")
    def _ensure_decimal(cls, v) -> Decimal:
        if isinstance(v, Decimal):
            value = v
        else:
            value = Decimal(str(v or "0"))
        if value < 0:
            raise ValueError("El monto no puede ser negativo")
        return value

    @field_validator("descripcion", mode="before")
    def _strip_descripcion(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        stripped = str(v).strip()
        return stripped or None

    @field_validator("whatsapp_user_id", "phone_number", mode="before")
    def _strip_required_str(cls, v: Optional[str]) -> str:
        value = (v or "").strip()
        if not value:
            raise ValueError("Campo requerido")
        return value

    @field_validator("proveedor", mode="before")
    def _strip_proveedor(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        val = str(v).strip()
        return val or None

    @classmethod
    def from_model(cls, obj: Any) -> "EgresoEntity":
        return cls.model_validate(obj)
