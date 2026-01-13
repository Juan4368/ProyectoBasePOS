from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.ingresoEntity import IngresoEntity
from domain.interfaces.ingreso_repository_interface import IngresoRepositoryInterface
from infrastructure.models.models import Ingreso


class IngresoRepository(IngresoRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_ingreso(self, entity: IngresoEntity) -> IngresoEntity:
        orm = Ingreso(
            id=entity.id,
            fecha=entity.fecha,
            monto=entity.monto,
            medio_pago=entity.medio_pago,
            descripcion=entity.descripcion,
            categoria_id=entity.categoria_id,
            whatsapp_user_id=entity.whatsapp_user_id,
            phone_number=entity.phone_number,
            cliente=entity.cliente,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return IngresoEntity.from_model(orm)

    def get_ingreso(self, ingreso_id: UUID) -> Optional[IngresoEntity]:
        record = self.db.get(Ingreso, ingreso_id)
        if not record:
            return None
        return IngresoEntity.from_model(record)

    def list_ingresos(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[IngresoEntity]:
        q = self.db.query(Ingreso)
        if desde is not None:
            q = q.filter(Ingreso.fecha >= desde)
        if hasta is not None:
            q = q.filter(Ingreso.fecha <= hasta)
        records = q.order_by(Ingreso.fecha.desc(), Ingreso.created_at.desc()).all()
        return [IngresoEntity.from_model(row) for row in records]
