from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResumenVentaDiariaEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `resumen_venta_diaria`.
    """

    id: UUID = Field(default_factory=uuid.uuid4)
    fecha: date
    total_ventas: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    total_efectivo: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    total_tarjeta: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    total_transferencia: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    cantidad_transacciones: int = Field(default=0, ge=0)
    generado_por_whatsapp_user_id: str = Field(..., min_length=1, max_length=255)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: str, UUID: str},
    )

    @field_validator(
        "total_ventas",
        "total_efectivo",
        "total_tarjeta",
        "total_transferencia",
        mode="before",
    )
    def _ensure_decimal(cls, v) -> Decimal:
        if isinstance(v, Decimal):
            value = v
        else:
            value = Decimal(str(v or "0"))
        if value < 0:
            raise ValueError("El total no puede ser negativo")
        return value

    @field_validator("generado_por_whatsapp_user_id", mode="before")
    def _strip_user_id(cls, v: Optional[str]) -> str:
        value = (v or "").strip()
        if not value:
            raise ValueError("generado_por_whatsapp_user_id es requerido")
        return value

    @classmethod
    def from_model(cls, obj: Any) -> "ResumenVentaDiariaEntity":
        return cls.model_validate(obj)

