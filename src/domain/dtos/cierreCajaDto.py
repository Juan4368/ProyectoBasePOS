from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CierreCajaRequest(BaseModel):
    fecha: date
    saldo_inicial: Decimal = Field(default=Decimal("0.00"))
    total_ingresos: Decimal = Field(default=Decimal("0.00"))
    total_egresos: Decimal = Field(default=Decimal("0.00"))
    saldo_teorico: Decimal = Field(default=Decimal("0.00"))
    saldo_real: Decimal = Field(default=Decimal("0.00"))
    diferencia: Decimal = Field(default=Decimal("0.00"))
    observaciones: Optional[str] = None
    cerrado_por_whatsapp_user_id: str = Field(..., min_length=1, max_length=255)


class CierreCajaResponse(BaseModel):
    id: UUID
    fecha: date
    saldo_inicial: Decimal
    total_ingresos: Decimal
    total_egresos: Decimal
    saldo_teorico: Decimal
    saldo_real: Decimal
    diferencia: Decimal
    observaciones: Optional[str]
    cerrado_por_whatsapp_user_id: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

