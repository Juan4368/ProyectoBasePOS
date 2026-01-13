from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ResumenVentaDiariaRequest(BaseModel):
    fecha: date
    total_ventas: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    total_efectivo: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    total_tarjeta: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    total_transferencia: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    cantidad_transacciones: int = Field(default=0, ge=0)
    generado_por_whatsapp_user_id: str = Field(..., min_length=1, max_length=255)


class ResumenVentaDiariaResponse(BaseModel):
    id: UUID
    fecha: date
    total_ventas: Decimal
    total_efectivo: Decimal
    total_tarjeta: Decimal
    total_transferencia: Decimal
    cantidad_transacciones: int
    generado_por_whatsapp_user_id: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

