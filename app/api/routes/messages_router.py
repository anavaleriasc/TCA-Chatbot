from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.messages_schema import MessagePublic
from services.messages_service import (
    listar_mensagens,
    listar_mensagem_by_thread,
)


router = APIRouter(prefix="/mensagens", tags=["mensagens"])


@router.get("", response_model=list[MessagePublic])
async def list_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[MessagePublic]:
    messages = await listar_mensagens(db, skip, limit)
    return [MessagePublic.model_validate(m) for m in messages]


@router.get("/{thread_id}", response_model=list[MessagePublic])
async def list_message_by_thread(
    thread_id: str,
    db: AsyncSession = Depends(get_db),
) -> list[MessagePublic]:
    messages = await listar_mensagem_by_thread(db, thread_id)
    return [MessagePublic.model_validate(m) for m in messages]