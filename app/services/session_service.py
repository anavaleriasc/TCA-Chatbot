from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from repositories.session_repository import chatSession
from models.chat_session_model import ChatSession

from schemas.session_schema import (
    SessionPublic,
)

 
async def listar_sessoes(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    user_id: int = None,
):
    return await chatSession.list(db, skip=skip, limit=limit, user_id=user_id)


async def get_sessao_by_thread(
    db: AsyncSession,
    thread_id: str,
):
    session = await chatSession.get_by_thread(db, thread_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sessão com thread_id '{thread_id}' não encontrada"
        )
    return session

async def update_sessao(
    db: AsyncSession,
    session_id: int,
    thread_id: str = None,
    user_id: str = None,
    conversation_summary: str = None,
    messages: list = None
):
    session = await chatSession.get(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sessão não encontrada"
        )
    return await chatSession.update(
        db,
        session,
        thread_id=thread_id,
        user_id=user_id,
        conversation_summary=conversation_summary,
        messages=messages
    )

async def remover_sessao(
    db: AsyncSession,
    session_id: int,
):
    session = await chatSession.get(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )


    return await chatSession.delete(db, session)




