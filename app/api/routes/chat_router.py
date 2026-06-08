from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from chatbot.schemas import ChatRequest, ChatResponse
from chatbot.chat_service import (send_message)
from services.auth_service import get_current_user
from models.user_model import User


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/invoke", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def invoke(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para enviar mensagens como este usuário.")
    return await send_message(session=db, payload=request)