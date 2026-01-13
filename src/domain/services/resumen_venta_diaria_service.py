from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.dtos.resumenVentaDiariaDto import (
    ResumenVentaDiariaRequest,
    ResumenVentaDiariaResponse,
)
from domain.entities.resumenVentaDiariaEntity import ResumenVentaDiariaEntity
from domain.interfaces.resumen_venta_diaria_repository_interface import (
    ResumenVentaDiariaRepositoryInterface,
)


class ResumenVentaDiariaService:
    def __init__(self, repository: ResumenVentaDiariaRepositoryInterface):
        self.repository = repository

    def create_resumen(self, data: ResumenVentaDiariaRequest) -> ResumenVentaDiariaResponse:
        entity = ResumenVentaDiariaEntity(
            fecha=data.fecha,
            total_ventas=data.total_ventas,
            total_efectivo=data.total_efectivo,
            total_tarjeta=data.total_tarjeta,
            total_transferencia=data.total_transferencia,
            cantidad_transacciones=data.cantidad_transacciones,
            generado_por_whatsapp_user_id=data.generado_por_whatsapp_user_id,
        )
        created = self.repository.create_resumen(entity)
        return ResumenVentaDiariaResponse.model_validate(created)

    def get_resumen(self, resumen_id: UUID) -> Optional[ResumenVentaDiariaResponse]:
        resumen = self.repository.get_resumen(resumen_id)
        if not resumen:
            return None
        return ResumenVentaDiariaResponse.model_validate(resumen)

    def get_by_fecha(self, fecha: date) -> Optional[ResumenVentaDiariaResponse]:
        resumen = self.repository.get_by_fecha(fecha)
        if not resumen:
            return None
        return ResumenVentaDiariaResponse.model_validate(resumen)

    def list_resumenes(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[ResumenVentaDiariaResponse]:
        resumenes = self.repository.list_resumenes(desde=desde, hasta=hasta)
        return [ResumenVentaDiariaResponse.model_validate(r) for r in resumenes]

