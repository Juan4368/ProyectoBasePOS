import os
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.app.services.webhook_service import (
    WebhookConversationState,
    WebhookService,
    build_whatsapp_client,
    setup_webhook_logger,
)
from src.config import get_db
from domain.services.ClienteService import ClienteService
from src.infrastructure.repository.ClienteRepository import ClienteRepository

router = APIRouter(tags=["webhook"])


def get_cliente_service(db: Session = Depends(get_db)) -> ClienteService:
    repo = ClienteRepository(db)
    return ClienteService(repo)


ClienteDep = Annotated[ClienteService, Depends(get_cliente_service)]

WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
_webhook_state = WebhookConversationState()
_webhook_logger = setup_webhook_logger()
_whatsapp_client = build_whatsapp_client()
_webhook_service = WebhookService(
    verify_token=WHATSAPP_VERIFY_TOKEN,
    state=_webhook_state,
    logger=_webhook_logger,
    whatsapp_client=_whatsapp_client,
)


def get_webhook_service() -> WebhookService:
    return _webhook_service


WebhookServiceDep = Annotated[WebhookService, Depends(get_webhook_service)]


@router.get("/webhook")
def whatsapp_verify(
    hub_mode: str | None = Query(default=None, alias="hub.mode"),
    hub_verify_token: str | None = Query(default=None, alias="hub.verify_token"),
    hub_challenge: int | None = Query(default=None, alias="hub.challenge"),
    webhook_service: WebhookService = Depends(get_webhook_service),
):
    return webhook_service.verify_subscription(
        hub_mode=hub_mode,
        hub_verify_token=hub_verify_token,
        hub_challenge=hub_challenge,
    )


@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    cliente_service: ClienteDep,
    webhook_service: WebhookService = Depends(get_webhook_service),
):
    body = await request.json()
    return webhook_service.handle_webhook(
        body=body,
        cliente_service=cliente_service,
    )
