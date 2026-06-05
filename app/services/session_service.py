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
):
    return await chatSession.list(db,skip=skip, limit=limit)


async def get_sessao_by_thread(
    db: AsyncSession,
    thread_id: str,
):
    return await chatSession.get_by_thread(db, thread_id)
    



   





