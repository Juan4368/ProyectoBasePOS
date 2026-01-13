from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.clienteEntity import ClienteEntity
from domain.interfaces.cliente_repository_interface import ClienteRepositoryInterface
from infrastructure.models.models import Cliente


def _normalizar_nombre(nombre: str) -> str:
    return nombre.strip().lower()


class ClienteRepository(ClienteRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_cliente(
        self, entity: ClienteEntity, nombre_normalizado: Optional[str] = None
    ) -> ClienteEntity:
        normalized = nombre_normalizado or _normalizar_nombre(entity.nombre)
        orm = Cliente(
            id=entity.id,
            nombre=entity.nombre,
            nombre_normalizado=normalized,
            telefono=entity.telefono,
            email=entity.email,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return ClienteEntity.from_model(orm)

    def get_cliente(self, cliente_id: UUID) -> Optional[ClienteEntity]:
        record = self.db.get(Cliente, cliente_id)
        if not record:
            return None
        return ClienteEntity.from_model(record)

    def get_by_nombre_normalizado(self, nombre_normalizado: str) -> Optional[ClienteEntity]:
        if not nombre_normalizado:
            return None
        record = (
            self.db.query(Cliente)
            .filter(Cliente.nombre_normalizado == nombre_normalizado.strip().lower())
            .first()
        )
        if not record:
            return None
        return ClienteEntity.from_model(record)

    def list_clientes(self) -> List[ClienteEntity]:
        records = self.db.query(Cliente).order_by(Cliente.nombre.asc()).all()
        return [ClienteEntity.from_model(r) for r in records]

    def search_clientes(self, term: str) -> List[ClienteEntity]:
        q = term.strip()
        if not q:
            return []
        like = f"%{q}%"
        records = (
            self.db.query(Cliente)
            .filter(
                (Cliente.nombre.ilike(like))
                | (Cliente.telefono.ilike(like))
                | (Cliente.email.ilike(like))
            )
            .order_by(Cliente.nombre.asc())
            .all()
        )
        return [ClienteEntity.from_model(r) for r in records]
