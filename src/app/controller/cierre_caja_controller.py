from datetime import date
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.cierreCajaDto import CierreCajaRequest, CierreCajaResponse
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.services.cierre_caja_service import CierreCajaService
from src.infrastructure.repository.createCierreCajaRepository import CierreCajaRepository

router = APIRouter(prefix="/contabilidad/cierre-caja", tags=["contabilidad-cierre-caja"])


def get_service(db: Session = Depends(get_db)) -> CierreCajaService:
    repo = CierreCajaRepository(db)
    return CierreCajaService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[CierreCajaService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[CierreCajaResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_cierre(
    payload: CierreCajaRequest,
    service: ServiceDep,
) -> CreationResponse[CierreCajaResponse]:
    try:
        created = service.create_cierre(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[CierreCajaResponse](id=created.id, data=created)


@router.get("/", response_model=list[CierreCajaResponse])
def list_cierres(
    service: ServiceDep,
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
) -> list[CierreCajaResponse]:
    return service.list_cierres(desde=desde, hasta=hasta)


@router.get("/fecha/{fecha}", response_model=CierreCajaResponse)
def get_by_fecha(fecha: date, service: ServiceDep) -> CierreCajaResponse:
    cierre = service.get_by_fecha(fecha)
    if not cierre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cierre de caja no encontrado para la fecha",
        )
    return cierre


@router.get("/{cierre_id}", response_model=CierreCajaResponse)
def get_cierre(cierre_id: UUID, service: ServiceDep) -> CierreCajaResponse:
    cierre = service.get_cierre(cierre_id)
    if not cierre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cierre de caja no encontrado")
    return cierre

