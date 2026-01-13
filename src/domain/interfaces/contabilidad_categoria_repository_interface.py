from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.contabilidadCategoriaEntity import ContabilidadCategoriaEntity
from domain.enums.contabilidadEnums import CategoriaTipo


class ContabilidadCategoriaRepositoryInterface(ABC):
    @abstractmethod
    def create_categoria(
        self, entity: ContabilidadCategoriaEntity
    ) -> ContabilidadCategoriaEntity:
        raise NotImplementedError

    @abstractmethod
    def list_categorias(
        self, *, tipo: Optional[CategoriaTipo] = None, activa: Optional[bool] = None
    ) -> List[ContabilidadCategoriaEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_categoria(self, categoria_id: UUID) -> Optional[ContabilidadCategoriaEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[ContabilidadCategoriaEntity]:
        raise NotImplementedError

