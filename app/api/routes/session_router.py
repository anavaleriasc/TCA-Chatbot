from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.session_schema import SessionPublic
from services.session_service import (
    listar_sessoes,
    get_sessao_by_thread,
)




router = APIRouter(prefix="/seções", tags=["seções"])


@router.get("", response_model=list[SessionPublic])
async def list_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[SessionPublic]:
    sessions = await listar_sessoes(db, skip, limit)
    return [SessionPublic.model_validate(s) for s in sessions]


@router.get("/{thread_id}", response_model=SessionPublic)
async def get_sessions_by_thread(
    thread_id: str,
    db: AsyncSession = Depends(get_db),
) -> SessionPublic:
    session = await get_sessao_by_thread(db, thread_id)
    return SessionPublic.model_validate(session)