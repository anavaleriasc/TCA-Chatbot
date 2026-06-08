from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.messages_schema import MessagePublic
from services.messages_service import (
    listar_mensagens,
    listar_mensagem_by_thread,
)
from services.auth_service import get_current_user
from models.user_model import User
from repositories.session_repository import chatSession


router = APIRouter(prefix="/mensagens", tags=["mensagens"])


@router.get("", response_model=list[MessagePublic])
async def list_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[MessagePublic]:
    messages = await listar_mensagens(db, skip, limit, current_user.id)
    return [MessagePublic.model_validate(m) for m in messages]


@router.get("/{thread_id}", response_model=list[MessagePublic])
async def list_message_by_thread(
    thread_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[MessagePublic]:
    session = await chatSession.get_by_thread(db, thread_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para acessar estas mensagens.")
    messages = await listar_mensagem_by_thread(db, thread_id)
    return [MessagePublic.model_validate(m) for m in messages]