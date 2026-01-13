from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.egresoEntity import EgresoEntity
from domain.interfaces.egreso_repository_interface import EgresoRepositoryInterface
from infrastructure.models.models import Egreso


class EgresoRepository(EgresoRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_egreso(self, entity: EgresoEntity) -> EgresoEntity:
        orm = Egreso(
            id=entity.id,
            fecha=entity.fecha,
            monto=entity.monto,
            medio_pago=entity.medio_pago,
            descripcion=entity.descripcion,
            categoria_id=entity.categoria_id,
            whatsapp_user_id=entity.whatsapp_user_id,
            phone_number=entity.phone_number,
            proveedor=entity.proveedor,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return EgresoEntity.from_model(orm)

    def get_egreso(self, egreso_id: UUID) -> Optional[EgresoEntity]:
        record = self.db.get(Egreso, egreso_id)
        if not record:
            return None
        return EgresoEntity.from_model(record)

    def list_egresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[EgresoEntity]:
        q = self.db.query(Egreso)
        if desde is not None:
            q = q.filter(Egreso.fecha >= desde)
        if hasta is not None:
            q = q.filter(Egreso.fecha <= hasta)
        records = q.order_by(Egreso.fecha.desc(), Egreso.created_at.desc()).all()
        return [EgresoEntity.from_model(row) for row in records]
