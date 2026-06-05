from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from chatbot.schemas import ChatRequest, ChatResponse
from chatbot.chat_service import (send_message)


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/invoke", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def invoke(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    return await send_message(session=db, payload=request)