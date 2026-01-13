from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.contabilidadEnums import CategoriaTipo


class ContabilidadCategoriaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    tipo: CategoriaTipo
    descripcion: Optional[str] = None
    activa: bool = True
    creada_por_whatsapp_user_id: str = Field(..., min_length=1, max_length=255)


class ContabilidadCategoriaResponse(BaseModel):
    id: UUID
    nombre: str
    tipo: CategoriaTipo
    descripcion: Optional[str]
    activa: bool
    creada_por_whatsapp_user_id: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

