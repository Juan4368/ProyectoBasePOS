from datetime import date
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.dtos.resumenVentaDiariaDto import (
    ResumenVentaDiariaRequest,
    ResumenVentaDiariaResponse,
)
from src.domain.services.resumen_venta_diaria_service import ResumenVentaDiariaService
from src.infrastructure.repository.createResumenVentaDiariaRepository import (
    ResumenVentaDiariaRepository,
)

router = APIRouter(
    prefix="/contabilidad/resumen-venta-diaria",
    tags=["contabilidad-resumen-venta-diaria"],
)


def get_service(db: Session = Depends(get_db)) -> ResumenVentaDiariaService:
    repo = ResumenVentaDiariaRepository(db)
    return ResumenVentaDiariaService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[ResumenVentaDiariaService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[ResumenVentaDiariaResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_resumen(
    payload: ResumenVentaDiariaRequest,
    service: ServiceDep,
) -> CreationResponse[ResumenVentaDiariaResponse]:
    try:
        created = service.create_resumen(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[ResumenVentaDiariaResponse](id=created.id, data=created)


@router.get("/", response_model=list[ResumenVentaDiariaResponse])
def list_resumenes(
    service: ServiceDep,
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
) -> list[ResumenVentaDiariaResponse]:
    return service.list_resumenes(desde=desde, hasta=hasta)


@router.get("/fecha/{fecha}", response_model=ResumenVentaDiariaResponse)
def get_by_fecha(fecha: date, service: ServiceDep) -> ResumenVentaDiariaResponse:
    resumen = service.get_by_fecha(fecha)
    if not resumen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resumen no encontrado para la fecha",
        )
    return resumen


@router.get("/{resumen_id}", response_model=ResumenVentaDiariaResponse)
def get_resumen(resumen_id: UUID, service: ServiceDep) -> ResumenVentaDiariaResponse:
    resumen = service.get_resumen(resumen_id)
    if not resumen:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resumen no encontrado")
    return resumen

