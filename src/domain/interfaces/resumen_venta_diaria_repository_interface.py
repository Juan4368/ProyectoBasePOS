from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.entities.resumenVentaDiariaEntity import ResumenVentaDiariaEntity


class ResumenVentaDiariaRepositoryInterface(ABC):
    @abstractmethod
    def create_resumen(
        self, entity: ResumenVentaDiariaEntity
    ) -> ResumenVentaDiariaEntity:
        raise NotImplementedError

    @abstractmethod
    def get_resumen(self, resumen_id: UUID) -> Optional[ResumenVentaDiariaEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_fecha(self, fecha: date) -> Optional[ResumenVentaDiariaEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_resumenes(
        self, *, desde: Optional[date] = None, hasta: Optional[date] = None
    ) -> List[ResumenVentaDiariaEntity]:
        raise NotImplementedError

