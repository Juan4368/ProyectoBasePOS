# ...existing code...
from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

from src.domain.enums.contabilidadEnums import CategoriaTipo, MedioPago

# Try to use native UUID type for Postgres, fallback to String(36) for portability
try:
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID  # type: ignore

    UUID_TYPE = PG_UUID(as_uuid=True)
except Exception:
    UUID_TYPE = String(36)

Base = declarative_base()


CATEGORIA_TIPO_ENUM = SAEnum(CategoriaTipo, name="categoria_tipo")
MEDIO_PAGO_ENUM = SAEnum(MedioPago, name="medio_pago")


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(Boolean, nullable=False, default=True)

    # relacion: una categoria tiene muchos productos
    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id!r}, nombre={self.nombre!r})>"


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("codigo_barras", name="uq_products_codigo_barras"),
    )

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)  # usa Decimal en Python
    codigo_barras = Column(String(100), nullable=True)
    stock_actual = Column(Integer, nullable=False, default=0)
    categoria_id = Column(UUID_TYPE, ForeignKey("categories.id"), nullable=False)
    imagen_url = Column(String(1000), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)

    # relacion: un producto pertenece a una categoria
    category = relationship("Category", back_populates="products", lazy="joined")

    # relacion opcional hacia OrderItem (si existe): un producto aparece en muchos items de pedido
    # order_items = relationship("OrderItem", back_populates="product", lazy="selectin")

    def precio_decimal(self) -> Decimal:
        return Decimal(self.precio)

    def __repr__(self) -> str:
        return f"<Product(id={self.id!r}, nombre={self.nombre!r}, precio={self.precio})>"


class Categoria(Base):
    __tablename__ = "categorias"
    __table_args__ = (UniqueConstraint("nombre", name="uq_categorias_nombre"),)

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    nombre = Column(String(150), nullable=False)
    tipo = Column(CATEGORIA_TIPO_ENUM, nullable=False)
    descripcion = Column(Text, nullable=True)
    activa = Column(Boolean, nullable=False, default=True)
    creada_por_whatsapp_user_id = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    ingresos = relationship(
        "Ingreso",
        back_populates="categoria",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    egresos = relationship(
        "Egreso",
        back_populates="categoria",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Categoria(id={self.id!r}, nombre={self.nombre!r}, tipo={self.tipo})>"


class Cliente(Base):
    __tablename__ = "clientes"
    __table_args__ = (
        UniqueConstraint("nombre_normalizado", name="uq_clientes_nombre_normalizado"),
    )

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    nombre_normalizado = Column(String(255), nullable=False)
    telefono = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id!r}, nombre={self.nombre!r})>"


class Proveedor(Base):
    __tablename__ = "proveedores"
    __table_args__ = (
        UniqueConstraint("nombre_normalizado", name="uq_proveedores_nombre_normalizado"),
    )

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    nombre_normalizado = Column(String(255), nullable=False)
    telefono = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Proveedor(id={self.id!r}, nombre={self.nombre!r})>"


class Ingreso(Base):
    __tablename__ = "ingresos"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    fecha = Column(Date, nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    medio_pago = Column(MEDIO_PAGO_ENUM, nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria_id = Column(UUID_TYPE, ForeignKey("categorias.id"), nullable=False)
    whatsapp_user_id = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=False)
    cliente = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    categoria = relationship("Categoria", back_populates="ingresos", lazy="joined")

    def monto_decimal(self) -> Decimal:
        return Decimal(self.monto)

    def __repr__(self) -> str:
        return f"<Ingreso(id={self.id!r}, fecha={self.fecha!r}, monto={self.monto})>"


class Egreso(Base):
    __tablename__ = "egresos"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    fecha = Column(Date, nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    medio_pago = Column(MEDIO_PAGO_ENUM, nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria_id = Column(UUID_TYPE, ForeignKey("categorias.id"), nullable=False)
    whatsapp_user_id = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=False)
    proveedor = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    categoria = relationship("Categoria", back_populates="egresos", lazy="joined")

    def monto_decimal(self) -> Decimal:
        return Decimal(self.monto)

    def __repr__(self) -> str:
        return f"<Egreso(id={self.id!r}, fecha={self.fecha!r}, monto={self.monto})>"


class ResumenVentaDiaria(Base):
    __tablename__ = "resumen_venta_diaria"
    __table_args__ = (
        UniqueConstraint("fecha", name="uq_resumen_venta_diaria_fecha"),
    )

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    fecha = Column(Date, nullable=False)
    total_ventas = Column(Numeric(12, 2), nullable=False, default=0)
    total_efectivo = Column(Numeric(12, 2), nullable=False, default=0)
    total_tarjeta = Column(Numeric(12, 2), nullable=False, default=0)
    total_transferencia = Column(Numeric(12, 2), nullable=False, default=0)
    cantidad_transacciones = Column(Integer, nullable=False, default=0)
    generado_por_whatsapp_user_id = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<ResumenVentaDiaria(id={self.id!r}, fecha={self.fecha!r}, total_ventas={self.total_ventas})>"


class CierreCaja(Base):
    __tablename__ = "cierre_caja"
    __table_args__ = (UniqueConstraint("fecha", name="uq_cierre_caja_fecha"),)

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    fecha = Column(Date, nullable=False)
    saldo_inicial = Column(Numeric(12, 2), nullable=False, default=0)
    total_ingresos = Column(Numeric(12, 2), nullable=False, default=0)
    total_egresos = Column(Numeric(12, 2), nullable=False, default=0)
    saldo_teorico = Column(Numeric(12, 2), nullable=False, default=0)
    saldo_real = Column(Numeric(12, 2), nullable=False, default=0)
    diferencia = Column(Numeric(12, 2), nullable=False, default=0)
    observaciones = Column(Text, nullable=True)
    cerrado_por_whatsapp_user_id = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<CierreCaja(id={self.id!r}, fecha={self.fecha!r}, diferencia={self.diferencia})>"
# ...existing code...
