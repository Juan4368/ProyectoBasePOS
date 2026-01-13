from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.proveedorEntity import ProveedorEntity
from domain.interfaces.proveedor_repository_interface import ProveedorRepositoryInterface
from infrastructure.models.models import Proveedor


def _normalizar_nombre(nombre: str) -> str:
    return nombre.strip().lower()


class ProveedorRepository(ProveedorRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_proveedor(
        self, entity: ProveedorEntity, nombre_normalizado: Optional[str] = None
    ) -> ProveedorEntity:
        normalized = nombre_normalizado or _normalizar_nombre(entity.nombre)
        orm = Proveedor(
            id=entity.id,
            nombre=entity.nombre,
            nombre_normalizado=normalized,
            telefono=entity.telefono,
            email=entity.email,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return ProveedorEntity.from_model(orm)

    def get_proveedor(self, proveedor_id: UUID) -> Optional[ProveedorEntity]:
        record = self.db.get(Proveedor, proveedor_id)
        if not record:
            return None
        return ProveedorEntity.from_model(record)

    def get_by_nombre_normalizado(self, nombre_normalizado: str) -> Optional[ProveedorEntity]:
        if not nombre_normalizado:
            return None
        record = (
            self.db.query(Proveedor)
            .filter(Proveedor.nombre_normalizado == nombre_normalizado.strip().lower())
            .first()
        )
        if not record:
            return None
        return ProveedorEntity.from_model(record)

    def list_proveedores(self) -> List[ProveedorEntity]:
        records = self.db.query(Proveedor).order_by(Proveedor.nombre.asc()).all()
        return [ProveedorEntity.from_model(r) for r in records]

    def search_proveedores(self, term: str) -> List[ProveedorEntity]:
        q = term.strip()
        if not q:
            return []
        like = f"%{q}%"
        records = (
            self.db.query(Proveedor)
            .filter(
                (Proveedor.nombre.ilike(like))
                | (Proveedor.telefono.ilike(like))
                | (Proveedor.email.ilike(like))
            )
            .order_by(Proveedor.nombre.asc())
            .all()
        )
        return [ProveedorEntity.from_model(r) for r in records]
