from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CierreCajaEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `cierre_caja`.
    """

    id: UUID = Field(default_factory=uuid.uuid4)
    fecha: date
    saldo_inicial: Decimal = Field(default=Decimal("0.00"))
    total_ingresos: Decimal = Field(default=Decimal("0.00"))
    total_egresos: Decimal = Field(default=Decimal("0.00"))
    saldo_teorico: Decimal = Field(default=Decimal("0.00"))
    saldo_real: Decimal = Field(default=Decimal("0.00"))
    diferencia: Decimal = Field(default=Decimal("0.00"))
    observaciones: Optional[str] = None
    cerrado_por_whatsapp_user_id: str = Field(..., min_length=1, max_length=255)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={Decimal: str, UUID: str},
    )

    @field_validator(
        "saldo_inicial",
        "total_ingresos",
        "total_egresos",
        "saldo_teorico",
        "saldo_real",
        "diferencia",
        mode="before",
    )
    def _ensure_decimal(cls, v) -> Decimal:
        if isinstance(v, Decimal):
            value = v
        else:
            value = Decimal(str(v or "0"))
        return value

    @field_validator("observaciones", mode="before")
    def _strip_observaciones(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        stripped = str(v).strip()
        return stripped or None

    @field_validator("cerrado_por_whatsapp_user_id", mode="before")
    def _strip_user_id(cls, v: Optional[str]) -> str:
        value = (v or "").strip()
        if not value:
            raise ValueError("cerrado_por_whatsapp_user_id es requerido")
        return value

    @classmethod
    def from_model(cls, obj: Any) -> "CierreCajaEntity":
        return cls.model_validate(obj)

