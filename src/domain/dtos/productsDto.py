from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    """
    DTO para manejar las solicitudes relacionadas con productos (crear/actualizar).
    """
    nombre: str = Field(..., min_length=1, max_length=200)
    codigo_barras: str = Field(..., max_length=100)
    categoria_id: Optional[int] = None
    descripcion: Optional[str] = None
    precio_venta: Decimal = Field(..., ge=Decimal("0.00"))
    costo: Decimal = Field(..., ge=Decimal("0.00"))
    margen: Optional[Decimal] = Field(None, ge=Decimal("0.00"))
    creado_por_id: Optional[int] = None
    actualizado_por_id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    estado: bool = True


class ProductStatusUpdate(BaseModel):
    """
    DTO para actualizar el estado de un producto.
    """

    estado: bool
    actualizado_por_id: Optional[int] = None
    fecha_actualizacion: Optional[datetime] = None


class ProductImportError(BaseModel):
    row: int
    message: str


class ProductImportResponse(BaseModel):
    created: int
    skipped: int
    invalid: int
    errors: list[ProductImportError] = Field(default_factory=list)


class ProductResponse(BaseModel):
    """
    DTO para manejar las respuestas relacionadas con productos.
    """
    producto_id: int
    codigo_barras: str
    nombre: str
    categoria_id: Optional[int]
    descripcion: Optional[str]
    precio_venta: Decimal
    costo: Decimal
    margen: Optional[Decimal] = None
    creado_por_id: Optional[int]
    actualizado_por_id: Optional[int]
    fecha_creacion: Optional[datetime]
    fecha_actualizacion: Optional[datetime]
    estado: bool
    categoria_nombre: Optional[str] = None
    creado_por_nombre: Optional[str] = None
    actualizado_por_nombre: Optional[str] = None

    class Config:
        from_attributes = True  # Permite construir desde objetos con atributos (ORM, entidades, etc.)
