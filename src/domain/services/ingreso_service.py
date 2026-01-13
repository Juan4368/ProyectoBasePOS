from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.dtos.ingresoDto import IngresoRequest, IngresoResponse
from domain.entities.ingresoEntity import IngresoEntity
from domain.interfaces.ingreso_repository_interface import IngresoRepositoryInterface


class IngresoService:
    def __init__(self, repository: IngresoRepositoryInterface):
        self.repository = repository

    def create_ingreso(self, data: IngresoRequest) -> IngresoResponse:
        entity = IngresoEntity(
            fecha=data.fecha,
            monto=data.monto,
            medio_pago=data.medio_pago,
            descripcion=data.descripcion,
            categoria_id=data.categoria_id,
            whatsapp_user_id=data.whatsapp_user_id,
            phone_number=data.phone_number,
            cliente=data.cliente,
        )
        created = self.repository.create_ingreso(entity)
        return IngresoResponse.model_validate(created)

    def get_ingreso(self, ingreso_id: UUID) -> Optional[IngresoResponse]:
        ingreso = self.repository.get_ingreso(ingreso_id)
        if not ingreso:
            return None
        return IngresoResponse.model_validate(ingreso)

    def list_ingresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[IngresoResponse]:
        ingresos = self.repository.list_ingresos(desde=desde, hasta=hasta)
        return [IngresoResponse.model_validate(i) for i in ingresos]
