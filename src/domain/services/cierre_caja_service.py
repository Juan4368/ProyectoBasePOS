from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.dtos.cierreCajaDto import CierreCajaRequest, CierreCajaResponse
from domain.entities.cierreCajaEntity import CierreCajaEntity
from domain.interfaces.cierre_caja_repository_interface import (
    CierreCajaRepositoryInterface,
)


class CierreCajaService:
    def __init__(self, repository: CierreCajaRepositoryInterface):
        self.repository = repository

    def create_cierre(self, data: CierreCajaRequest) -> CierreCajaResponse:
        entity = CierreCajaEntity(
            fecha=data.fecha,
            saldo_inicial=data.saldo_inicial,
            total_ingresos=data.total_ingresos,
            total_egresos=data.total_egresos,
            saldo_teorico=data.saldo_teorico,
            saldo_real=data.saldo_real,
            diferencia=data.diferencia,
            observaciones=data.observaciones,
            cerrado_por_whatsapp_user_id=data.cerrado_por_whatsapp_user_id,
        )
        created = self.repository.create_cierre(entity)
        return CierreCajaResponse.model_validate(created)

    def get_cierre(self, cierre_id: UUID) -> Optional[CierreCajaResponse]:
        cierre = self.repository.get_cierre(cierre_id)
        if not cierre:
            return None
        return CierreCajaResponse.model_validate(cierre)

    def get_by_fecha(self, fecha: date) -> Optional[CierreCajaResponse]:
        cierre = self.repository.get_by_fecha(fecha)
        if not cierre:
            return None
        return CierreCajaResponse.model_validate(cierre)

    def list_cierres(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[CierreCajaResponse]:
        cierres = self.repository.list_cierres(desde=desde, hasta=hasta)
        return [CierreCajaResponse.model_validate(c) for c in cierres]

