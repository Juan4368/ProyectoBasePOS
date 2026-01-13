from __future__ import annotations

from enum import Enum


class CategoriaTipo(str, Enum):
    INGRESO = "INGRESO"
    EGRESO = "EGRESO"


class MedioPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"

