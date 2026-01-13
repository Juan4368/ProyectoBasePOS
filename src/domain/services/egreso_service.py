from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.dtos.egresoDto import EgresoRequest, EgresoResponse
from domain.entities.egresoEntity import EgresoEntity
from domain.interfaces.egreso_repository_interface import EgresoRepositoryInterface


class EgresoService:
    def __init__(self, repository: EgresoRepositoryInterface):
        self.repository = repository

    def create_egreso(self, data: EgresoRequest) -> EgresoResponse:
        entity = EgresoEntity(
            fecha=data.fecha,
            monto=data.monto,
            medio_pago=data.medio_pago,
            descripcion=data.descripcion,
            categoria_id=data.categoria_id,
            whatsapp_user_id=data.whatsapp_user_id,
            phone_number=data.phone_number,
            proveedor=data.proveedor,
        )
        created = self.repository.create_egreso(entity)
        return EgresoResponse.model_validate(created)

    def get_egreso(self, egreso_id: UUID) -> Optional[EgresoResponse]:
        egreso = self.repository.get_egreso(egreso_id)
        if not egreso:
            return None
        return EgresoResponse.model_validate(egreso)

    def list_egresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[EgresoResponse]:
        egresos = self.repository.list_egresos(desde=desde, hasta=hasta)
        return [EgresoResponse.model_validate(e) for e in egresos]
