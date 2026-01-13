from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from domain.dtos.contabilidadCategoriaDto import (
    ContabilidadCategoriaRequest,
    ContabilidadCategoriaResponse,
)
from domain.entities.contabilidadCategoriaEntity import ContabilidadCategoriaEntity
from domain.enums.contabilidadEnums import CategoriaTipo
from domain.interfaces.contabilidad_categoria_repository_interface import (
    ContabilidadCategoriaRepositoryInterface,
)


class ContabilidadCategoriaService:
    def __init__(self, repository: ContabilidadCategoriaRepositoryInterface):
        self.repository = repository

    def create_categoria(
        self, data: ContabilidadCategoriaRequest
    ) -> ContabilidadCategoriaResponse:
        entity = ContabilidadCategoriaEntity(
            nombre=data.nombre,
            tipo=data.tipo,
            descripcion=data.descripcion,
            activa=data.activa,
            creada_por_whatsapp_user_id=data.creada_por_whatsapp_user_id,
        )
        created = self.repository.create_categoria(entity)
        return ContabilidadCategoriaResponse.model_validate(created)

    def list_categorias(
        self, *, tipo: Optional[CategoriaTipo] = None, activa: Optional[bool] = None
    ) -> List[ContabilidadCategoriaResponse]:
        categorias = self.repository.list_categorias(tipo=tipo, activa=activa)
        return [ContabilidadCategoriaResponse.model_validate(c) for c in categorias]

    def get_categoria(self, categoria_id: UUID) -> Optional[ContabilidadCategoriaResponse]:
        categoria = self.repository.get_categoria(categoria_id)
        if not categoria:
            return None
        return ContabilidadCategoriaResponse.model_validate(categoria)

    def get_by_nombre(self, nombre: str) -> Optional[ContabilidadCategoriaResponse]:
        categoria = self.repository.get_by_nombre(nombre)
        if not categoria:
            return None
        return ContabilidadCategoriaResponse.model_validate(categoria)

