from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from domain.dtos.proveedorDto import ProveedorRequest, ProveedorResponse
from domain.entities.proveedorEntity import ProveedorEntity
from domain.interfaces.proveedor_repository_interface import ProveedorRepositoryInterface


def _normalizar_nombre(nombre: str) -> str:
    return nombre.strip().lower()


class ProveedorService:
    def __init__(self, repository: ProveedorRepositoryInterface):
        self.repository = repository

    def create_proveedor(self, data: ProveedorRequest) -> ProveedorResponse:
        normalized = _normalizar_nombre(data.nombre)
        existing = self.repository.get_by_nombre_normalizado(normalized)
        if existing:
            raise ValueError("El proveedor ya existe")

        entity = ProveedorEntity(
            nombre=data.nombre,
            telefono=data.telefono,
            email=data.email,
        )
        created = self.repository.create_proveedor(entity, nombre_normalizado=normalized)
        return ProveedorResponse.model_validate(created)

    def get_proveedor(self, proveedor_id: UUID) -> Optional[ProveedorResponse]:
        proveedor = self.repository.get_proveedor(proveedor_id)
        if not proveedor:
            return None
        return ProveedorResponse.model_validate(proveedor)

    def list_proveedores(self) -> List[ProveedorResponse]:
        proveedores = self.repository.list_proveedores()
        return [ProveedorResponse.model_validate(p) for p in proveedores]

    def search_proveedores(self, term: str) -> List[ProveedorResponse]:
        if not term.strip():
            return []
        proveedores = self.repository.search_proveedores(term.strip())
        return [ProveedorResponse.model_validate(p) for p in proveedores]
