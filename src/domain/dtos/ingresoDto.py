from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.contabilidadEnums import MedioPago


class IngresoRequest(BaseModel):
    fecha: date
    monto: Decimal = Field(..., ge=Decimal("0.00"))
    medio_pago: MedioPago
    descripcion: Optional[str] = None
    categoria_id: UUID
    whatsapp_user_id: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=1, max_length=50)
    cliente: Optional[str] = Field(default=None, max_length=255)


class IngresoResponse(BaseModel):
    id: UUID
    fecha: date
    monto: Decimal
    medio_pago: MedioPago
    descripcion: Optional[str]
    categoria_id: UUID
    whatsapp_user_id: str
    phone_number: str
    cliente: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
