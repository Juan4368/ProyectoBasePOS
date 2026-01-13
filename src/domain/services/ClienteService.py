from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from domain.dtos.clienteDto import ClienteRequest, ClienteResponse
from domain.entities.clienteEntity import ClienteEntity
from domain.interfaces.cliente_repository_interface import ClienteRepositoryInterface
from domain.interfaces.IClientService import IClientService


def _normalizar_nombre(nombre: str) -> str:
    return nombre.strip().lower()


class ClienteService(IClientService):
    def __init__(self, repository: ClienteRepositoryInterface):
        self.repository = repository

    def create_cliente(self, data: ClienteRequest) -> ClienteResponse:
        normalized = _normalizar_nombre(data.nombre)
        existing = self.repository.get_by_nombre_normalizado(normalized)
        if existing:
            raise ValueError("El cliente ya existe")

        entity = ClienteEntity(
            nombre=data.nombre,
            telefono=data.telefono,
            email=data.email,
        )
        created = self.repository.create_cliente(entity, nombre_normalizado=normalized)
        return ClienteResponse.model_validate(created)

    def get_cliente(self, cliente_id: UUID) -> Optional[ClienteResponse]:
        cliente = self.repository.get_cliente(cliente_id)
        if not cliente:
            return None
        return ClienteResponse.model_validate(cliente)

    def list_clientes(self) -> List[ClienteResponse]:
        clientes = self.repository.list_clientes()
        return [ClienteResponse.model_validate(c) for c in clientes]

    def search_clientes(self, term: str) -> List[ClienteResponse]:
        if not term.strip():
            return []
        clientes = self.repository.search_clientes(term.strip())
        return [ClienteResponse.model_validate(c) for c in clientes]

    def get_by_nombre_normalizado(self, nombre_normalizado: str) -> Optional[ClienteResponse]:
        if not nombre_normalizado.strip():
            return None
        cliente = self.repository.get_by_nombre_normalizado(nombre_normalizado.strip().lower())
        if not cliente:
            return None
        return ClienteResponse.model_validate(cliente)
