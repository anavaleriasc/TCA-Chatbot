from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from repositories.messages_repository import chatMessages
from models.chat_message_model import ChatMessage
from schemas.messages_schema import MessagePublic


async def listar_mensagens(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    user_id: int = None,
):
    return await chatMessages.list(db, skip=skip, limit=limit, user_id=user_id)


async def listar_mensagem_by_thread(
    db: AsyncSession,
    thread_id: str,
):
    return await chatMessages.list_by_thread(db, thread_id)

  



   





