from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.contabilidadCategoriaEntity import ContabilidadCategoriaEntity
from domain.enums.contabilidadEnums import CategoriaTipo
from domain.interfaces.contabilidad_categoria_repository_interface import (
    ContabilidadCategoriaRepositoryInterface,
)
from infrastructure.models.models import Categoria


class ContabilidadCategoriaRepository(ContabilidadCategoriaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_categoria(
        self, entity: ContabilidadCategoriaEntity
    ) -> ContabilidadCategoriaEntity:
        orm = Categoria(
            id=entity.id,
            nombre=entity.nombre,
            tipo=entity.tipo,
            descripcion=entity.descripcion,
            activa=entity.activa,
            creada_por_whatsapp_user_id=entity.creada_por_whatsapp_user_id,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return ContabilidadCategoriaEntity.from_model(orm)

    def list_categorias(
        self, *, tipo: Optional[CategoriaTipo] = None, activa: Optional[bool] = None
    ) -> List[ContabilidadCategoriaEntity]:
        q = self.db.query(Categoria)
        if tipo is not None:
            q = q.filter(Categoria.tipo == tipo)
        if activa is not None:
            q = q.filter(Categoria.activa.is_(bool(activa)))
        records = q.order_by(Categoria.nombre.asc()).all()
        return [ContabilidadCategoriaEntity.from_model(row) for row in records]

    def get_categoria(self, categoria_id: UUID) -> Optional[ContabilidadCategoriaEntity]:
        record = self.db.get(Categoria, categoria_id)
        if not record:
            return None
        return ContabilidadCategoriaEntity.from_model(record)

    def get_by_nombre(self, nombre: str) -> Optional[ContabilidadCategoriaEntity]:
        term = (nombre or "").strip()
        if not term:
            return None
        record = self.db.query(Categoria).filter(Categoria.nombre == term).first()
        if not record:
            return None
        return ContabilidadCategoriaEntity.from_model(record)

