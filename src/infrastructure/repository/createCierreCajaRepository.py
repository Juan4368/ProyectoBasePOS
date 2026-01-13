from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.cierreCajaEntity import CierreCajaEntity
from domain.interfaces.cierre_caja_repository_interface import (
    CierreCajaRepositoryInterface,
)
from infrastructure.models.models import CierreCaja


class CierreCajaRepository(CierreCajaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_cierre(self, entity: CierreCajaEntity) -> CierreCajaEntity:
        orm = CierreCaja(
            id=entity.id,
            fecha=entity.fecha,
            saldo_inicial=entity.saldo_inicial,
            total_ingresos=entity.total_ingresos,
            total_egresos=entity.total_egresos,
            saldo_teorico=entity.saldo_teorico,
            saldo_real=entity.saldo_real,
            diferencia=entity.diferencia,
            observaciones=entity.observaciones,
            cerrado_por_whatsapp_user_id=entity.cerrado_por_whatsapp_user_id,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return CierreCajaEntity.from_model(orm)

    def get_cierre(self, cierre_id: UUID) -> Optional[CierreCajaEntity]:
        record = self.db.get(CierreCaja, cierre_id)
        if not record:
            return None
        return CierreCajaEntity.from_model(record)

    def get_by_fecha(self, fecha: date) -> Optional[CierreCajaEntity]:
        record = self.db.query(CierreCaja).filter(CierreCaja.fecha == fecha).first()
        if not record:
            return None
        return CierreCajaEntity.from_model(record)

    def list_cierres(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[CierreCajaEntity]:
        q = self.db.query(CierreCaja)
        if desde is not None:
            q = q.filter(CierreCaja.fecha >= desde)
        if hasta is not None:
            q = q.filter(CierreCaja.fecha <= hasta)
        records = q.order_by(CierreCaja.fecha.desc()).all()
        return [CierreCajaEntity.from_model(row) for row in records]

