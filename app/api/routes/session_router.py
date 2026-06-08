from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.session_schema import SessionPublic, SessionUpdate
from services.session_service import (
    listar_sessoes,
    get_sessao_by_thread,
    update_sessao,
    remover_sessao
)
from services.auth_service import get_current_user
from models.user_model import User


router = APIRouter(prefix="/sessoes", tags=["sessoes"])


@router.get("", response_model=list[SessionPublic])
async def list_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[SessionPublic]:
    sessions = await listar_sessoes(db, skip, limit, current_user.id)
    return sessions


@router.get("/{thread_id}", response_model=SessionPublic)
async def get_sessions_by_thread(
    thread_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SessionPublic:
    session = await get_sessao_by_thread(db, thread_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para acessar esta sessão.")
    return session

@router.patch("/{session_id}", response_model=SessionPublic)
async def update_session(
    session_id: int,
    payload: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SessionPublic:
    session = await update_sessao(db, session_id, payload.thread_id,
     payload.user_id, payload.conversation_summary, payload.messages)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para atualizar esta sessão.")
    return session


@router.delete("/{session_id}", response_model=SessionPublic)
async def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SessionPublic:
    session = await remover_sessao(db, session_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar esta sessão.")
    return session
