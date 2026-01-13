from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.resumenVentaDiariaEntity import ResumenVentaDiariaEntity
from domain.interfaces.resumen_venta_diaria_repository_interface import (
    ResumenVentaDiariaRepositoryInterface,
)
from infrastructure.models.models import ResumenVentaDiaria


class ResumenVentaDiariaRepository(ResumenVentaDiariaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_resumen(self, entity: ResumenVentaDiariaEntity) -> ResumenVentaDiariaEntity:
        orm = ResumenVentaDiaria(
            id=entity.id,
            fecha=entity.fecha,
            total_ventas=entity.total_ventas,
            total_efectivo=entity.total_efectivo,
            total_tarjeta=entity.total_tarjeta,
            total_transferencia=entity.total_transferencia,
            cantidad_transacciones=entity.cantidad_transacciones,
            generado_por_whatsapp_user_id=entity.generado_por_whatsapp_user_id,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return ResumenVentaDiariaEntity.from_model(orm)

    def get_resumen(self, resumen_id: UUID) -> Optional[ResumenVentaDiariaEntity]:
        record = self.db.get(ResumenVentaDiaria, resumen_id)
        if not record:
            return None
        return ResumenVentaDiariaEntity.from_model(record)

    def get_by_fecha(self, fecha: date) -> Optional[ResumenVentaDiariaEntity]:
        record = self.db.query(ResumenVentaDiaria).filter(ResumenVentaDiaria.fecha == fecha).first()
        if not record:
            return None
        return ResumenVentaDiariaEntity.from_model(record)

    def list_resumenes(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[ResumenVentaDiariaEntity]:
        q = self.db.query(ResumenVentaDiaria)
        if desde is not None:
            q = q.filter(ResumenVentaDiaria.fecha >= desde)
        if hasta is not None:
            q = q.filter(ResumenVentaDiaria.fecha <= hasta)
        records = q.order_by(ResumenVentaDiaria.fecha.desc()).all()
        return [ResumenVentaDiariaEntity.from_model(row) for row in records]

