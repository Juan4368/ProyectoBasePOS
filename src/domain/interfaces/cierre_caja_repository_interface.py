from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.entities.cierreCajaEntity import CierreCajaEntity


class CierreCajaRepositoryInterface(ABC):
    @abstractmethod
    def create_cierre(self, entity: CierreCajaEntity) -> CierreCajaEntity:
        raise NotImplementedError

    @abstractmethod
    def get_cierre(self, cierre_id: UUID) -> Optional[CierreCajaEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_fecha(self, fecha: date) -> Optional[CierreCajaEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_cierres(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[CierreCajaEntity]:
        raise NotImplementedError

